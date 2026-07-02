# ecap-skills — commits 2026-07-01

共 3 个 commit


## fix(publish): add _BGM to PUBLISHED_SKILLS whitelist (#226)

- **SHA**: `6b86ec42e37a1e95a190c1e2a562b4a07cc57e54`
- **作者**: allenz-srp <allenz@srp.one>
- **日期**: 2026-07-01T12:09:54Z
- **URL**: https://github.com/SerendipityOneInc/ecap-skills/commit/6b86ec42e37a1e95a190c1e2a562b4a07cc57e54
- **PR**: #226

### 完整 Commit Message

```
fix(publish): add _BGM to PUBLISHED_SKILLS whitelist (#226)

## Summary
- Register the shared `_BGM` library in `PUBLISHED_SKILLS` so it is
actually published to the JuiceFS S3 gateway.

## Root cause
PR #225 added `_BGM/` (mp3 via Git LFS + `bgm.json` + scripts) and
correctly configured `.gitattributes` (`*.mp3` → LFS) and the workflow
checkout (`lfs: true`). However, `publish-skills.yml` does **not** sync
the whole repo — it only copies directories listed in `PUBLISHED_SKILLS`
into a staging dir, then runs `aws s3 sync --delete`.

Since `_BGM` was never added to the whitelist, it was silently skipped.
Run
[#28507111747](https://github.com/SerendipityOneInc/ecap-skills/actions/runs/28507111747)
reported success but the BGM assets never reached JuiceFS. Same class of
issue previously handled for `_fonts`.

## Fix
Add `_BGM` to `PUBLISHED_SKILLS` (next to `_fonts` as a shared LFS
library).

## After merge
Cut a new tag (e.g. `v0.6.9-beta.2`) to re-trigger the staging publish,
or run the workflow via `workflow_dispatch`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Register the shared `_BGM` library in `PUBLISHED_SKILLS` so it is actually published to the JuiceFS S3 gateway.

## Root cause
PR #225 added `_BGM/` (mp3 via Git LFS + `bgm.json` + scripts) and correctly configured `.gitattributes` (`*.mp3` → LFS) and the workflow checkout (`lfs: true`). However, `publish-skills.yml` does **not** sync the whole repo — it only copies directories listed in `PUBLISHED_SKILLS` into a staging dir, then runs `aws s3 sync --delete`.

Since `_BGM` was never added to the whitelist, it was silently skipped. Run [#28507111747](https://github.com/SerendipityOneInc/ecap-skills/actions/runs/28507111747) reported success but the BGM assets never reached JuiceFS. Same class of issue previously handled for `_fonts`.

## Fix
Add `_BGM` to `PUBLISHED_SKILLS` (next to `_fonts` as a shared LFS library).

## After merge
Cut a new tag (e.g. `v0.6.9-beta.2`) to re-trigger the staging publish, or run the workflow via `workflow_dispatch`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Add shared BGM library (#225)

- **SHA**: `caace94eb8a73a083c7331b14551fa59c1f0a23b`
- **作者**: lynn Zhuang <lynn@srp.one>
- **日期**: 2026-07-01T09:06:18Z
- **URL**: https://github.com/SerendipityOneInc/ecap-skills/commit/caace94eb8a73a083c7331b14551fa59c1f0a23b
- **PR**: #225

### 完整 Commit Message

```
Add shared BGM library (#225)

## Summary
- add a shared _BGM library with the Founder IP Studio BGM collection
- add bgm.json metadata and resolve_bgm.py for agent consumption
- publish _BGM alongside _fonts and track mp3 assets with Git LFS

## Verification
- jq empty _BGM/bgm.json
- python3 _BGM/scripts/resolve_bgm.py --id calm-ambition
- python3 _BGM/scripts/resolve_bgm.py --use-case 'founder vision'
--energy medium --format json
- confirmed mp3 files are staged and pushed as Git LFS pointers

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary
- add a shared _BGM library with the Founder IP Studio BGM collection
- add bgm.json metadata and resolve_bgm.py for agent consumption
- publish _BGM alongside _fonts and track mp3 assets with Git LFS

## Verification
- jq empty _BGM/bgm.json
- python3 _BGM/scripts/resolve_bgm.py --id calm-ambition
- python3 _BGM/scripts/resolve_bgm.py --use-case 'founder vision' --energy medium --format json
- confirmed mp3 files are staged and pushed as Git LFS pointers


## docs(review): customized code-review.md (#224)

- **SHA**: `7e46f342efee319773026a75d68d99b94de5c9c2`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-07-01T07:24:55Z
- **URL**: https://github.com/SerendipityOneInc/ecap-skills/commit/7e46f342efee319773026a75d68d99b94de5c9c2
- **PR**: #224

### 完整 Commit Message

```
docs(review): customized code-review.md (#224)

Customized review guide (PR 2 of 2, stacked on baseline). Distilled from
~3mo local git history + CLAUDE.md/docs + ECA Linear, lean
ecap-workspace style. Base is the baseline branch (diff reads baseline
-> custom); auto-retargets to main when baseline merges.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

Customized review guide (PR 2 of 2, stacked on baseline). Distilled from ~3mo local git history + CLAUDE.md/docs + ECA Linear, lean ecap-workspace style. Base is the baseline branch (diff reads baseline -> custom); auto-retargets to main when baseline merges.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
