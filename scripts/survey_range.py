#!/usr/bin/env python3
"""Survey commits per day in a date range. Titles only, no PR bodies (cheap)."""
import json, sys, datetime, urllib.request, urllib.error, collections

TOKEN = open('/tmp/gh_token.txt').read().strip()
REPOS = ['SerendipityOneInc/ecap-skills', 'SerendipityOneInc/ecap-workspace']

start = datetime.date.fromisoformat(sys.argv[1])
end = datetime.date.fromisoformat(sys.argv[2])  # inclusive

since = datetime.datetime(start.year, start.month, start.day, tzinfo=datetime.timezone.utc)
until = datetime.datetime(end.year, end.month, end.day, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)
SINCE_ISO = since.isoformat().replace('+00:00', 'Z')
UNTIL_ISO = until.isoformat().replace('+00:00', 'Z')


def api(url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + TOKEN)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'zooclaw-sync')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print('HTTP %s for %s: %s' % (e.code, url, e.read().decode()[:200]), file=sys.stderr)
        return None


out = collections.defaultdict(lambda: collections.defaultdict(list))
for repo in REPOS:
    page = 1
    while True:
        url = ('https://api.github.com/repos/%s/commits?since=%s&until=%s&per_page=100&page=%d'
               % (repo, SINCE_ISO, UNTIL_ISO, page))
        commits = api(url) or []
        if not commits:
            break
        for c in commits:
            d = c['commit']['author']['date'][:10]
            title = c['commit']['message'].split('\n')[0]
            out[d][repo].append({'sha': c['sha'], 'title': title})
        if len(commits) < 100:
            break
        page += 1

json.dump({k: dict(v) for k, v in out.items()}, open('/tmp/survey.json', 'w'), ensure_ascii=False, indent=1)

total = 0
print('日期          skills  workspace  合计')
cur = start
while cur <= end:
    k = cur.isoformat()
    s = len(out.get(k, {}).get(REPOS[0], []))
    w = len(out.get(k, {}).get(REPOS[1], []))
    total += s + w
    print('%s   %4d      %5d  %5d' % (k, s, w, s + w))
    cur += datetime.timedelta(days=1)
print('窗口合计 %d 条' % total)
