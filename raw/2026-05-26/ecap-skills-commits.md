# SerendipityOneInc/ecap-skills Commits — 2026-05-26

## 0bd9b02d
- **Author:** sharplee-srp
- **Date:** 2026-05-26T06:20:36Z
- **SHA:** 0bd9b02d57ad8c17c967b667a9ea1fe53be576ab

### Commit Message
```
fix(designer): send generated images to current chat (#205)

Instruct designer to deliver every generated image through the message media parameter while omitting current-chat target aliases.\n\nLinear: https://linear.app/srpone/issue/ECA-803
```

### PR #205: fix(designer): send generated images to current chat

**PR Description:**
## Summary
- Update designer image delivery instructions to send every generated file through message media.
- Tell the agent to omit target/channel for current-chat delivery and never use user:me aliases.
- Pin the devcontainer to the OpenClaw 2026.5.7 product baseline.

## Root cause
- The failed image send came from an assistant tool call that used target=user:me for a Mattermost media message. OpenClaw 5.7 did not treat that alias as current-chat delivery, so Mattermost rejected it as an invalid user id.
- The designer instructions did not explicitly forbid current-chat self aliases or require all generated image paths to be sent.

## Linear
- https://linear.app/srpone/issue/ECA-803

## Test plan
- [x] git diff --check
- [x] Devcontainer tested on OpenClaw 2026.5.7 baseline with local Mattermost extension package.
- [x] Staging test intentionally did not overwrite designer/SKILL.md; only non-skill plugin paths were hotpatched and validated.

---
