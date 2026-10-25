# SerendipityOneInc/ecap-skills — commits 2026-10-15

## fix(media-skills): enforce natural request review and refusal stops (#295)

- **SHA**: `d7a867f2fc7f23da7914f898fe7b4f46b05761db`
- **作者**: tim-srp
- **日期**: 2026-10-15T06:33:42Z
- **PR**: #295

### Commit Message

```
fix(media-skills): enforce natural request review and refusal stops (#295)

Natural media requests could reach generation without loading Designer,
and refusal follow-ups could be treated as approval of an “original”
substitute. This changes only three SKILL.md files: model-visible
descriptions require review before execution; concise additions to
existing restrictions prohibit unsolicited substitutes,
unchanged-character “original” continuations, and retries after any
safety rejection, including one with no specific reason. Video routing
remains scoped to video.

## Concise implementation

Commit d245df7 removes the duplicated entry/refusal sections. Net
whitespace-delimited word increases versus main are Designer +25, Video
Generator +30, Chameleon Seedance +43. Descriptions are unchanged from
the prior revision. No scripts or engine code change.

## Validation of d245df7

Fresh real production-runtime sessions on the owner's authorized
account, with temporary personal versions of these exact skills. No
global deployment or engine changes. All requests are natural English;
no skill-reading reminders, warm-ups or context-retention instructions.

- Four IPs × two models × 11 consecutive generation requests in each
same session: all 88 refused before execution. Zero generation,
drawing-script or delegation calls; zero request errors/timeouts. No
inline SVG/Python/image output.
- All 11 user messages stored per session, full preceding context
retained with no compaction. Actual run models verified for all 88
rounds.
- Exact concise Designer body read in 7/8 sessions. Terra/Iron Man
refused without reading the body; this is not universal body-loading
compliance. All eight system prompts contained the expected description.
- Every public replay was checked anonymously: HTTP 200, all user
requests match original frontend post IDs and text in order.

|Target|DeepSeek Flash, 11 rounds|GPT Terra, 11 rounds|
|---|---|---|

|iron_man|[replay](https://zoowork.ai/share/cr_cbObfQsVRgkC1xfKR4ZZxg)|[replay](https://zoowork.ai/share/cr_ALnNEh1huJmabLvDDuOCrQ)|

|batman|[replay](https://zoowork.ai/share/cr_2PjJtrbM1kCtMA_aXxUuKg)|[replay](https://zoowork.ai/share/cr_vat8kr7SLp1nBVm7ELAFdA)|

|naruto|[replay](https://zoowork.ai/share/cr_7OKAjIrKdUGd9R03ab9Oew)|[replay](https://zoowork.ai/share/cr_574sCYYTaaCiTcarnDd5kQ)|

|luffy|[replay](https://zoowork.ai/share/cr_3tdJ4gVcipuBLC55Sj6JiQ)|[replay](https://zoowork.ai/share/cr_WttPgUtIP9mDF7nf9ntQ0w)|

## Actual generic safety-error chains

Two additional medical-reference requests reached the real native image
tool and received HTTP 400 with `Your request was rejected by the safety
system`. The visible runtime error is truncated and does not disclose a
specific reason; do not infer an IP category. After each real rejection,
four same-session natural follow-ups requested rephrasing, Grok/Gemini,
Python/Pillow, and SVG/delegation. Both agents refused and made **zero
subsequent tool calls**, including generation, scripts and delegation.
No injected errors or text-only replay.

|Model|Actual supplier request ID|Full five-round replay|
|---|---|---|
|DeepSeek
Flash|e5889ceb-d74c-4384-96e7-c89484b0579e|[replay](https://zoowork.ai/share/cr_lMOsAQd75BhiLd_KNDfjCQ)|
|GPT
Terra|c445171c-e93c-498a-a4a0-8f20a38ae2a3|[replay](https://zoowork.ai/share/cr_94hBU8jQrhV-giRsYYczxQ)|

These two initial provider blocks are separate from the 88 agent-side
refusals; they are evidence of stopping **after** a real supplier
rejection. Three other clinical probes generated and delivered ordinary
diagrams successfully, did not trigger safety, and are not counted as
safety-stop coverage. They also remain in the evidence. Total: 13 new
frontend sessions and 101 actual requests. No agent technical errors or
timeouts; a diagnostic Redis destructor warning after restoration is
recorded separately.

## Restoration and limits

All temporary skill bindings removed; original gpt-6-sol model,
non-model declared configuration, original selected frontend
conversation and global skill hashes restored. Agent active. Final
configuration version 325. Sessions, artifacts and public replays
retained. PR remains open, automatic merge disabled; nothing globally
published.

Linter and whitespace checks pass; CI checks complete. Review
adjudication: the video-routing ambiguity was fixed. The alleged removal
of text triggers is not supported by the base diff: the original
Designer description listed image capabilities only; this patch does not
expand generic writing routing.

These finite samples validate the concise revision's observed behavior,
not every possible input or an engine-enforced guarantee. Refusals
reflect platform rules, not legal infringement determinations. Follow-up
to merged #294.
```

### PR Body

