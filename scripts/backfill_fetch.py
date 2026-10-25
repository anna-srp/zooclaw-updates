#!/usr/bin/env python3
"""Backfill: fetch full commit details for a date range and write raw/<date>/ files."""
import json, os, sys, datetime, urllib.request, urllib.error, re, time

TOKEN = open('/tmp/gh_token.txt').read().strip()
REPOS = ['SerendipityOneInc/ecap-skills', 'SerendipityOneInc/ecap-workspace']
REPO_ROOT = '/tmp/zu'
BF_DIR = '/tmp/bf'

PACK_NOTE = (
    '# Agent Pack Updates\n\n'
    '本日为 2026-10-25 回补。Agent Pack 版本变化不可追溯：pack 列表接口只返回当前版本，'
    '且 USER_INTERNAL_TOKEN 自 2026-10-05 起返回 401。本日未做 pack 检测。\n'
)


def api(url, retries=3):
    for attempt in range(retries):
        req = urllib.request.Request(url)
        req.add_header('Authorization', 'token ' + TOKEN)
        req.add_header('Accept', 'application/vnd.github+json')
        req.add_header('User-Agent', 'zooclaw-sync')
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:150]
            if e.code in (403, 429) and attempt < retries - 1:
                time.sleep(20)
                continue
            print('HTTP %s %s :: %s' % (e.code, url, body), file=sys.stderr)
            return None
        except Exception as exc:
            if attempt < retries - 1:
                time.sleep(5)
                continue
            print('ERR %s :: %s' % (url, exc), file=sys.stderr)
            return None
    return None


def fetch_day(day):
    since = datetime.datetime(day.year, day.month, day.day, tzinfo=datetime.timezone.utc)
    until = since + datetime.timedelta(days=1)
    s_iso = since.isoformat().replace('+00:00', 'Z')
    u_iso = until.isoformat().replace('+00:00', 'Z')
    result = {}
    for repo in REPOS:
        commits = api('https://api.github.com/repos/%s/commits?since=%s&until=%s&per_page=100'
                      % (repo, s_iso, u_iso)) or []
        detailed = []
        for c in commits:
            sha = c['sha']
            full = api('https://api.github.com/repos/%s/commits/%s' % (repo, sha))
            msg = full['commit']['message'] if full else c['commit']['message']
            author = full['commit']['author']['name'] if full else c['commit']['author']['name']
            cdate = full['commit']['author']['date'] if full else c['commit']['author']['date']
            title = msg.split('\n')[0]
            pr_body = None
            pr_num = None
            m = re.search(r'\(#(\d+)\)', title)
            if m:
                pr_num = m.group(1)
                pr = api('https://api.github.com/repos/%s/pulls/%s' % (repo, pr_num))
                if pr:
                    pr_body = pr.get('body')
            detailed.append({'sha': sha, 'author': author, 'date': cdate, 'title': title,
                             'message': msg, 'pr_number': pr_num, 'pr_body': pr_body})
        result[repo] = detailed
    return {'yesterday': day.isoformat(), 'since': s_iso, 'until': u_iso, 'repos': result}


def write_raw(d):
    day = d['yesterday']
    base = os.path.join(REPO_ROOT, 'raw', day)
    os.makedirs(base, exist_ok=True)
    for repo, commits in d['repos'].items():
        name = repo.split('/')[1]
        with open(os.path.join(base, name + '-commits.json'), 'w') as f:
            json.dump(commits, f, ensure_ascii=False, indent=2)
        lines = ['# %s — commits %s' % (repo, day), '']
        if not commits:
            lines.append('今日无更新')
        else:
            for c in commits:
                lines.append('## ' + c['title'])
                lines.append('')
                lines.append('- **SHA**: `%s`' % c['sha'])
                lines.append('- **作者**: %s' % c['author'])
                lines.append('- **日期**: %s' % c['date'])
                lines.append('- **PR**: %s' % ('#' + c['pr_number'] if c['pr_number'] else '（无）'))
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
        with open(os.path.join(base, name + '-commits.md'), 'w') as f:
            f.write(chr(10).join(lines))
    with open(os.path.join(base, 'agent-pack-updates.md'), 'w') as f:
        f.write(PACK_NOTE)
    with open(os.path.join(base, 'agent-pack-updates.json'), 'w') as f:
        json.dump({'backfilled': True, 'detected': False,
                   'reason': 'historical backfill on 2026-10-25; pack API exposes current versions only, and USER_INTERNAL_TOKEN has returned 401 since 2026-10-05',
                   'total_packs': None, 'updated_count': None, 'updated': [], 'all': []},
                  f, ensure_ascii=False, indent=1)


def main():
    os.makedirs(BF_DIR, exist_ok=True)
    start = datetime.date.fromisoformat(sys.argv[1])
    end = datetime.date.fromisoformat(sys.argv[2])
    cur = start
    while cur <= end:
        out_path = os.path.join(BF_DIR, cur.isoformat() + '.json')
        if os.path.exists(out_path):
            print('skip %s (exists)' % cur.isoformat())
        else:
            d = fetch_day(cur)
            with open(out_path, 'w') as f:
                json.dump(d, f, ensure_ascii=False)
            write_raw(d)
            n = sum(len(v) for v in d['repos'].values())
            print('%s: %d commits -> raw written' % (cur.isoformat(), n))
        cur += datetime.timedelta(days=1)


main()
