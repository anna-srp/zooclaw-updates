# ecap-workspace — 2026-06-07

Total commits: 7


## fa5dbed0 — 2026-06-07T07:37:53Z
**Author:** bill-srp
**PR:** #2241

### Commit Message
```
fix(web): show connected topbar from Mattermost status (#2241)

## Summary
- Use Mattermost connection state as the topbar status source when
Mattermost context is present.
- Keep OpenClaw websocket status as the fallback for pages without
Mattermost context.
- Update the header unit expectation for MM-connected /
gateway-WS-disconnected state.

## Root cause
The topbar still required the old OpenClaw gateway websocket status to
be connected. After removing the status-connect token-check dependency,
that websocket can remain disconnected while Mattermost is connected, so
the header incorrectly showed the disconnected state.

## Test plan
- [x] Commit created: 3d2c25225
- [ ] pnpm --dir web run lint — blocked locally by ESLint config/tooling
error: eslint-config-next/plugin:@next/next reports unexpected top-level
property "name".
- [ ] pnpm --dir web run tsc — blocked locally by pnpm command dispatch
error: Unknown option "if-present".
- [ ] pnpm --dir web run test:unit — blocked locally by incomplete
node_modules; many suites fail to resolve declared deps including
usehooks-ts, zustand, and @tanstack/query-sync-storage-persister.
```

### PR Description
## Summary
- Use Mattermost connection state as the topbar status source when Mattermost context is present.
- Keep OpenClaw websocket status as the fallback for pages without Mattermost context.
- Update the header unit expectation for MM-connected / gateway-WS-disconnected state.

## Root cause
The topbar still required the old OpenClaw gateway websocket status to be connected. After removing the status-connect token-check dependency, that websocket can remain disconnected while Mattermost is connected, so the header incorrectly showed the disconnected state.

## Test plan
- [x] Commit created: 3d2c25225
- [ ] pnpm --dir web run lint — blocked locally by ESLint config/tooling error: eslint-config-next/plugin:@next/next reports unexpected top-level property "name".
- [ ] pnpm --dir web run tsc — blocked locally by pnpm command dispatch error: Unknown option "if-present".
- [ ] pnpm --dir web run test:unit — blocked locally by incomplete node_modules; many suites fail to resolve declared deps including usehooks-ts, zustand, and @tanstack/query-sync-storage-persister.


---

## 99fcb10f — 2026-06-07T03:26:53Z
**Author:** dependabot[bot]
**PR:** #2234

