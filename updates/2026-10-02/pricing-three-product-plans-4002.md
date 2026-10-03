---
title: "定价页改版：Agent Builder、Managed Agent API、Enterprise 分开定价，API 侧公开模型与工具单价"
type: "新功能"
priority: "高"
date: "2026-10-02"
status: "待审核"
channels: ""
---

# 定价页改版：Agent Builder、Managed Agent API、Enterprise 分开定价，API 侧公开模型与工具单价

## 核心宣传点

官网 Pricing 从单纯的订阅对比页改成三个产品的统一价格入口：Agent Builder、Managed Agent API、Enterprise，三个下划线 Tab 可以用 ?product=builder|api|enterprise 直接分享，刷新、浏览器返回和键盘切换都保持当前选中项。Agent Builder 侧集中展示 Pro $30/月、原价 $100/月、70% OFF 和每月节省金额，保留月度 credits 与限时赠送说明。Managed Agent API 第一次把价目表完整公开：LLM 覆盖 9 家公司 37 个在售模型（33 个固定公开费率、4 个按实际用量结算），支持搜索、结果计数与费用条件展开；工具分 Images、Video & avatars、Audio、Search & web、Browser、Data & knowledge 六个 Tab；Compute 明确 Pro 4 vCPU / 4 GiB、$0.20 每运行小时。没有确定公开单价的能力（Browser Use、ZooData 等）按实际用量说明并跳转文档，不虚构单价或免费承诺。Enterprise 侧汇总定制 Agent、行业数据与知识、模型网关与 BYOK、后训练与评估、私有化治理、FDE 咨询，继续走现有 Contact Sales 路径。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

将官网 Pricing 从订阅对比页调整为三个产品的统一价格入口：**Agent Builder / Managed Agent API /
Enterprise**。用户已在本地预览并确认本轮设计。

## 改动入口与交互

### 1. `/pricing`：产品导航与统一 CTA

- 三个开放式下划线 Tab；支持 `?product=builder|api|enterprise` 分享、刷新、浏览器返回和键盘切换。
- 明确 Hover 与选中反馈；Builder Tab 的 `70% OFF` 标记呼应全站 Pricing 导航，统一使用蓝紫色品牌强调色。
- 三个产品使用同一套无边框右侧 CTA 组件，统一价格信息、按钮、间距及响应式布局。
- 更新页面 SEO 标题与描述，新增内容提供中英文，其他语言沿用现有英文回退。

### 2. Agent Builder

- Pro `$30/月`、原价 `$100/月`、`70% OFF`、每月节省金额集中呈现，保留月度 credits 与限时赠送说明。
- 订阅详情独立展示，原有登录、购买及管理订阅流程继续复用。
- 十种语言的 Builder 运行环境文案去掉 API 承诺；提供页内 Managed Agent API 切换入口。

### 3. Managed Agent API：模型、工具、Compute 三类费用

- 顶部 **Add Funds** 安全新标签页打开 Platform Billing；文档及 Usage 链接也新开。
- **LLM**：九家公司、37 个当前支持的语言模型（33 个固定公开费率、4
个按实际用量结算）；公司内按输出价格降序、同价按模型版本降序，支持搜索、结果计数、清空与费用条件展开。
- 补齐 Claude、DeepSeek、Kimi 等；Dola Seed 与 Seed 聚合到 BytePlus。Claude
缓存写入明确为每百万 token 的费用，5 分钟/1 小时表示缓存保留期。长上下文、峰谷时段等条件单独披露。
- **工具**：Images、Video & avatars、Audio、Search & web、Browser、Data &
knowledge 六个 Tab，增加明确选中态及逐行 Hover。
- 图片覆盖 10 个当前授权型号，区分 image-output token、成功请求与实际用量单位；Seedance/HeyGen
示例明确标为估算并列出规格与官方参考链接。
- 补充 ZooWork ASR/TTS、音文对齐、说话人识别、微信公众号搜索/历史、商品与创作者搜索、网页抽取、小红书链接/ID
内容读取、社媒/电商数据、知识与文件能力。
- Browser Use、ZooData 等无确定独立公开单价的项目按实际用量说明；仅能力介绍的项目跳转文档，不虚构单价或免费承诺。
- 工具扩展目录去重，仅保留命令/文件操作、字幕去除、穿搭/情绪板及自定义工具四类上表未展示能力。
- **Compute**：展示 Pro 4 vCPU / 4 GiB、`$0.20/运行小时`，解释实际沙箱运行区间；规格对应已合并的
#3999。

