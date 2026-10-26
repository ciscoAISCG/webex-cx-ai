---
name: ai-calculator
description: Work with the AI Calculator — the contact center cost & ROI engine (CallCenterCalculator + QMCalculator) behind the /call-center-analysis page. Use when modifying, debugging, extending, or explaining call-center savings calculations, the optimization levers, AI cost modeling, the calculation trace, monthly projections / pie charts, calculator templates, or the PDF/PPTX exports.
---

# AI Calculator

The AI Calculator quantifies the financial impact of AI in a contact center. It takes current-state metrics (call volume, AHT, agent salary, occupancy, FCR, digital volume) plus a set of AI optimization levers, and returns annual savings, agent (FTE) reduction, a per-lever savings breakdown, and a step-by-step calculation `trace`. Results render on screen and export to PDF/PPTX.

The Python engine is a faithful port of an original React `CallCenterAnalysisTool` — when changing formulas, preserve parity with that logic and the inline comments referencing it.

## Where the code lives

| Concern | Path |
|---|---|
| Core engine | `app/utils/call_center_calculator.py` — `CallCenterCalculator` |
| Quality Mgmt engine | `app/utils/quality_management_calculator.py` — `QMCalculator` (7-lever QM model) |
| Web route (entry point) | `app/routes/discovery.py` — `/call-center-analysis` (GET/POST), lines ~577–1046 |
| Input form (50+ fields) | `app/forms/discovery_forms.py` — `CallCenterAnalysisForm` (~line 259+) |
| PDF export | `app/utils/call_center_pdf_generator.py` — `CallCenterPDFGenerator` |
| Template model | `app/models/calculator_template.py` — `CalculatorTemplate` (max 5/org) |
| Template admin CRUD | `app/routes/admin_calculator_templates.py` |
| UI (tabbed) | `app/templates/v2/discovery/call_center_analysis.html` |
| Trace test | `tests/test_kpi_roi_trace.py` |
| System defaults | `SystemConfiguration.get_system_defaults()` (bundle pricing, etc.) |

## How it runs (the pipeline)

```python
from app.utils.call_center_calculator import CallCenterCalculator

calculator = CallCenterCalculator(current_metrics)            # raises ValueError if salary/occupancy missing
analysis   = calculator.calculate_comprehensive_analysis(optimizations, vertical_parameters)
projections = calculator.generate_monthly_projections(analysis, months=12)  # linear 8.33%→100% ramp
pie         = calculator.generate_pie_chart_data(analysis)
```

In the route, results are persisted into the `Assessment` model under `call_center_analysis` (org-shared, optimistic-locking guard). QM runs separately via `QMCalculator(qm_params).calculate()` when enabled.

`current_metrics` requires `agent_hourly_salary` and `occupancy_rate`. Voice fields (`annual_call_volume`, `average_handle_time`) default to 0 to support **digital-only** scenarios — guard against zero AHT/volume (see the `has_voice` flag in `calculate_comprehensive_analysis`).

## Optimization levers (each gated by an `enable_*` toggle)

1. **FCR improvement** — reduces repeat calls.
2. **Voice Bio** (caller ID verification) — time-based AHT reduction.
3. **Agent Assist** — percentage-based AHT reduction (sequenced after Voice Bio).
4. **IVR / Voice AI containment** — deflects calls; AI cost = scripted + autonomous minute mix.
5. **Digital deflection** — moves voice calls to digital channels.
6. **Digital AI containment** — contains digital interactions (turn/session-based AI cost).
7. **Predictive Analytics & WFM** — efficiency improvement on remaining agents.
8. **Abandonment recovery** — M/M/c queue model; lower wait → recovered calls × value.
9. **Vertical parameters** — industry upcharge/savings applied to IVR-hitting calls.

Volume flows as a **cascade**: `annual_calls → after_fcr → after_ivr → after_digital → remaining_calls`. AHT reductions are **sequential** (Voice Bio → Agent Assist) with a 30-second floor.

## Key methods

- `calculate_cost_per_interaction(aht, hourly_salary, occupancy)` — core: `salary / (60 * occupancy / aht)`
- `calculate_call_volume_cascade(optimizations)` — applies FCR/IVR/digital reductions in order
- `calculate_aht_reductions(optimizations)` — Voice Bio then Agent Assist, 30s floor
- `calculate_ai_costs(volume_data, optimizations)` — IVR/Agent Assist/digital AI costs + vertical upcharge + bundle counts
- `calculate_licensing_costs(optimizations)` — premium/standard licenses, implementation (Y1), maintenance
- `calculate_workforce_optimization(agent_counts, optimizations)` — WFM efficiency savings
- `calculate_abandonment_recovery_savings(...)` — queue-model + elasticity recovery
- `calculate_weighted_contact_costs(...)` — digital weight = `1 / concurrent_capacity` (agents handle multiple sessions)
- `calculate_comprehensive_analysis(optimizations, vertical_parameters=None)` — orchestrates all of the above

## Output shape (`calculate_comprehensive_analysis` return)

```python
{
  'current_cost_per_interaction', 'optimized_cost_per_interaction',   # blended voice+digital
  'annual_savings', 'savings_percentage',
  'trace': [ {key, label, value, formula, inputs}, ... ],            # audit trail → PDF appendix & UI popovers
  'volume_data', 'aht_data',
  'cost_breakdown': { agent_costs, ai_costs, digital_costs, ivr_ai_costs(_scripted/_autonomous),
                      agent_assist_ai_costs, digital_assist_ai_costs, digital_ai_costs(...),
                      vertical_upcharge_annual, wfm_license_costs, licensing_costs },
  'savings_breakdown': { fcr_savings, voice_bio_savings, agent_assist_savings, ivr_net_savings,
                         digital_savings, digital_containment_savings, workforce_savings,
                         vertical_parameters_savings, vertical_parameters_breakdown,
                         abandonment_recovery_savings },
  'abandonment_recovery', 'agent_counts' (current/optimized/reduction/...),
  'workforce_optimization', 'metrics' (current_total_cost/optimized_total_cost),
  'weighted_digital_data', 'digital_containment_data', 'digital_ai_costs_data'
}
```

## Working on it — gotchas & conventions

- **The `trace` is a contract.** `tests/test_kpi_roi_trace.py` asserts each entry has `key`, `label`, `value`, and a human-readable `formula`. Any new lever/savings line must append a well-formed trace entry, or the test (and the PDF audit + UI popover) breaks.
- **Keep React parity.** Comments cite the original `calculationUtils.js` / React `useEffect`. Match its ordering and normalization (e.g. `calculate_normalized_ivr_percentages` caps total IVR usage at 100%).
- **Savings vs. AI cost.** Several levers report **net** savings (gross savings minus the lever's AI cost) — e.g. `ivr_net_savings = containment_savings - annual_ivr_ai_cost`. Don't double-count: the vertical upcharge is applied in IVR costs and must NOT be re-added in Agent Assist cost-per-interaction.
- **Digital-only & zero-guards.** Always guard divisions on `aht > 0`, `volume > 0`, `occupancy > 0`; methods return 0 rather than throwing.
- **Adding an input field:** wire it in three places — `CallCenterAnalysisForm` (form), the route's `optimizations`/`current_metrics` dict assembly in `discovery.py`, and the calculator method that consumes it. Surface it in the PDF generator if it affects results.
- **After changes**, run `pytest tests/test_kpi_roi_trace.py` and exercise `/call-center-analysis` (POST) end-to-end, including a digital-only and a full-lever scenario.