### Commit Message
```
chore(deps): bump the minor-and-patch group in /web with 18 updates (#2234)

[//]: # (dependabot-start)
⚠️  **Dependabot is rebasing this PR** ⚠️ 

Rebasing might not happen immediately, so don't worry if this takes some
time.

Note: if you make any changes to this PR yourself, they will take
precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps the minor-and-patch group in /web with 18 updates:

| Package | From | To |
| --- | --- | --- |
|
[@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react)
| `0.14.7` | `0.14.11` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) |
`10.53.1` | `10.55.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) |
`10.53.1` | `10.55.0` |
|
[@tanstack/query-sync-storage-persister](https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister)
| `5.100.13` | `5.100.14` |
|
[@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query)
| `5.100.13` | `5.100.14` |
|
[@tanstack/react-query-persist-client](https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client)
| `5.100.13` | `5.100.14` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.4.5` | `3.4.7` |
| [heic-to](https://github.com/hoppergee/heic-to) | `1.4.3` | `1.5.2` |
| [zustand](https://github.com/pmndrs/zustand) | `5.0.13` | `5.0.14` |
|
[@tanstack/react-query-devtools](https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools)
| `5.100.13` | `5.100.14` |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) |
`17.4.0` | `17.4.2` |
|
[eslint-plugin-prettier](https://github.com/prettier/eslint-plugin-prettier)
| `5.5.5` | `5.5.6` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.13.0` |
`12.14.0` |
| [jscpd](https://github.com/kucherenko/jscpd) | `4.2.3` | `4.2.4` |
|
[wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler)
| `4.94.0` | `4.95.0` |
|
[react-router](https://github.com/remix-run/react-router/tree/HEAD/packages/react-router)
| `7.15.1` | `7.16.0` |
|
[@react-router/dev](https://github.com/remix-run/react-router/tree/HEAD/packages/react-router-dev)
| `7.15.1` | `7.16.0` |
|
[typescript-eslint](https://github.com/typescript-eslint/typescript-eslint/tree/HEAD/packages/typescript-eslint)
| `8.59.4` | `8.60.0` |

Updates `@assistant-ui/react` from 0.14.7 to 0.14.11
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/releases">@​assistant-ui/react's
releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.14.11</h2>
<h3>Patch Changes</h3>
<ul>
<li><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4125">#4125</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a>
- chore: drop tracker-behaviour explainer comments left behind in
satellite runtimes (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.14.9</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4120">#4120</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>
- feat: simplify <code>MessagePrimitive.GroupedParts</code> API and add
<code>groupPartByType</code> helper. (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<ul>
<li>New <code>groupPartByType({ ... })</code> helper builds a
<code>groupBy</code> from a <code>part.type → group-key path</code>
lookup. The map keys are typed against
<code>PartState[&quot;type&quot;]</code> (autocomplete + typo
rejection), missing keys leave the part ungrouped, and the returned
function carries an internal memo fingerprint so the tree survives
unrelated re-renders even when reconstructed inline.</li>
<li>Special map key <code>&quot;mcp-app&quot;</code> matches tool-call
parts that point at an assistant-ui MCP app resource
(<code>ui://...</code>). It takes precedence over the
<code>&quot;tool-call&quot;</code> entry for those parts, so MCP apps
can be routed separately (e.g. rendered outside a chain-of-thought
wrapper).</li>
<li><code>groupBy</code> signature simplified from <code>(part, index,
parts) =&gt; string | string[] | null | undefined</code> to <code>(part)
=&gt; readonly \</code>group-${string}`[] | null<code>. The 2nd/3rd args
were unused in practice. Arrays are required (no bare-string shorthand);
</code>null<code>is accepted as an alias for</code>[]` to soften the
migration.</li>
<li>Internal memoization now uses the helper's memo fingerprint when
present, otherwise rebuilds the tree per render (O(n), cheap). The
previous &quot;pass a stable reference&quot; advice is dropped — inline
<code>groupBy</code> is fine.</li>
<li>Docs and examples updated to lead with <code>groupPartByType</code>.
The <code>getMcpAppFromToolPart</code> branch in
<code>packages/ui</code> switches to <code>&quot;mcp-app&quot;:
[]</code> via the helper.</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4107">#4107</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>
- feat: surface AI SDK v6 tool approvals as a first-class
<code>respondToApproval</code> prop on tool components. tool-call parts
in the <code>approval-requested</code> state now carry
<code>part.approval = { id, isAutomatic? }</code>; tool components call
<code>respondToApproval({ approved, reason? })</code> to ack the gate
without threading <code>chatHelpers</code> through application context.
also fixes a transient <code>requires-action</code> flicker for the
<code>approval-responded</code> state and tightens the external-message
converter so interrupt vs pending tool calls are distinguished by an
actual <code>interrupt</code>/<code>approval</code> field rather than by
<code>result === undefined</code>. (<a
href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/d4f1db428b1a1fe5c122150e1e366a377e9adb5f"><code>d4f1db4</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.6</li>
<li>assistant-stream@0.3.17</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.14.8</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4093">#4093</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a>
- feat(react): <code>unstable_insertNewlineOnTouchEnter</code> on
<code>ComposerPrimitive.Input</code> (<a
href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
<p>When set, plain Enter on a touch-primary device — detected via the
<code>(pointer: coarse) and (not (any-pointer: fine))</code> media query
— inserts a newline instead of submitting. Messages then dispatch only
via the explicit Send button, matching the chat-input convention used by
WhatsApp, Slack, Discord, iMessage, ChatGPT, and Claude.ai, and avoiding
the consumer-side caret-aware re-insertion dance the previous workaround
required.</p>
<p>Orthogonal to <code>submitMode</code>: only takes effect when
<code>submitMode</code> resolves to <code>&quot;enter&quot;</code> (the
default). A tablet paired with a hardware keyboard can still submit via
<code>submitMode=&quot;ctrlEnter&quot;</code> (Cmd/Ctrl+Enter), and
<code>submitMode=&quot;none&quot;</code> is unchanged.</p>
<pre lang="tsx"><code>&lt;ComposerPrimitive.Input
  placeholder=&quot;Ask anything...&quot;
  unstable_insertNewlineOnTouchEnter
/&gt;
</code></pre>
<p>Stays <code>unstable_</code> until we have enough field signal to
flip the behavior on by default.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3967">#3967</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/0a0c306286598ea885b046a1dfb85016f720051c"><code>0a0c306</code></a>
- feat(core, react): add <code>MessagePrimitive.GenerativeUI</code>
primitive (<a
href="https://github.com/samdickson22"><code>@​samdickson22</code></a>)</p>
<p>A new first-class primitive for rendering agent-described React UI
from a JSON
spec, with a consumer-provided component allowlist as the security
boundary.</p>
<p>The agent emits a new <code>generative-ui</code> message part
containing a tree of
components by name; <code>MessagePrimitive.GenerativeUI</code> walks the
spec and resolves
each name against the registry you pass in. Unknown names throw a typed
<code>GenerativeUIRenderError</code> (or invoke the optional
<code>Fallback</code>). Composes with
<code>MessagePrimitive.Parts</code> via the new
<code>components.generativeUI</code> option, and
supports streaming partial specs.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md">@​assistant-ui/react's
changelog</a>.</em></p>
<blockquote>
<h2>0.14.11</h2>
<h3>Patch Changes</h3>
<ul>
<li><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4125">#4125</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a>
- chore: drop tracker-behaviour explainer comments left behind in
satellite runtimes (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<h2>0.14.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4118">#4118</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a>
- feat(core): build a client-side tool-invocations pipeline directly
into <code>useExternalStoreRuntime</code>. Tool-call parts in messages
now fire <code>streamCall</code> / <code>execute</code> automatically
for any external-store runtime that opts in. Opt in per-adapter via
<code>unstable_enableToolInvocations: true</code> (off by default — most
external-store runtimes either run tools server-side or already wire
their own client-side dispatch path; double-firing is the risk). The
<code>_store.isLoading</code> flag signals when initial history is
loaded: snapshots observed while <code>isLoading === true</code> are
treated as historical (no fire), matching the contract that callers like
<code>importExternalState</code> already rely on. Six in-tree runtimes
(<code>useAssistantTransportRuntime</code>,
<code>useAISDKRuntime</code>, <code>useLangGraphRuntime</code>,
<code>useStreamRuntime</code>, <code>useAgUiRuntime</code>,
<code>useAdkRuntime</code>) are migrated to the embedded tracker; the
standalone <code>useToolInvocations</code> React hook is removed. Adds
<code>ExternalStoreAdapter.setToolStatuses</code> so adapters can mirror
the tracker's per-tool-call status into local React state for converter
metadata. Auto-aborts in-flight tool calls on new turns
(<code>append()</code> with <code>startRun</code>,
<code>startRun()</code>) so a tool that finishes after the user moves on
can no longer feed a stale result into the next turn. (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/73950929dbebadb275e3bdee23331f65f2635a33"><code>7395092</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/cabfc715e99f23a55dc1276a6028792d7ecad822"><code>cabfc71</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a
href="https://github.com/0"><code>@​0</code></a>.5.13</li>
</ul>
</li>
</ul>
<h2>0.14.9</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4120">#4120</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>
- feat: simplify <code>MessagePrimitive.GroupedParts</code> API and add
<code>groupPartByType</code> helper. (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<ul>
<li>New <code>groupPartByType({ ... })</code> helper builds a
<code>groupBy</code> from a <code>part.type → group-key path</code>
lookup. The map keys are typed against
<code>PartState[&quot;type&quot;]</code> (autocomplete + typo
rejection), missing keys leave the part ungrouped, and the returned
function carries an internal memo fingerprint so the tree survives
unrelated re-renders even when reconstructed inline.</li>
<li>Special map key <code>&quot;mcp-app&quot;</code> matches tool-call
parts that point at an assistant-ui MCP app resource
(<code>ui://...</code>). It takes precedence over the
<code>&quot;tool-call&quot;</code> entry for those parts, so MCP apps
can be routed separately (e.g. rendered outside a chain-of-thought
wrapper).</li>
<li><code>groupBy</code> signature simplified from <code>(part, index,
parts) =&gt; string | string[] | null | undefined</code> to <code>(part)
=&gt; readonly \</code>group-${string}`[] | null<code>. The 2nd/3rd args
were unused in practice. Arrays are required (no bare-string shorthand);
</code>null<code>is accepted as an alias for</code>[]` to soften the
migration.</li>
<li>Internal memoization now uses the helper's memo fingerprint when
present, otherwise rebuilds the tree per render (O(n), cheap). The
previous &quot;pass a stable reference&quot; advice is dropped — inline
<code>groupBy</code> is fine.</li>
<li>Docs and examples updated to lead with <code>groupPartByType</code>.
The <code>getMcpAppFromToolPart</code> branch in
<code>packages/ui</code> switches to <code>&quot;mcp-app&quot;:
[]</code> via the helper.</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4107">#4107</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>
- feat: surface AI SDK v6 tool approvals as a first-class
<code>respondToApproval</code> prop on tool components. tool-call parts
in the <code>approval-requested</code> state now carry
<code>part.approval = { id, isAutomatic? }</code>; tool components call
<code>respondToApproval({ approved, reason? })</code> to ack the gate
without threading <code>chatHelpers</code> through application context.
also fixes a transient <code>requires-action</code> flicker for the
<code>approval-responded</code> state and tightens the external-message
converter so interrupt vs pending tool calls are distinguished by an
actual <code>interrupt</code>/<code>approval</code> field rather than by
<code>result === undefined</code>. (<a
href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/d4f1db428b1a1fe5c122150e1e366a377e9adb5f"><code>d4f1db4</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.6</li>
<li>assistant-stream@0.3.17</li>
</ul>
</li>
</ul>
<h2>0.14.8</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4093">#4093</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a>
- feat(react): <code>unstable_insertNewlineOnTouchEnter</code> on
<code>ComposerPrimitive.Input</code> (<a
href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
<p>When set, plain Enter on a touch-primary device — detected via the
<code>(pointer: coarse) and (not (any-pointer: fine))</code> media query
— inserts a newline instead of submitting. Messages then dispatch only
via the explicit Send button, matching the chat-input convention used by
WhatsApp, Slack, Discord, iMessage, ChatGPT, and Claude.ai, and avoiding
the consumer-side caret-aware re-insertion dance the previous workaround
required.</p>
<p>Orthogonal to <code>submitMode</code>: only takes effect when
<code>submitMode</code> resolves to <code>&quot;enter&quot;</code> (the
default). A tablet paired with a hardware keyboard can still submit via
<code>submitMode=&quot;ctrlEnter&quot;</code> (Cmd/Ctrl+Enter), and
<code>submitMode=&quot;none&quot;</code> is unchanged.</p>
<pre lang="tsx"><code>&lt;ComposerPrimitive.Input
  placeholder=&quot;Ask anything...&quot;
  unstable_insertNewlineOnTouchEnter
/&gt;
</code></pre>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/0ffe1a55027956bf53ec1956810f5df26d547b29"><code>0ffe1a5</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4126">#4126</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/837ff1d5c79590e57a9feecd9df12a764bf1d245"><code>837ff1d</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4122">#4122</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a>
chore: drop tracker-behaviour explainer comments in satellites (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4125">#4125</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a>
feat(core): build tool-invocations pipeline into useExternalStoreRuntime
(<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4118">#4118</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/f965eafa9f5ff0f995098a3b48c1f92d77d20a84"><code>f965eaf</code></a>
chore: prototype migration from Biome to oxlint + oxfmt (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4100">#4100</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/286adc29b161e67f735e53e7edf23792040330c6"><code>286adc2</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4114">#4114</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>
feat: simplify GroupedParts API and add groupPartByType helper (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4120">#4120</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>
feat: add respondToApproval prop for AI SDK v6 tool approvals (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4107">#4107</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/190d8d67262961cb6abaf83b85719b7980278913"><code>190d8d6</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4080">#4080</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a>
feat(react): add unstable_insertNewlineOnTouchEnter to composer input
(<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4093">#4093</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.14.11/packages/react">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.53.1 to 10.55.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases">@​sentry/cloudflare's
releases</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and
deprecate <code>honoIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a
href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry
Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code>
SDK to beta. For details on how to use it, check out the
<a
href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry
TanStack Start SDK docs</a>. Please reach out on
<a
href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a>
if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to
<code>sentry()</code> middleware (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a
<code>shouldHandleError</code> callback to control which errors are
captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored
and 5xx errors and plain <code>Error</code> objects are captured. Return
<code>true</code> from the callback to capture an error,
<code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
return status === 401 || status === 403 || typeof status !== 'number' ||
status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client
entry point (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do
<code>Sentry.init()</code> in the client entry file to capture telemetry
that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing
you to see the full request lifecycle from server-side rendering through
client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route
parametrization (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g.,
<code>GET /users/123</code> becomes <code>GET /users/$userId</code>),
improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function
names in traces (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET
/_serverFn/greet</code> instead of <code>GET
/_serverFn/a10e70b3...</code>). The
<code>tanstackstart.function.hash.sha256</code> span attribute has been
renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
<li>feat(hono): Add warning in Bun for double init (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21195">#21195</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md">@​sentry/cloudflare's
changelog</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and
deprecate <code>honoIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a
href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry
Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code>
SDK to beta. For details on how to use it, check out the
<a
href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry
TanStack Start SDK docs</a>. Please reach out on
<a
href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a>
if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to
<code>sentry()</code> middleware (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a
<code>shouldHandleError</code> callback to control which errors are
captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored
and 5xx errors and plain <code>Error</code> objects are captured. Return
<code>true</code> from the callback to capture an error,
<code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
return status === 401 || status === 403 || typeof status !== 'number' ||
status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client
entry point (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do
<code>Sentry.init()</code> in the client entry file to capture telemetry
that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing
you to see the full request lifecycle from server-side rendering through
client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route
parametrization (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g.,
<code>GET /users/123</code> becomes <code>GET /users/$userId</code>),
improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function
names in traces (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET
/_serverFn/greet</code> instead of <code>GET
/_serverFn/a10e70b3...</code>). The
<code>tanstackstart.function.hash.sha256</code> span attribute has been
renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/acd7b57e1daa9041ee8a081c42af219aa994cca8"><code>acd7b57</code></a>
release: 10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/d5323d24e790bf3200e029bce30ceb86954a7685"><code>d5323d2</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21216">#21216</a>
from getsentry/prepare-release/10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/2fb19298a7236ff5421916851439c20b2634c701"><code>2fb1929</code></a>
meta(changelog): Update changelog for 10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/556bcb391de918a64cc9dcdfa5f58a4b365b0444"><code>556bcb3</code></a>
feat(hono): Add <code>shouldHandleError</code> as middleware option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21205">#21205</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/7a67ea48b66d173d8db4cf4f8610c9aa8221fc74"><code>7a67ea4</code></a>
feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate
<code>honoIntegration</code> ...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/cead7f9836034226bec77ebdb168e8338cffeb21"><code>cead7f9</code></a>
fix(e2e): Fix <code>astro-6</code> e2e test build by relaxing astro
version range (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21211">#21211</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/75fd1d545dbba62faa72c15f0905aea2055d7bf1"><code>75fd1d5</code></a>
chore(changelog): clarify array attributes impact on
<code>beforeSend*</code> callbacks ...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8a2a490df1340df136cb051d9d8f06aaeb36aad6"><code>8a2a490</code></a>
fix(cloudflare): Use original waitUntil to not create a deadlock (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21197">#21197</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/f7b506d5ad421a755c368b4a7754d4cd8027de48"><code>f7b506d</code></a>
feat(metrics): Migrate metrics to use <code>dataCollection</code>
instead of `sendDefaul...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/f55fc305ee86eb4e276105f7fda4c0328f862ab9"><code>f55fc30</code></a>
feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21071">#21071</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.53.1...10.55.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.53.1 to 10.55.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases">@​sentry/nextjs's
releases</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and
deprecate <code>honoIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a
href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry
Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code>
SDK to beta. For details on how to use it, check out the
<a
href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry
TanStack Start SDK docs</a>. Please reach out on
<a
href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a>
if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to
<code>sentry()</code> middleware (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a
<code>shouldHandleError</code> callback to control which errors are
captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored
and 5xx errors and plain <code>Error</code> objects are captured. Return
<code>true</code> from the callback to capture an error,
<code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
return status === 401 || status === 403 || typeof status !== 'number' ||
status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client
entry point (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do
<code>Sentry.init()</code> in the client entry file to capture telemetry
that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing
you to see the full request lifecycle from server-side rendering through
client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route
parametrization (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g.,
<code>GET /users/123</code> becomes <code>GET /users/$userId</code>),
improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function
names in traces (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET
/_serverFn/greet</code> instead of <code>GET
/_serverFn/a10e70b3...</code>). The
<code>tanstackstart.function.hash.sha256</code> span attribute has been
renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
<li>feat(hono): Add warning in Bun for double init (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21195">#21195</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md">@​sentry/nextjs's
changelog</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and
deprecate <code>honoIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a
href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry
Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code>
SDK to beta. For details on how to use it, check out the
<a
href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry
TanStack Start SDK docs</a>. Please reach out on
<a
href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a>
if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to
<code>sentry()</code> middleware (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a
<code>shouldHandleError</code> callback to control which errors are
captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored
and 5xx errors and plain <code>Error</code> objects are captured. Return
<code>true</code> from the callback to capture an error,
<code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
return status === 401 || status === 403 || typeof status !== 'number' ||
status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client
entry point (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do
<code>Sentry.init()</code> in the client entry file to capture telemetry
that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing
you to see the full request lifecycle from server-side rendering through
client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route
parametrization (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g.,
<code>GET /users/123</code> becomes <code>GET /users/$userId</code>),
improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function
names in traces (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET
/_serverFn/greet</code> instead of <code>GET
/_serverFn/a10e70b3...</code>). The
<code>tanstackstart.function.hash.sha256</code> span attribute has been
renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/acd7b57e1daa9041ee8a081c42af219aa994cca8"><code>acd7b57</code></a>
release: 10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/d5323d24e790bf3200e029bce30ceb86954a7685"><code>d5323d2</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21216">#21216</a>
from getsentry/prepare-release/10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/2fb19298a7236ff5421916851439c20b2634c701"><code>2fb1929</code></a>
meta(changelog): Update changelog for 10.55.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/556bcb391de918a64cc9dcdfa5f58a4b365b0444"><code>556bcb3</code></a>
feat(hono): Add <code>shouldHandleError</code> as middleware option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21205">#21205</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/7a67ea48b66d173d8db4cf4f8610c9aa8221fc74"><code>7a67ea4</code></a>
feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate
<code>honoIntegration</code> ...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/cead7f9836034226bec77ebdb168e8338cffeb21"><code>cead7f9</code></a>
fix(e2e): Fix <code>astro-6</code> e2e test build by relaxing astro
version range (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21211">#21211</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/75fd1d545dbba62faa72c15f0905aea2055d7bf1"><code>75fd1d5</code></a>
chore(changelog): clarify array attributes impact on
<code>beforeSend*</code> callbacks ...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8a2a490df1340df136cb051d9d8f06aaeb36aad6"><code>8a2a490</code></a>
fix(cloudflare): Use original waitUntil to not create a deadlock (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21197">#21197</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/f7b506d5ad421a755c368b4a7754d4cd8027de48"><code>f7b506d</code></a>
feat(metrics): Migrate metrics to use <code>dataCollection</code>
instead of `sendDefaul...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/f55fc305ee86eb4e276105f7fda4c0328f862ab9"><code>f55fc30</code></a>
feat(core): Migrate request data to <code>dataCollection</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/21071">#21071</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.53.1...10.55.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/query-sync-storage-persister` from 5.100.13 to
5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/query-sync-storage-persister's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/query-sync-storage-persister</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/query-sync-storage-persister/CHANGELOG.md">@​tanstack/query-sync-storage-persister's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10767">#10767</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/query-sync-storage-persister@5.100.14/packages/query-sync-storage-persister">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>fix(react-query): do not go into optimistic fetching state when not
subscribed (<a
href="https://redirect.github.com/TanStack/query/pull/10759">#10759</a>)</p>
</li>
<li>
<p>Updated dependencies []:</p>
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md">@​tanstack/react-query's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>fix(react-query): do not go into optimistic fetching state when not
subscribed (<a
href="https://redirect.github.com/TanStack/query/pull/10759">#10759</a>)</p>
</li>
<li>
<p>Updated dependencies []:</p>
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10767">#10767</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>
fix(react): do not go into optimistic fetching state when not subscribed
(<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10">#10</a>...</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.100.14/packages/react-query">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-persist-client` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query-persist-client's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query-persist-client/CHANGELOG.md">@​tanstack/react-query-persist-client's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10767">#10767</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query-persist-client@5.100.14/packages/react-query-persist-client">compare
view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.4.5 to 3.4.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/cure53/DOMPurify/releases">dompurify's
releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.7</h2>
<ul>
<li>Hardened the handling of Shadow Roots when using
<code>IN_PLACE</code>, thanks <a
href="https://github.com/GameZoneHacker"><code>@​GameZoneHacker</code></a></li>
<li>Removed a problem leading to permanent hook pollution, thanks <a
href="https://github.com/offset"><code>@​offset</code></a></li>
<li>Refactored the test suite and expanded test coverage
significantly</li>
</ul>
<h2>DOMPurify 3.4.6</h2>
<ul>
<li>Fixed several issues with DOM Clobbering in <code>IN_PLACE</code>
mode, thanks <a
href="https://github.com/offset"><code>@​offset</code></a> &amp; <a
href="https://github.com/Bankde"><code>@​Bankde</code></a></li>
<li>Hardened the checks for cross-realm <code>IN_PLACE</code> and Shadow
DOM sanitization, thanks <a
href="https://github.com/offset"><code>@​offset</code></a> &amp; <a
href="https://github.com/Bankde"><code>@​Bankde</code></a></li>
<li>Added more test coverage for <code>IN_PLACE</code> and general DOM
Clobbering attacks</li>
<li>Bumped several dependencies where possible</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/cure53/DOMPurify/commit/ca30f070c360df162a3e3848e80e6fd3c9e74bff"><code>ca30f07</code></a>
release: 3.4.7 (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1414">#1414</a>)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/bb7739e5bccec7e1ab3dae3f3e42d02db3acaaae"><code>bb7739e</code></a>
release: 3.4.6 (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1394">#1394</a>)</li>
<li>See full diff in <a
href="https://github.com/cure53/DOMPurify/compare/3.4.5...3.4.7">compare
view</a></li>
</ul>
</details>
<br />

Updates `heic-to` from 1.4.3 to 1.5.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/hoppergee/heic-to/releases">heic-to's
releases</a>.</em></p>
<blockquote>
<h2>v1.5.2</h2>
<ul>
<li>Upgrade libheif to <a
href="https://github.com/strukturag/libheif/releases/tag/v1.22.2">1.22.2</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/hoppergee/heic-to/compare/v1.5.1...v1.5.2">https://github.com/hoppergee/heic-to/compare/v1.5.1...v1.5.2</a></p>
<h2>v1.5.1</h2>
<ul>
<li>Upgrade libheif to <a
href="https://github.com/strukturag/libheif/releases/tag/v1.22.1">1.22.1</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/hoppergee/heic-to/compare/v1.5.0...v1.5.1">https://github.com/hoppergee/heic-to/compare/v1.5.0...v1.5.1</a></p>
<h2>v1.5.0</h2>
<ul>
<li>Upgrade libheif to <a
href="https://github.com/strukturag/libheif/releases/tag/v1.22.0">1.22.0</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.0">https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.0</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/hoppergee/heic-to/commit/f37af866f9aa6212ddc84b67a279c9f2386aba4f"><code>f37af86</code></a>
Bump to v1.5.2</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/04bcd5e0e9a9bedfb437d942dec54487a4642caa"><code>04bcd5e</code></a>
Upgrade to libheif v1.22.2</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/19104293df35740726af8fe26549d47e828bbfdd"><code>1910429</code></a>
Bump to v1.5.1</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/ed8706b7e1e554292a32fe8e65b7761eff09cade"><code>ed8706b</code></a>
Upgrade libheift v1.22.1</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/4db71b8b6805d30fd193d8e6d2c12f7fc0ad227c"><code>4db71b8</code></a>
Bump to 1.5.0</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/ea8d837eabf66bac5f970a2202f65893c176913d"><code>ea8d837</code></a>
Upgrade to libheif 1.22.0</li>
<li><a
href="https://github.com/hoppergee/heic-to/commit/7e75ce0e96a4e044df4d4535bd472f97bcd1c76a"><code>7e75ce0</code></a>
Update package-lock.json</li>
<li>See full diff in <a
href="https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.2">compare
view</a></li>
</ul>
</details>
<br />

Updates `zustand` from 5.0.13 to 5.0.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/pmndrs/zustand/releases">zustand's
releases</a>.</em></p>
<blockquote>
<h2>v5.0.14</h2>
<p>This release fixes a type issue in devtools.</p>
<h2>What's Changed</h2>
<ul>
<li>fix(devtools): improve type inference for Devtools initializer by <a
href="https://github.com/dbritto-dev"><code>@​dbritto-dev</code></a> in
<a
href="https://redirect.github.com/pmndrs/zustand/pull/3511">pmndrs/zustand#3511</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a
href="https://github.com/TheSeydiCharyyev"><code>@​TheSeydiCharyyev</code></a>
made their first contribution in <a
href="https://redirect.github.com/pmndrs/zustand/pull/3487">pmndrs/zustand#3487</a></li>
<li><a href="https://github.com/brofrong"><code>@​brofrong</code></a>
made their first contribution in <a
href="https://redirect.github.com/pmndrs/zustand/pull/3496">pmndrs/zustand#3496</a></li>
<li><a href="https://github.com/hyun907"><code>@​hyun907</code></a> made
their first contribution in <a
href="https://redirect.github.com/pmndrs/zustand/pull/3506">pmndrs/zustand#3506</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14">https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pmndrs/zustand/commit/bfb2a9e7ce52608d54d8a077fb87ac9d12e73c58"><code>bfb2a9e</code></a>
5.0.14</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/62b2aff30c3860a1ad735d61801c6cc379771d24"><code>62b2aff</code></a>
chore(deps): update dev dependencies (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3513">#3513</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/ad77bd3bb6f7bbd12fea8b458ed5c0673df0793a"><code>ad77bd3</code></a>
fix(devtools): improve type inference for Devtools initializer (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3511">#3511</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/8476d2ca288d787c1ffdd53615f44c85e98f87be"><code>8476d2c</code></a>
update pnpm etc (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3512">#3512</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/d690ec29a923977d7a9091554445d1026dfe4611"><code>d690ec2</code></a>
docs(combine): add object constraints to T and U in signature (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3506">#3506</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/fd8c60190191c66270ced434196a210f481e9d35"><code>fd8c601</code></a>
docs(react): add Action constraint to redux middleware signature (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3492">#3492</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/2ce8226ba4481bec4ab7e1573606d336f4003fba"><code>2ce8226</code></a>
docs(immer): fix setPerson updater type in usage examples (<a
href="https://redirect.github.com/pmndrs/zustand/issues/3502">#3502</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/038b93861b232e3b7e15a40d561c0d69fec2f2f1"><code>038b938</code></a>
docs(updating-state): use curried create form with explicit state type
(<a
href="https://redirect.github.com/pmndrs/zustand/issues/3503">#3503</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/60a91b480b0d1742584c651cc0ddd58ac9a230ea"><code>60a91b4</code></a>
docs(devtools): add missing devtools import to troubleshooting example
(<a
href="https://redirect.github.com/pmndrs/zustand/issues/3501">#3501</a>)</li>
<li><a
href="https://github.com/pmndrs/zustand/commit/efad16936dd6f648075dc1e86abe9a072746530e"><code>efad169</code></a>
Update FUNDING.json</li>
<li>Additional commits viewable in <a
href="https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-devtools` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query-devtools's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query-devtools/CHANGELOG.md">@​tanstack/react-query-devtools's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10767">#10767</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query-devtools@5.100.14/packages/react-query-devtools">compare
view</a></li>
</ul>
</details>
<br />

Updates `dependency-cruiser` from 17.4.0 to 17.4.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/sverweij/dependency-cruiser/releases">dependency-cruiser's
releases</a>.</em></p>
<blockquote>
<h2>v17.4.2</h2>
<h2>📖 documentation</h2>
<ul>
<li>ae0fcd40 doc: corrects typos</li>
</ul>
<h2>👷 maintenance</h2>
<ul>
<li>ccef0faf chore(npm): sets ignore-scripts on ci</li>
<li>ca1fe64a chore(npm): makes publishing staged only</li>
<li>d4dad0e9/ 1d1bc84a/ ca1fe64a build(npm): updates external
dependencies</li>
</ul>
<h2>v17.4.1</h2>
<p>This release was created on github, but not published to npmjs</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/643462527f7a57ebf0ebc6277b4f47e4cf5180ab"><code>6434625</code></a>
17.4.2</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/17595296667bdf8fb0c352042621dd84dce7f4b2"><code>1759529</code></a>
chore(ci): simplifies release flow again</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/56e501fd13e44fad8377997edf183f6930f6afa9"><code>56e501f</code></a>
17.4.1</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/ccef0fafbb4f7ef740f74477a97c2b7bc54606ca"><code>ccef0fa</code></a>
chore(npm): sets ignore-scripts on ci</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/ca1fe64a4eef04e7a9177fd7c70ddf73ce0a903c"><code>ca1fe64</code></a>
chore(npm): makes publishing staged only</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/b5b2c36b0bd0120f949ac1d0b7e74babeca3f8c5"><code>b5b2c36</code></a>
build(npm): updates external dependencies</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/1d1bc84a22d1020c275b9e6408096bac1ac795bb"><code>1d1bc84</code></a>
build(npm): updates external dependencies</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/ae0fcd40b90ecf03be2b471b7608c602d744fd58"><code>ae0fcd4</code></a>
doc: corrects typos</li>
<li><a
href="https://github.com/sverweij/dependency-cruiser/commit/d4dad0e951e90c76c0a164bb960a1aa4b7bca8db"><code>d4dad0e</code></a>
build(npm): updates external dependencies</li>
<li>See full diff in <a
href="https://github.com/sverweij/dependency-cruiser/compare/v17.4.0...v17.4.2">compare
view</a></li>
</ul>
</details>
<br />

Updates `eslint-plugin-prettier` from 5.5.5 to 5.5.6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/prettier/eslint-plugin-prettier/releases">eslint-plugin-prettier's
releases</a>.</em></p>
<blockquote>
<h2>v5.5.6</h2>
<h3>Patch Changes</h3>
<ul>
<li><a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/pull/791">#791</a>
<a
href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a>
Thanks <a href="https://github.com/JounQin"><code>@​JounQin</code></a>!
- chore: bump all (dev)Dependencies</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/prettier/eslint-plugin-prettier/blob/main/CHANGELOG.md">eslint-plugin-prettier's
changelog</a>.</em></p>
<blockquote>
<h2>5.5.6</h2>
<h3>Patch Changes</h3>
<ul>
<li><a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/pull/791">#791</a>
<a
href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a>
Thanks <a href="https://github.com/JounQin"><code>@​JounQin</code></a>!
- chore: bump all (dev)Dependencies</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/prettier/eslint-plugin-prettier/commit/4f33ea5a503c6cdbda93424ebd13188a46a1a890"><code>4f33ea5</code></a>
chore: release eslint-plugin-prettier (<a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/792">#792</a>)</li>
<li><a
href="https://github.com/prettier/eslint-plugin-prettier/commit/4745b54882a9011704764070a28aaaf0504efc92"><code>4745b54</code></a>
ci: declare workflow-level contents: read on 2 workflows (<a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/790">#790</a>)</li>
<li><a
href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a>
chore: bump all (dev)Dependencies (<a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/791">#791</a>)</li>
<li><a
href="https://github.com/prettier/eslint-plugin-prettier/commit/e867680b2c1cf3748322c8c802690e7cfb78e233"><code>e867680</code></a>
chore(deps): update all dependencies (<a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/766">#766</a>)</li>
<li><a
href="https://github.com/prettier/eslint-plugin-prettier/commit/e8e2f7f1dcad747f1d43168ee09956b512956593"><code>e8e2f7f</code></a>
chore: testing eslint v10 (<a
href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/779">#779</a>)</li>
<li><a
href="https://github.com…
```

### PR Description
Bumps the minor-and-patch group in /web with 18 updates:

| Package | From | To |
| --- | --- | --- |
| [@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react) | `0.14.7` | `0.14.11` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) | `10.53.1` | `10.55.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) | `10.53.1` | `10.55.0` |
| [@tanstack/query-sync-storage-persister](https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister) | `5.100.13` | `5.100.14` |
| [@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query) | `5.100.13` | `5.100.14` |
| [@tanstack/react-query-persist-client](https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client) | `5.100.13` | `5.100.14` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.4.5` | `3.4.7` |
| [heic-to](https://github.com/hoppergee/heic-to) | `1.4.3` | `1.5.2` |
| [zustand](https://github.com/pmndrs/zustand) | `5.0.13` | `5.0.14` |
| [@tanstack/react-query-devtools](https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools) | `5.100.13` | `5.100.14` |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) | `17.4.0` | `17.4.2` |
| [eslint-plugin-prettier](https://github.com/prettier/eslint-plugin-prettier) | `5.5.5` | `5.5.6` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.13.0` | `12.14.0` |
| [jscpd](https://github.com/kucherenko/jscpd) | `4.2.3` | `4.2.4` |
| [wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler) | `4.94.0` | `4.95.0` |
| [react-router](https://github.com/remix-run/react-router/tree/HEAD/packages/react-router) | `7.15.1` | `7.16.0` |
| [@react-router/dev](https://github.com/remix-run/react-router/tree/HEAD/packages/react-router-dev) | `7.15.1` | `7.16.0` |
| [typescript-eslint](https://github.com/typescript-eslint/typescript-eslint/tree/HEAD/packages/typescript-eslint) | `8.59.4` | `8.60.0` |

Updates `@assistant-ui/react` from 0.14.7 to 0.14.11
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/releases">@​assistant-ui/react's releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.14.11</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4125">#4125</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a> - chore: drop tracker-behaviour explainer comments left behind in satellite runtimes (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.14.9</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4120">#4120</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a> - feat: simplify <code>MessagePrimitive.GroupedParts</code> API and add <code>groupPartByType</code> helper. (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<ul>
<li>New <code>groupPartByType({ ... })</code> helper builds a <code>groupBy</code> from a <code>part.type → group-key path</code> lookup. The map keys are typed against <code>PartState[&quot;type&quot;]</code> (autocomplete + typo rejection), missing keys leave the part ungrouped, and the returned function carries an internal memo fingerprint so the tree survives unrelated re-renders even when reconstructed inline.</li>
<li>Special map key <code>&quot;mcp-app&quot;</code> matches tool-call parts that point at an assistant-ui MCP app resource (<code>ui://...</code>). It takes precedence over the <code>&quot;tool-call&quot;</code> entry for those parts, so MCP apps can be routed separately (e.g. rendered outside a chain-of-thought wrapper).</li>
<li><code>groupBy</code> signature simplified from <code>(part, index, parts) =&gt; string | string[] | null | undefined</code> to <code>(part) =&gt; readonly \</code>group-${string}`[] | null<code>. The 2nd/3rd args were unused in practice. Arrays are required (no bare-string shorthand); </code>null<code>is accepted as an alias for</code>[]` to soften the migration.</li>
<li>Internal memoization now uses the helper's memo fingerprint when present, otherwise rebuilds the tree per render (O(n), cheap). The previous &quot;pass a stable reference&quot; advice is dropped — inline <code>groupBy</code> is fine.</li>
<li>Docs and examples updated to lead with <code>groupPartByType</code>. The <code>getMcpAppFromToolPart</code> branch in <code>packages/ui</code> switches to <code>&quot;mcp-app&quot;: []</code> via the helper.</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4107">#4107</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a> - feat: surface AI SDK v6 tool approvals as a first-class <code>respondToApproval</code> prop on tool components. tool-call parts in the <code>approval-requested</code> state now carry <code>part.approval = { id, isAutomatic? }</code>; tool components call <code>respondToApproval({ approved, reason? })</code> to ack the gate without threading <code>chatHelpers</code> through application context. also fixes a transient <code>requires-action</code> flicker for the <code>approval-responded</code> state and tightens the external-message converter so interrupt vs pending tool calls are distinguished by an actual <code>interrupt</code>/<code>approval</code> field rather than by <code>result === undefined</code>. (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/d4f1db428b1a1fe5c122150e1e366a377e9adb5f"><code>d4f1db4</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.6</li>
<li>assistant-stream@0.3.17</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.14.8</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4093">#4093</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a> - feat(react): <code>unstable_insertNewlineOnTouchEnter</code> on <code>ComposerPrimitive.Input</code> (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
<p>When set, plain Enter on a touch-primary device — detected via the <code>(pointer: coarse) and (not (any-pointer: fine))</code> media query — inserts a newline instead of submitting. Messages then dispatch only via the explicit Send button, matching the chat-input convention used by WhatsApp, Slack, Discord, iMessage, ChatGPT, and Claude.ai, and avoiding the consumer-side caret-aware re-insertion dance the previous workaround required.</p>
<p>Orthogonal to <code>submitMode</code>: only takes effect when <code>submitMode</code> resolves to <code>&quot;enter&quot;</code> (the default). A tablet paired with a hardware keyboard can still submit via <code>submitMode=&quot;ctrlEnter&quot;</code> (Cmd/Ctrl+Enter), and <code>submitMode=&quot;none&quot;</code> is unchanged.</p>
<pre lang="tsx"><code>&lt;ComposerPrimitive.Input
  placeholder=&quot;Ask anything...&quot;
  unstable_insertNewlineOnTouchEnter
/&gt;
</code></pre>
<p>Stays <code>unstable_</code> until we have enough field signal to flip the behavior on by default.</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3967">#3967</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/0a0c306286598ea885b046a1dfb85016f720051c"><code>0a0c306</code></a> - feat(core, react): add <code>MessagePrimitive.GenerativeUI</code> primitive (<a href="https://github.com/samdickson22"><code>@​samdickson22</code></a>)</p>
<p>A new first-class primitive for rendering agent-described React UI from a JSON
spec, with a consumer-provided component allowlist as the security boundary.</p>
<p>The agent emits a new <code>generative-ui</code> message part containing a tree of
components by name; <code>MessagePrimitive.GenerativeUI</code> walks the spec and resolves
each name against the registry you pass in. Unknown names throw a typed
<code>GenerativeUIRenderError</code> (or invoke the optional <code>Fallback</code>). Composes with
<code>MessagePrimitive.Parts</code> via the new <code>components.generativeUI</code> option, and
supports streaming partial specs.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md">@​assistant-ui/react's changelog</a>.</em></p>
<blockquote>
<h2>0.14.11</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4125">#4125</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a> - chore: drop tracker-behaviour explainer comments left behind in satellite runtimes (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<h2>0.14.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4118">#4118</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a> - feat(core): build a client-side tool-invocations pipeline directly into <code>useExternalStoreRuntime</code>. Tool-call parts in messages now fire <code>streamCall</code> / <code>execute</code> automatically for any external-store runtime that opts in. Opt in per-adapter via <code>unstable_enableToolInvocations: true</code> (off by default — most external-store runtimes either run tools server-side or already wire their own client-side dispatch path; double-firing is the risk). The <code>_store.isLoading</code> flag signals when initial history is loaded: snapshots observed while <code>isLoading === true</code> are treated as historical (no fire), matching the contract that callers like <code>importExternalState</code> already rely on. Six in-tree runtimes (<code>useAssistantTransportRuntime</code>, <code>useAISDKRuntime</code>, <code>useLangGraphRuntime</code>, <code>useStreamRuntime</code>, <code>useAgUiRuntime</code>, <code>useAdkRuntime</code>) are migrated to the embedded tracker; the standalone <code>useToolInvocations</code> React hook is removed. Adds <code>ExternalStoreAdapter.setToolStatuses</code> so adapters can mirror the tracker's per-tool-call status into local React state for converter metadata. Auto-aborts in-flight tool calls on new turns (<code>append()</code> with <code>startRun</code>, <code>startRun()</code>) so a tool that finishes after the user moves on can no longer feed a stale result into the next turn. (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/73950929dbebadb275e3bdee23331f65f2635a33"><code>7395092</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/cabfc715e99f23a55dc1276a6028792d7ecad822"><code>cabfc71</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a href="https://github.com/0"><code>@​0</code></a>.5.13</li>
</ul>
</li>
</ul>
<h2>0.14.9</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4120">#4120</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a> - feat: simplify <code>MessagePrimitive.GroupedParts</code> API and add <code>groupPartByType</code> helper. (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<ul>
<li>New <code>groupPartByType({ ... })</code> helper builds a <code>groupBy</code> from a <code>part.type → group-key path</code> lookup. The map keys are typed against <code>PartState[&quot;type&quot;]</code> (autocomplete + typo rejection), missing keys leave the part ungrouped, and the returned function carries an internal memo fingerprint so the tree survives unrelated re-renders even when reconstructed inline.</li>
<li>Special map key <code>&quot;mcp-app&quot;</code> matches tool-call parts that point at an assistant-ui MCP app resource (<code>ui://...</code>). It takes precedence over the <code>&quot;tool-call&quot;</code> entry for those parts, so MCP apps can be routed separately (e.g. rendered outside a chain-of-thought wrapper).</li>
<li><code>groupBy</code> signature simplified from <code>(part, index, parts) =&gt; string | string[] | null | undefined</code> to <code>(part) =&gt; readonly \</code>group-${string}`[] | null<code>. The 2nd/3rd args were unused in practice. Arrays are required (no bare-string shorthand); </code>null<code>is accepted as an alias for</code>[]` to soften the migration.</li>
<li>Internal memoization now uses the helper's memo fingerprint when present, otherwise rebuilds the tree per render (O(n), cheap). The previous &quot;pass a stable reference&quot; advice is dropped — inline <code>groupBy</code> is fine.</li>
<li>Docs and examples updated to lead with <code>groupPartByType</code>. The <code>getMcpAppFromToolPart</code> branch in <code>packages/ui</code> switches to <code>&quot;mcp-app&quot;: []</code> via the helper.</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4107">#4107</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a> - feat: surface AI SDK v6 tool approvals as a first-class <code>respondToApproval</code> prop on tool components. tool-call parts in the <code>approval-requested</code> state now carry <code>part.approval = { id, isAutomatic? }</code>; tool components call <code>respondToApproval({ approved, reason? })</code> to ack the gate without threading <code>chatHelpers</code> through application context. also fixes a transient <code>requires-action</code> flicker for the <code>approval-responded</code> state and tightens the external-message converter so interrupt vs pending tool calls are distinguished by an actual <code>interrupt</code>/<code>approval</code> field rather than by <code>result === undefined</code>. (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/d4f1db428b1a1fe5c122150e1e366a377e9adb5f"><code>d4f1db4</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.6</li>
<li>assistant-stream@0.3.17</li>
</ul>
</li>
</ul>
<h2>0.14.8</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4093">#4093</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a> - feat(react): <code>unstable_insertNewlineOnTouchEnter</code> on <code>ComposerPrimitive.Input</code> (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
<p>When set, plain Enter on a touch-primary device — detected via the <code>(pointer: coarse) and (not (any-pointer: fine))</code> media query — inserts a newline instead of submitting. Messages then dispatch only via the explicit Send button, matching the chat-input convention used by WhatsApp, Slack, Discord, iMessage, ChatGPT, and Claude.ai, and avoiding the consumer-side caret-aware re-insertion dance the previous workaround required.</p>
<p>Orthogonal to <code>submitMode</code>: only takes effect when <code>submitMode</code> resolves to <code>&quot;enter&quot;</code> (the default). A tablet paired with a hardware keyboard can still submit via <code>submitMode=&quot;ctrlEnter&quot;</code> (Cmd/Ctrl+Enter), and <code>submitMode=&quot;none&quot;</code> is unchanged.</p>
<pre lang="tsx"><code>&lt;ComposerPrimitive.Input
  placeholder=&quot;Ask anything...&quot;
  unstable_insertNewlineOnTouchEnter
/&gt;
</code></pre>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/0ffe1a55027956bf53ec1956810f5df26d547b29"><code>0ffe1a5</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4126">#4126</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/837ff1d5c79590e57a9feecd9df12a764bf1d245"><code>837ff1d</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4122">#4122</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/e639a11838642aa111644077ba51acf6277051f2"><code>e639a11</code></a> chore: drop tracker-behaviour explainer comments in satellites (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4125">#4125</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/a6e0653bad29fb93627646a77c3383000c57ee33"><code>a6e0653</code></a> feat(core): build tool-invocations pipeline into useExternalStoreRuntime (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4118">#4118</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/f965eafa9f5ff0f995098a3b48c1f92d77d20a84"><code>f965eaf</code></a> chore: prototype migration from Biome to oxlint + oxfmt (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4100">#4100</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/286adc29b161e67f735e53e7edf23792040330c6"><code>286adc2</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4114">#4114</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/372d4f0c538a766fd9a849fef74e413dde86d74a"><code>372d4f0</code></a> feat: simplify GroupedParts API and add groupPartByType helper (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4120">#4120</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/32ae846a91b61eccd01330693868a48f2f3bb0c4"><code>32ae846</code></a> feat: add respondToApproval prop for AI SDK v6 tool approvals (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4107">#4107</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/190d8d67262961cb6abaf83b85719b7980278913"><code>190d8d6</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4080">#4080</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/b02b7012cff158b4e73b82503b9ea90638b7398d"><code>b02b701</code></a> feat(react): add unstable_insertNewlineOnTouchEnter to composer input (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4093">#4093</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.14.11/packages/react">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.53.1 to 10.55.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases">@​sentry/cloudflare's releases</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code> SDK to beta. For details on how to use it, check out the
<a href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry TanStack Start SDK docs</a>. Please reach out on
<a href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a> if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to <code>sentry()</code> middleware (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a <code>shouldHandleError</code> callback to control which errors are captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored and 5xx errors and plain <code>Error</code> objects are captured. Return <code>true</code> from the callback to capture an error, <code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
      return status === 401 || status === 403 || typeof status !== 'number' || status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client entry point (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do <code>Sentry.init()</code> in the client entry file to capture telemetry that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing you to see the full request lifecycle from server-side rendering through client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route parametrization (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g., <code>GET /users/123</code> becomes <code>GET /users/$userId</code>), improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function names in traces (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET /_serverFn/greet</code> instead of <code>GET /_serverFn/a10e70b3...</code>). The <code>tanstackstart.function.hash.sha256</code> span attribute has been renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
<li>feat(hono): Add warning in Bun for double init (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21195">#21195</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md">@​sentry/cloudflare's changelog</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code> SDK to beta. For details on how to use it, check out the
<a href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry TanStack Start SDK docs</a>. Please reach out on
<a href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a> if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to <code>sentry()</code> middleware (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a <code>shouldHandleError</code> callback to control which errors are captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored and 5xx errors and plain <code>Error</code> objects are captured. Return <code>true</code> from the callback to capture an error, <code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
      return status === 401 || status === 403 || typeof status !== 'number' || status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client entry point (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do <code>Sentry.init()</code> in the client entry file to capture telemetry that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing you to see the full request lifecycle from server-side rendering through client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route parametrization (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g., <code>GET /users/123</code> becomes <code>GET /users/$userId</code>), improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function names in traces (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET /_serverFn/greet</code> instead of <code>GET /_serverFn/a10e70b3...</code>). The <code>tanstackstart.function.hash.sha256</code> span attribute has been renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/acd7b57e1daa9041ee8a081c42af219aa994cca8"><code>acd7b57</code></a> release: 10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/d5323d24e790bf3200e029bce30ceb86954a7685"><code>d5323d2</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21216">#21216</a> from getsentry/prepare-release/10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/2fb19298a7236ff5421916851439c20b2634c701"><code>2fb1929</code></a> meta(changelog): Update changelog for 10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/556bcb391de918a64cc9dcdfa5f58a4b365b0444"><code>556bcb3</code></a> feat(hono): Add <code>shouldHandleError</code> as middleware option (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21205">#21205</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/7a67ea48b66d173d8db4cf4f8610c9aa8221fc74"><code>7a67ea4</code></a> feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> ...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/cead7f9836034226bec77ebdb168e8338cffeb21"><code>cead7f9</code></a> fix(e2e): Fix <code>astro-6</code> e2e test build by relaxing astro version range (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21211">#21211</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/75fd1d545dbba62faa72c15f0905aea2055d7bf1"><code>75fd1d5</code></a> chore(changelog): clarify array attributes impact on <code>beforeSend*</code> callbacks ...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8a2a490df1340df136cb051d9d8f06aaeb36aad6"><code>8a2a490</code></a> fix(cloudflare): Use original waitUntil to not create a deadlock (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21197">#21197</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/f7b506d5ad421a755c368b4a7754d4cd8027de48"><code>f7b506d</code></a> feat(metrics): Migrate metrics to use <code>dataCollection</code> instead of `sendDefaul...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/f55fc305ee86eb4e276105f7fda4c0328f862ab9"><code>f55fc30</code></a> feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21071">#21071</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.53.1...10.55.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.53.1 to 10.55.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases">@​sentry/nextjs's releases</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code> SDK to beta. For details on how to use it, check out the
<a href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry TanStack Start SDK docs</a>. Please reach out on
<a href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a> if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to <code>sentry()</code> middleware (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a <code>shouldHandleError</code> callback to control which errors are captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored and 5xx errors and plain <code>Error</code> objects are captured. Return <code>true</code> from the callback to capture an error, <code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
      return status === 401 || status === 403 || typeof status !== 'number' || status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client entry point (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do <code>Sentry.init()</code> in the client entry file to capture telemetry that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing you to see the full request lifecycle from server-side rendering through client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route parametrization (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g., <code>GET /users/123</code> becomes <code>GET /users/$userId</code>), improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function names in traces (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET /_serverFn/greet</code> instead of <code>GET /_serverFn/a10e70b3...</code>). The <code>tanstackstart.function.hash.sha256</code> span attribute has been renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
<li>feat(hono): Add warning in Bun for double init (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21195">#21195</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md">@​sentry/nextjs's changelog</a>.</em></p>
<blockquote>
<h2>10.55.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21208">#21208</a>)</strong></p>
<p>The <code>@sentry/hono</code> SDK is now stable. See the <a href="https://docs.sentry.io/platforms/javascript/guides/hono/">Sentry Hono SDK docs</a> to get started.</p>
</li>
<li>
<p><strong>docs(tanstackstart-react): Promote SDK status to beta (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21175">#21175</a>)</strong></p>
<p>This release promotes the <code>@sentry/tanstackstart-react</code> SDK to beta. For details on how to use it, check out the
<a href="https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/">Sentry TanStack Start SDK docs</a>. Please reach out on
<a href="https://github.com/getsentry/sentry-javascript/issues/new/choose">GitHub</a> if you have any feedback or concerns.</p>
</li>
<li>
<p><strong>feat(hono): Add <code>shouldHandleError</code> option to <code>sentry()</code> middleware (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21205">#21205</a>)</strong></p>
<p>The <code>sentry()</code> middleware now accepts a <code>shouldHandleError</code> callback to control which errors are captured and sent to Sentry. By default, 3xx/4xx HTTP errors are ignored and 5xx errors and plain <code>Error</code> objects are captured. Return <code>true</code> from the callback to capture an error, <code>false</code> to suppress it.</p>
<pre lang="ts"><code>app.use(
  sentry(app, {
    dsn: '__DSN__',
    shouldHandleError(error) {
      const status = (error as { status?: number })?.status;
      // Capture 401/403 in addition to the default 5xx errors
      return status === 401 || status === 403 || typeof status !== 'number' || status &gt;= 500;
    },
  }),
);
</code></pre>
</li>
<li>
<p><strong>test(tanstackstart-react): Move initialization to client entry point (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21161">#21161</a>)</strong></p>
<p>Change the recommended setup for the SDK to do <code>Sentry.init()</code> in the client entry file to capture telemetry that is emitted ahead of page hydration.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add distributed tracing (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21144">#21144</a>)</strong></p>
<p>Server and client traces are now automatically connected, allowing you to see the full request lifecycle from server-side rendering through client-side hydration in a single trace.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Add server-side route parametrization (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21147">#21147</a>)</strong></p>
<p>Server transaction names are now parametrized automatically (e.g., <code>GET /users/123</code> becomes <code>GET /users/$userId</code>), improving transaction grouping in Sentry.</p>
</li>
<li>
<p><strong>feat(tanstackstart-react): Show readable server function names in traces (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21190">#21190</a>)</strong></p>
<p>Server function spans now show human-readable names (e.g., <code>GET /_serverFn/greet</code> instead of <code>GET /_serverFn/a10e70b3...</code>). The <code>tanstackstart.function.hash.sha256</code> span attribute has been renamed to <code>tanstackstart.function.id</code>.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/21071">#21071</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/acd7b57e1daa9041ee8a081c42af219aa994cca8"><code>acd7b57</code></a> release: 10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/d5323d24e790bf3200e029bce30ceb86954a7685"><code>d5323d2</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21216">#21216</a> from getsentry/prepare-release/10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/2fb19298a7236ff5421916851439c20b2634c701"><code>2fb1929</code></a> meta(changelog): Update changelog for 10.55.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/556bcb391de918a64cc9dcdfa5f58a4b365b0444"><code>556bcb3</code></a> feat(hono): Add <code>shouldHandleError</code> as middleware option (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21205">#21205</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/7a67ea48b66d173d8db4cf4f8610c9aa8221fc74"><code>7a67ea4</code></a> feat(hono): Promote <code>@sentry/hono</code> to stable and deprecate <code>honoIntegration</code> ...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/cead7f9836034226bec77ebdb168e8338cffeb21"><code>cead7f9</code></a> fix(e2e): Fix <code>astro-6</code> e2e test build by relaxing astro version range (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21211">#21211</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/75fd1d545dbba62faa72c15f0905aea2055d7bf1"><code>75fd1d5</code></a> chore(changelog): clarify array attributes impact on <code>beforeSend*</code> callbacks ...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8a2a490df1340df136cb051d9d8f06aaeb36aad6"><code>8a2a490</code></a> fix(cloudflare): Use original waitUntil to not create a deadlock (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21197">#21197</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/f7b506d5ad421a755c368b4a7754d4cd8027de48"><code>f7b506d</code></a> feat(metrics): Migrate metrics to use <code>dataCollection</code> instead of `sendDefaul...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/f55fc305ee86eb4e276105f7fda4c0328f862ab9"><code>f55fc30</code></a> feat(core): Migrate request data to <code>dataCollection</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/21071">#21071</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.53.1...10.55.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/query-sync-storage-persister` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/query-sync-storage-persister's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/query-sync-storage-persister</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/query-sync-storage-persister/CHANGELOG.md">@​tanstack/query-sync-storage-persister's changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10767">#10767</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/query-sync-storage-persister@5.100.14/packages/query-sync-storage-persister">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>fix(react-query): do not go into optimistic fetching state when not subscribed (<a href="https://redirect.github.com/TanStack/query/pull/10759">#10759</a>)</p>
</li>
<li>
<p>Updated dependencies []:</p>
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md">@​tanstack/react-query's changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>fix(react-query): do not go into optimistic fetching state when not subscribed (<a href="https://redirect.github.com/TanStack/query/pull/10759">#10759</a>)</p>
</li>
<li>
<p>Updated dependencies []:</p>
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10767">#10767</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a> fix(react): do not go into optimistic fetching state when not subscribed (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10">#10</a>...</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.100.14/packages/react-query">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-persist-client` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query-persist-client's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query-persist-client/CHANGELOG.md">@​tanstack/react-query-persist-client's changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10767">#10767</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query-persist-client@5.100.14/packages/react-query-persist-client">compare view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.4.5 to 3.4.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/cure53/DOMPurify/releases">dompurify's releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.7</h2>
<ul>
<li>Hardened the handling of Shadow Roots when using <code>IN_PLACE</code>, thanks <a href="https://github.com/GameZoneHacker"><code>@​GameZoneHacker</code></a></li>
<li>Removed a problem leading to permanent hook pollution, thanks <a href="https://github.com/offset"><code>@​offset</code></a></li>
<li>Refactored the test suite and expanded test coverage significantly</li>
</ul>
<h2>DOMPurify 3.4.6</h2>
<ul>
<li>Fixed several issues with DOM Clobbering in <code>IN_PLACE</code> mode, thanks <a href="https://github.com/offset"><code>@​offset</code></a> &amp; <a href="https://github.com/Bankde"><code>@​Bankde</code></a></li>
<li>Hardened the checks for cross-realm <code>IN_PLACE</code> and Shadow DOM sanitization, thanks <a href="https://github.com/offset"><code>@​offset</code></a> &amp; <a href="https://github.com/Bankde"><code>@​Bankde</code></a></li>
<li>Added more test coverage for <code>IN_PLACE</code> and general DOM Clobbering attacks</li>
<li>Bumped several dependencies where possible</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/cure53/DOMPurify/commit/ca30f070c360df162a3e3848e80e6fd3c9e74bff"><code>ca30f07</code></a> release: 3.4.7 (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1414">#1414</a>)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/bb7739e5bccec7e1ab3dae3f3e42d02db3acaaae"><code>bb7739e</code></a> release: 3.4.6 (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1394">#1394</a>)</li>
<li>See full diff in <a href="https://github.com/cure53/DOMPurify/compare/3.4.5...3.4.7">compare view</a></li>
</ul>
</details>
<br />

Updates `heic-to` from 1.4.3 to 1.5.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/hoppergee/heic-to/releases">heic-to's releases</a>.</em></p>
<blockquote>
<h2>v1.5.2</h2>
<ul>
<li>Upgrade libheif to <a href="https://github.com/strukturag/libheif/releases/tag/v1.22.2">1.22.2</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/hoppergee/heic-to/compare/v1.5.1...v1.5.2">https://github.com/hoppergee/heic-to/compare/v1.5.1...v1.5.2</a></p>
<h2>v1.5.1</h2>
<ul>
<li>Upgrade libheif to <a href="https://github.com/strukturag/libheif/releases/tag/v1.22.1">1.22.1</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/hoppergee/heic-to/compare/v1.5.0...v1.5.1">https://github.com/hoppergee/heic-to/compare/v1.5.0...v1.5.1</a></p>
<h2>v1.5.0</h2>
<ul>
<li>Upgrade libheif to <a href="https://github.com/strukturag/libheif/releases/tag/v1.22.0">1.22.0</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.0">https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.0</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/hoppergee/heic-to/commit/f37af866f9aa6212ddc84b67a279c9f2386aba4f"><code>f37af86</code></a> Bump to v1.5.2</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/04bcd5e0e9a9bedfb437d942dec54487a4642caa"><code>04bcd5e</code></a> Upgrade to libheif v1.22.2</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/19104293df35740726af8fe26549d47e828bbfdd"><code>1910429</code></a> Bump to v1.5.1</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/ed8706b7e1e554292a32fe8e65b7761eff09cade"><code>ed8706b</code></a> Upgrade libheift v1.22.1</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/4db71b8b6805d30fd193d8e6d2c12f7fc0ad227c"><code>4db71b8</code></a> Bump to 1.5.0</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/ea8d837eabf66bac5f970a2202f65893c176913d"><code>ea8d837</code></a> Upgrade to libheif 1.22.0</li>
<li><a href="https://github.com/hoppergee/heic-to/commit/7e75ce0e96a4e044df4d4535bd472f97bcd1c76a"><code>7e75ce0</code></a> Update package-lock.json</li>
<li>See full diff in <a href="https://github.com/hoppergee/heic-to/compare/v1.4.3...v1.5.2">compare view</a></li>
</ul>
</details>
<br />

Updates `zustand` from 5.0.13 to 5.0.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/pmndrs/zustand/releases">zustand's releases</a>.</em></p>
<blockquote>
<h2>v5.0.14</h2>
<p>This release fixes a type issue in devtools.</p>
<h2>What's Changed</h2>
<ul>
<li>fix(devtools): improve type inference for Devtools initializer by <a href="https://github.com/dbritto-dev"><code>@​dbritto-dev</code></a> in <a href="https://redirect.github.com/pmndrs/zustand/pull/3511">pmndrs/zustand#3511</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/TheSeydiCharyyev"><code>@​TheSeydiCharyyev</code></a> made their first contribution in <a href="https://redirect.github.com/pmndrs/zustand/pull/3487">pmndrs/zustand#3487</a></li>
<li><a href="https://github.com/brofrong"><code>@​brofrong</code></a> made their first contribution in <a href="https://redirect.github.com/pmndrs/zustand/pull/3496">pmndrs/zustand#3496</a></li>
<li><a href="https://github.com/hyun907"><code>@​hyun907</code></a> made their first contribution in <a href="https://redirect.github.com/pmndrs/zustand/pull/3506">pmndrs/zustand#3506</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14">https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pmndrs/zustand/commit/bfb2a9e7ce52608d54d8a077fb87ac9d12e73c58"><code>bfb2a9e</code></a> 5.0.14</li>
<li><a href="https://github.com/pmndrs/zustand/commit/62b2aff30c3860a1ad735d61801c6cc379771d24"><code>62b2aff</code></a> chore(deps): update dev dependencies (<a href="https://redirect.github.com/pmndrs/zustand/issues/3513">#3513</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/ad77bd3bb6f7bbd12fea8b458ed5c0673df0793a"><code>ad77bd3</code></a> fix(devtools): improve type inference for Devtools initializer (<a href="https://redirect.github.com/pmndrs/zustand/issues/3511">#3511</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/8476d2ca288d787c1ffdd53615f44c85e98f87be"><code>8476d2c</code></a> update pnpm etc (<a href="https://redirect.github.com/pmndrs/zustand/issues/3512">#3512</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/d690ec29a923977d7a9091554445d1026dfe4611"><code>d690ec2</code></a> docs(combine): add object constraints to T and U in signature (<a href="https://redirect.github.com/pmndrs/zustand/issues/3506">#3506</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/fd8c60190191c66270ced434196a210f481e9d35"><code>fd8c601</code></a> docs(react): add Action constraint to redux middleware signature (<a href="https://redirect.github.com/pmndrs/zustand/issues/3492">#3492</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/2ce8226ba4481bec4ab7e1573606d336f4003fba"><code>2ce8226</code></a> docs(immer): fix setPerson updater type in usage examples (<a href="https://redirect.github.com/pmndrs/zustand/issues/3502">#3502</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/038b93861b232e3b7e15a40d561c0d69fec2f2f1"><code>038b938</code></a> docs(updating-state): use curried create form with explicit state type (<a href="https://redirect.github.com/pmndrs/zustand/issues/3503">#3503</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/60a91b480b0d1742584c651cc0ddd58ac9a230ea"><code>60a91b4</code></a> docs(devtools): add missing devtools import to troubleshooting example (<a href="https://redirect.github.com/pmndrs/zustand/issues/3501">#3501</a>)</li>
<li><a href="https://github.com/pmndrs/zustand/commit/efad16936dd6f648075dc1e86abe9a072746530e"><code>efad169</code></a> Update FUNDING.json</li>
<li>Additional commits viewable in <a href="https://github.com/pmndrs/zustand/compare/v5.0.13...v5.0.14">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-devtools` from 5.100.13 to 5.100.14
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query-devtools's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query-devtools/CHANGELOG.md">@​tanstack/react-query-devtools's changelog</a>.</em></p>
<blockquote>
<h2>5.100.14</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/ed20b6d7541c908033acfcad92b0cd112930d1c3"><code>ed20b6d</code></a>]:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.14</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/ba6e7beebd50143408f01fcf5d9aee2ec1486f60"><code>ba6e7be</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10767">#10767</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query-devtools@5.100.14/packages/react-query-devtools">compare view</a></li>
</ul>
</details>
<br />

Updates `dependency-cruiser` from 17.4.0 to 17.4.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/sverweij/dependency-cruiser/releases">dependency-cruiser's releases</a>.</em></p>
<blockquote>
<h2>v17.4.2</h2>
<h2>📖 documentation</h2>
<ul>
<li>ae0fcd40 doc: corrects typos</li>
</ul>
<h2>👷 maintenance</h2>
<ul>
<li>ccef0faf chore(npm): sets ignore-scripts on ci</li>
<li>ca1fe64a chore(npm): makes publishing staged only</li>
<li>d4dad0e9/ 1d1bc84a/ ca1fe64a build(npm): updates external dependencies</li>
</ul>
<h2>v17.4.1</h2>
<p>This release was created on github, but not published to npmjs</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/643462527f7a57ebf0ebc6277b4f47e4cf5180ab"><code>6434625</code></a> 17.4.2</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/17595296667bdf8fb0c352042621dd84dce7f4b2"><code>1759529</code></a> chore(ci): simplifies release flow again</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/56e501fd13e44fad8377997edf183f6930f6afa9"><code>56e501f</code></a> 17.4.1</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/ccef0fafbb4f7ef740f74477a97c2b7bc54606ca"><code>ccef0fa</code></a> chore(npm): sets ignore-scripts on ci</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/ca1fe64a4eef04e7a9177fd7c70ddf73ce0a903c"><code>ca1fe64</code></a> chore(npm): makes publishing staged only</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/b5b2c36b0bd0120f949ac1d0b7e74babeca3f8c5"><code>b5b2c36</code></a> build(npm): updates external dependencies</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/1d1bc84a22d1020c275b9e6408096bac1ac795bb"><code>1d1bc84</code></a> build(npm): updates external dependencies</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/ae0fcd40b90ecf03be2b471b7608c602d744fd58"><code>ae0fcd4</code></a> doc: corrects typos</li>
<li><a href="https://github.com/sverweij/dependency-cruiser/commit/d4dad0e951e90c76c0a164bb960a1aa4b7bca8db"><code>d4dad0e</code></a> build(npm): updates external dependencies</li>
<li>See full diff in <a href="https://github.com/sverweij/dependency-cruiser/compare/v17.4.0...v17.4.2">compare view</a></li>
</ul>
</details>
<br />

Updates `eslint-plugin-prettier` from 5.5.5 to 5.5.6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/prettier/eslint-plugin-prettier/releases">eslint-plugin-prettier's releases</a>.</em></p>
<blockquote>
<h2>v5.5.6</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/prettier/eslint-plugin-prettier/pull/791">#791</a> <a href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a> Thanks <a href="https://github.com/JounQin"><code>@​JounQin</code></a>! - chore: bump all (dev)Dependencies</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/prettier/eslint-plugin-prettier/blob/main/CHANGELOG.md">eslint-plugin-prettier's changelog</a>.</em></p>
<blockquote>
<h2>5.5.6</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/prettier/eslint-plugin-prettier/pull/791">#791</a> <a href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a> Thanks <a href="https://github.com/JounQin"><code>@​JounQin</code></a>! - chore: bump all (dev)Dependencies</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/4f33ea5a503c6cdbda93424ebd13188a46a1a890"><code>4f33ea5</code></a> chore: release eslint-plugin-prettier (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/792">#792</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/4745b54882a9011704764070a28aaaf0504efc92"><code>4745b54</code></a> ci: declare workflow-level contents: read on 2 workflows (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/790">#790</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/b5c96a30d3e292a379d6e8ac030c29fd7acbc90b"><code>b5c96a3</code></a> chore: bump all (dev)Dependencies (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/791">#791</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/e867680b2c1cf3748322c8c802690e7cfb78e233"><code>e867680</code></a> chore(deps): update all dependencies (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/766">#766</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/e8e2f7f1dcad747f1d43168ee09956b512956593"><code>e8e2f7f</code></a> chore: testing eslint v10 (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/779">#779</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/ca076d95aaf69aaf9c95abcc1692f8269197f248"><code>ca076d9</code></a> chore: update dev dependencies (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/780">#780</a>)</li>
<li><a href="https://github.com/prettier/eslint-plugin-prettier/commit/42e636951f8d53d169b1f8c2b7e7dfd792711113"><code>42e6369</code></a> build(deps): Bump the actions group with 2 updates (<a href="https://redirect.github.com/prettier/eslint-plugin-prettier/issues/778">#778</a>)</li>
<li><a h...

_Description has been truncated_

---

## 1920db6d — 2026-06-07T03:26:19Z
**Author:** dependabot[bot]
**PR:** #2235

### Commit Message
```
chore(deps-dev): bump globals from 16.4.0 to 17.6.0 in /web (#2235)

Bumps [globals](https://github.com/sindresorhus/globals) from 16.4.0 to
17.6.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/sindresorhus/globals/releases">globals's
releases</a>.</em></p>
<blockquote>
<h2>v17.6.0</h2>
<ul>
<li>Update globals (2026-05-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/343">#343</a>)
00a4dd9</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.5.0...v17.6.0">https://github.com/sindresorhus/globals/compare/v17.5.0...v17.6.0</a></p>
<h2>v17.5.0</h2>
<ul>
<li>Update globals (2026-04-12) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/342">#342</a>)
5d84602</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.4.0...v17.5.0">https://github.com/sindresorhus/globals/compare/v17.4.0...v17.5.0</a></p>
<h2>v17.4.0</h2>
<ul>
<li>Update globals (2026-03-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/338">#338</a>)
d43a051</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.3.0...v17.4.0">https://github.com/sindresorhus/globals/compare/v17.3.0...v17.4.0</a></p>
<h2>v17.3.0</h2>
<ul>
<li>Update globals (2026-02-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/336">#336</a>)
295fba9</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.2.0...v17.3.0">https://github.com/sindresorhus/globals/compare/v17.2.0...v17.3.0</a></p>
<h2>v17.2.0</h2>
<ul>
<li><code>jasmine</code>: Add <code>throwUnless</code> and
<code>throwUnlessAsync</code> globals (<a
href="https://redirect.github.com/sindresorhus/globals/issues/335">#335</a>)
97f23a7</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.1.0...v17.2.0">https://github.com/sindresorhus/globals/compare/v17.1.0...v17.2.0</a></p>
<h2>v17.1.0</h2>
<ul>
<li>Add <code>webpack</code> and <code>rspack</code> globals (<a
href="https://redirect.github.com/sindresorhus/globals/issues/333">#333</a>)
65cae73</li>
</ul>
<hr />
<p><a
href="https://github.com/sindresorhus/globals/compare/v17.0.0...v17.1.0">https://github.com/sindresorhus/globals/compare/v17.0.0...v17.1.0</a></p>
<h2>v17.0.0</h2>
<h3>Breaking</h3>
<ul>
<li>Split <code>audioWorklet</code> environment from
<code>browser</code> (<a
href="https://redirect.github.com/sindresorhus/globals/issues/320">#320</a>)
7bc293e</li>
</ul>
<h3>Improvements</h3>
<ul>
<li>Update globals (<a
href="https://redirect.github.com/sindresorhus/globals/issues/329">#329</a>)
ebe1063</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/sindresorhus/globals/commit/6b15870f1c08b60b5b57afe45a703d9ed0be39bc"><code>6b15870</code></a>
17.6.0</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/00a4dd9821830a9b044798120e86b1bb1a54648d"><code>00a4dd9</code></a>
Update globals (2026-05-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/343">#343</a>)</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/b8170c8e1d648291b613c5b39a69652c796fa36c"><code>b8170c8</code></a>
17.5.0</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/5d846029679832931f38ced6381cc95bcb9abd80"><code>5d84602</code></a>
Update globals (2026-04-12) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/342">#342</a>)</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/1b727e5f4cc39121b8e77b9f27574a8ca27391fc"><code>1b727e5</code></a>
Fix build script for ES globals (<a
href="https://redirect.github.com/sindresorhus/globals/issues/341">#341</a>)</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/a9cfd7493fb701474d4dc946283c7b9d63d64134"><code>a9cfd74</code></a>
17.4.0</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/d43a051c48fbb8c549bb98a7cf294ba84680a7a1"><code>d43a051</code></a>
Update globals (2026-03-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/338">#338</a>)</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/5edc6020698a76964b0fa17cb604f4484451143b"><code>5edc602</code></a>
17.3.0</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/295fba929adf8b44f945688233778a57ff754368"><code>295fba9</code></a>
Update globals (2026-02-01) (<a
href="https://redirect.github.com/sindresorhus/globals/issues/336">#336</a>)</li>
<li><a
href="https://github.com/sindresorhus/globals/commit/8176ac7290e6eb0be1403b80a4184651c4cd95f6"><code>8176ac7</code></a>
17.2.0</li>
<li>Additional commits viewable in <a
href="https://github.com/sindresorhus/globals/compare/v16.4.0...v17.6.0">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description
Bumps [globals](https://github.com/sindresorhus/globals) from 16.4.0 to 17.6.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/sindresorhus/globals/releases">globals's releases</a>.</em></p>
<blockquote>
<h2>v17.6.0</h2>
<ul>
<li>Update globals (2026-05-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/343">#343</a>)  00a4dd9</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.5.0...v17.6.0">https://github.com/sindresorhus/globals/compare/v17.5.0...v17.6.0</a></p>
<h2>v17.5.0</h2>
<ul>
<li>Update globals (2026-04-12) (<a href="https://redirect.github.com/sindresorhus/globals/issues/342">#342</a>)  5d84602</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.4.0...v17.5.0">https://github.com/sindresorhus/globals/compare/v17.4.0...v17.5.0</a></p>
<h2>v17.4.0</h2>
<ul>
<li>Update globals (2026-03-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/338">#338</a>)  d43a051</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.3.0...v17.4.0">https://github.com/sindresorhus/globals/compare/v17.3.0...v17.4.0</a></p>
<h2>v17.3.0</h2>
<ul>
<li>Update globals (2026-02-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/336">#336</a>)  295fba9</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.2.0...v17.3.0">https://github.com/sindresorhus/globals/compare/v17.2.0...v17.3.0</a></p>
<h2>v17.2.0</h2>
<ul>
<li><code>jasmine</code>: Add <code>throwUnless</code> and <code>throwUnlessAsync</code> globals (<a href="https://redirect.github.com/sindresorhus/globals/issues/335">#335</a>)  97f23a7</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.1.0...v17.2.0">https://github.com/sindresorhus/globals/compare/v17.1.0...v17.2.0</a></p>
<h2>v17.1.0</h2>
<ul>
<li>Add <code>webpack</code> and <code>rspack</code> globals (<a href="https://redirect.github.com/sindresorhus/globals/issues/333">#333</a>)  65cae73</li>
</ul>
<hr />
<p><a href="https://github.com/sindresorhus/globals/compare/v17.0.0...v17.1.0">https://github.com/sindresorhus/globals/compare/v17.0.0...v17.1.0</a></p>
<h2>v17.0.0</h2>
<h3>Breaking</h3>
<ul>
<li>Split <code>audioWorklet</code> environment from <code>browser</code> (<a href="https://redirect.github.com/sindresorhus/globals/issues/320">#320</a>)  7bc293e</li>
</ul>
<h3>Improvements</h3>
<ul>
<li>Update globals (<a href="https://redirect.github.com/sindresorhus/globals/issues/329">#329</a>)  ebe1063</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/sindresorhus/globals/commit/6b15870f1c08b60b5b57afe45a703d9ed0be39bc"><code>6b15870</code></a> 17.6.0</li>
<li><a href="https://github.com/sindresorhus/globals/commit/00a4dd9821830a9b044798120e86b1bb1a54648d"><code>00a4dd9</code></a> Update globals (2026-05-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/343">#343</a>)</li>
<li><a href="https://github.com/sindresorhus/globals/commit/b8170c8e1d648291b613c5b39a69652c796fa36c"><code>b8170c8</code></a> 17.5.0</li>
<li><a href="https://github.com/sindresorhus/globals/commit/5d846029679832931f38ced6381cc95bcb9abd80"><code>5d84602</code></a> Update globals (2026-04-12) (<a href="https://redirect.github.com/sindresorhus/globals/issues/342">#342</a>)</li>
<li><a href="https://github.com/sindresorhus/globals/commit/1b727e5f4cc39121b8e77b9f27574a8ca27391fc"><code>1b727e5</code></a> Fix build script for ES globals (<a href="https://redirect.github.com/sindresorhus/globals/issues/341">#341</a>)</li>
<li><a href="https://github.com/sindresorhus/globals/commit/a9cfd7493fb701474d4dc946283c7b9d63d64134"><code>a9cfd74</code></a> 17.4.0</li>
<li><a href="https://github.com/sindresorhus/globals/commit/d43a051c48fbb8c549bb98a7cf294ba84680a7a1"><code>d43a051</code></a> Update globals (2026-03-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/338">#338</a>)</li>
<li><a href="https://github.com/sindresorhus/globals/commit/5edc6020698a76964b0fa17cb604f4484451143b"><code>5edc602</code></a> 17.3.0</li>
<li><a href="https://github.com/sindresorhus/globals/commit/295fba929adf8b44f945688233778a57ff754368"><code>295fba9</code></a> Update globals (2026-02-01) (<a href="https://redirect.github.com/sindresorhus/globals/issues/336">#336</a>)</li>
<li><a href="https://github.com/sindresorhus/globals/commit/8176ac7290e6eb0be1403b80a4184651c4cd95f6"><code>8176ac7</code></a> 17.2.0</li>
<li>Additional commits viewable in <a href="https://github.com/sindresorhus/globals/compare/v16.4.0...v17.6.0">compare view</a></li>
</ul>
</details>
<br />


---

## 021e752c — 2026-06-07T03:17:36Z
**Author:** dependabot[bot]
**PR:** #2233

### Commit Message
```
chore(deps-dev): update ruff requirement from >=0.15.14 to >=0.15.15 in /services/claw-interface (#2233)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.15</h2>
<h2>Release Notes</h2>
<p>Released on 2026-05-28.</p>
<h3>Preview features</h3>
<ul>
<li>Fix Markdown closing fence handling (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25310">#25310</a>)</li>
<li>[<code>pyflakes</code>] Report duplicate imports in
<code>typing.TYPE_CHECKING</code> block (<code>F811</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22560">#22560</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>pyflakes</code>] Treat function-scope bare annotations as
locals per PEP 526 (<code>F821</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/21540">#21540</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant <code>TokenValue</code> drops in the lexer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25300">#25300</a>)</li>
<li>Reduce memory usage by dropping token-excess capacity and improve
performance by approximating the initial tokens <code>Vec</code> size
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/25354">#25354</a>)</li>
<li>Use <code>ThinVec</code> in AST to shrink <code>Stmt</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25361">#25361</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> example for <code>--config</code>
option (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25389">#25389</a>)</li>
<li>[<code>flake8-comprehensions</code>] Document
<code>RecursionError</code> edge case in <code>__len__</code>
(<code>C416</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25286">#25286</a>)</li>
<li>[<code>mccabe</code>] Improve example (<code>C901</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25287">#25287</a>)</li>
<li>[<code>pyupgrade</code>] Clarify fix safety docs
(<code>UP007</code>, <code>UP045</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25288">#25288</a>)</li>
<li>[<code>refurb</code>] Document <code>FURB192</code> exception change
for empty sequences (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25317">#25317</a>)</li>
<li>[<code>ruff</code>] Document false negative for user-defined types
(<code>RUF013</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25289">#25289</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Fix formatting of lambdas nested within f-strings (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25398">#25398</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Return code action for <code>codeAction/resolve</code> requests that
contain no or no valid URL (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25365">#25365</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Expand semantic syntax errors for invalid walruses (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25415">#25415</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a
href="https://github.com/fallintoplace"><code>@​fallintoplace</code></a></li>
<li><a
href="https://github.com/martin-schlossarek"><code>@​martin-schlossarek</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.15.15</h2>
<p>Released on 2026-05-28.</p>
<h3>Preview features</h3>
<ul>
<li>Fix Markdown closing fence handling (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25310">#25310</a>)</li>
<li>[<code>pyflakes</code>] Report duplicate imports in
<code>typing.TYPE_CHECKING</code> block (<code>F811</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22560">#22560</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>pyflakes</code>] Treat function-scope bare annotations as
locals per PEP 526 (<code>F821</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/21540">#21540</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant <code>TokenValue</code> drops in the lexer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25300">#25300</a>)</li>
<li>Reduce memory usage by dropping token-excess capacity and improve
performance by approximating the initial tokens <code>Vec</code> size
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/25354">#25354</a>)</li>
<li>Use <code>ThinVec</code> in AST to shrink <code>Stmt</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25361">#25361</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> example for <code>--config</code>
option (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25389">#25389</a>)</li>
<li>[<code>flake8-comprehensions</code>] Document
<code>RecursionError</code> edge case in <code>__len__</code>
(<code>C416</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25286">#25286</a>)</li>
<li>[<code>mccabe</code>] Improve example (<code>C901</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25287">#25287</a>)</li>
<li>[<code>pyupgrade</code>] Clarify fix safety docs
(<code>UP007</code>, <code>UP045</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25288">#25288</a>)</li>
<li>[<code>refurb</code>] Document <code>FURB192</code> exception change
for empty sequences (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25317">#25317</a>)</li>
<li>[<code>ruff</code>] Document false negative for user-defined types
(<code>RUF013</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25289">#25289</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Fix formatting of lambdas nested within f-strings (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25398">#25398</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Return code action for <code>codeAction/resolve</code> requests that
contain no or no valid URL (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25365">#25365</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Expand semantic syntax errors for invalid walruses (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25415">#25415</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a
href="https://github.com/fallintoplace"><code>@​fallintoplace</code></a></li>
<li><a
href="https://github.com/martin-schlossarek"><code>@​martin-schlossarek</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a
href="https://github.com/Ruchir28"><code>@​Ruchir28</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/db5aa0a5f1b92cb91d910bf0866a967554dd94f5"><code>db5aa0a</code></a>
Bump 0.15.15 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25431">#25431</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/366fe21ba369ccdd01eb99c1043c9a969c99230b"><code>366fe21</code></a>
[ty] Improve diagnostics for syntax errors in forward annotations (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25158">#25158</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/e2e1e647d182b8567845039c9a65fb0608a4dcfc"><code>e2e1e64</code></a>
[ty] Remove excess capacity from more Salsa cached collections (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25411">#25411</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/1bd77e1646f2213d86b8da215f08279187867d72"><code>1bd77e1</code></a>
[ty] Use diagnostic message as tie breaker when sorting (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25424">#25424</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/7e1bc1e75f15795f12c846294b13df4535f2abbf"><code>7e1bc1e</code></a>
Add agent skills for working on ty (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25422">#25422</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/574e10752f8cfa9e0cdbe3b01e96c4380950469b"><code>574e107</code></a>
Expand semantic syntax errors for invalid walruses (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25415">#25415</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/4a7ca062fccd80443a43aa61e5dc7e5858e88dc1"><code>4a7ca06</code></a>
[ty] Display docs for matching parameter when hovering over the name of
an ar...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/54327092dbfe455040690d63bb1e5e4b5f551239"><code>5432709</code></a>
Refine a few agents instructions (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25423">#25423</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/3cb09eba689ebb49e799131092121928cc789c18"><code>3cb09eb</code></a>
[ty] Support <code>typing.TypeForm</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25334">#25334</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c8cd59f189f2b6f55d542b29bddb953622add6fc"><code>c8cd59f</code></a>
[ty] Infer class attributes assigned by metaclass initialization (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25342">#25342</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.14...0.15.15">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description
Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.15</h2>
<h2>Release Notes</h2>
<p>Released on 2026-05-28.</p>
<h3>Preview features</h3>
<ul>
<li>Fix Markdown closing fence handling (<a href="https://redirect.github.com/astral-sh/ruff/pull/25310">#25310</a>)</li>
<li>[<code>pyflakes</code>] Report duplicate imports in <code>typing.TYPE_CHECKING</code> block (<code>F811</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/22560">#22560</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>pyflakes</code>] Treat function-scope bare annotations as locals per PEP 526 (<code>F821</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/21540">#21540</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant <code>TokenValue</code> drops in the lexer (<a href="https://redirect.github.com/astral-sh/ruff/pull/25300">#25300</a>)</li>
<li>Reduce memory usage by dropping token-excess capacity and improve performance by approximating the initial tokens <code>Vec</code> size (<a href="https://redirect.github.com/astral-sh/ruff/pull/25354">#25354</a>)</li>
<li>Use <code>ThinVec</code> in AST to shrink <code>Stmt</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/25361">#25361</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> example for <code>--config</code> option (<a href="https://redirect.github.com/astral-sh/ruff/pull/25389">#25389</a>)</li>
<li>[<code>flake8-comprehensions</code>] Document <code>RecursionError</code> edge case in <code>__len__</code> (<code>C416</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25286">#25286</a>)</li>
<li>[<code>mccabe</code>] Improve example (<code>C901</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25287">#25287</a>)</li>
<li>[<code>pyupgrade</code>] Clarify fix safety docs (<code>UP007</code>, <code>UP045</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25288">#25288</a>)</li>
<li>[<code>refurb</code>] Document <code>FURB192</code> exception change for empty sequences (<a href="https://redirect.github.com/astral-sh/ruff/pull/25317">#25317</a>)</li>
<li>[<code>ruff</code>] Document false negative for user-defined types (<code>RUF013</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25289">#25289</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Fix formatting of lambdas nested within f-strings (<a href="https://redirect.github.com/astral-sh/ruff/pull/25398">#25398</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Return code action for <code>codeAction/resolve</code> requests that contain no or no valid URL (<a href="https://redirect.github.com/astral-sh/ruff/pull/25365">#25365</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Expand semantic syntax errors for invalid walruses (<a href="https://redirect.github.com/astral-sh/ruff/pull/25415">#25415</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/fallintoplace"><code>@​fallintoplace</code></a></li>
<li><a href="https://github.com/martin-schlossarek"><code>@​martin-schlossarek</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.15</h2>
<p>Released on 2026-05-28.</p>
<h3>Preview features</h3>
<ul>
<li>Fix Markdown closing fence handling (<a href="https://redirect.github.com/astral-sh/ruff/pull/25310">#25310</a>)</li>
<li>[<code>pyflakes</code>] Report duplicate imports in <code>typing.TYPE_CHECKING</code> block (<code>F811</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/22560">#22560</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>pyflakes</code>] Treat function-scope bare annotations as locals per PEP 526 (<code>F821</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/21540">#21540</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant <code>TokenValue</code> drops in the lexer (<a href="https://redirect.github.com/astral-sh/ruff/pull/25300">#25300</a>)</li>
<li>Reduce memory usage by dropping token-excess capacity and improve performance by approximating the initial tokens <code>Vec</code> size (<a href="https://redirect.github.com/astral-sh/ruff/pull/25354">#25354</a>)</li>
<li>Use <code>ThinVec</code> in AST to shrink <code>Stmt</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/25361">#25361</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> example for <code>--config</code> option (<a href="https://redirect.github.com/astral-sh/ruff/pull/25389">#25389</a>)</li>
<li>[<code>flake8-comprehensions</code>] Document <code>RecursionError</code> edge case in <code>__len__</code> (<code>C416</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25286">#25286</a>)</li>
<li>[<code>mccabe</code>] Improve example (<code>C901</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25287">#25287</a>)</li>
<li>[<code>pyupgrade</code>] Clarify fix safety docs (<code>UP007</code>, <code>UP045</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25288">#25288</a>)</li>
<li>[<code>refurb</code>] Document <code>FURB192</code> exception change for empty sequences (<a href="https://redirect.github.com/astral-sh/ruff/pull/25317">#25317</a>)</li>
<li>[<code>ruff</code>] Document false negative for user-defined types (<code>RUF013</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25289">#25289</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Fix formatting of lambdas nested within f-strings (<a href="https://redirect.github.com/astral-sh/ruff/pull/25398">#25398</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Return code action for <code>codeAction/resolve</code> requests that contain no or no valid URL (<a href="https://redirect.github.com/astral-sh/ruff/pull/25365">#25365</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Expand semantic syntax errors for invalid walruses (<a href="https://redirect.github.com/astral-sh/ruff/pull/25415">#25415</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/fallintoplace"><code>@​fallintoplace</code></a></li>
<li><a href="https://github.com/martin-schlossarek"><code>@​martin-schlossarek</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/Ruchir28"><code>@​Ruchir28</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/db5aa0a5f1b92cb91d910bf0866a967554dd94f5"><code>db5aa0a</code></a> Bump 0.15.15 (<a href="https://redirect.github.com/astral-sh/ruff/issues/25431">#25431</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/366fe21ba369ccdd01eb99c1043c9a969c99230b"><code>366fe21</code></a> [ty] Improve diagnostics for syntax errors in forward annotations (<a href="https://redirect.github.com/astral-sh/ruff/issues/25158">#25158</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/e2e1e647d182b8567845039c9a65fb0608a4dcfc"><code>e2e1e64</code></a> [ty] Remove excess capacity from more Salsa cached collections (<a href="https://redirect.github.com/astral-sh/ruff/issues/25411">#25411</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/1bd77e1646f2213d86b8da215f08279187867d72"><code>1bd77e1</code></a> [ty] Use diagnostic message as tie breaker when sorting (<a href="https://redirect.github.com/astral-sh/ruff/issues/25424">#25424</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/7e1bc1e75f15795f12c846294b13df4535f2abbf"><code>7e1bc1e</code></a> Add agent skills for working on ty (<a href="https://redirect.github.com/astral-sh/ruff/issues/25422">#25422</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/574e10752f8cfa9e0cdbe3b01e96c4380950469b"><code>574e107</code></a> Expand semantic syntax errors for invalid walruses (<a href="https://redirect.github.com/astral-sh/ruff/issues/25415">#25415</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/4a7ca062fccd80443a43aa61e5dc7e5858e88dc1"><code>4a7ca06</code></a> [ty] Display docs for matching parameter when hovering over the name of an ar...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/54327092dbfe455040690d63bb1e5e4b5f551239"><code>5432709</code></a> Refine a few agents instructions (<a href="https://redirect.github.com/astral-sh/ruff/issues/25423">#25423</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/3cb09eba689ebb49e799131092121928cc789c18"><code>3cb09eb</code></a> [ty] Support <code>typing.TypeForm</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/25334">#25334</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c8cd59f189f2b6f55d542b29bddb953622add6fc"><code>c8cd59f</code></a> [ty] Infer class attributes assigned by metaclass initialization (<a href="https://redirect.github.com/astral-sh/ruff/issues/25342">#25342</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.14...0.15.15">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## 743f63da — 2026-06-07T03:10:36Z
**Author:** dependabot[bot]
**PR:** #2236

### Commit Message
```
chore(deps-dev): bump vite from 7.3.3 to 8.0.14 in /web (#2236)

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite)
from 7.3.3 to 8.0.14.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/vitejs/vite/releases">vite's
releases</a>.</em></p>
<blockquote>
<h2>v8.0.14</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.14/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.13</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.13/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.12</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.12/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.11</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.11/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.10</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.10/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.9</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.9/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.8</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.8/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.7</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.7/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.6</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.6/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.5</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.5/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.4</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.4/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>create-vite@8.0.3</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/create-vite@8.0.3/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.3</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.3/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>create-vite@8.0.2</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/create-vite@8.0.2/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>v8.0.2</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/v8.0.2/packages/vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>plugin-legacy@8.0.2</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/plugin-legacy@8.0.2/packages/plugin-legacy/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<h2>create-vite@8.0.1</h2>
<p>Please refer to <a
href="https://github.com/vitejs/vite/blob/create-vite@8.0.1/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a>
for details.</p>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/vitejs/vite/blob/main/packages/vite/CHANGELOG.md">vite's
changelog</a>.</em></p>
<blockquote>
<h2><!-- raw HTML omitted --><a
href="https://github.com/vitejs/vite/compare/v8.0.13...v8.0.14">8.0.14</a>
(2026-05-21)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li>update rolldown to 1.0.2 (<a
href="https://redirect.github.com/vitejs/vite/issues/22484">#22484</a>)
(<a
href="https://github.com/vitejs/vite/commit/96efc88570b6a6ddf1a910f106920cbac07b3cf0">96efc88</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update all non-major dependencies (<a
href="https://redirect.github.com/vitejs/vite/issues/22471">#22471</a>)
(<a
href="https://github.com/vitejs/vite/commit/98b81632139d51820f82036e58d6fbbf122b77b3">98b8163</a>)</li>
<li><strong>dev:</strong> handle errors when sending messages to vite
server (<a
href="https://redirect.github.com/vitejs/vite/issues/22450">#22450</a>)
(<a
href="https://github.com/vitejs/vite/commit/e8e9a34dcf2540139de558a10187630884d10217">e8e9a34</a>)</li>
<li><strong>html:</strong> handle trailing slash paths in
transformIndexHtml (<a
href="https://redirect.github.com/vitejs/vite/issues/22480">#22480</a>)
(<a
href="https://github.com/vitejs/vite/commit/5d94d1bffdb2a15de9341194d89baec86ce1f693">5d94d1b</a>)</li>
<li><strong>optimizer:</strong> pass oxc jsx options to transformSync in
dependency scan (<a
href="https://redirect.github.com/vitejs/vite/issues/22342">#22342</a>)
(<a
href="https://github.com/vitejs/vite/commit/b3132dacea9c6e0cf526cd9f0f09d850f577c262">b3132da</a>)</li>
</ul>
<h3>Miscellaneous Chores</h3>
<ul>
<li><strong>deps:</strong> update rolldown-related dependencies (<a
href="https://redirect.github.com/vitejs/vite/issues/22470">#22470</a>)
(<a
href="https://github.com/vitejs/vite/commit/7cb728eb629cc677661f1bc52a044ffc0b87fc7f">7cb728e</a>)</li>
<li>remove irrelevant commits from changelog (<a
href="https://github.com/vitejs/vite/commit/2c69495f250edf01132d4a20128de19dbe836086">2c69495</a>)</li>
</ul>
<h3>Code Refactoring</h3>
<ul>
<li><strong>glob:</strong> do not rewrite import path for absolute base
(<a
href="https://redirect.github.com/vitejs/vite/issues/22310">#22310</a>)
(<a
href="https://github.com/vitejs/vite/commit/0ae2844ab6d6d1ccf78a2975b8132769fc35b302">0ae2844</a>)</li>
</ul>
<h3>Tests</h3>
<ul>
<li><strong>css:</strong> sass does not use main field (<a
href="https://redirect.github.com/vitejs/vite/issues/22449">#22449</a>)
(<a
href="https://github.com/vitejs/vite/commit/ebf39a04329ddc6ba765e006a5d463680a952270">ebf39a0</a>)</li>
</ul>
<h2><!-- raw HTML omitted --><a
href="https://github.com/vitejs/vite/compare/v8.0.12...v8.0.13">8.0.13</a>
(2026-05-14)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li><strong>bundled-dev:</strong> add lazy bundling support (<a
href="https://redirect.github.com/vitejs/vite/issues/21406">#21406</a>)
(<a
href="https://github.com/vitejs/vite/commit/4f0949f3f13e4b2b34d32bf7b2b4de5f26bea192">4f0949f</a>)</li>
<li><strong>optimizer:</strong> improve the esbuild plugin converter to
pass some properties of build result to <code>onEnd</code> (<a
href="https://redirect.github.com/vitejs/vite/issues/22357">#22357</a>)
(<a
href="https://github.com/vitejs/vite/commit/47071ce53f21726cf39e999c4407c4828ecbe957">47071ce</a>)</li>
<li>update rolldown to 1.0.1 (<a
href="https://redirect.github.com/vitejs/vite/issues/22444">#22444</a>)
(<a
href="https://github.com/vitejs/vite/commit/8c766a6c5ee014969c4e32f29cc265e8e2c96e18">8c766a6</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>build:</strong> copy public directory after building same
environment with <code>write=false</code> (<a
href="https://redirect.github.com/vitejs/vite/issues/22328">#22328</a>)
(<a
href="https://github.com/vitejs/vite/commit/158e8ae8efdf7075ab295727e36b5ff68da3243e">158e8ae</a>)</li>
<li><strong>css:</strong> await sass/less/styl worker disposal on
teardown (fix <a
href="https://redirect.github.com/vitejs/vite/issues/22274">#22274</a>)
(<a
href="https://redirect.github.com/vitejs/vite/issues/22275">#22275</a>)
(<a
href="https://github.com/vitejs/vite/commit/b7edcb7d0dd17ddfeef4ace78d610c099216dade">b7edcb7</a>)</li>
<li><strong>css:</strong> keep deprecated
<code>name</code>/<code>originalFileName</code> in synthetic
<code>assetFileNames</code> call (<a
href="https://redirect.github.com/vitejs/vite/issues/22439">#22439</a>)
(<a
href="https://github.com/vitejs/vite/commit/8e59c97a44d923c4c06f67287a793c9aa5a4ebaa">8e59c97</a>)</li>
<li>make <code>isBundled</code> per environment (<a
href="https://redirect.github.com/vitejs/vite/issues/22257">#22257</a>)
(<a
href="https://github.com/vitejs/vite/commit/a5763266170f8606836da5c6f987b4b2fd6ddc55">a576326</a>)</li>
<li><strong>ssr:</strong> avoid rewriting labels that collide with
imports (<a
href="https://redirect.github.com/vitejs/vite/issues/22451">#22451</a>)
(<a
href="https://github.com/vitejs/vite/commit/d9b18e0387a253628d3d834288e79c5f7e85d566">d9b18e0</a>)</li>
</ul>
<h3>Miscellaneous Chores</h3>
<ul>
<li>remove irrelevant commits from changelog (<a
href="https://redirect.github.com/vitejs/vite/issues/22430">#22430</a>)
(<a
href="https://github.com/vitejs/vite/commit/6ea383859aaf0ef8e673b458f164e84aeb6ff51d">6ea3838</a>)</li>
<li>update changelog (<a
href="https://redirect.github.com/vitejs/vite/issues/22413">#22413</a>)
(<a
href="https://github.com/vitejs/vite/commit/fcdc87cc6799857e2bab0f44f333a681694fff74">fcdc87c</a>)</li>
</ul>
<h2><!-- raw HTML omitted --><a
href="https://github.com/vitejs/vite/compare/v8.0.11...v8.0.12">8.0.12</a>
(2026-05-11)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li>update rolldown to 1.0.0 (<a
href="https://redirect.github.com/vitejs/vite/issues/22401">#22401</a>)
(<a
href="https://github.com/vitejs/vite/commit/cf0ff4154b26cffbf18541ade1a50818842731d3">cf0ff41</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/vitejs/vite/commit/c917f1ef9d9c6ef131af96d89089d8ec680b18f2"><code>c917f1e</code></a>
release: v8.0.14</li>
<li><a
href="https://github.com/vitejs/vite/commit/5d94d1bffdb2a15de9341194d89baec86ce1f693"><code>5d94d1b</code></a>
fix(html): handle trailing slash paths in transformIndexHtml (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22480">#22480</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/98b81632139d51820f82036e58d6fbbf122b77b3"><code>98b8163</code></a>
fix(deps): update all non-major dependencies (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22471">#22471</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/96efc88570b6a6ddf1a910f106920cbac07b3cf0"><code>96efc88</code></a>
feat: update rolldown to 1.0.2 (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22484">#22484</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/ebf39a04329ddc6ba765e006a5d463680a952270"><code>ebf39a0</code></a>
test(css): sass does not use main field (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22449">#22449</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/0ae2844ab6d6d1ccf78a2975b8132769fc35b302"><code>0ae2844</code></a>
refactor(glob): do not rewrite import path for absolute base (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22310">#22310</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/7cb728eb629cc677661f1bc52a044ffc0b87fc7f"><code>7cb728e</code></a>
chore(deps): update rolldown-related dependencies (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22470">#22470</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/b3132dacea9c6e0cf526cd9f0f09d850f577c262"><code>b3132da</code></a>
fix(optimizer): pass oxc jsx options to transformSync in dependency scan
...</li>
<li><a
href="https://github.com/vitejs/vite/commit/e8e9a34dcf2540139de558a10187630884d10217"><code>e8e9a34</code></a>
fix(dev): handle errors when sending messages to vite server (<a
href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22450">#22450</a>)</li>
<li><a
href="https://github.com/vitejs/vite/commit/2c69495f250edf01132d4a20128de19dbe836086"><code>2c69495</code></a>
chore: remove irrelevant commits from changelog</li>
<li>Additional commits viewable in <a
href="https://github.com/vitejs/vite/commits/v8.0.14/packages/vite">compare
view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite&package-manager=npm_and_yarn&previous-version=7.3.3&new-version=8.0.14)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description
Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 7.3.3 to 8.0.14.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite/releases">vite's releases</a>.</em></p>
<blockquote>
<h2>v8.0.14</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.14/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.13</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.13/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.12</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.12/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.11</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.11/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.10</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.10/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.9</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.9/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.8</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.8/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.7</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.7/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.6</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.6/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.5</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.5/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.4</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.4/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>create-vite@8.0.3</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/create-vite@8.0.3/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.3</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.3/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>create-vite@8.0.2</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/create-vite@8.0.2/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v8.0.2</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v8.0.2/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>plugin-legacy@8.0.2</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/plugin-legacy@8.0.2/packages/plugin-legacy/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>create-vite@8.0.1</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/create-vite@8.0.1/packages/create-vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite/blob/main/packages/vite/CHANGELOG.md">vite's changelog</a>.</em></p>
<blockquote>
<h2><!-- raw HTML omitted --><a href="https://github.com/vitejs/vite/compare/v8.0.13...v8.0.14">8.0.14</a> (2026-05-21)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li>update rolldown to 1.0.2 (<a href="https://redirect.github.com/vitejs/vite/issues/22484">#22484</a>) (<a href="https://github.com/vitejs/vite/commit/96efc88570b6a6ddf1a910f106920cbac07b3cf0">96efc88</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update all non-major dependencies (<a href="https://redirect.github.com/vitejs/vite/issues/22471">#22471</a>) (<a href="https://github.com/vitejs/vite/commit/98b81632139d51820f82036e58d6fbbf122b77b3">98b8163</a>)</li>
<li><strong>dev:</strong> handle errors when sending messages to vite server (<a href="https://redirect.github.com/vitejs/vite/issues/22450">#22450</a>) (<a href="https://github.com/vitejs/vite/commit/e8e9a34dcf2540139de558a10187630884d10217">e8e9a34</a>)</li>
<li><strong>html:</strong> handle trailing slash paths in transformIndexHtml (<a href="https://redirect.github.com/vitejs/vite/issues/22480">#22480</a>) (<a href="https://github.com/vitejs/vite/commit/5d94d1bffdb2a15de9341194d89baec86ce1f693">5d94d1b</a>)</li>
<li><strong>optimizer:</strong> pass oxc jsx options to transformSync in dependency scan                                                            (<a href="https://redirect.github.com/vitejs/vite/issues/22342">#22342</a>) (<a href="https://github.com/vitejs/vite/commit/b3132dacea9c6e0cf526cd9f0f09d850f577c262">b3132da</a>)</li>
</ul>
<h3>Miscellaneous Chores</h3>
<ul>
<li><strong>deps:</strong> update rolldown-related dependencies (<a href="https://redirect.github.com/vitejs/vite/issues/22470">#22470</a>) (<a href="https://github.com/vitejs/vite/commit/7cb728eb629cc677661f1bc52a044ffc0b87fc7f">7cb728e</a>)</li>
<li>remove irrelevant commits from changelog (<a href="https://github.com/vitejs/vite/commit/2c69495f250edf01132d4a20128de19dbe836086">2c69495</a>)</li>
</ul>
<h3>Code Refactoring</h3>
<ul>
<li><strong>glob:</strong> do not rewrite import path for absolute base (<a href="https://redirect.github.com/vitejs/vite/issues/22310">#22310</a>) (<a href="https://github.com/vitejs/vite/commit/0ae2844ab6d6d1ccf78a2975b8132769fc35b302">0ae2844</a>)</li>
</ul>
<h3>Tests</h3>
<ul>
<li><strong>css:</strong> sass does not use main field (<a href="https://redirect.github.com/vitejs/vite/issues/22449">#22449</a>) (<a href="https://github.com/vitejs/vite/commit/ebf39a04329ddc6ba765e006a5d463680a952270">ebf39a0</a>)</li>
</ul>
<h2><!-- raw HTML omitted --><a href="https://github.com/vitejs/vite/compare/v8.0.12...v8.0.13">8.0.13</a> (2026-05-14)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li><strong>bundled-dev:</strong> add lazy bundling support (<a href="https://redirect.github.com/vitejs/vite/issues/21406">#21406</a>) (<a href="https://github.com/vitejs/vite/commit/4f0949f3f13e4b2b34d32bf7b2b4de5f26bea192">4f0949f</a>)</li>
<li><strong>optimizer:</strong> improve the esbuild plugin converter to pass some properties of build result to <code>onEnd</code> (<a href="https://redirect.github.com/vitejs/vite/issues/22357">#22357</a>) (<a href="https://github.com/vitejs/vite/commit/47071ce53f21726cf39e999c4407c4828ecbe957">47071ce</a>)</li>
<li>update rolldown to 1.0.1 (<a href="https://redirect.github.com/vitejs/vite/issues/22444">#22444</a>) (<a href="https://github.com/vitejs/vite/commit/8c766a6c5ee014969c4e32f29cc265e8e2c96e18">8c766a6</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>build:</strong> copy public directory after building same environment with <code>write=false</code> (<a href="https://redirect.github.com/vitejs/vite/issues/22328">#22328</a>) (<a href="https://github.com/vitejs/vite/commit/158e8ae8efdf7075ab295727e36b5ff68da3243e">158e8ae</a>)</li>
<li><strong>css:</strong> await sass/less/styl worker disposal on teardown (fix <a href="https://redirect.github.com/vitejs/vite/issues/22274">#22274</a>) (<a href="https://redirect.github.com/vitejs/vite/issues/22275">#22275</a>) (<a href="https://github.com/vitejs/vite/commit/b7edcb7d0dd17ddfeef4ace78d610c099216dade">b7edcb7</a>)</li>
<li><strong>css:</strong> keep deprecated <code>name</code>/<code>originalFileName</code> in synthetic <code>assetFileNames</code> call (<a href="https://redirect.github.com/vitejs/vite/issues/22439">#22439</a>) (<a href="https://github.com/vitejs/vite/commit/8e59c97a44d923c4c06f67287a793c9aa5a4ebaa">8e59c97</a>)</li>
<li>make <code>isBundled</code> per environment (<a href="https://redirect.github.com/vitejs/vite/issues/22257">#22257</a>) (<a href="https://github.com/vitejs/vite/commit/a5763266170f8606836da5c6f987b4b2fd6ddc55">a576326</a>)</li>
<li><strong>ssr:</strong> avoid rewriting labels that collide with imports (<a href="https://redirect.github.com/vitejs/vite/issues/22451">#22451</a>) (<a href="https://github.com/vitejs/vite/commit/d9b18e0387a253628d3d834288e79c5f7e85d566">d9b18e0</a>)</li>
</ul>
<h3>Miscellaneous Chores</h3>
<ul>
<li>remove irrelevant commits from changelog (<a href="https://redirect.github.com/vitejs/vite/issues/22430">#22430</a>) (<a href="https://github.com/vitejs/vite/commit/6ea383859aaf0ef8e673b458f164e84aeb6ff51d">6ea3838</a>)</li>
<li>update changelog (<a href="https://redirect.github.com/vitejs/vite/issues/22413">#22413</a>) (<a href="https://github.com/vitejs/vite/commit/fcdc87cc6799857e2bab0f44f333a681694fff74">fcdc87c</a>)</li>
</ul>
<h2><!-- raw HTML omitted --><a href="https://github.com/vitejs/vite/compare/v8.0.11...v8.0.12">8.0.12</a> (2026-05-11)<!-- raw HTML omitted --></h2>
<h3>Features</h3>
<ul>
<li>update rolldown to 1.0.0 (<a href="https://redirect.github.com/vitejs/vite/issues/22401">#22401</a>) (<a href="https://github.com/vitejs/vite/commit/cf0ff4154b26cffbf18541ade1a50818842731d3">cf0ff41</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/vitejs/vite/commit/c917f1ef9d9c6ef131af96d89089d8ec680b18f2"><code>c917f1e</code></a> release: v8.0.14</li>
<li><a href="https://github.com/vitejs/vite/commit/5d94d1bffdb2a15de9341194d89baec86ce1f693"><code>5d94d1b</code></a> fix(html): handle trailing slash paths in transformIndexHtml (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22480">#22480</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/98b81632139d51820f82036e58d6fbbf122b77b3"><code>98b8163</code></a> fix(deps): update all non-major dependencies (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22471">#22471</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/96efc88570b6a6ddf1a910f106920cbac07b3cf0"><code>96efc88</code></a> feat: update rolldown to 1.0.2 (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22484">#22484</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/ebf39a04329ddc6ba765e006a5d463680a952270"><code>ebf39a0</code></a> test(css): sass does not use main field (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22449">#22449</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/0ae2844ab6d6d1ccf78a2975b8132769fc35b302"><code>0ae2844</code></a> refactor(glob): do not rewrite import path for absolute base (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22310">#22310</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/7cb728eb629cc677661f1bc52a044ffc0b87fc7f"><code>7cb728e</code></a> chore(deps): update rolldown-related dependencies (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22470">#22470</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/b3132dacea9c6e0cf526cd9f0f09d850f577c262"><code>b3132da</code></a> fix(optimizer): pass oxc jsx options to transformSync in dependency scan     ...</li>
<li><a href="https://github.com/vitejs/vite/commit/e8e9a34dcf2540139de558a10187630884d10217"><code>e8e9a34</code></a> fix(dev): handle errors when sending messages to vite server (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22450">#22450</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/2c69495f250edf01132d4a20128de19dbe836086"><code>2c69495</code></a> chore: remove irrelevant commits from changelog</li>
<li>Additional commits viewable in <a href="https://github.com/vitejs/vite/commits/v8.0.14/packages/vite">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite&package-manager=npm_and_yarn&previous-version=7.3.3&new-version=8.0.14)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## 5d002ed2 — 2026-06-07T03:00:59Z
**Author:** Chris@ZooClaw
**PR:** #2240

### Commit Message
```
ci: pin claude-code-action to v1.0.88 in arch-review (#2240)

## What

Pin `anthropics/claude-code-action` from the floating `@v1` tag to
`@v1.0.88` in `claude-arch-review.yaml`.

## Why

The floating `@v1` tag was retagged on 2026-06-06 (~23:43 UTC) to a
build whose bundled Claude Agent SDK fails to start and reports `API
Error: Unable to connect to API (ConnectionRefused)` against Bedrock
(`total_cost_usd: 0`, never makes a successful call).

This already broke the production Feishu release notification:
`srp-actions/.github/workflows/release-notify-lark.yml` uses the same
floating `@v1`, so the `ecap-v0.7.6-release` notify run failed at the
"Generate release notes (Claude Code / Bedrock)" step and the message
was never sent. Our `claude-review` / `claude-assistant` /
`claude-develop` workflows were unaffected because they already pin
`@v1.0.88` (released 2026-04-04).

This PR closes the same exposure in this repo's arch-review workflow.
The companion fix pins `release-notify-lark.yml` in `srp-actions`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description
## What

Pin `anthropics/claude-code-action` from the floating `@v1` tag to `@v1.0.88` in `claude-arch-review.yaml`.

## Why

The floating `@v1` tag was retagged on 2026-06-06 (~23:43 UTC) to a build whose bundled Claude Agent SDK fails to start and reports `API Error: Unable to connect to API (ConnectionRefused)` against Bedrock (`total_cost_usd: 0`, never makes a successful call).

This already broke the production Feishu release notification: `srp-actions/.github/workflows/release-notify-lark.yml` uses the same floating `@v1`, so the `ecap-v0.7.6-release` notify run failed at the "Generate release notes (Claude Code / Bedrock)" step and the message was never sent. Our `claude-review` / `claude-assistant` / `claude-develop` workflows were unaffected because they already pin `@v1.0.88` (released 2026-04-04).

This PR closes the same exposure in this repo's arch-review workflow. The companion fix pins `release-notify-lark.yml` in `srp-actions`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## a8de6fde — 2026-06-07T02:28:00Z
**Author:** Chris@ZooClaw
**PR:** #2237

### Commit Message
```
perf(web): provider tree refactor spec + phase 1 memoization (#2237)

## What

1. **Design spec** at
`docs/superpowers/specs/2026-06-06-provider-tree-refactor.md` analyzing
the 16-level nested provider pyramid in
`web/app/src/components/ClientLayout.tsx` and a staged refactor plan
toward cleaner architecture.
2. **Phase 1 implementation** — pure, behavior-preserving value
memoization to stop re-render cascades from providers high in the
pyramid.

## Investigation findings

1. **No opt-out** — the full pyramid is universal under `[locale]/` (no
nested layouts), so public pages (landing/pricing) boot chat-websocket +
billing infra they never use.
2. **Depth isn't the perf problem** — cascades come from unmemoized
context values high in the tree, not nesting depth.
3. **Route-scoping is partially blocked** by shared chrome, but the
codebase already has the escape hatch
(`useOpenClawOptional`/`useMattermostOptional` + `AppLayout.tsx:24`
landing gate).

## Phase 1 changes (this PR)

- `AppEnvironmentContext`: pass the already-stable `envState` directly
instead of re-bundling a fresh object literal every render.
- `Toast`: `useMemo` the `{ showToast }` value.
- `FeedbackProvider`: `useMemo` the value (was re-allocated on every
`HealthMonitor` tick → continuous cascade).
- `LoginCheckProvider`: `useCallback` the three handlers + `useMemo` the
value.
- `UserBusinessDataContext`: **intentionally unchanged** — `useQuery`
runs once in the provider (consumers only read context), so
`refetchOnMount: 'always'` fires once per app load, not per consumer; no
cascade, and changing it would alter data-freshness semantics. The
original HIGH rating was a misread; spec records this.

## Target architecture (later phases)

Route-group split `(marketing)` / `(app)` / `(chat)` / `(billing)`:
universal pyramid collapses 16 → ~4; remaining providers mount only
where consumed; state-only contexts → Zustand; overlays flatten into one
`<GlobalOverlays/>`.

## Remaining phases (not in this PR)

2. Extract `<GlobalOverlays/>` · 3. Route-group split · 4. Sink
chat/billing providers · 5. Context → Zustand.

## Verification

- `pnpm tsc` — no `src/` errors
- `pnpm lint` — clean on changed files
- `pnpm vitest run` — 461 files / 6818 tests green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description
## What

1. **Design spec** at `docs/superpowers/specs/2026-06-06-provider-tree-refactor.md` analyzing the 16-level nested provider pyramid in `web/app/src/components/ClientLayout.tsx` and a staged refactor plan toward cleaner architecture.
2. **Phase 1 implementation** — pure, behavior-preserving value memoization to stop re-render cascades from providers high in the pyramid.

## Investigation findings

1. **No opt-out** — the full pyramid is universal under `[locale]/` (no nested layouts), so public pages (landing/pricing) boot chat-websocket + billing infra they never use.
2. **Depth isn't the perf problem** — cascades come from unmemoized context values high in the tree, not nesting depth.
3. **Route-scoping is partially blocked** by shared chrome, but the codebase already has the escape hatch (`useOpenClawOptional`/`useMattermostOptional` + `AppLayout.tsx:24` landing gate).

## Phase 1 changes (this PR)

- `AppEnvironmentContext`: pass the already-stable `envState` directly instead of re-bundling a fresh object literal every render.
- `Toast`: `useMemo` the `{ showToast }` value.
- `FeedbackProvider`: `useMemo` the value (was re-allocated on every `HealthMonitor` tick → continuous cascade).
- `LoginCheckProvider`: `useCallback` the three handlers + `useMemo` the value.
- `UserBusinessDataContext`: **intentionally unchanged** — `useQuery` runs once in the provider (consumers only read context), so `refetchOnMount: 'always'` fires once per app load, not per consumer; no cascade, and changing it would alter data-freshness semantics. The original HIGH rating was a misread; spec records this.

## Target architecture (later phases)

Route-group split `(marketing)` / `(app)` / `(chat)` / `(billing)`: universal pyramid collapses 16 → ~4; remaining providers mount only where consumed; state-only contexts → Zustand; overlays flatten into one `<GlobalOverlays/>`.

## Remaining phases (not in this PR)

2. Extract `<GlobalOverlays/>` · 3. Route-group split · 4. Sink chat/billing providers · 5. Context → Zustand.

## Verification

- `pnpm tsc` — no `src/` errors
- `pnpm lint` — clean on changed files
- `pnpm vitest run` — 461 files / 6818 tests green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---