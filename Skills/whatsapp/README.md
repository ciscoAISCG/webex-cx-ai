# WhatsApp SIP Gateway

This skill guides an assistant through building, deploying, and troubleshooting a Meta WhatsApp Business Calling SIP-mode gateway that bridges to Cisco Webex Contact Center or a Webex AI Agent through FreeSWITCH, Docker, and AWS EC2.

It includes the production lessons from the first working build, including the Meta/Webex number split, SDES-SRTP, Opus-to-PCMU/PCMA transcoding, Webex trunk registration, PAI/RPID caller identity, and the `silence_stream://500` cold-call warmup fix.

## Files

- [SKILL.md](./SKILL.md)
- [agents/openai.yaml](./agents/openai.yaml)