### 4. Enterprise

- 汇总定制 Agent、行业数据/知识、模型网关与 BYOK、后训练/评估、私有化治理、FDE/转型咨询。
- Contact Sales / Enterprise 入口继续使用现有站内销售路径。

### 5. 代码与素材

- 页面拆分为 render-only 产品组件、统一展示原语、URL flow hook 与纯价格目录，复用营销导航、设计系统和语义色值。
- Logo 本地托管，保留来源及 MIT 许可；Kimi 使用黑色主体和蓝色右上角点，Z.ai 使用黑色标志。
- 研究文件、原始生产响应、供应商内部路由、采购折扣、凭证与本地截图均未纳入提交。

## Test plan

- [x] 本地用户逐轮验收三个产品布局、促销强度、Logo、价格分组与工具去重。
- [x] 最终定向 Vitest：4 个文件、48 个测试通过（目录/排序/计费单位、Builder、URL 导航、marketing
chrome）。
- [x] TypeScript、仓库前端治理检查、ESLint、`git diff --check`。
- [x] 浏览器验证：英文桌面、中文桌面与手机；产品深链/刷新/返回、键盘切换、搜索/空结果、费用展开、六类工具选中/hover、CTA
对齐，无整页横向溢出。
- [x] 2026-10-02 核对当前产品目录、媒体型号与公开费率；无付费模型/工具执行或客户账单操作。
- [ ] GitHub CI 与 `tim-srp` review。

## 首轮评审与 CI 处理

- 修复自动审查发现的 `Z.ai` 搜索缺口：公司展示名与搜索共用映射，新增别名回归测试；目录测试 13/13 通过，浏览器验证返回 4 个
Zhipu 模型。
- 清理旧价格表重构后残留的三个无用常量导出；价格数值与计算保持不变，针对 CI 的 Knip 硬门禁复验。
- Claude 关于展开状态使用模型名称的建议暂不调整：当前目录名称唯一，ID 也由名称派生，没有可复现的错误或额外身份稳定性收益。
- 首轮生产构建、全量前端测试及 CodeQL 通过；修复后的最新提交等待 CI 重新验证。

## 影响与上线注意

- 仅官网前端展示与文案，无后端、支付金额或计费逻辑修改。
- 价格目录为注明核对日期的静态快照，后续模型或费率变更需同步更新；估算媒体费用不作为最终账单承诺。
- 正式发布前确认 #3999 的 Pro 默认规格已部署。本 PR 的 merge 不等同于生产发布。

设计与实现记录见
`docs/superpowers/specs/2026-10-02-pricing-products.md`、`docs/superpowers/plans/2026-10-02-pricing-products.md`。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `3654d4472715b390eedbf9b7bfe30a0ac2cf032f`
- PR: #4002
- 作者：david-srp
- 日期：2026-10-02T14:19:38Z

### Commit Message

