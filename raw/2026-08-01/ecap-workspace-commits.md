# SerendipityOneInc/ecap-workspace — commits 2026-08-01

## feat(web): consume V2 artifacts and workspace files (#3181)

- **SHA**: `8ee27ed3d686c211c85c8fbf28c277ea116557de`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-01T13:11:01Z
- **PR**: #3181

### Commit Message

```
feat(web): consume V2 artifacts and workspace files (#3181)

## What changed

- adds Artifact list/detail, preview and download UI using stable URLs;
- consumes additive structured refs when present but retains URL-only
rendering;
- keeps Files UI independent from Published Artifact snapshots.

## Why

Controlled ecap clients can use Artifact IDs for richer presentation,
but forwarded/V1/old-ACS messages still need the same preview and
download behavior from URLs alone.

## Validation

- frontend/backend targeted Artifact tests pass;
- the complete stack passes the Python validation recorded in #3180;
- URL-only and structured-ref cases are included in the staging canary
defined by SerendipityOneInc/zooclaw-dev#18.

This is PR 2/3 and is based on #3180.
```

### PR Body

## What changed

- adds Artifact list/detail, preview and download UI using stable URLs;
- consumes additive structured refs when present but retains URL-only rendering;
- keeps Files UI independent from Published Artifact snapshots.

## Why

Controlled ecap clients can use Artifact IDs for richer presentation, but forwarded/V1/old-ACS messages still need the same preview and download behavior from URLs alone.

## Validation

- frontend/backend targeted Artifact tests pass;
- the complete stack passes the Python validation recorded in #3180;
- URL-only and structured-ref cases are included in the staging canary defined by SerendipityOneInc/zooclaw-dev#18.

This is PR 2/3 and is based on #3180.


---

## chore(deps): update websockets requirement from >=16.1 to >=16.1.1 in /services/claw-interface (#3177)

- **SHA**: `a3b377cd171ec1e75b41a8a10c1974adc0441887`
- **作者**: dependabot[bot]
- **日期**: 2026-08-01T12:54:27Z
- **PR**: #3177

### Commit Message

