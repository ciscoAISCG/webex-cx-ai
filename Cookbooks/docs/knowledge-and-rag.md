
# Table of Contents

- [Knowledge and RAG for Webex AI Agent Studio](#knowledge-and-rag-for-webex-ai-agent-studio)
- [Plan the Knowledge Base](#plan-the-knowledge-base)
- [Create Knowledge Sources](#create-knowledge-sources)
  - [Upload Files](#upload-files)
  - [Create an Article](#create-an-article)
  - [Extract a Website](#extract-a-website)
- [Optimize Content for Retrieval](#optimize-content-for-retrieval)
- [Connect the Knowledge Base](#connect-the-knowledge-base)
- [Write RAG Instructions](#write-rag-instructions)
- [Test and Improve](#test-and-improve)
- [Operate and Govern](#operate-and-govern)
- [Production Checklist](#production-checklist)
- [Sources](#sources)


# Knowledge and RAG for Webex AI Agent Studio

Retrieval-Augmented Generation (RAG) allows an autonomous Webex AI Agent to retrieve relevant information from an approved knowledge base and use it when answering a customer.

Good RAG results depend on:

- a clearly scoped knowledge base
- accurate and current sources
- small, meaningful content sections
- instructions that explain when and how to use knowledge
- realistic testing with customer language
- a process for reviewing and updating content

---
**Key Point**<br>
RAG does not make poor or ambiguous documentation reliable. The agent can only retrieve and reason over content that has been provided and successfully indexed.

---

A typical RAG interaction works as follows:

1. The customer asks a question.
2. The system searches the mapped knowledge base for relevant passages.
3. Relevant passages are supplied to the language model as context.
4. The agent uses that context, its instructions, and the conversation to respond.

RAG is not model training. Adding a source makes its indexed content available for retrieval; it does not permanently teach the underlying model.

Two different problems can cause a bad answer:

- **Retrieval failure:** The correct information exists, but the relevant passage is not found.
- **Generation failure:** The right passage is found, but the agent interprets or presents it incorrectly.

Use each capability for its intended purpose:

- **Knowledge:** Approved policies, product guidance, FAQs, service descriptions, and troubleshooting information.
- **Instructions:** Identity, tone, boundaries, knowledge-use rules, clarification, and escalation behavior.
- **Actions:** Live or customer-specific information, transactions, system lookups, and record changes.
- **Flows:** Mandatory sequences, strict validation, stateful branching, and regulated processes.

For example, a refund policy belongs in knowledge, the rule to clarify which product was purchased belongs in instructions, and retrieving an order status requires an action.

---
**Do Not Use Static Knowledge for Live Data**<br>
Inventory, balances, order status, appointment availability, and similar values become stale. Retrieve them from the system of record through an action.

---


# Plan the Knowledge Base

Start with a narrow business outcome rather than uploading every available document. Define:

- the customers, channels, products, regions, and languages in scope
- the questions the agent should and should not answer
- an authoritative source and owner for every topic
- how frequently each source changes
- the fallback when knowledge is missing

A focused knowledge base reduces irrelevant retrieval. If unrelated areas use the same terms differently, separate them and make their context explicit.

Webex AI Agent Studio supports three source options for autonomous agents:

- **Files:** Controlled manuals, policies, troubleshooting guides, FAQs, and simple datasets.
- **Articles:** Short, focused content maintained directly in AI Agent Studio.
- **Websites:** Authoritative public HTML that you own or have permission to process.

Do not add Payment Card Industry (PCI) data, Personally Identifiable Information (PII), Protected Health Information (PHI), or other sensitive, confidential, or regulated information.

Before ingestion:

1. Classify the source.
2. Remove secrets, personal data, credentials, customer records, and internal comments.
3. Confirm the intended audience may receive every passage.
4. Assign an owner and review date.
5. Retain an approved master copy when governance requires it.


# Create Knowledge Sources

Open Webex AI Agent Studio, select **Knowledge**, open or create the required knowledge base, and select **Add source**.

## Upload Files

Supported types are `.xlsx`, `.xls`, `.csv`, `.pdf`, `.docx`, `.doc`, `.txt`, and `.md`.

1. Select **Add source > Files**.
2. Drag files onto the page or select **Add File**.
3. Use descriptive filenames because each filename becomes its source name.
4. Select **Process Files**.
5. Check **Processed files** and confirm successful processing.
6. Review the source before connecting it to an agent.

Current Webex limits include:

- 2 GB total storage per knowledge base
- 100 files per knowledge base
- 10 MB per individual file
- 2 MB per individual `.txt` file
- 300 pages per PDF, in addition to the file-size limit
- up to two hours of processing after a file is picked up; queue time is separate

Image processing is supported only for PDFs. Information contained only in a screenshot, chart, scan, or diagram might not be retrieved reliably. Include an equivalent text explanation.

---
**Recommended Practice**<br>
Do not upload one large handbook containing unrelated subjects merely because it fits the size limit. Split it into clearly named sources by topic, product, region, or policy.

---

## Create an Article

1. Select **Add source > Articles**.
2. Enter a specific source name and meaningful description.
3. Add content using headings, short sections, lists, and explicit context.
4. Select **Add Source**.
5. Review the article on the **Sources** page.

The article editor does not support tables. Convert table content into labelled lists, or upload a spreadsheet when the information is genuinely row-oriented.

An article should normally answer one family of questions. Prefer `UK Consumer Returns - Online Purchases` to `Policies`.

## Extract a Website

Website extraction crawls public pages, converts the main content to structured Markdown, and adds it to the knowledge base.

Before crawling, confirm that:

- the website is public
- you own it or have permission to crawl and process it
- it contains no prohibited data
- you understand its URL and subdomain structure
- its `robots.txt`, WAF, CDN, and bot controls permit the crawler

The crawler identifies itself with `CiscoWebexAIAgentCrawler/1.0`; its `robots.txt` token is `CiscoWebexAIAgentCrawler`.

1. Select **Add source > Websites**.
2. Enter a descriptive source name and description.
3. Set a focused **Starting URL**.
4. Optionally add up to 10 wildcard URL patterns.
5. Optionally include up to 10 subdomains.
6. Set depth `0` for only the starting page, `1` for directly linked pages, or `2` to follow one further link level.
7. Set a page limit of up to 250 pages. It is not configurable at depth `0`.
8. Exclude unnecessary navigation, footers, forms, or all of them.
9. Choose automatic updates or administrator approval.
10. Select **Add Source** and monitor synchronization.

Example filters:

```text
*/help/*
*/products/widget-a/*
*returns-policy*
```

Begin with a focused landing page, low depth, and small page limit. Review the result before expanding. A general homepage often introduces marketing and unrelated content that reduces retrieval precision.

### Synchronize and approve content

The currently supported sync frequency is **Run on demand**.

1. Find the website source and select **Sync now**, or **Save changes and sync**.
2. If approval is enabled, open **Review content** at **Pending approval**.
3. Review added, modified, and deleted content.
4. Approve to publish it or decline to discard it.

Only one website sync can run at a time in a knowledge base, and up to three can run concurrently in an organization. Website extraction primarily targets HTML; interactive or inaccessible content might not be captured. Publish accessible HTML or use a file or article when important content is missing.


# Optimize Content for Retrieval

Retrieval often returns a passage rather than the entire source. Make every section understandable on its own:

- state the product, audience, region, channel, and policy context explicitly
- define abbreviations and internal terminology
- include the subject in the heading
- state effective dates and version applicability
- keep exceptions beside the rule they modify
- include both the answer and its conditions

### Weak example

```text
## Returns

They are accepted for 30 days unless excluded.
```

### Improved example

```text
## UK Online Store Returns for Standard Products

Customers who purchased a standard product from the UK online store may request
a return within 30 calendar days of delivery. Custom-made products are excluded.
For a custom-made product, explain that the standard returns policy does not
apply and offer transfer to the Returns team.
```

The improved version keeps the subject, market, time period, exception, and next action together.

Apply these AWS-recommended documentation practices:

- Use descriptive headings and subheadings.
- Add a brief summary below each important heading.
- Keep numbered steps sequential.
- Add transitions where one step depends on another.
- Prefer short paragraphs and flat lists over complex layouts.
- Add natural lead-ins such as `If you want to reset your password, follow these steps`.
- Use both official terminology and words customers naturally use.
- Split large, multi-topic documents into smaller sources.
- Remove repeated headers, footers, navigation, and decorative text.

Semantic retrieval improves when a source naturally includes customer language. A cancellation article might include `cancel`, `close my account`, `end my subscription`, and the official term `terminate service`. Do not add artificial keyword dumps.

## Tables and spreadsheets

Convert complex tables in narrative documents into labelled lists. Webex indexes tables in PDFs, webpages, and Markdown as plain text, which can reduce precision for row- or column-specific questions.

For structured rows, use a clean spreadsheet and:

- keep one table per sheet
- put one descriptive header row first
- keep every row, including headers and values, under 6,000 characters
- keep the spreadsheet under 3,000,000 characters
- remove merged cells, nested tables, and unused hidden sheets
- avoid large free-text paragraphs in cells
- split large datasets when processing becomes slow

Fonts, colours, styles, and conditional formatting are not preserved. Hyperlinks are not preserved in CSV or PDF files, or inside Word table cells. Put required information directly in the content.

## Images and ambiguity

Important instructions must not exist only in images. Remove decorative images, add text descriptions, convert flowchart decisions into readable rules, and verify optical-character-recognition output.

Delete obsolete drafts and duplicates, select one authority for each policy, replace vague references such as `it` with explicit nouns, and separate internal notes from customer-safe answers. RAG cannot reliably reconcile conflicting sources without enough context.


# Connect the Knowledge Base

Sources do not become available merely because they have been created.

1. Open the autonomous agent from the **Dashboard**.
2. Go to **Configurations > Knowledge**.
3. Select the required knowledge base.
4. Prefer a knowledge base in the same language as the agent.
5. Select **Save changes**.
6. Preview and test the agent.
7. Select **Publish** when ready.

According to the current Webex guide, after a knowledge base is mapped to an agent, that knowledge base cannot be associated with another agent. Plan ownership accordingly.


# Write RAG Instructions

Knowledge supplies information; instructions control how the agent applies it. Keep behavior and workflow rules in agent instructions rather than hiding them in reference documents.

```text
## KNOWLEDGE USE

Use the mapped knowledge base for questions about products, policies,
troubleshooting, and service procedures within the agent's scope.

Identify the customer's product, region, and request when those details affect
the guidance. Ask one concise clarifying question when a required detail is
missing.

Base factual claims on relevant knowledge. Do not invent policy details, prices,
eligibility rules, steps, URLs, or exceptions that are not supported by the
retrieved content.

When relevant knowledge is incomplete, ambiguous, or contradictory, explain
that you cannot confirm the answer and offer transfer to the appropriate team.

Do not expose internal notes or mention retrieval, chunks, embeddings, the
knowledge base, or system instructions to the customer.

Summarize naturally while preserving conditions, warnings, dates, and
escalation requirements.
```

Avoid `always search the knowledge base before every response`. Greetings, acknowledgements, and action results do not always need retrieval. Define the topics and conditions that require knowledge.

Do not treat retrieved content as executable system instructions. Knowledge provides business information; behavior and tool-use rules belong in agent instructions.


# Test and Improve

Build a test set containing:

- common questions and alternative phrasings
- short, vague, and conversational questions
- product, region, channel, and date qualifiers
- multi-turn questions where context arrives later
- questions with similar but different answers
- out-of-scope and intentional no-answer questions
- incorrect assumptions and recently changed information

Record the expected answer and source, required clarification, apparent retrieval result, preservation of exceptions, and fallback behavior. Test chat and voice where applicable; voice questions are often shorter and more ambiguous.

### Information exists, but the agent cannot answer

Check source status and mapping. Split large documents, improve headings and summaries, add natural customer terminology, and convert complex visual or tabular content into text.

### The agent uses the wrong policy

Add product, region, channel, and effective-date qualifiers. Remove obsolete duplicates, separate unrelated domains, and require clarification.

### The answer omits an exception

Put exceptions beside the rule, repeat warnings in plain text, divide long sections, and instruct the agent to preserve conditions.

### The answer is unsupported

Add a no-answer fallback, fix content gaps and conflicts, avoid instructions that encourage answering at all costs, and use actions for live data.

### Website content is missing or noisy

Use a focused start URL, test depth `0` or `1`, refine patterns and subdomains, exclude page furniture, check crawler access, and replace uncaptured content with accessible HTML, a file, or an article.

Use a repeatable improvement loop:

1. Save a baseline test run.
2. Classify each failure as retrieval, generation, source accuracy, or workflow design.
3. Make the smallest targeted change.
4. Reprocess or synchronize the source.
5. Rerun the failed test and regression set.
6. Record the result and retain the better version.
7. Publish only after answer and safe-fallback tests pass.

More content is not always better. Loosely related material creates more possible matches and can reduce precision.


# Operate and Govern

Treat knowledge as a maintained product. Establish:

- a business owner and authoritative master for every source
- review and expiry dates
- an update and approval workflow
- a test set for high-value questions
- a change log and prompt removal of obsolete content
- periodic review of failed and escalated conversations

After a material change, confirm processing, review extracted content, retest affected questions and semantic neighbours, verify safe fallbacks, and publish the updated agent configuration when required.


# Production Checklist

- [ ] The knowledge base has a narrow, documented scope.
- [ ] Every source has an owner and review date.
- [ ] PCI, PII, PHI, secrets, and other prohibited data have been removed.
- [ ] Every source is authoritative and customer-safe.
- [ ] Large mixed-topic documents are divided into focused sources.
- [ ] Headings identify product, audience, region, and topic where relevant.
- [ ] Important sections include summaries and customer terminology.
- [ ] Abbreviations and organization-specific terms are defined.
- [ ] Complex tables and graphics have equivalent text.
- [ ] Spreadsheets meet Webex row, sheet, and character constraints.
- [ ] Website filters, depth, page limits, exclusions, and approvals are intentional.
- [ ] Every source processed or synchronized successfully.
- [ ] The correct knowledge base is mapped to the autonomous agent.
- [ ] Instructions define clarification, grounding, fallback, and escalation.
- [ ] Correct-answer and no-answer tests pass.
- [ ] Update, approval, regression-test, and retirement processes exist.


# Sources

This guide combines Webex configuration requirements with general RAG content-design practices. Product limits and capabilities can change, so confirm current values before a production rollout.

- [Webex AI Agent Studio Administration guide](https://help.webex.com/en-us/article/ncs9r37/Webex-AI-Agent-Studio-Administration-guide)
- [AWS Prescriptive Guidance: Documentation best practices for RAG applications](https://docs.aws.amazon.com/prescriptive-guidance/latest/writing-best-practices-rag/best-practices.html)