```
feat(pricing): 区分 Builder、Managed Agent API 与 Enterprise 价格方案 (#4002)

## Summary

将官网 Pricing 从订阅对比页调整为三个产品的统一价格入口：**Agent Builder / Managed Agent API /
Enterprise**。用户已在本地预览并确认本轮设计。

## 改动入口与交互

### 1. `/pricing`：产品导航与统一 CTA

- 三个开放式下划线 Tab；支持 `?product=builder|api|enterprise` 分享、刷新、浏览器返回和键盘切换。
- 明确 Hover 与选中反馈；Builder Tab 的 `70% OFF` 标记呼应全站 Pricing 导航，统一使用蓝紫色品牌强调色。
- 三个产品使用同一套无边框右侧 CTA 组件，统一价格信息、按钮、间距及响应式布局。
- 更新页面 SEO 标题与描述，新增内容提供中英文，其他语言沿用现有英文回退。

### 2. Agent Builder

- Pro `$30/月`、原价 `$100/月`、`70% OFF`、每月节省金额集中呈现，保留月度 credits 与限时赠送说明。
- 订阅详情独立展示，原有登录、购买及管理订阅流程继续复用。
- 十种语言的 Builder 运行环境文案去掉 API 承诺；提供页内 Managed Agent API 切换入口。

### 3. Managed Agent API：模型、工具、Compute 三类费用

- 顶部 **Add Funds** 安全新标签页打开 Platform Billing；文档及 Usage 链接也新开。
- **LLM**：九家公司、37 个当前支持的语言模型（33 个固定公开费率、4
个按实际用量结算）；公司内按输出价格降序、同价按模型版本降序，支持搜索、结果计数、清空与费用条件展开。
- 补齐 Claude、DeepSeek、Kimi 等；Dola Seed 与 Seed 聚合到 BytePlus。Claude
缓存写入明确为每百万 token 的费用，5 分钟/1 小时表示缓存保留期。长上下文、峰谷时段等条件单独披露。
- **工具**：Images、Video & avatars、Audio、Search & web、Browser、Data &
knowledge 六个 Tab，增加明确选中态及逐行 Hover。
- 图片覆盖 10 个当前授权型号，区分 image-output token、成功请求与实际用量单位；Seedance/HeyGen
示例明确标为估算并列出规格与官方参考链接。
- 补充 ZooWork ASR/TTS、音文对齐、说话人识别、微信公众号搜索/历史、商品与创作者搜索、网页抽取、小红书链接/ID
内容读取、社媒/电商数据、知识与文件能力。
- Browser Use、ZooData 等无确定独立公开单价的项目按实际用量说明；仅能力介绍的项目跳转文档，不虚构单价或免费承诺。
- 工具扩展目录去重，仅保留命令/文件操作、字幕去除、穿搭/情绪板及自定义工具四类上表未展示能力。
- **Compute**：展示 Pro 4 vCPU / 4 GiB、`$0.20/运行小时`，解释实际沙箱运行区间；规格对应已合并的
#3999。

### 4. Enterprise

- 汇总定制 Agent、行业数据/知识、模型网关与 BYOK、后训练/评估、私有化治理、FDE/转型咨询。
- Contact Sales / Enterprise 入口继续使用现有站内销售路径。

### 5. 代码与素材

- 页面拆分为 render-only 产品组件、统一展示原语、URL flow hook 与纯价格目录，复用营销导航、设计系统和语义色值。
- Logo 本地托管，保留来源及 MIT 许可；Kimi 使用黑色主体和蓝色右上角点，Z.ai 使用黑色标志。
- 研究文件、原始生产响应、供应商内部路由、采购折扣、凭证与本地截图均未纳入提交。

## Test plan

- [x] 本地用户逐轮验收三个产品布局、促销强度、Logo、价格分组与工具去重。
- [x] 最终定向 Vitest：4 个文件、48 个测试通过（目录/排序/计费单位、Builder、URL 导航、marketing
chrome）。
- [x] TypeScript、仓库前端治理检查、ESLint、`git diff --check`。
- [x] 浏览器验证：英文桌面、中文桌面与手机；产品深链/刷新/返回、键盘切换、搜索/空结果、费用展开、六类工具选中/hover、CTA
对齐，无整页横向溢出。
- [x] 2026-10-02 核对当前产品目录、媒体型号与公开费率；无付费模型/工具执行或客户账单操作。
- [ ] GitHub CI 与 `tim-srp` review。

## 首轮评审与 CI 处理

- 修复自动审查发现的 `Z.ai` 搜索缺口：公司展示名与搜索共用映射，新增别名回归测试；目录测试 13/13 通过，浏览器验证返回 4 个
Zhipu 模型。
- 清理旧价格表重构后残留的三个无用常量导出；价格数值与计算保持不变，针对 CI 的 Knip 硬门禁复验。
- Claude 关于展开状态使用模型名称的建议暂不调整：当前目录名称唯一，ID 也由名称派生，没有可复现的错误或额外身份稳定性收益。
- 首轮生产构建、全量前端测试及 CodeQL 通过；修复后的最新提交等待 CI 重新验证。

## 影响与上线注意

- 仅官网前端展示与文案，无后端、支付金额或计费逻辑修改。
- 价格目录为注明核对日期的静态快照，后续模型或费率变更需同步更新；估算媒体费用不作为最终账单承诺。
- 正式发布前确认 #3999 的 Pro 默认规格已部署。本 PR 的 merge 不等同于生产发布。

设计与实现记录见
`docs/superpowers/specs/2026-10-02-pricing-products.md`、`docs/superpowers/plans/2026-10-02-pricing-products.md`。
```

来源：SerendipityOneInc/ecap-workspace @ 3654d447，PR #4002，作者 david-srp。
