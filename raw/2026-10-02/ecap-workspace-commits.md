# SerendipityOneInc/ecap-workspace — commits 2026-10-02

## style(marketing): 优化官网导航反馈与页眉按钮留白 (#4003)

- **SHA**: `b9197fa39664180f45a7c7b992e5ccff4546648c`
- **作者**: david-srp
- **日期**: 2026-10-02T14:38:23Z
- **PR**: #4003

### Commit Message

```
style(marketing): 优化官网导航反馈与页眉按钮留白 (#4003)

## Summary

官网顶层导航原先通过降低文字不透明度反馈 hover，辨识度偏弱。现在使用细下划线提示当前项目，并为页眉主按钮增加留白。

- 桌面导航
`Products`、`Solutions`、`Pricing`、`Enterprise`、`Developer`、`Resources`：hover
显示 2px 下划线，键盘焦点和菜单展开态使用同一反馈；支持减少动态效果设置。
- 桌面下拉菜单：补齐列表项的焦点背景和 Solutions 分组标题的 hover / 焦点背景；共享导航文字保持完整对比度。
- 移动导航：补齐分组标题与 Pricing、Enterprise 等顶层链接的 hover / 焦点背景；禁用项不显示高亮。
- 桌面页眉 `Get Started`：左右内边距由 8px 增至 16px。

以上变更通过 `LandingHeader`、`LandingMobileNav` 和 `LandingNavItem`
覆盖使用共享页眉的官网营销页面。

## Test plan

- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint 和仓库治理检查通过。
- [x] 提交钩子全量 ESLint 通过。
- [x] 本地浏览器检查导航反馈、菜单展开状态和键盘焦点；最终版本在 1117px 视口验证按钮左右留白为 16px，页眉布局无横向溢出。
- [x] 首轮在 1200px、1440px 视口检查导航项无重叠。
- [x] 根据 Tim review，在 1000px 本地页面验证移动菜单 Pricing 链接的键盘焦点背景已生效，并重新运行
`verify-web.sh` 与推送前检查。

本次为样式调整，未新增单元测试；验证脚本的 Vitest 定向筛选未匹配到对应测试文件。
```

### PR Body

## Summary

官网顶层导航原先通过降低文字不透明度反馈 hover，辨识度偏弱。现在使用细下划线提示当前项目，并为页眉主按钮增加留白。

- 桌面导航 `Products`、`Solutions`、`Pricing`、`Enterprise`、`Developer`、`Resources`：hover 显示 2px 下划线，键盘焦点和菜单展开态使用同一反馈；支持减少动态效果设置。
- 桌面下拉菜单：补齐列表项的焦点背景和 Solutions 分组标题的 hover / 焦点背景；共享导航文字保持完整对比度。
- 移动导航：补齐分组标题与 Pricing、Enterprise 等顶层链接的 hover / 焦点背景；禁用项不显示高亮。
- 桌面页眉 `Get Started`：左右内边距由 8px 增至 16px。

以上变更通过 `LandingHeader`、`LandingMobileNav` 和 `LandingNavItem` 覆盖使用共享页眉的官网营销页面。

## Test plan

- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint 和仓库治理检查通过。
- [x] 提交钩子全量 ESLint 通过。
- [x] 本地浏览器检查导航反馈、菜单展开状态和键盘焦点；最终版本在 1117px 视口验证按钮左右留白为 16px，页眉布局无横向溢出。
- [x] 首轮在 1200px、1440px 视口检查导航项无重叠。
- [x] 根据 Tim review，在 1000px 本地页面验证移动菜单 Pricing 链接的键盘焦点背景已生效，并重新运行 `verify-web.sh` 与推送前检查。

本次为样式调整，未新增单元测试；验证脚本的 Vitest 定向筛选未匹配到对应测试文件。

---

## fix(platform): remove terms entry from profile settings (#4004)

- **SHA**: `98c4bd443f7edfc5a0c5a7b1636a4a7383082a6b`
- **作者**: ericma-srp
- **日期**: 2026-10-02T14:28:13Z
- **PR**: #4004

### Commit Message

