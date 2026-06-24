# SerendipityOneInc/ecap-agent-pack — commits 2026-06-23


共 1 个 commit


---

## ci: upload Agent Studio pack after release (#187)

- **SHA**: `fa7b5ed4bfb8901524958b3b7f1c0d168df71ca4`
- **作者**: bill-srp
- **日期**: 2026-06-23T13:51:44Z
- **PR**: #187

### 完整 commit message

```
ci: upload Agent Studio pack after release (#187)

* ci: upload agent studio pack after release

* ci: route agent studio upload by environment

* ci: support semver beta release tags

* ci: log agent studio manifest name

* fix(agent-studio): restore pack manifest name
```

### PR body

## Summary
- upload Agent Studio pack to the backend after GitHub release packaging
- route main releases through production and semver beta tags through staging
- build a root-level Agent Studio upload zip so the backend can parse agent-pack.yaml

## Testing
- ruby -e 'require "yaml"; YAML.load_file(".github/workflows/release-agent-zips.yml"); puts "yaml parse ok"'
- git diff --check
- python3 .github/scripts/agent_release.py package-release --root . --assets-dir /private/tmp/ecap-agent-pack-release-tag-verify --metadata-output /private/tmp/ecap-agent-pack-release-tag-verify/release-artifacts.json
