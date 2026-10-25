---
title: "修复：PDF 技能复用环境预装浏览器，不再报依赖缺失或偷装东西"
type: "Skill 上架/更新"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 修复：PDF 技能复用环境预装浏览器，不再报依赖缺失或偷装东西

## 核心宣传点

托管 Agent 默认环境其实已预装精简版 Playwright 和配套 Chromium，但 PDF 加载器只认完整版包，导致标准生成流程直接报依赖缺失；之前的修法还会尝试往技能目录里安装、使用浏览器安装器不支持的静默参数并吞掉错误，业务 Agent 只好改用临时渲染脚本绕过。本次让依赖检查与实际渲染共用同一个加载器，挑选真正能启动的匹配浏览器并在失败时保留原因，文档任务不再自动安装 Playwright、浏览器或字体，也不会调用 sudo。检查命令会显式打印选中的模块与浏览器路径便于核对，仅为诊断输出、不含凭证、不写入 PDF。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `853410be46fa9ec4722bc72c22be519837e03397`
- PR: #299
- 作者：sharplee-srp
- 日期：2026-10-23T04:08:16Z

### Commit Message

```
fix(pdf): reuse matching preinstalled browser and remove runtime installs (#299)

默认 Managed Agents 环境已经预装 `playwright-core` 和配套 Chromium，但 PDF 加载器只识别完整
`playwright`，导致标准 CREATE 流程报依赖缺失。原 `fix` 会尝试向 skill 目录安装，并使用 Chromium
安装器不支持的 `--silent`、隐藏错误，业务 Agent 随后改用临时渲染脚本。

本 PR 让检查与渲染使用同一个加载器，选用可启动的匹配浏览器，失败时保留原因；文档任务不再自动安装 Playwright/浏览器/字体或调用
sudo。Python 原有 `uv run --with` 行为保留。

`make.sh check` 会显示选中的模块和浏览器路径，用于核对实际依赖配对。这是显式诊断输出，不包含凭证、不写入
PDF；该命令输出由诊断 JSON 和可读检查结果组成，并以退出码表示成功与否。

## 行为对比

| 场景 | 修复前 | 修复后 |
|---|---|---|
| 环境仅预装可用的 playwright-core | renderer exit 2：`playwright not found` | 通过
NODE_PATH 找到 core，启动其匹配 Chromium，renderer exit 0 |
| 本地残留安装缺少浏览器 | 本地依赖遮蔽共享安装，进入安装恢复 | 继续尝试其他候选；兼容完整 playwright 和全局安装 |
| 依赖检查 | 模块可导入或 CLI 有版本就可能通过，与实际渲染不一致 | 与渲染共用加载器，实际启动并关闭浏览器 |
| 依赖或权限不足 | 隐式 npm/npx 安装；错误被隐藏；字体脚本可能 sudo | `fix` 仅诊断；错误带原因；字体显式准备且不提权
|
| skill 目录 | 安装和 Python 字节码可能写入 | 不在 skill 目录安装或写字节码；真实测试前后文件 hash 一致 |
| 同会话修改 PDF | 观测到继续编辑备用脚本 | 更新保存的内容，复用标准 `make.sh run` |

另修复本地 HTML 文件路径含空格或 `#` 时的 file URL 转义；新增 PDF 回归并注册到现有 Skill Tests 工作流。

## Managed Agents 前后实测

2026-10-21，使用相同 `gpt-5.6-terra`、Environment v21 / 相同 E2B
build、原样冻结的中文周报提示词：先新建 3–4 页周报，再在原会话更新看板进度、累计支出和预算决策。提示词没有指定脚本、路径或诊断捷径。