```
fix(platform): remove terms entry from profile settings (#4004)

## Summary
Remove the Terms footer and its divider from Platform's
`/settings/profile` page, as requested by the product owner. The login
and credit-purchase Terms links and the supplied agreement remain
unchanged.

## Root cause
The earlier terms rollout added a Profile entry. The owner's October 2
follow-up removes that entry; the product rule and existing Profile
assertion now reflect this decision.

## Test plan
- [x] Platform lint and production build, including TypeScript checks.
- [x] All 53 router tests passed, including the updated Profile
assertion and existing public Terms / purchase-entry coverage.
- [x] Local browser preview: Profile renders account and appearance
settings with zero Terms links. Uses sample data; no live account or
payment changes.
```

### PR Body

## Summary
Remove the Terms footer and its divider from Platform's `/settings/profile` page, as requested by the product owner. The login and credit-purchase Terms links and the supplied agreement remain unchanged.

## Root cause
The earlier terms rollout added a Profile entry. The owner's October 2 follow-up removes that entry; the product rule and existing Profile assertion now reflect this decision.

## Test plan
- [x] Platform lint and production build, including TypeScript checks.
- [x] All 53 router tests passed, including the updated Profile assertion and existing public Terms / purchase-entry coverage.
- [x] Local browser preview: Profile renders account and appearance settings with zero Terms links. Uses sample data; no live account or payment changes.

---

## feat(pricing): 区分 Builder、Managed Agent API 与 Enterprise 价格方案 (#4002)

- **SHA**: `3654d4472715b390eedbf9b7bfe30a0ac2cf032f`
- **作者**: david-srp
- **日期**: 2026-10-02T14:19:38Z
- **PR**: #4002

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

### PR Body

## Summary

将官网 Pricing 从订阅对比页调整为三个产品的统一价格入口：**Agent Builder / Managed Agent API / Enterprise**。用户已在本地预览并确认本轮设计。

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
- **LLM**：九家公司、37 个当前支持的语言模型（33 个固定公开费率、4 个按实际用量结算）；公司内按输出价格降序、同价按模型版本降序，支持搜索、结果计数、清空与费用条件展开。
- 补齐 Claude、DeepSeek、Kimi 等；Dola Seed 与 Seed 聚合到 BytePlus。Claude 缓存写入明确为每百万 token 的费用，5 分钟/1 小时表示缓存保留期。长上下文、峰谷时段等条件单独披露。
- **工具**：Images、Video & avatars、Audio、Search & web、Browser、Data & knowledge 六个 Tab，增加明确选中态及逐行 Hover。
- 图片覆盖 10 个当前授权型号，区分 image-output token、成功请求与实际用量单位；Seedance/HeyGen 示例明确标为估算并列出规格与官方参考链接。
- 补充 ZooWork ASR/TTS、音文对齐、说话人识别、微信公众号搜索/历史、商品与创作者搜索、网页抽取、小红书链接/ID 内容读取、社媒/电商数据、知识与文件能力。
- Browser Use、ZooData 等无确定独立公开单价的项目按实际用量说明；仅能力介绍的项目跳转文档，不虚构单价或免费承诺。
- 工具扩展目录去重，仅保留命令/文件操作、字幕去除、穿搭/情绪板及自定义工具四类上表未展示能力。
- **Compute**：展示 Pro 4 vCPU / 4 GiB、`$0.20/运行小时`，解释实际沙箱运行区间；规格对应已合并的 #3999。

### 4. Enterprise

- 汇总定制 Agent、行业数据/知识、模型网关与 BYOK、后训练/评估、私有化治理、FDE/转型咨询。
- Contact Sales / Enterprise 入口继续使用现有站内销售路径。

### 5. 代码与素材

- 页面拆分为 render-only 产品组件、统一展示原语、URL flow hook 与纯价格目录，复用营销导航、设计系统和语义色值。
- Logo 本地托管，保留来源及 MIT 许可；Kimi 使用黑色主体和蓝色右上角点，Z.ai 使用黑色标志。
- 研究文件、原始生产响应、供应商内部路由、采购折扣、凭证与本地截图均未纳入提交。

## Test plan

