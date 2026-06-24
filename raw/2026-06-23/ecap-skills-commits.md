# SerendipityOneInc/ecap-skills — commits 2026-06-23


共 1 个 commit


---

## feat(chameleon-seedance): 支持 4K 输出 + bitrate_mode 高码率 (#216)

- **SHA**: `df81e1356398f8bf7e7c363ca9f83361b0ba7f97`
- **作者**: david-srp
- **日期**: 2026-06-23T14:01:16Z
- **PR**: #216

### 完整 commit message

```
feat(chameleon-seedance): 支持 4K 输出 + bitrate_mode 高码率 (#216)

* feat(chameleon-seedance): support 4K output + bitrate_mode high

- --resolution: add `4k` (Pro-only; reject on fast/mini before request)
- add --bitrate-mode high -> payload `bitrate_mode` (file size ~3-5x)
- record bitrate_mode in generation_log.csv (appended column, keeps old
  logs aligned)
- refresh kb-summary / API reference / SKILL.md with 4K facts (H.265/HEVC,
  10-bit, default high bitrate, separate 4K rate limit) + bitrate,
  concurrency and pricing notes
- mark resolution/bitrate items done in script-roadmap

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

* fix(chameleon-seedance): migrate generation_log header + add regression tests

Address Codex review on PR #216:

- generation_log.csv: migrate older append-only headers to the current
  schema in place (rewrite header + pad existing rows atomically), and
  align the appender to the file's actual header. Adding the bitrate_mode
  column no longer produces a ragged CSV on pre-existing logs.
- add tests/test_chameleon_generate.py: 4k payload on Pro, 4k rejection
  on fast/mini, bitrate_mode high/omitted/invalid, and CSV header
  migration (stays rectangular, legacy row padded, new column captured).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR body

## 背景
官方更新:Seedance 2.0(pro)新增 **4K 输出**,且 Seedance 2.0 / 2.0 fast 上线 **高码率**(`bitrate_mode: high`)。本 PR 把这些参数接入 `chameleon-seedance` skill 的脚本与各文档。

## 改动(仅 5 个文件,+100/-7)
**脚本 `scripts/chameleon_generate.py`**
- `--resolution` 新增 `4k` 选项;`4k` 仅 pro 模型可用,fast/mini 在发请求前直接拒(新增 `MINI_MODEL_MARKER`)
- 新增 `--bitrate-mode high`,写入请求 `bitrate_mode` 字段(默认不传,保持请求体清爽;文件体积约增大 3~5×)
- `generation_log.csv` 末列新增 `bitrate_mode`(追加在末尾,不破坏已有台账列对齐)
- docstring 补 4K / 高码率两个用法示例

**文档**
- `references/chameleon-kb-summary.md`:新增「4K 输出」「码率模式」「计费参考」三节,更新分辨率/默认值/客户端限制
- `references/byteplus-dreamina-seedance-2.0-api.md`:参数表加入 4K + `bitrate_mode`,新增「05 4K output & bitrate」(并发/限流表 + 计费表)
- `SKILL.md`:修正过时的 output 分辨率描述为 `480p/720p/1080p/4k`
- `_dev/script-roadmap.md`:把已实现项标注清楚

## 关键事实
- 4K:仅 pro;H.265/HEVC + 10bit;默认高码率;独立限流(个人/企业各 1 并发 15RPM)
- `bitrate_mode:high`:2.0 与 fast 均支持;文件增大 3~5×;4K 默认即高码率

## 验证(dry-run,全部通过)
- 4K@pro → payload 含 `"resolution":"4k"`;`--bitrate-mode high` → 含 `"bitrate_mode":"high"`
- 4K@fast、4K@mini → 发请求前 exit 1 并给出明确原因
- 默认请求不含 `bitrate_mode`;非法分辨率被 argparse 拒;CSV 行携带 `bitrate_mode` 且列对齐

> 注:`safety_identifier` 在 API 参考里已记录但脚本仍未接入,本 PR 暂不处理(roadmap 已标「仍待补」)。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
