---
title: "修复：同一 Agent 多个会话并行跑技能时，临时文件不再互相覆盖导致产物出错"
type: "Bug Fix"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：同一 Agent 多个会话并行跑技能时，临时文件不再互相覆盖导致产物出错

## 核心宣传点

v2 的沙箱是按 Agent 共享的：同一个 Agent 下并发的多个会话共用 /tmp、/workspace 和 home 目录。而技能文档里写死的固定临时路径（例如 xlsx 的固定工作目录、批量视频的固定输出目录、固定名的中间图片）会被模型照抄，于是两个同时运行的会话会往同一个目录写文件、互相覆盖，表现就是表格、PPT、图片或视频产物内容错乱、张冠李戴。这次把 xlsx、pdf、pptx、web-designer、viral-ads、meeting-notes 等技能的示例与脚本默认目录，全部改成每次运行现场生成的唯一目录，并在规范里固化了这条要求；批量视频脚本的输出目录默认值也改为每次运行新建并打印，恢复模式下不指定目录会直接报错，避免复用到别人会话的语音文件。同时修掉了 Word/PPT 转换组件在共享目录里编译中间文件的竞争问题，改为唯一命名后原子发布。按内容哈希或 UUID 命名的路径、以及本来就加了锁的跨运行状态目录保持不变。

## 分级

- 内部：P0
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 摘要

v2 的 Sandbox 是 agent-scoped：`/tmp`、`/workspace`、`~` 由同一 Agent 的并发 session 共享，而模型会照抄 skill 里的示例路径。skill 里写死的 `/tmp/<固定名>`（如 `/tmp/xlsx_work/`、`/tmp/viral_batch/`、`/tmp/raw.jpg`）会让两个并发 session 互相覆盖。engine 侧不做 per-session 私有 /tmp（SerendipityOneInc/zooclaw-engine#1719 已否决），冲突改为在 skills 里靠约定解决（背景：SerendipityOneInc/zooclaw-engine#1203）。

- **规范**：`CLAUDE.md` §6 新增规则——每次运行的临时目录用 `mktemp -d` / `tempfile.mkdtemp` 生成；示例里后续步骤引用同一变量，SKILL.md 要求复用打印出的字面路径（shell 变量不一定能带到下一次 exec）；脚本默认目录同样适用；只有按 hash/uuid 命名的文件和确需跨运行保留、原子写或加锁的 `/tmp/openclaw/<skill>/` 状态可以共享。`code-review.md` 加 "Unique scratch" 检查项。
- **文档**：xlsx（SKILL.md 与 references 全部场景）、pdf/pptx/web-designer 的图片处理、pptx 的 zooclaw-ppt-runtime 与 editing、viral-ads、meeting-notes（workspace 下的确认状态目录）改为每次运行唯一的目录。
- **脚本**：`viral-ads/scripts/batch.py`、`gen_video.py` 的 `--output-dir` 默认值从固定 `/tmp` 目录改为 mkdtemp 并打印路径；`gen_video.py --mode resume` 未给 `--output-dir` 时报错退出（原固定目录会让不同 session 复用彼此的 TTS）。xlsx 脚本只改 usage 注释。

已审计但保留：hash/uuid/mkdtemp 命名的路径（designer、video-generator、docx、zooclaw-asr/tts 等），council 的 deps/锁目录（已有 bounded flock + `os.replace`），pptx shape-cli 的历史目录（按 deck 路径 hash 分子目录且持有写锁）。

### 共享写入的竞争修复（6d1a761、8bc8a00）