- [x] 本地用户逐轮验收三个产品布局、促销强度、Logo、价格分组与工具去重。
- [x] 最终定向 Vitest：4 个文件、48 个测试通过（目录/排序/计费单位、Builder、URL 导航、marketing chrome）。
- [x] TypeScript、仓库前端治理检查、ESLint、`git diff --check`。
- [x] 浏览器验证：英文桌面、中文桌面与手机；产品深链/刷新/返回、键盘切换、搜索/空结果、费用展开、六类工具选中/hover、CTA 对齐，无整页横向溢出。
- [x] 2026-10-02 核对当前产品目录、媒体型号与公开费率；无付费模型/工具执行或客户账单操作。
- [ ] GitHub CI 与 `tim-srp` review。

## 首轮评审与 CI 处理

- 修复自动审查发现的 `Z.ai` 搜索缺口：公司展示名与搜索共用映射，新增别名回归测试；目录测试 13/13 通过，浏览器验证返回 4 个 Zhipu 模型。
- 清理旧价格表重构后残留的三个无用常量导出；价格数值与计算保持不变，针对 CI 的 Knip 硬门禁复验。
- Claude 关于展开状态使用模型名称的建议暂不调整：当前目录名称唯一，ID 也由名称派生，没有可复现的错误或额外身份稳定性收益。
- 首轮生产构建、全量前端测试及 CodeQL 通过；修复后的最新提交等待 CI 重新验证。

## 影响与上线注意

- 仅官网前端展示与文案，无后端、支付金额或计费逻辑修改。
- 价格目录为注明核对日期的静态快照，后续模型或费率变更需同步更新；估算媒体费用不作为最终账单承诺。
- 正式发布前确认 #3999 的 Pro 默认规格已部署。本 PR 的 merge 不等同于生产发布。

设计与实现记录见 `docs/superpowers/specs/2026-10-02-pricing-products.md`、`docs/superpowers/plans/2026-10-02-pricing-products.md`。

---

## fix(billing): 由 Stripe 统一判断优惠码使用资格 (#4001)

- **SHA**: `b226e79e077ee05eb547e43f11a53b62488022c7`
- **作者**: ericma-srp
- **日期**: 2026-10-02T08:50:31Z
- **PR**: #4001

### Commit Message

```
fix(billing): 由 Stripe 统一判断优惠码使用资格 (#4001)

## Summary

ZooWork 和 Platform
的充值结账始终提供优惠码输入入口，不再由本地判断用户是否首次充值、是否充值过或是否使用过优惠券。优惠码的首单限制、适用产品、核销次数和有效期全部由
Stripe 决定。ZooWork 订阅结账也保持这一规则。

- Platform 删除历史充值查询、首次优惠资格占用/消耗/释放，以及为了复用资格而关闭旧 Checkout 的逻辑。新 Checkout
复用稳定的 Stripe Customer，并始终启用优惠码输入。
- Stripe 已确认的优惠支付不再依赖本地首次订单标记才能到账。保留订单/Customer
归属、产品和金额验证、退款处理、审计及防重复到账机制。
- ZooWork 订阅与 Top up 原本已无条件开放输入入口，本次增加新老客户与两种 Checkout 模式的回归覆盖。

## Root cause

PR #3967 的 Platform 实现把优惠码入口绑定到本地“首次充值资格”：历史
Checkout（包括未付款的尝试）、已记录的首次订单和待完成的优惠资格占用，都会关闭入口或阻止再次充值。这与产品要求不符。

本次明确取消这一层业务判断；数据库中的旧资格字段仅保留用于兼容读取和审计，不参与优惠资格判断。删除不再使用的历史查询，并同步维护隔离的
staging CSFLE 检查脚本。

## Compatibility and release

- 已经发给 Stripe 的请求参数、幂等键和已生成的付款链接保持不变，避免重试时参数冲突。**上线后从 Add funds
发起一笔新的充值来验收；旧链接不会自动增加输入入口。**
- 充值金额范围、订单面额、抵扣金额与到账额度算法、Stripe 后台的券配置均不变；不新增生产数据库查询形式或数据迁移。
- 仅后端需要部署；此 PR 不执行部署或真实支付。
- 按产品负责人 Eric 已确认的验收分工，staging/线上真实优惠券资格和到账验收、加密数据库 fixture 读取/CAS 验收由
Eric 执行。代码评审工具负责代码正确性，不以代替上述环境验收为要求。此次本地测试不宣称完成真实 Stripe 或 staging CSFLE
验收。
- 需求及验收细则：`docs/superpowers/specs/2026-10-02-stripe-promotion-entry.md`。

## Test plan

- [x] 247 项定向回归：Platform 充值/Customer/重试/结算、CSFLE probe 安全逻辑、ZooWork
Checkout 与 Stripe SDK 重试（最终同一次运行：247 passed）。
- [x] `bash scripts/verify-py.sh`：ruff、格式、pyright（app/tests）、8 项 import
contracts 全通过。
- [x] 函数复杂度及其余 pre-commit 检查通过；dead-code 检查未发现本次改动遗留的死函数。原有 pyright hook
未给含空格的路径加引号，已用上述完整 app/tests 检查替代该 hook。
- [x] PR CI 全部通过（后端测试/静态检查/重复代码/CodeQL）；Codex、Claude 自动评审均
APPROVE，无需要修复的问题。Claude 对既有身份冲突重试和注释的非缺陷观察已复核：保留身份恢复机制，不恢复任何优惠资格判断。
- [ ] Eric 在部署后分别用新账号、有充值/用券历史的账号发起全新 Checkout，确认入口始终显示；核对 Stripe
接受可用券、拒绝受限券，以及全额/部分抵扣到账。
```

