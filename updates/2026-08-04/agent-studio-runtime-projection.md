---
title: "Agent Studio 支持 Pack 声明的 Python/二进制依赖自动装配"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "0df94387bc3087107e057623f2a45a274f2b19d1"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

v2 Agent Pack 里声明的 dependencies.python 和 dependencies.bins 现在会自动装配进引擎运行环境，创作者的 Pack 依赖开箱即用，无需手动配置环境。

## 原始内容

```
feat(agent-builder): complete v2 Agent Studio runtime projection (#3215)

## Summary

- project v2 Agent Pack `dependencies.python` and `dependencies.bins`
into Engine Environment packages and include them in Environment
identity;
- keep ordinary installed Agents and Pack Test on Engine's default
onboarding lifecycle, while creating only the shared hidden Agent
Builder with `onboarding:false`;
- apply candidate avatar metadata to the Pack Test workspace using the
same bounded archive validation used by Submit;
- preserve Pack Test's existing physical-Agent reuse policy: no
onboarding-specific replacement or update branch;
- share avatar parsing and split dependency/model/install policy into
focused modules so existing service files stay within repository size
limits.

Agent Studio source changes are reviewed separately in [ecap-agent-pack
PR #209](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209).

## Design

The implementation follows [the checked-in
design](docs/superpowers/specs/2026-08-04-agent-studio-v2-runtime-completeness.md).

Important lifecycle behavior:

- each newly created installed Agent inherits Engine onboarding and
onboards once;
- Pack updates and new Sessions do not reset onboarding;
- uninstall/reinstall creates a new Agent and therefore onboards again;
- Agent Builder's hidden shared authoring Agent skips onboarding;
- Pack Test receives no onboarding special case.

## Compatibility

- normal install omits the `onboarding` field, preserving the existing
Engine default;
- legacy Pack translation remains permissive; strict dependency
validation is enabled only for v2 runtime assets and v2 Pack Test
candidates;
- empty dependency sets preserve the legacy Environment hash;
- no endpoint or Engine API shape is added beyond using Engine's
existing optional create-time `onboarding` field;
- v1 Builder behavior is unchanged; the only shared-file change moves
existing avatar validation into a common helper with its tests
preserved.

## Validation

- `bash scripts/verify-py.sh` — passed (ruff, formatting, pyright,
import contracts);
- focused Engine/Pack runtime tests — `279 passed`;
- additional model/lifecycle refactor coverage — `206 passed`;
- Pack Test runtime — `5 passed`;
- pre-commit and pre-push repository gates — passed.

## Staging acceptance

- create/open an Agent Builder v2 project;
- Package & Test a Pack with Python/binary dependencies and a relative
avatar;
- rerun Package & Test with persona-only changes and confirm Test Agent
reuse with a fresh Session;
- change Environment content/dependencies and confirm physical Agent
replacement;
- install a submitted Agent and confirm its own onboarding starts once.

---

### PR Body

## Summary

- project v2 Agent Pack `dependencies.python` and `dependencies.bins` into Engine Environment packages and include them in Environment identity;
- keep ordinary installed Agents and Pack Test on Engine's default onboarding lifecycle, while creating only the shared hidden Agent Builder with `onboarding:false`;
- apply candidate avatar metadata to the Pack Test workspace using the same bounded archive validation used by Submit;
- preserve Pack Test's existing physical-Agent reuse policy: no onboarding-specific replacement or update branch;
- share avatar parsing and split dependency/model/install policy into focused modules so existing service files stay within repository size limits.

Agent Studio source changes are reviewed separately in [ecap-agent-pack PR #209](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209).

## Design

The implementation follows [the checked-in design](docs/superpowers/specs/2026-08-04-agent-studio-v2-runtime-completeness.md).

Important lifecycle behavior:

- each newly created installed Agent inherits Engine onboarding and onboards once;
- Pack updates and new Sessions do not reset onboarding;
- uninstall/reinstall creates a new Agent and therefore onboards again;
- Agent Builder's hidden shared authoring Agent skips onboarding;
- Pack Test receives no onboarding special case.

## Compatibility

- normal install omits the `onboarding` field, preserving the existing Engine default;
- legacy Pack translation remains permissive; strict dependency validation is enabled only for v2 runtime assets and v2 Pack Test candidates;
- empty dependency sets preserve the legacy Environment hash;
- no endpoint or Engine API shape is added beyond using Engine's existing optional create-time `onboarding` field;
- v1 Builder behavior is unchanged; the only shared-file change moves existing avatar validation into a common helper with its tests preserved.

## Validation

- `bash scripts/verify-py.sh` — passed (ruff, formatting, pyright, import contracts);
- focused Engine/Pack runtime tests — `279 passed`;
- additional model/lifecycle refactor coverage — `206 passed`;
- Pack Test runtime — `5 passed`;
- pre-commit and pre-push repository gates — passed.

## Staging acceptance

- create/open an Agent Builder v2 project;
- Package & Test a Pack with Python/binary dependencies and a relative avatar;
- rerun Package & Test with persona-only changes and confirm Test Agent reuse with a fresh Session;
- change Environment content/dependencies and confirm physical Agent replacement;
- install a submitted Agent and confirm its own onboarding starts once.

```