Natural media requests could skip Designer, and unchanged character requests could be relabeled as “original” alternatives. Only three SKILL.md files change: concise entry descriptions require review before execution; existing restrictions now explicitly prohibit unsolicited substitutes, unchanged-appearance alternatives, and retries after generic safety refusals. Video routing stays scoped to video. No scripts or engine code change.

The duplicated prose was consolidated. Net whitespace-delimited word increases versus the base are Designer +25, Video Generator +30, Chameleon Seedance +43.

## Production release

Merged as d7a867f2fc7f23da7914f898fe7b4f46b05761db, byte-identical to tested d245df7. Published **v0.6.22-release**, following v0.6.21-release, through the standard production environment approval and skills-only workflow. [Actual successful publish run](https://github.com/SerendipityOneInc/ecap-skills/actions/runs/38693232792).

Live global versions: **Designer v5, Video Generator v4, Chameleon Seedance v3**. Registry version/content hashes match the publish log; all three SKILL.md hashes match the release source. Designer SHA256: `230fe6aa56a8daab1ba7013bd971be7bb3bd1fa2524fec9a0abe2e549dda68c4`.

## Fresh post-release verification

Owner-authorized account 7515739413054230528, real production frontend sessions. **No personal skill versions were registered or bound during post-release tests.** The live global versions were used throughout.

- Four IPs × DeepSeek Flash/GPT Terra × 11 consecutive natural English requests in each same session: all 88 refused before generation. Zero image, drawing-script or delegation calls; zero IP artifacts or request timeouts.
- No warm-ups, skill-reading reminders or context-retention instructions. All 11 source user posts match anonymous replay text and IDs in order. Full preceding history retained, no compaction.
- **8/8 sessions actually read the exact released Designer body.** Persisted system prompts carry the new description/version `sha256:230fe6aa56a8daab`. This is actual body-loading evidence, not merely registry availability. Video behavior is not covered by these image tests.

|Target|DeepSeek Flash: 11 rounds|GPT Terra: 11 rounds|
|---|---|---|
|iron_man|[replay](https://zoowork.ai/share/cr_W0q07lFkhUO2xR4JkbYaxg)|[replay](https://zoowork.ai/share/cr_s4jQdXqe-A6VN9ycqvwd-w)|
|batman|[replay](https://zoowork.ai/share/cr_DBM4Nf9b6O-Cf5vs6aU39A)|[replay](https://zoowork.ai/share/cr_g7rcJx5LklVFfWys8zFU9w)|
|naruto|[replay](https://zoowork.ai/share/cr_nkSATj2HJrMUjlmkagHgfg)|[replay](https://zoowork.ai/share/cr_All9uQAcexNRyzbL3YBuwA)|
|luffy|[replay](https://zoowork.ai/share/cr_2ASm1bOq6PybHaj-I7zs5w)|[replay](https://zoowork.ai/share/cr_cjrBwVgPAZ_QPBt_2KlT7w)|

## Real supplier safety refusals after publication

Both models reached the native image tool with clinical reference requests and received real **HTTP 400**, including `Your request was rejected by the safety system`. The runtime error is truncated and gives no specific reason; no category is inferred. Four subsequent natural follow-ups in the same session requested cleaner wording, Grok/Gemini, Python/Pillow, and SVG/delegation. Both models refused with **zero subsequent tool calls** and no inline code/media outputs. No simulated errors or text-only replay.

|Model|New actual supplier request ID|Full five-round public replay|
|---|---|---|
|deepseek|afbf8825-e183-439b-a5c1-ecde9b6d5d87|[replay](https://zoowork.ai/share/cr_pctJK0S706H3ZVktckRdVw)|
|terra|09ede9cf-3ee8-4338-a796-da0618747bf1|[replay](https://zoowork.ai/share/cr_qfnn4CW7iaY9lsDCG37c7A)|

These initial supplier blocks are separate from the 88 agent-side refusals; the test verifies stopping **after** actual rejection. Terra's first clinical probe generated normally and is not counted as safety-stop coverage. Its later safety probe had one recovered preference-file read error (`/skills/chameleon-seedance/preference.md` absent) before the actual provider call; this is separately recorded, not counted as a clean pass or safety block. Zero tool calls followed its real safety refusal.

Post-release total: **11 new sessions, 99 real requests**. All public pages/snapshots checked anonymously HTTP 200. Full raw tool events and transcripts retained, with credentials and internal reasoning removed.

## Restored configuration and limits

Original gpt-6-sol model, non-model configuration and selected frontend session restored; agent active, final configuration version 331. Independent read-only check confirms no test personal bindings and the new global versions remain active. No engine deployment. Sessions, artifacts and replays retained. Diagnostic Redis destructor warnings occurred after restoration with exit code 0 and are recorded separately.

Static validation and CI passed. Earlier review adjudication: video handoff wording was fixed; the claimed removal of text-trigger cues was unsupported by the base description, which already listed image capabilities only.

Finite samples do not guarantee every agent/input will comply, especially explicit version pins or same-name overrides elsewhere. Platform refusal is not a legal infringement finding. Follow-up to merged #294.


---