### PR Body

## Summary

ZooWork 和 Platform 的充值结账始终提供优惠码输入入口，不再由本地判断用户是否首次充值、是否充值过或是否使用过优惠券。优惠码的首单限制、适用产品、核销次数和有效期全部由 Stripe 决定。ZooWork 订阅结账也保持这一规则。

- Platform 删除历史充值查询、首次优惠资格占用/消耗/释放，以及为了复用资格而关闭旧 Checkout 的逻辑。新 Checkout 复用稳定的 Stripe Customer，并始终启用优惠码输入。
- Stripe 已确认的优惠支付不再依赖本地首次订单标记才能到账。保留订单/Customer 归属、产品和金额验证、退款处理、审计及防重复到账机制。
- ZooWork 订阅与 Top up 原本已无条件开放输入入口，本次增加新老客户与两种 Checkout 模式的回归覆盖。

## Root cause

PR #3967 的 Platform 实现把优惠码入口绑定到本地“首次充值资格”：历史 Checkout（包括未付款的尝试）、已记录的首次订单和待完成的优惠资格占用，都会关闭入口或阻止再次充值。这与产品要求不符。

本次明确取消这一层业务判断；数据库中的旧资格字段仅保留用于兼容读取和审计，不参与优惠资格判断。删除不再使用的历史查询，并同步维护隔离的 staging CSFLE 检查脚本。

## Compatibility and release

- 已经发给 Stripe 的请求参数、幂等键和已生成的付款链接保持不变，避免重试时参数冲突。**上线后从 Add funds 发起一笔新的充值来验收；旧链接不会自动增加输入入口。**
- 充值金额范围、订单面额、抵扣金额与到账额度算法、Stripe 后台的券配置均不变；不新增生产数据库查询形式或数据迁移。
- 仅后端需要部署；此 PR 不执行部署或真实支付。
- 按产品负责人 Eric 已确认的验收分工，staging/线上真实优惠券资格和到账验收、加密数据库 fixture 读取/CAS 验收由 Eric 执行。代码评审工具负责代码正确性，不以代替上述环境验收为要求。此次本地测试不宣称完成真实 Stripe 或 staging CSFLE 验收。
- 需求及验收细则：`docs/superpowers/specs/2026-10-02-stripe-promotion-entry.md`。

## Test plan

- [x] 247 项定向回归：Platform 充值/Customer/重试/结算、CSFLE probe 安全逻辑、ZooWork Checkout 与 Stripe SDK 重试（最终同一次运行：247 passed）。
- [x] `bash scripts/verify-py.sh`：ruff、格式、pyright（app/tests）、8 项 import contracts 全通过。
- [x] 函数复杂度及其余 pre-commit 检查通过；dead-code 检查未发现本次改动遗留的死函数。原有 pyright hook 未给含空格的路径加引号，已用上述完整 app/tests 检查替代该 hook。
- [x] PR CI 全部通过（后端测试/静态检查/重复代码/CodeQL）；Codex、Claude 自动评审均 APPROVE，无需要修复的问题。Claude 对既有身份冲突重试和注释的非缺陷观察已复核：保留身份恢复机制，不恢复任何优惠资格判断。
- [ ] Eric 在部署后分别用新账号、有充值/用券历史的账号发起全新 Checkout，确认入口始终显示；核对 Stripe 接受可用券、拒绝受限券，以及全额/部分抵扣到账。

