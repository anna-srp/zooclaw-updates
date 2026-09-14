# SerendipityOneInc/ecap-workspace — commits 2026-09-12

## feat(desktop): unify remote v2 cloud sessions and desktop source (#3701)

- **SHA**: `54809790934639ab9d12bbf1d1a55caa7f073293`
- **作者**: zayne-srp
- **日期**: 2026-09-12T04:23:10Z
- **PR**: #3701

### Commit Message

```
feat(desktop): unify remote v2 cloud sessions and desktop source (#3701)

## Summary

- Make Remote V2 use the Web/Mattermost conversation list and canonical
history; send ACP prompts through Mattermost/ACS rather than creating
unrelated Engine sessions.
- Reuse Web optimistic send feedback, reaction UI, model selection and
agent filtering; preserve local ACP agent behavior and keep unsupported
attachments disabled.
- Add versioned Desktop source metadata for the companion ACS PR
https://github.com/SerendipityOneInc/agent-channel-service/pull/121.
Metadata is contextual only and never authorization or a device-routing
credential.
- Update packaged DSH runtime through Git LFS, expose Desktop tools
naming, and fix packaged web staging manifests. Runtime manifest records
dirty DSH source hashes; this is a beta artifact, not a clean upstream
DSH release.

## Validation

- Targeted frontend and Desktop tests run locally; backend ACP tests,
Ruff and import boundaries checked.
- Synthetic ACS acceptance verifies final Engine input, unchanged Web
follow-up, session identity and duplicate suppression. It does not
exercise a real model.
- Staging deployments succeeded: Claw Interface
`service-v0.18.3-beta.desktop-source.1`, Web `ecap-v0.19.4-beta`, ACS
`v0.1.14-beta.desktop-source.1`. Packaged arm64 App rebuilt from
b7beaed8a and installed locally; no dev server.
- Real packaged App -> staging -> Engine verified Desktop source
context. Desktop MCP read retrieved the local sentinel through
`mcp__acp-desktop-tools__read`; Engine history contains the correct tool
result and final answer.
- Web displays Desktop messages and answers; a Web follow-up and reply
appear live in Desktop. Model catalog (34 entries) and picker menu match
Web exactly. Source context is not rendered in Mattermost message
bodies.
- Added identity-scoped Remote V2 cache regression tests: 17
conversation tests pass; local ACP keys and prefix invalidation
preserved. Review timeout claim adjudicated separately: DSH prompt API
returns queue acceptance, not full turn completion.

## Acceptance findings still open — not a full pass

- Concurrent Desktop/Web prompts in one thread can leave an incorrect
“Completed without a visible response” label on the earlier prompt. The
shared Web status helper associates visible replies with the nearest
preceding user post rather than the explicit run identity.
- A late `assistant_phase=preview` post can arrive after that same run's
final segment and terminal marker, producing a duplicate visible answer.
Staging evidence: conversation `a85747c961ba49a3a3a01d6828df030f`, run
`run-JNIgv7UcRpeVqXbuiMBVVQ-2`; final `xcpa4hk5y3d9tbky73wu15rcje`,
terminal `pizme78c43fat8ysnk3xgqxixe`, late preview
`3yx4xabai7fc8xicsti6gw8kya`.
- This does not indicate a missing Engine answer or failed MCP bridge:
both real Engine history and Mattermost contain the final result. Keep
PR unmerged pending adjudication/repair of these ordering issues.
- Live local Codex/Claude, reaction persistence and a >30-second prompt
have not been included in this staging acceptance pass; unit coverage is
not being represented as those live checks.

## Deployment

Deploy both Claw Interface and Web from this branch using staging beta
tags, together with ACS #121. No production deployment or main merge
requested. Rebuild the Desktop App with the new relay header for source
metadata to take effect.

## Exclusions

No local hooks, npm credentials, test launcher secrets, or local
environment files are included. No Engine implementation changes.

## Desktop-owned context update

- Editable template: `desktop/resources/dsh/desktop-source-context.txt`,
automatically included by the existing Electron resources packaging
rule. No DSH binary changes required.
- The Remote V2 relay adds `params._meta["zoowork.ai/message-source"] =
{version: 1, client: "desktop", context}` to each ACP `session/prompt`,
preserving user text, pending-post metadata and unrelated RPC frames.
This is our extension, not an official ACP field.
- Claw Interface validates exact fields/version/client and a nonblank,
NUL-free, valid UTF-8 context of at most 4096 bytes before sending, then
forwards it in the existing Mattermost property on Desktop-marked
connections only. Invalid source input returns invalid-params before
submission. Without source context it sends no source property; ACS does
not inject any fallback text.
- Latest local verification: 4 real relay/WebSocket tests, 54 targeted
backend tests, Desktop typecheck, Ruff/Pyright/import contracts passed.
Companion ACS adds custom-context and Web isolation coverage.
- Deploy ACS first, then Claw Interface, then updated Desktop. No
staging deployment or installed-App replacement was performed for this
update; earlier beta acceptance evidence is not a live verification of
the new custom-context contract.

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```