- `docx|pptx/scripts/office/soffice.py`：`lo_socket_shim` 的 .c/.so 在同目录用 `mkstemp` 唯一命名编译，再 `os.replace` 发布到固定名，只清理自己的临时文件。新增 `docx/tests/test_soffice_shim.py`（5 例，含真实 gcc 6 路并发）；对 origin/main 代码 5 例全红（旧代码 6 个并发构建者有 5 个因 `src.unlink` 竞争报 `FileNotFoundError`）。
- `web-designer/scripts/init.sh`：`mkdir "$BUILD_DIR"`（不带 `-p`）做原子认领，已存在即报错退出；实测 `pnpm create vite` 可写入已存在的空目录。5 进程抢同名：新代码 1 成功 4 拒绝，旧代码 4 个撞进同一目录。`bundle.sh` 与 SKILL.md 同步说明。
- `browser-skill/scripts/state.js`：`.state.json` 先写唯一临时文件再 `rename`；SKILL.md 注明该状态由并发 session 共享、最后写入者生效。压测 6 writer + 1 reader：旧代码读到 345 次半写文件，新代码 0 次。
- pptx 编辑流程（`references/editing.md` 及脚本 usage）：解包树、template、thumbnails 放进 `WORK=$(mktemp -d /tmp/pptx.XXXXXX)`，最终 deck 写到用户指定路径。
- `pptx/references/zooclaw-ppt-runtime.md` 的 intermediate commands：`inspect/`、starter deck/map、`shape-ops.json`、`qa/` 放进同一次运行的 `$OUT`，只有 `final.pptx` 写到用户指定路径（`cp` starter 后 apply，与 `run-template` 内部一致）。

## 仍未覆盖

- pptx 的 `deckspec.json`、`template-frame-map.json` 与 SKILL.md 里 `--inspect-dir inspect/`、`build-raw --out-dir output/` 仍按 cwd 约定。彻底修需要为每个 deck 任务定统一工作目录，并受 asset root 约束牵动 images.md、agent-contracts.md 的资产下载位置，超出本 PR 范围。

## 验证

- `python3 .github/scripts/lint_skills.py`：All skills passed（12 warnings，与 origin/main 逐字相同）。
- `xlsx/tests`：21 passed。
- 按改写后的文档实跑 xlsx CREATE / EDIT / format 流程通过；`WORK` 为空时 `xlsx_unpack.py` 报 `FileNotFoundError: ''` 退出，不会触及 `/`（参数不带结尾斜杠）。
- ruff：改动的 py 文件无新增问题。
- viral-ads 冒烟：`batch.py` 默认打印 mkdtemp 目录；`gen_video.py --mode resume` 缺 `--output-dir` 时 exit 1。
- docx CI 命令 `DOCX_REAL_OFFICE=1 python3 -m unittest discover -s docx/tests -p "test_*.py" -v`：18 tests OK。
- pptx `smoke_test.sh`：PASS 6 / FAIL 0 / SKIP 1（pptxgenjs 未安装）；`check_links.py`：60 个内部链接有效；改写后的 zooclaw-ppt-runtime intermediate 命令端到端跑通（apply 24/24，render-qa `qa_gate: pass`），用户目录只多出 `final.pptx`。
- pyright（docx/pptx soffice 等）0 errors；ruff 无新增。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `7a70736caad744da4ca57f2cd39f9ed8fbd01b6b`
- PR: #289
- 作者：Chris@ZooClaw
- 日期：2026-09-28T07:15:17Z

### Commit Message