---

## fix(platform): 恢复 Project Key 创建 Agent 的 Pro 默认规格 (#3999)

- **SHA**: `d6a300f73642a7b9496812cdba0406e05d2b0ca7`
- **作者**: finn-srp
- **日期**: 2026-10-02T07:02:19Z
- **PR**: #3999

### Commit Message

```
fix(platform): 恢复 Project Key 创建 Agent 的 Pro 默认规格 (#3999)

## Summary

Platform Project Key 创建 Agent 时，默认规格从误用的 Starter 恢复为 Pro（4 vCPU、4
GiB），与原 API Platform 产品规则一致。新旧 API Platform 路径共用默认规格常量，调用方传入的规格仍由服务端覆盖。

Fixes #3998

## Root cause

接入 `zwp_live_` Project Key 时新增分支固定使用 `starter`，没有沿用旧 API Platform 的 Pro
默认规则。内部 `starter_20_month` 计量套餐与 sandbox 计算规格是独立配置；API Platform 没有 Work
业务订阅，也应按既定规则默认 Pro。

同步补充 runtime 契约。本次只影响后续创建的 Agent，不开放用户自选规格，不修改存量 Agent。

## Test plan

- [x] 回归测试先复现原代码转发 `starter`、预期 `pro` 的失败，再验证修复通过。
- [x] 93 项定向测试通过：Default/具名 Project；省略规格或提交 `starter` /
`ultra`；凭据初始化、ownership 和 usage attribution；旧 API Platform 不查询 Work
订阅；Work 规格策略及内部规格接口隔离。
- [x] 提交前 Python lint、类型和 import 检查通过。
- [x] 同步最新 main 后，在最终 commit `7ab5bac5203201cae10d8710c819928bf01a7445`
运行 `ecap-verify-py-ci`：**13,661 passed、5 skipped、4 warnings；coverage
89.96%**（4 workers、sysmon、89.5% threshold）。Linux 依赖解析、静态/all CI lint 和两个
jscpd 检查全部通过。

Engine/Gateway 使用 mock，MongoDB
测试使用本地实例。本次没有更改数据库查询形式，未执行线上数据修改、部署或真实付费调用。
```

### PR Body

## Summary

Platform Project Key 创建 Agent 时，默认规格从误用的 Starter 恢复为 Pro（4 vCPU、4 GiB），与原 API Platform 产品规则一致。新旧 API Platform 路径共用默认规格常量，调用方传入的规格仍由服务端覆盖。

Fixes #3998

## Root cause

接入 `zwp_live_` Project Key 时新增分支固定使用 `starter`，没有沿用旧 API Platform 的 Pro 默认规则。内部 `starter_20_month` 计量套餐与 sandbox 计算规格是独立配置；API Platform 没有 Work 业务订阅，也应按既定规则默认 Pro。

同步补充 runtime 契约。本次只影响后续创建的 Agent，不开放用户自选规格，不修改存量 Agent。

## Test plan

- [x] 回归测试先复现原代码转发 `starter`、预期 `pro` 的失败，再验证修复通过。
- [x] 93 项定向测试通过：Default/具名 Project；省略规格或提交 `starter` / `ultra`；凭据初始化、ownership 和 usage attribution；旧 API Platform 不查询 Work 订阅；Work 规格策略及内部规格接口隔离。
- [x] 提交前 Python lint、类型和 import 检查通过。
- [x] 同步最新 main 后，在最终 commit `7ab5bac5203201cae10d8710c819928bf01a7445` 运行 `ecap-verify-py-ci`：**13,661 passed、5 skipped、4 warnings；coverage 89.96%**（4 workers、sysmon、89.5% threshold）。Linux 依赖解析、静态/all CI lint 和两个 jscpd 检查全部通过。

Engine/Gateway 使用 mock，MongoDB 测试使用本地实例。本次没有更改数据库查询形式，未执行线上数据修改、部署或真实付费调用。

---

## feat(billing): integrate Stripe Managed Payments with tax-safe fulfillment (#3997)

