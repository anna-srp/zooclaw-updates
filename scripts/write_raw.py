#!/usr/bin/env python3
import json, os, datetime

d = json.load(open('/tmp/commits.json'))
yesterday = d['yesterday']
base = f'/home/node/.openclaw/workspace/tmp/zooclaw-updates/raw/{yesterday}'
os.makedirs(base, exist_ok=True)

for repo, commits in d['repos'].items():
    name = repo.split('/')[1]
    md_path = os.path.join(base, f'{name}-commits.md')
    json_path = os.path.join(base, f'{name}-commits.json')
    # JSON
    with open(json_path, 'w') as f:
        json.dump(commits, f, ensure_ascii=False, indent=2)
    # MD
    lines = [f'# {repo} — commits {yesterday}', '']
    if not commits:
        lines.append('今日无更新')
    else:
        for c in commits:
            lines.append(f"## {c['title']}")
            lines.append('')
            lines.append(f"- **SHA**: `{c['sha']}`")
            lines.append(f"- **作者**: {c['author']}")
            lines.append(f"- **日期**: {c['date']}")
            lines.append(f"- **PR**: {'#'+c['pr_number'] if c['pr_number'] else '（无）'}")
            lines.append('')
            lines.append('### Commit Message')
            lines.append('')
            lines.append('```')
            lines.append(c['message'])
            lines.append('```')
            lines.append('')
            if c['pr_body']:
                lines.append('### PR Body')
                lines.append('')
                lines.append(c['pr_body'])
                lines.append('')
            lines.append('---')
            lines.append('')
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'wrote {md_path} ({len(commits)} commits)')
    print(f'wrote {json_path}')