```
chore(deps): update websockets requirement from >=16.1 to >=16.1.1 in /services/claw-interface (#3177)

Updates the requirements on
[websockets](https://github.com/python-websockets/websockets) to permit
the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/python-websockets/websockets/releases">websockets's
releases</a>.</em></p>
<blockquote>
<h2>16.1.1</h2>
<p>See <a
href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a>
for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/python-websockets/websockets/commit/01df1e4e4d482cc70dfcd4a13c7bac1e956d4b9a"><code>01df1e4</code></a>
Revert &quot;Decode non-ASCII header values with iso-8859-1.&quot;</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/2d61f74dcca4425b1d8563523e04d4ffaca24bbc"><code>2d61f74</code></a>
Clarify restriction on headers in 16.1.</li>
<li>See full diff in <a
href="https://github.com/python-websockets/websockets/compare/16.1...16.1.1">compare
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

### PR Body

Updates the requirements on [websockets](https://github.com/python-websockets/websockets) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/python-websockets/websockets/releases">websockets's releases</a>.</em></p>
<blockquote>
<h2>16.1.1</h2>
<p>See <a href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/python-websockets/websockets/commit/01df1e4e4d482cc70dfcd4a13c7bac1e956d4b9a"><code>01df1e4</code></a> Revert &quot;Decode non-ASCII header values with iso-8859-1.&quot;</li>
<li><a href="https://github.com/python-websockets/websockets/commit/2d61f74dcca4425b1d8563523e04d4ffaca24bbc"><code>2d61f74</code></a> Clarify restriction on headers in 16.1.</li>
<li>See full diff in <a href="https://github.com/python-websockets/websockets/compare/16.1...16.1.1">compare view</a></li>
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

## chore(deps): update cachetools requirement from >=7.1.4 to >=7.1.6 in /services/claw-interface (#3178)

- **SHA**: `85ec04b9307a90ef18c4f8c1863ddf0365c98844`
- **作者**: dependabot[bot]
- **日期**: 2026-08-01T12:54:15Z
- **PR**: #3178

### Commit Message

```
chore(deps): update cachetools requirement from >=7.1.4 to >=7.1.6 in /services/claw-interface (#3178)

Updates the requirements on
[cachetools](https://github.com/tkem/cachetools) to permit the latest
version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's
changelog</a>.</em></p>
<blockquote>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
</li>
</ul>
<h1>v7.1.1 (2026-05-03)</h1>
<ul>
<li>Various type stub improvements.</li>
</ul>
<p>v7.1.0 (2026-05-01)</p>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/tkem/cachetools/commit/13bb86a55e36e501cf0b3e4c35db516ed9409fd7"><code>13bb86a</code></a>
Minor style improvements to keep ruff happy.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/e2250be46b9d8ed76b82c1c18a4465c0b1167b8a"><code>e2250be</code></a>
Fix RTD version handling.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/0d2a6ea17b3627bcf334c7360a8abe5889dd6235"><code>0d2a6ea</code></a>
Release v7.1.5.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/d64cf805de3c35feac4d2acc0d9d092bd9afd77e"><code>d64cf80</code></a>
Prepare v7.1.5.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/fcbb0de97fc09de646d2e210def765d07dee66e8"><code>fcbb0de</code></a>
Fix <a
href="https://redirect.github.com/tkem/cachetools/issues/406">#406</a>:
Merge branch 'gaoflow-fix-tlru-overwrite-expired-stale-value' into
...</li>
<li><a
href="https://github.com/tkem/cachetools/commit/c0fdf6abab38040947d6fe2e38c507401d5e2350"><code>c0fdf6a</code></a>
Fix TLRUCache silently keeping stale value on expired overwrite</li>
<li><a
href="https://github.com/tkem/cachetools/commit/978d34d40cdbf3b4cbfce104f3166032cc4ea028"><code>978d34d</code></a>
Bump actions/setup-python from 6.2.0 to 6.3.0</li>
<li><a
href="https://github.com/tkem/cachetools/commit/d5c7eea7e52d18fed0ec1b575db1956b1d035782"><code>d5c7eea</code></a>
Reject negative cache item sizes</li>
<li><a
href="https://github.com/tkem/cachetools/commit/578e97648dd312880f8aea172437c6dd424d0028"><code>578e976</code></a>
Update build environment.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/e164b7020e4211b57d20fe2b252d931af6244ad4"><code>e164b70</code></a>
Bump codecov/codecov-action from 6.0.0 to 7.0.0</li>
<li>Additional commits viewable in <a
href="https://github.com/tkem/cachetools/compare/v7.1.4...v7.1.6">compare
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

### PR Body

Updates the requirements on [cachetools](https://github.com/tkem/cachetools) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's changelog</a>.</em></p>
<blockquote>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
</li>
</ul>
<h1>v7.1.1 (2026-05-03)</h1>
<ul>
<li>Various type stub improvements.</li>
</ul>
<p>v7.1.0 (2026-05-01)</p>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/tkem/cachetools/commit/13bb86a55e36e501cf0b3e4c35db516ed9409fd7"><code>13bb86a</code></a> Minor style improvements to keep ruff happy.</li>
<li><a href="https://github.com/tkem/cachetools/commit/e2250be46b9d8ed76b82c1c18a4465c0b1167b8a"><code>e2250be</code></a> Fix RTD version handling.</li>
<li><a href="https://github.com/tkem/cachetools/commit/0d2a6ea17b3627bcf334c7360a8abe5889dd6235"><code>0d2a6ea</code></a> Release v7.1.5.</li>
<li><a href="https://github.com/tkem/cachetools/commit/d64cf805de3c35feac4d2acc0d9d092bd9afd77e"><code>d64cf80</code></a> Prepare v7.1.5.</li>
<li><a href="https://github.com/tkem/cachetools/commit/fcbb0de97fc09de646d2e210def765d07dee66e8"><code>fcbb0de</code></a> Fix <a href="https://redirect.github.com/tkem/cachetools/issues/406">#406</a>: Merge branch 'gaoflow-fix-tlru-overwrite-expired-stale-value' into ...</li>
<li><a href="https://github.com/tkem/cachetools/commit/c0fdf6abab38040947d6fe2e38c507401d5e2350"><code>c0fdf6a</code></a> Fix TLRUCache silently keeping stale value on expired overwrite</li>
<li><a href="https://github.com/tkem/cachetools/commit/978d34d40cdbf3b4cbfce104f3166032cc4ea028"><code>978d34d</code></a> Bump actions/setup-python from 6.2.0 to 6.3.0</li>
<li><a href="https://github.com/tkem/cachetools/commit/d5c7eea7e52d18fed0ec1b575db1956b1d035782"><code>d5c7eea</code></a> Reject negative cache item sizes</li>
<li><a href="https://github.com/tkem/cachetools/commit/578e97648dd312880f8aea172437c6dd424d0028"><code>578e976</code></a> Update build environment.</li>
<li><a href="https://github.com/tkem/cachetools/commit/e164b7020e4211b57d20fe2b252d931af6244ad4"><code>e164b70</code></a> Bump codecov/codecov-action from 6.0.0 to 7.0.0</li>
<li>Additional commits viewable in <a href="https://github.com/tkem/cachetools/compare/v7.1.4...v7.1.6">compare view</a></li>
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

## chore(deps-dev): update ruff requirement from >=0.15.22 to >=0.16.0 in /services/claw-interface (#3179)

- **SHA**: `3066dfa47be3fc2949054bee9b3b29bcd8e38513`
- **作者**: dependabot[bot]
- **日期**: 2026-08-01T12:54:03Z
- **PR**: #3179

### Commit Message

```
chore(deps-dev): update ruff requirement from >=0.15.22 to >=0.16.0 in /services/claw-interface (#3179)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.0</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-23.</p>
<p>Check out the <a href="https://astral.sh/blog/ruff-v0.16.0">blog
post</a> for a migration guide and overview of the changes!</p>
<h3>Breaking changes</h3>
<ul>
<li>
<p>Ruff now enables a much larger set of rules by default (413, up from
59). See the blog post for more details and the new <a
href="https://docs.astral.sh/ruff/default-rules/">Default Rules</a> page
for a full listing of the enabled rules. Note that this is primarily an
expansion, but 18 of the more opinionated pycodestyle (<code>E</code>)
and pyflakes (<code>F</code>) rules have been removed from the default
set: <code>E401</code>, <code>E402</code>, <code>E701</code>,
<code>E702</code>, <code>E703</code>, <code>E711</code>,
<code>E712</code>, <code>E713</code>, <code>E714</code>,
<code>E721</code>, <code>E731</code>, <code>E741</code>,
<code>E742</code>, <code>E743</code>, <code>F403</code>,
<code>F405</code>, <code>F406</code>, and <code>F722</code>.</p>
</li>
<li>
<p>Ruff can now format Python code blocks in Markdown files and will do
this by default. See the <a
href="https://docs.astral.sh/ruff/formatter/#markdown-code-formatting">documentation</a>
for more details.</p>
</li>
<li>
<p>Ruff now supports <code>ruff: ignore</code> comments at the ends of
lines, like <code>noqa</code> comments, or on the line preceding a
diagnostic. For example, these both suppress an <a
href="https://docs.astral.sh/ruff/rules/unused-import/"><code>unused-import</code></a>
(<code>F401</code>) diagnostic:</p>
<pre lang="py"><code>import math  # ruff: ignore[F401]
<h1>ruff: ignore[F401]</h1>
<p>import os
</code></pre></p>
</li>
<li>
<p>Fixes are now shown in <code>check</code> and <code>format
--check</code> output:</p>
<pre lang="console"><code>❯ ruff format --check .
unformatted: File would be reformatted
 --&gt; try.md:1:1
  |
1 | ```python
  - import   math
2 + import math
3 | ```
  |
<p>1 file would be reformatted
</code></pre></p>
<p>This example also shows off the Markdown formatting.</p>
</li>
<li>
<p><code>format --check</code> now supports the same output formats as
the linter, including the <code>github</code> and <code>gitlab</code>
outputs for rendering annotations in CI:</p>
<pre lang="console"><code>❯ ruff format --check --output-format github .
::error title=ruff
(unformatted),file=try.md,line=2,col=8,endLine=2,endColumn=10::try.md:2:8:
unformatted: File would be reformatted
</code></pre>
<p>See the CLI help or <a
href="https://docs.astral.sh/ruff/settings/#output-format">documentation</a>
for the full list of supported formats.</p>
</li>
<li>
<p>The <code>filename</code>, <code>location</code>,
<code>end_location</code>, <code>fix.edits[].location</code>, and
<code>fix.edits[].end_location</code> fields in the JSON output format
may now be <code>null</code> rather than defaulting to the empty string
and row 1, column 1, respectively.</p>
</li>
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
<h2>0.16.0</h2>
<p>Released on 2026-07-23.</p>
<p>Check out the <a href="https://astral.sh/blog/ruff-v0.16.0">blog
post</a> for a migration
guide and overview of the changes!</p>
<h3>Breaking changes</h3>
<ul>
<li>
<p>Ruff now enables a much larger set of rules by default (413, up from
59). See the blog post for
more details and the new <a
href="https://docs.astral.sh/ruff/default-rules/">Default Rules</a> page
for a
full listing of the enabled rules. Note that this is primarily an
expansion, but 18 of the more
opinionated pycodestyle (<code>E</code>) and pyflakes (<code>F</code>)
rules have been removed from the default set:
<code>E401</code>, <code>E402</code>, <code>E701</code>,
<code>E702</code>, <code>E703</code>, <code>E711</code>,
<code>E712</code>, <code>E713</code>, <code>E714</code>,
<code>E721</code>, <code>E731</code>, <code>E741</code>,
<code>E742</code>, <code>E743</code>, <code>F403</code>,
<code>F405</code>, <code>F406</code>, and <code>F722</code>.</p>
</li>
<li>
<p>Ruff can now format Python code blocks in Markdown files and will do
this by default. See the
<a
href="https://docs.astral.sh/ruff/formatter/#markdown-code-formatting">documentation</a>
for more details.</p>
</li>
<li>
<p>Ruff now supports <code>ruff: ignore</code> comments at the ends of
lines, like <code>noqa</code> comments, or on the line preceding a
diagnostic. For example, these both suppress an <a
href="https://docs.astral.sh/ruff/rules/unused-import/"><code>unused-import</code></a>
(<code>F401</code>) diagnostic:</p>
<pre lang="py"><code>import math  # ruff: ignore[F401]
<h1>ruff: ignore[F401]</h1>
<p>import os
</code></pre></p>
</li>
<li>
<p>Fixes are now shown in <code>check</code> and <code>format
--check</code> output:</p>
<pre lang="console"><code>❯ ruff format --check .
unformatted: File would be reformatted
 --&gt; try.md:1:1
  |
1 | ```python
  - import   math
2 + import math
3 | ```
  |
<p>1 file would be reformatted
</code></pre></p>
<p>This example also shows off the Markdown formatting.</p>
</li>
<li>
<p><code>format --check</code> now supports the same output formats as
the linter, including the <code>github</code> and
<code>gitlab</code> outputs for rendering annotations in CI:</p>
<pre lang="console"><code></code></pre>
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
href="https://github.com/astral-sh/ruff/commit/a2635fd8f39e1d34ce8074cb486809426148f3e9"><code>a2635fd</code></a>
Bump 0.16.0 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27136">#27136</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/34334491652f8ceca5246d15c5c5afe0d6bc77ae"><code>3433449</code></a>
[ty] Reuse full call diagnostics for implicit setter calls (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27115">#27115</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/22400709220931375e072ad5d7460b9fc781af78"><code>2240070</code></a>
Reflect <code>ruff: ignore</code> and <code>--add-ignore</code>
stabilization in documentation (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27">#27</a>...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/17ef71142c52230b923dad46ee5554140fc3fd2e"><code>17ef711</code></a>
Stabilize <code>--add-ignore</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27125">#27125</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ef912bbbe466856aa4aac10ad2a8856eb3d5aef3"><code>ef912bb</code></a>
Add newly stabilized rules to defaults (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27055">#27055</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/b30f04023281b46f12011f13ce6b45c247e0d2e3"><code>b30f040</code></a>
Stabilize new default rules (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27035">#27035</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/bcd70c5f10ea97ed52a785d70e7f33b83b7c697a"><code>bcd70c5</code></a>
Exclude Markdown files from <code>format-dev</code> runs (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27052">#27052</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/87e51e2cbbaed376fc13dead40fd772361fa07c0"><code>87e51e2</code></a>
Fix <code>format --check</code> spans for syntax errors (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27045">#27045</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/afe2723a348364ac7f4b9abd76fc67779490c05e"><code>afe2723</code></a>
[<code>flake8-gettext</code>] Stabilize qualified-name and built-in
binding resolution (...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/a9702d8928344f77a41dbe535f655a69fb04e2df"><code>a9702d8</code></a>
[<code>flake8-bandit</code>] Stabilize string literal binding resolution
(<code>S310</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26944">#26944</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.22...0.16.0">compare
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

### PR Body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.0</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-23.</p>
<p>Check out the <a href="https://astral.sh/blog/ruff-v0.16.0">blog post</a> for a migration guide and overview of the changes!</p>
<h3>Breaking changes</h3>
<ul>
<li>
<p>Ruff now enables a much larger set of rules by default (413, up from 59). See the blog post for more details and the new <a href="https://docs.astral.sh/ruff/default-rules/">Default Rules</a> page for a full listing of the enabled rules. Note that this is primarily an expansion, but 18 of the more opinionated pycodestyle (<code>E</code>) and pyflakes (<code>F</code>) rules have been removed from the default set: <code>E401</code>, <code>E402</code>, <code>E701</code>, <code>E702</code>, <code>E703</code>, <code>E711</code>, <code>E712</code>, <code>E713</code>, <code>E714</code>, <code>E721</code>, <code>E731</code>, <code>E741</code>, <code>E742</code>, <code>E743</code>, <code>F403</code>, <code>F405</code>, <code>F406</code>, and <code>F722</code>.</p>
</li>
<li>
<p>Ruff can now format Python code blocks in Markdown files and will do this by default. See the <a href="https://docs.astral.sh/ruff/formatter/#markdown-code-formatting">documentation</a> for more details.</p>
</li>
<li>
<p>Ruff now supports <code>ruff: ignore</code> comments at the ends of lines, like <code>noqa</code> comments, or on the line preceding a diagnostic. For example, these both suppress an <a href="https://docs.astral.sh/ruff/rules/unused-import/"><code>unused-import</code></a> (<code>F401</code>) diagnostic:</p>
<pre lang="py"><code>import math  # ruff: ignore[F401]
<h1>ruff: ignore[F401]</h1>
<p>import os
</code></pre></p>
</li>
<li>
<p>Fixes are now shown in <code>check</code> and <code>format --check</code> output:</p>
<pre lang="console"><code>❯ ruff format --check .
unformatted: File would be reformatted
 --&gt; try.md:1:1
  |
1 | ```python
  - import   math
2 + import math
3 | ```
  |
<p>1 file would be reformatted
</code></pre></p>
<p>This example also shows off the Markdown formatting.</p>
</li>
<li>
<p><code>format --check</code> now supports the same output formats as the linter, including the <code>github</code> and <code>gitlab</code> outputs for rendering annotations in CI:</p>
<pre lang="console"><code>❯ ruff format --check --output-format github .
::error title=ruff (unformatted),file=try.md,line=2,col=8,endLine=2,endColumn=10::try.md:2:8: unformatted: File would be reformatted
</code></pre>
<p>See the CLI help or <a href="https://docs.astral.sh/ruff/settings/#output-format">documentation</a> for the full list of supported formats.</p>
</li>
<li>
<p>The <code>filename</code>, <code>location</code>, <code>end_location</code>, <code>fix.edits[].location</code>, and <code>fix.edits[].end_location</code> fields in the JSON output format may now be <code>null</code> rather than defaulting to the empty string and row 1, column 1, respectively.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.0</h2>
<p>Released on 2026-07-23.</p>
<p>Check out the <a href="https://astral.sh/blog/ruff-v0.16.0">blog post</a> for a migration
guide and overview of the changes!</p>
<h3>Breaking changes</h3>
<ul>
<li>
<p>Ruff now enables a much larger set of rules by default (413, up from 59). See the blog post for
more details and the new <a href="https://docs.astral.sh/ruff/default-rules/">Default Rules</a> page for a
full listing of the enabled rules. Note that this is primarily an expansion, but 18 of the more
opinionated pycodestyle (<code>E</code>) and pyflakes (<code>F</code>) rules have been removed from the default set:
<code>E401</code>, <code>E402</code>, <code>E701</code>, <code>E702</code>, <code>E703</code>, <code>E711</code>, <code>E712</code>, <code>E713</code>, <code>E714</code>, <code>E721</code>, <code>E731</code>, <code>E741</code>,
<code>E742</code>, <code>E743</code>, <code>F403</code>, <code>F405</code>, <code>F406</code>, and <code>F722</code>.</p>
</li>
<li>
<p>Ruff can now format Python code blocks in Markdown files and will do this by default. See the
<a href="https://docs.astral.sh/ruff/formatter/#markdown-code-formatting">documentation</a> for more details.</p>
</li>
<li>
<p>Ruff now supports <code>ruff: ignore</code> comments at the ends of lines, like <code>noqa</code> comments, or on the line preceding a diagnostic. For example, these both suppress an <a href="https://docs.astral.sh/ruff/rules/unused-import/"><code>unused-import</code></a> (<code>F401</code>) diagnostic:</p>
<pre lang="py"><code>import math  # ruff: ignore[F401]
<h1>ruff: ignore[F401]</h1>
<p>import os
</code></pre></p>
</li>
<li>
<p>Fixes are now shown in <code>check</code> and <code>format --check</code> output:</p>
<pre lang="console"><code>❯ ruff format --check .
unformatted: File would be reformatted
 --&gt; try.md:1:1
  |
1 | ```python
  - import   math
2 + import math
3 | ```
  |
<p>1 file would be reformatted
</code></pre></p>
<p>This example also shows off the Markdown formatting.</p>
</li>
<li>
<p><code>format --check</code> now supports the same output formats as the linter, including the <code>github</code> and
<code>gitlab</code> outputs for rendering annotations in CI:</p>
<pre lang="console"><code></code></pre>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/a2635fd8f39e1d34ce8074cb486809426148f3e9"><code>a2635fd</code></a> Bump 0.16.0 (<a href="https://redirect.github.com/astral-sh/ruff/issues/27136">#27136</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/34334491652f8ceca5246d15c5c5afe0d6bc77ae"><code>3433449</code></a> [ty] Reuse full call diagnostics for implicit setter calls (<a href="https://redirect.github.com/astral-sh/ruff/issues/27115">#27115</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/22400709220931375e072ad5d7460b9fc781af78"><code>2240070</code></a> Reflect <code>ruff: ignore</code> and <code>--add-ignore</code> stabilization in documentation (<a href="https://redirect.github.com/astral-sh/ruff/issues/27">#27</a>...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/17ef71142c52230b923dad46ee5554140fc3fd2e"><code>17ef711</code></a> Stabilize <code>--add-ignore</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/27125">#27125</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ef912bbbe466856aa4aac10ad2a8856eb3d5aef3"><code>ef912bb</code></a> Add newly stabilized rules to defaults (<a href="https://redirect.github.com/astral-sh/ruff/issues/27055">#27055</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/b30f04023281b46f12011f13ce6b45c247e0d2e3"><code>b30f040</code></a> Stabilize new default rules (<a href="https://redirect.github.com/astral-sh/ruff/issues/27035">#27035</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/bcd70c5f10ea97ed52a785d70e7f33b83b7c697a"><code>bcd70c5</code></a> Exclude Markdown files from <code>format-dev</code> runs (<a href="https://redirect.github.com/astral-sh/ruff/issues/27052">#27052</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/87e51e2cbbaed376fc13dead40fd772361fa07c0"><code>87e51e2</code></a> Fix <code>format --check</code> spans for syntax errors (<a href="https://redirect.github.com/astral-sh/ruff/issues/27045">#27045</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/afe2723a348364ac7f4b9abd76fc67779490c05e"><code>afe2723</code></a> [<code>flake8-gettext</code>] Stabilize qualified-name and built-in binding resolution (...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/a9702d8928344f77a41dbe535f655a69fb04e2df"><code>a9702d8</code></a> [<code>flake8-bandit</code>] Stabilize string literal binding resolution (<code>S310</code>) (<a href="https://redirect.github.com/astral-sh/ruff/issues/26944">#26944</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.22...0.16.0">compare view</a></li>
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

## feat(artifacts): add runtime-neutral workspace APIs (#3180)

- **SHA**: `ff4b6fe716febabb79c3a55b8658f17018fb0d00`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-01T12:47:41Z
- **PR**: #3180

### Commit Message

```
feat(artifacts): add runtime-neutral workspace APIs (#3180)

## What changed

- adds runtime-neutral backend adapters for V1/V2 Files and Published
Artifacts;
- keeps Files and Artifacts as separate resources and preserves URL
fallback;
- normalizes auth, ownership and error handling without exposing R2
coordinates.

## Why

ecap must read workspace files and immutable Published Artifacts through
their own APIs while remaining compatible with historical V1 URLs.

## Validation

- 100 targeted Python tests passed across the complete stack;
- `verify-py` passed ruff, format, pyright and import-linter.

This is PR 1/3 of the ecap Artifact V2 stack.
```

### PR Body

## What changed

- adds runtime-neutral backend adapters for V1/V2 Files and Published Artifacts;
- keeps Files and Artifacts as separate resources and preserves URL fallback;
- normalizes auth, ownership and error handling without exposing R2 coordinates.

## Why

ecap must read workspace files and immutable Published Artifacts through their own APIs while remaining compatible with historical V1 URLs.

## Validation

- 100 targeted Python tests passed across the complete stack;
- `verify-py` passed ruff, format, pyright and import-linter.

This is PR 1/3 of the ecap Artifact V2 stack.


---