- **SHA**: `eb9a503f1e3d1fc516ab643bf34fefaf93213b60`
- **作者**: tim-srp
- **日期**: 2026-10-02T04:14:44Z
- **PR**: #3997

### Commit Message

```
feat(billing): integrate Stripe Managed Payments with tax-safe fulfillment (#3997)
```

### PR Body

## Summary

Adds opt-in Stripe Managed Payments for current Pro monthly subscriptions and credit topups. Managed Checkout can add tax to a USD 30 subscription or a topup; the previous zero-tax validators rejected those successful payments. Settlement now verifies list price minus discount plus exclusive tax, records tax separately, and grants the original purchased credits.

- `STRIPE_MANAGED_PAYMENTS_ENABLED` defaults to `false`. Ordinary Checkout retains its existing parameters. Managed requests omit unsupported payment-method/invoice parameters and require tax-exclusive pricing.
- Pin each order's Checkout mode in the existing audited pre-request CAS so timeouts, concurrent requests and flag changes cannot switch an attempted payment's mode. Pre-migration uncertain requests and existing sessions keep their original behavior.
- Preserve invoice identity/period/price checks, customer balance and verified small-amount deferrals, payment ordering, zero-cash guards and refund/credit idempotency. Tax remains visible in payment audit history after refunds.

## Validation

- 769 targeted Stripe/payment tests passed; 5 existing removed-trial tests skipped.
- 95.95% combined coverage for the six Checkout/tax/settlement modules; new invoice tax parser and Checkout recovery both 100%.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8 import contracts passed.
- Independent read-only code review: no confirmed blockers; added the suggested taxed full-refund/replay regression.
- Local Python 3.12.3 crashed compiling a pre-existing large test module; the same tests passed with the installed Python 3.12.9 and existing dependencies. No runtime/dependency change in this PR.

## Rollout and limits

Backend-only deployment; the default-off flag does not change production routing. Before enabling, enroll the Stripe account, configure eligible product tax codes, and ensure the existing Pro Price is explicitly `exclusive` without replacing the Price ID still used by subscriptions. Topup inline prices explicitly set `exclusive`.

Real Stripe Sandbox payment/renewal/refund/local-currency testing has **not** been performed. The runbook includes paid/zero-tax, promotion, balance, async webhook and flag rollback scenarios. The repository change only adds a nullable field equality to the existing atomic update (no new aggregation/query form); no live CSFLE validation was performed.

Disable the flag to stop new managed checkouts. Keep tax-capable fulfillment deployed while any managed subscriptions exist. Existing subscriptions are not migrated.

Design: `docs/superpowers/specs/2026-10-02-stripe-managed-payments.md`.
Runbook: `services/claw-interface/docs/stripe-credits-v1.md`.


## Follow-up review (2026-10-02)

Kept this as the sole Managed Payments PR after comparison with a separate Claude Code implementation. Commit `bfbd76bc7` preserves the legacy zero-tax contract on non-Managed top-ups and Pro renewals, while continuing to accept verified tax on Managed orders. It pins only Managed Checkout creation and tax-bearing subscription lookups to Stripe API `2026-04-22.dahlia`; the repository's Stripe SDK defaults to `2026-02-25.clover`, where the stable `managed_payments` parameter is unavailable. Ordinary Checkout and other Stripe calls keep the existing version. The flag remains default-off.

Focused regression verification after the follow-up: 547 passed, 5 skipped; Ruff, formatting, Pyright, import contracts, file-length/complexity/dead-code guards passed. Tests include SDK-level HTTP-header/body checks for the per-request version and idempotency retry, plus legacy-versus-Managed tax settlement. No live Stripe Sandbox payment has been run.

Scope: Pro subscriptions and billing-v2 credit top-ups. API Platform top-ups remain on their separate card-only path. Failed asynchronous Managed payments remain unfulfilled and pending for manual review; the buyer can create a new top-up order. The runbook no longer claims automatic handling. Before enabling, confirm Stripe account enrollment/terms, eligible tax codes for both products, the current Pro Price's exclusive tax behavior, and run the Sandbox checklist (including taxed payment, renewal, refund, and delayed-method failure). Do not enable the flag until these checks pass.

Stripe API version evidence: https://docs.stripe.com/changelog/dahlia/2026-04-22/managed-payments