| 指标 | 修复前：新建 | 修复后：新建 | 修复前：改稿 | 修复后：改稿 |
|---|---:|---:|---:|---:|
| 提交至收到终态 | 131.201 秒 | 51.797 秒 | 119.142 秒 | 45.742 秒 |
| 工具区间并集 | 53.439 秒 | 11.190 秒 | 64.058 秒 | 8.480 秒 |
| 工具调用数 | 10 | 6 | 6 | 5 |
| 命令失败数 | 2 | 0 | 0 | 0 |
| 渲染路径 | 备用脚本 | 标准 make.sh run | 备用脚本 | 标准 make.sh run |
| 视觉工具 | 调用 1 次 | 未调用 | 调用 1 次，失败 | 未调用 |

**这是单次观测，不是受控性能 A/B，不能把耗时差全部归因于修复。**
旧流程包含依赖恢复、备用脚本和视觉调用；新流程没有调用视觉模型，因此没有验证视觉模型成功/429
延迟。总耗时使用客户端同一时钟，工具区间使用服务端同源事件；工具外时间包含模型、调度和传输。

修复后的实际 `make.sh run` 进程耗时为新建 **5.584 秒**、改稿 **3.411 秒**，均 exit
0。另在同一诊断沙箱对照旧/新 renderer：旧版明确报错，新版真实浏览器生成成功；首次独立封面探针 9.564 秒，随后简短中文
CREATE 2.689 秒，预热及内容不同，不作为平均性能。

## 验证与验收

- PDF 回归 **10/10**；同组用例在旧脚本上暴露故障。覆盖 core、完整
playwright、残留安装、启动失败回退、缺失/不可启动浏览器、无隐式安装、检查/渲染一致性及目录不变性。单测替代外部浏览器，实际
Chromium 在独立环境验证。
- CI 选择器 **3/3**，严格类型检查、Shell/JS 语法、`git diff --check`、完整 skill lint
通过；lint 的 10 条警告来自其他 skill。
- **环境有效（隔离测试）**：实际 core 1.63.0 / Chromium 1243 启动成功；网络探针可访问 npm
registry；浏览器缓存和系统字体对 uid 1000 不可写，字体权限失败清晰且无 sudo。
- **流程通过**：新建、同会话改稿均走标准入口，终态 succeeded，无备用 renderer 或人工修补产物；业务过程中全部 23
个运行文件 hash、Agent 配置和环境不变。
- **确定性检查通过**：两份成品均 4 页，下载 HTTP 200，大小及 SHA-256 与产物记录一致；改稿的 55%、+5
个百分点、19.8 万支出、66% 执行率、3.6 万增量、10.2 万余额和原预算内批准 2 万元均同步更新。
- **业务/视觉部分通过**：主控逐页检查全部 8 页业务产物及 2 页
smoke，中文正常，无明显裁切、重叠或空白页；模型仍补写未提供的部门/负责人，另有封面拆词、低对比度字幕和表格换行问题。这些内容及视觉问题另行处理，不能宣称完整业务验收通过。

可重复执行的本地回归：

```sh
node --test pdf/tests/*.test.cjs .github/scripts/skill-tests.test.mjs
bash -n pdf/scripts/make.sh pdf/scripts/setup-noto.sh
node --check pdf/scripts/browser_runtime.js
node --check pdf/scripts/render_cover.js
uv run --with pyyaml python .github/scripts/lint_skills.py
```

## 范围与限制

仅修改 PDF 模块及其现有 CI 接入。业务测试使用任务独占 Agent 中冻结的私有文件覆盖，全局 PDF v2 注册表未变；准备会话已预先
materialize skill，因此不是冷启动或网页/渠道 E2E。测试结束后仅澄清 SKILL.md 对 Python uv
的说明，并补全图片指南的 `{baseDir}` 路径；可执行代码与实测版本一致。

未断网验证真实沙箱中的 Python 冷缓存或字体下载；其他 skill 全量测试交由本 PR
CI。Word、Engine、内容一致性、视觉模型/429 不在此次修复范围。测试 Agent 已停止；本 PR 不发布
skill、不部署，也未修改生产配置。
```