```
fix(skills): use per-run mktemp scratch instead of fixed /tmp paths (#289)

## 摘要

v2 的 Sandbox 是 agent-scoped：`/tmp`、`/workspace`、`~` 由同一 Agent 的并发
session 共享，而模型会照抄 skill 里的示例路径。skill 里写死的 `/tmp/<固定名>`（如
`/tmp/xlsx_work/`、`/tmp/viral_batch/`、`/tmp/raw.jpg`）会让两个并发 session
互相覆盖。engine 侧不做 per-session 私有
/tmp（SerendipityOneInc/zooclaw-engine#1719 已否决），冲突改为在 skills
里靠约定解决（背景：SerendipityOneInc/zooclaw-engine#1203）。

- **规范**：`CLAUDE.md` §6 新增规则——每次运行的临时目录用 `mktemp -d` /
`tempfile.mkdtemp` 生成；示例里后续步骤引用同一变量，SKILL.md 要求复用打印出的字面路径（shell
变量不一定能带到下一次 exec）；脚本默认目录同样适用；只有按 hash/uuid 命名的文件和确需跨运行保留、原子写或加锁的
`/tmp/openclaw/<skill>/` 状态可以共享。`code-review.md` 加 "Unique scratch" 检查项。
- **文档**：xlsx（SKILL.md 与 references 全部场景）、pdf/pptx/web-designer
的图片处理、pptx 的 zooclaw-ppt-runtime 与
editing、viral-ads、meeting-notes（workspace 下的确认状态目录）改为每次运行唯一的目录。
- **脚本**：`viral-ads/scripts/batch.py`、`gen_video.py` 的 `--output-dir`
默认值从固定 `/tmp` 目录改为 mkdtemp 并打印路径；`gen_video.py --mode resume` 未给
`--output-dir` 时报错退出（原固定目录会让不同 session 复用彼此的 TTS）。xlsx 脚本只改 usage 注释。

已审计但保留：hash/uuid/mkdtemp
命名的路径（designer、video-generator、docx、zooclaw-asr/tts 等），council 的
deps/锁目录（已有 bounded flock + `os.replace`），pptx shape-cli 的历史目录（按 deck 路径
hash 分子目录且持有写锁）。

### 共享写入的竞争修复（6d1a761、8bc8a00）

- `docx|pptx/scripts/office/soffice.py`：`lo_socket_shim` 的 .c/.so 在同目录用
`mkstemp` 唯一命名编译，再 `os.replace` 发布到固定名，只清理自己的临时文件。新增
`docx/tests/test_soffice_shim.py`（5 例，含真实 gcc 6 路并发）；对 origin/main 代码 5
例全红（旧代码 6 个并发构建者有 5 个因 `src.unlink` 竞争报 `FileNotFoundError`）。
- `web-designer/scripts/init.sh`：`mkdir "$BUILD_DIR"`（不带
`-p`）做原子认领，已存在即报错退出；实测 `pnpm create vite` 可写入已存在的空目录。5 进程抢同名：新代码 1 成功 4
拒绝，旧代码 4 个撞进同一目录。`bundle.sh` 与 SKILL.md 同步说明。
- `browser-skill/scripts/state.js`：`.state.json` 先写唯一临时文件再
`rename`；SKILL.md 注明该状态由并发 session 共享、最后写入者生效。压测 6 writer + 1
reader：旧代码读到 345 次半写文件，新代码 0 次。
- pptx 编辑流程（`references/editing.md` 及脚本 usage）：解包树、template、thumbnails
放进 `WORK=$(mktemp -d /tmp/pptx.XXXXXX)`，最终 deck 写到用户指定路径。
- `pptx/references/zooclaw-ppt-runtime.md` 的 intermediate
commands：`inspect/`、starter deck/map、`shape-ops.json`、`qa/` 放进同一次运行的
`$OUT`，只有 `final.pptx` 写到用户指定路径（`cp` starter 后 apply，与 `run-template`
内部一致）。

## 仍未覆盖

- pptx 的 `deckspec.json`、`template-frame-map.json` 与 SKILL.md 里
`--inspect-dir inspect/`、`build-raw --out-dir output/` 仍按 cwd
约定。彻底修需要为每个 deck 任务定统一工作目录，并受 asset root 约束牵动
images.md、agent-contracts.md 的资产下载位置，超出本 PR 范围。

## 验证

- `python3 .github/scripts/lint_skills.py`：All skills passed（12
warnings，与 origin/main 逐字相同）。
- `xlsx/tests`：21 passed。
- 按改写后的文档实跑 xlsx CREATE / EDIT / format 流程通过；`WORK` 为空时 `xlsx_unpack.py`
报 `FileNotFoundError: ''` 退出，不会触及 `/`（参数不带结尾斜杠）。
- ruff：改动的 py 文件无新增问题。
- viral-ads 冒烟：`batch.py` 默认打印 mkdtemp 目录；`gen_video.py --mode resume` 缺
`--output-dir` 时 exit 1。
- docx CI 命令 `DOCX_REAL_OFFICE=1 python3 -m unittest discover -s
docx/tests -p "test_*.py" -v`：18 tests OK。
- pptx `smoke_test.sh`：PASS 6 / FAIL 0 / SKIP 1（pptxgenjs
未安装）；`check_links.py`：60 个内部链接有效；改写后的 zooclaw-ppt-runtime intermediate
命令端到端跑通（apply 24/24，render-qa `qa_gate: pass`），用户目录只多出 `final.pptx`。
- pyright（docx/pptx soffice 等）0 errors；ruff 无新增。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

来源：SerendipityOneInc/ecap-skills @ 7a70736c，PR #289，作者 Chris@ZooClaw。