## Opus 5.5 end-to-end review

Reviewed the frontend purchase action, order creation, pending-order guards, Checkout retries, webhooks, settlement and user retry path. A pending top-up does **not** prevent a new top-up order; the suggested async-failure state-machine patch was reverted as unnecessary and disproportionate. A failed delayed-payment subscription could block a new subscription order, but the current USD-only Pro Price should not expose the recurring delayed Pix/UPI methods because they require local-currency presentment and do not support Adaptive Pricing. This is a **Sandbox rollout gate**, not a verified production incident: confirm with Brazil/India test addresses that those methods are absent before enabling the flag, and do not add BRL/INR Price currency options without implementing a safe subscription-failure recovery. Opus 5.5 ran 1,726 related unit tests (5 skipped), plus backend static gates; no live Stripe calls. Details in the runbook.

Managed Payments payment-method matrix: https://docs.stripe.com/payments/managed-payments/how-it-works#payment-method-availability

---

## feat(agents): expose owned Build creation recovery status (#3964)

- **SHA**: `0ae9eec1fa36a23c891aa7d65dce3756e9d8a801`
- **作者**: Chris@ZooClaw
- **日期**: 2026-10-02T03:55:32Z
- **PR**: #3964

### Commit Message

```
feat(agents): expose owned Build creation recovery status (#3964)

## Problem and behavior

New Agent Build smoke (zooclaw-engine#1784) needs to recover a creation
whose response was lost, or whose ECAP uninstall completed before Engine
teardown. Public definition reads require a revision and hide terminal
workspaces; replaying creation cannot recover terminal identity.

Add owner-scoped `POST /agent-definitions/creation-status` accepting
only the original idempotency key. It derives the same workspace
identity as creation and returns explicit absent/partial/terminal
status, runtime IDs and the definition's opaque runtime ownership. It
rejects main, internal, adopted, template and shared-copy records. The
endpoint is read-only and reuses the existing single-collection owned
lookup; no new query form, migration or lifecycle lease.

The existing read-only source-root discovery response also exposes its
saved `change_set_id`, so B02 can use the existing owned ChangeSet API
instead of asking the model to invent an ID. No additional write API or
server ID algorithm is duplicated.

## Validation

- 98 targeted tests passed: new lifecycle/ownership/HTTP contracts plus
existing creation and route boundaries.
- `bash scripts/verify-py.sh` passed: ruff, format, pyright and import
contracts.
- Commit hooks passed, including CSFLE-related repository guards and
architecture checks.
- Live encrypted-client/staging acceptance remains pending deployment
with the Engine smoke companion. No shared staging or production data
was mutated.

Related:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1784.
Server-side stuck lifecycle and late authoring fencing remain separate
product issues #3960 and #3963. This PR does not claim to fix those
lifecycle races.
```

### PR Body

## Problem and behavior

New Agent Build smoke (zooclaw-engine#1784) needs to recover a creation whose response was lost, or whose ECAP uninstall completed before Engine teardown. Public definition reads require a revision and hide terminal workspaces; replaying creation cannot recover terminal identity.

Add owner-scoped `POST /agent-definitions/creation-status` accepting only the original idempotency key. It derives the same workspace identity as creation and returns explicit absent/partial/terminal status, runtime IDs and the definition's opaque runtime ownership. It rejects main, internal, adopted, template and shared-copy records. The endpoint is read-only and reuses the existing single-collection owned lookup; no new query form, migration or lifecycle lease.

The existing read-only source-root discovery response also exposes its saved `change_set_id`, so B02 can use the existing owned ChangeSet API instead of asking the model to invent an ID. No additional write API or server ID algorithm is duplicated.

## Validation

- 98 targeted tests passed: new lifecycle/ownership/HTTP contracts plus existing creation and route boundaries.
- `bash scripts/verify-py.sh` passed: ruff, format, pyright and import contracts.
- Commit hooks passed, including CSFLE-related repository guards and architecture checks.
- Live encrypted-client/staging acceptance remains pending deployment with the Engine smoke companion. No shared staging or production data was mutated.

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/1784. Server-side stuck lifecycle and late authoring fencing remain separate product issues #3960 and #3963. This PR does not claim to fix those lifecycle races.

---

