# SerendipityOneInc/ecap-skills commits — 2026-07-31

## c938f68e — fix: use ECAP proxy URL for speech skills (#250)

- **SHA**: c938f68e09931b7b55d1fe7ffbeb57324b1906a7
- **作者**: sharplee-srp
- **日期**: 2026-07-31T07:12:36Z
- **PR**: #250

### Commit Message

```
fix: use ECAP proxy URL for speech skills (#250)

## Summary

- migrate ZooClaw ASR and TTS skill scripts from
`ZOOCLAW_TTS_GATEWAY_URL` to the canonical `ECAP_PROXY_BASE_URL`
- fail fast when the proxy base URL is missing instead of silently
falling back to the production gateway
- update skill metadata, prerequisites, endpoint documentation, and
`.env.example` files

## Validation

- `bash -n` passed for all five changed shell scripts
- `uv run --with pyyaml python .github/scripts/lint_skills.py` passed
- confirmed all speech skill scripts reject the legacy variable when
`ECAP_PROXY_BASE_URL` is unset
- completed a live staging TTS → ASR smoke test against
`https://ecap-proxy-service.ecap.yesy.live/` with the legacy variable
unset
  - TTS generated a valid 1.6-second WAV
  - ASR returned `Speech Gateway Migration Test.`

## Notes

- the legacy variable remains in `.devcontainer/openclaw-default.env`
for compatibility with native runtime plugins outside the scope of these
skills
- current staging and production Bot Pods already receive
`ECAP_PROXY_BASE_URL`
```

### PR Body

## Summary

- migrate ZooClaw ASR and TTS skill scripts from `ZOOCLAW_TTS_GATEWAY_URL` to the canonical `ECAP_PROXY_BASE_URL`
- fail fast when the proxy base URL is missing instead of silently falling back to the production gateway
- update skill metadata, prerequisites, endpoint documentation, and `.env.example` files

## Validation

- `bash -n` passed for all five changed shell scripts
- `uv run --with pyyaml python .github/scripts/lint_skills.py` passed
- confirmed all speech skill scripts reject the legacy variable when `ECAP_PROXY_BASE_URL` is unset
- completed a live staging TTS → ASR smoke test against `https://ecap-proxy-service.ecap.yesy.live/` with the legacy variable unset
  - TTS generated a valid 1.6-second WAV
  - ASR returned `Speech Gateway Migration Test.`

## Notes

- the legacy variable remains in `.devcontainer/openclaw-default.env` for compatibility with native runtime plugins outside the scope of these skills
- current staging and production Bot Pods already receive `ECAP_PROXY_BASE_URL`



---
