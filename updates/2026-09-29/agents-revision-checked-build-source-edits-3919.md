---
title: "Agent Builder 改文件更省事了：小范围修改不再要求整份源文件重传"
type: "Improvement"
priority: "中"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# Agent Builder 改文件更省事了：小范围修改不再要求整份源文件重传

## 核心宣传点

Agent Builder 里以前改一点东西也要让模型把整份源文件重新发一遍，既慢又容易出错。现在新增了受限的内部读写操作，引擎可以直接应用常规的文件工具编辑，并通过已有的变更集把受影响的文件持久化。读写都绑定在规范的 Build 会话、计算实例和已有的编辑权限上，变更必须带一个不透明的修订令牌并通过原有的状态与版本 CAS 校验。变更按相对不可变基线的净差异存储：同一路径反复编辑只占一条操作记录，改回原样则该操作被移除。32 个路径、4 MiB 的上限，头像规范化、派生产物、继承引用和技能校验全部保留。候选结果会在头像晋级前完整校验一次，CAS 之前再校验一次规范化后的结果；非法的新技能名、超大输入和含 NUL 的输入在落盘前就被拒绝。旧的编写工具保持兼容，没有新增表、后台同步或跨轮次的自动草稿。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

Build currently requires the model to resend whole source files for small edits. Add bounded internal `files_read` / `files_apply` operations so Engine can apply ordinary file-tool edits and persist affected files through the existing ChangeSet.

- Bind reads and writes to the canonical Build session, computer and existing edit permission. Require an opaque revision token and the existing state/version CAS for mutation.
- Store net changes relative to the immutable base: repeated edits consume one operation per changed path, and reverting removes the operation. Preserve the 32-path / 4 MiB limits, avatar normalization, derived assets, inherited references and Skill validation.
- Validate the complete candidate before avatar promotion; check the normalized result again before CAS. Invalid new Skill names, oversize and NUL inputs are rejected before artifact I/O.
- Keep legacy authoring tools compatible. No new tables, background synchronization or automatic cross-turn draft continuation.

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/1693. Companion Engine PR: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1758. Deploy this backend before Engine; roll Engine back first.

## Test plan

- Independent local review completed; 120 backend tests passed after rebasing onto main and adding avatar pre-validation regressions (240 broader tests passed in the implementation validation).
- Backend static verification and commit hooks passed.
- Real existing zooclaw-dev lane with staging CSFLE Mongo, actual model and staging E2B: ordinary edit/write/patch → validate → isolated run_test → commit → a new active task executing the registered Skill. Both evaluation and active execution returned `SOURCE_VERSION_2`.
- Readback confirmed only two expected files changed; untouched CRLF script bytes remained identical. Exact 4 MiB snapshot, oversize rejection, stale retry, concurrent 200/409 CAS, failed-batch atomicity and session/computer authorization checked through HTTP.
- Disposable fixtures and sandboxes cleaned. No production or existing user data changed.

The live evidence predates the final rebase onto main; focused regression/static checks are repeated on the rebased branch. This does not claim browser UI, deployed ingress, channel delivery or concurrent peak-memory validation.

Atomicity covers ChangeSet content/version persistence. Avatar promotion retains the existing shared content-addressed storage behavior: a concurrent CAS loss can leave an unreferenced object, and this PR does not add object deletion/GC that could remove another reference to the same immutable bytes.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ab84000b1e07a7e8650bdea01bc5a35efc1f0ee7`
- PR: #3919
- 作者：kaka-srp
- 日期：2026-09-29T04:02:13Z

### Commit Message

```
feat(agents): support revision-checked Build source file edits (#3919)

## Summary

Build currently requires the model to resend whole source files for
small edits. Add bounded internal `files_read` / `files_apply`
operations so Engine can apply ordinary file-tool edits and persist
affected files through the existing ChangeSet.

- Bind reads and writes to the canonical Build session, computer and
existing edit permission. Require an opaque revision token and the
existing state/version CAS for mutation.
- Store net changes relative to the immutable base: repeated edits
consume one operation per changed path, and reverting removes the
operation. Preserve the 32-path / 4 MiB limits, avatar normalization,
derived assets, inherited references and Skill validation.
- Validate the complete candidate before avatar promotion; check the
normalized result again before CAS. Invalid new Skill names, oversize
and NUL inputs are rejected before artifact I/O.
- Keep legacy authoring tools compatible. No new tables, background
synchronization or automatic cross-turn draft continuation.

Related:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1693.
Companion Engine PR:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1758. Deploy
this backend before Engine; roll Engine back first.

## Test plan

- Independent local review completed; 120 backend tests passed after
rebasing onto main and adding avatar pre-validation regressions (240
broader tests passed in the implementation validation).
- Backend static verification and commit hooks passed.
- Real existing zooclaw-dev lane with staging CSFLE Mongo, actual model
and staging E2B: ordinary edit/write/patch → validate → isolated
run_test → commit → a new active task executing the registered Skill.
Both evaluation and active execution returned `SOURCE_VERSION_2`.
- Readback confirmed only two expected files changed; untouched CRLF
script bytes remained identical. Exact 4 MiB snapshot, oversize
rejection, stale retry, concurrent 200/409 CAS, failed-batch atomicity
and session/computer authorization checked through HTTP.
- Disposable fixtures and sandboxes cleaned. No production or existing
user data changed.

The live evidence predates the final rebase onto main; focused
regression/static checks are repeated on the rebased branch. This does
not claim browser UI, deployed ingress, channel delivery or concurrent
peak-memory validation.

Atomicity covers ChangeSet content/version persistence. Avatar promotion
retains the existing shared content-addressed storage behavior: a
concurrent CAS loss can leave an unreferenced object, and this PR does
not add object deletion/GC that could remove another reference to the
same immutable bytes.
```

来源：SerendipityOneInc/ecap-workspace @ ab84000b，PR #3919，作者 kaka-srp。
