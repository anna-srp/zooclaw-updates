#!/usr/bin/env python3
import json, sys, datetime, urllib.request, urllib.error, re

TOKEN = open('/tmp/gh_token.txt').read().strip()
REPOS = ['SerendipityOneInc/ecap-skills', 'SerendipityOneInc/ecap-workspace']

now = datetime.datetime.now(datetime.timezone.utc)
yesterday = (now.date() - datetime.timedelta(days=1))
since = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=datetime.timezone.utc)
until = since + datetime.timedelta(days=1)
SINCE_ISO = since.isoformat().replace('+00:00', 'Z')
UNTIL_ISO = until.isoformat().replace('+00:00', 'Z')

def api(url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {TOKEN}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'zooclaw-sync')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code} for {url}: {e.read().decode()[:200]}', file=sys.stderr)
        return None

result = {}
for repo in REPOS:
    owner, name = repo.split('/')
    # list commits in window
    url = f'https://api.github.com/repos/{repo}/commits?since={SINCE_ISO}&until={UNTIL_ISO}&per_page=100'
    commits = api(url) or []
    detailed = []
    for c in commits:
        sha = c['sha']
        # full commit
        full = api(f'https://api.github.com/repos/{repo}/commits/{sha}')
        msg = full['commit']['message'] if full else c['commit']['message']
        author = full['commit']['author']['name'] if full else c['commit']['author']['name']
        cdate = full['commit']['author']['date'] if full else c['commit']['author']['date']
        title = msg.split('\n')[0]
        # PR body
        pr_body = None
        pr_num = None
        m = re.search(r'\(#(\d+)\)', title)
        if m:
            pr_num = m.group(1)
            pr = api(f'https://api.github.com/repos/{repo}/pulls/{pr_num}')
            if pr:
                pr_body = pr.get('body')
        detailed.append({
            'sha': sha, 'author': author, 'date': cdate, 'title': title,
            'message': msg, 'pr_number': pr_num, 'pr_body': pr_body
        })
    result[repo] = detailed
    print(f'{repo}: {len(detailed)} commits', file=sys.stderr)

print(json.dumps({'yesterday': yesterday.isoformat(), 'since': SINCE_ISO, 'until': UNTIL_ISO, 'repos': result}, ensure_ascii=False))
