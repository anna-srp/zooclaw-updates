import subprocess, re, json, datetime, urllib.request, os, sys

remote = subprocess.check_output(['git','-C','/home/node/.openclaw/workspace/tmp/zooclaw-updates','remote','get-url','origin']).decode().strip()
m = re.search(r'https://[^:/]+:([^@]+)@', remote)
TOKEN = m.group(1)
print("token prefix:", TOKEN[:7])

YEST = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).date()
since = f"{YEST}T00:00:00Z"
until = f"{YEST + datetime.timedelta(days=1)}T00:00:00Z"
print("window", since, until)

def gh(url):
    req = urllib.request.Request(url, headers={'Authorization':f'token {TOKEN}','Accept':'application/vnd.github+json','User-Agent':'zooclaw'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

out = {}
for repo in ['SerendipityOneInc/ecap-skills','SerendipityOneInc/ecap-workspace']:
    commits = gh(f'https://api.github.com/repos/{repo}/commits?since={since}&until={until}&per_page=100')
    res=[]
    for c in commits:
        sha=c['sha']
        full = gh(f'https://api.github.com/repos/{repo}/commits/{sha}')
        msg = full['commit']['message']
        title = msg.split('\n')[0]
        pr_body=None; pr_num=None
        pm = re.search(r'\(#(\d+)\)', title)
        if pm:
            pr_num=int(pm.group(1))
            try:
                pr = gh(f'https://api.github.com/repos/{repo}/pulls/{pr_num}')
                pr_body = pr.get('body')
            except Exception as e:
                pr_body=f"(fetch failed {e})"
        res.append({'sha':sha,'author':full['commit']['author']['name'],'date':full['commit']['author']['date'],'message':msg,'pr_number':pr_num,'pr_body':pr_body,'files':[f['filename'] for f in full.get('files',[])][:60]})
    out[repo]=res
    print(repo, len(res))

json.dump({'date':str(YEST),'repos':out}, open('/home/node/.openclaw/workspace/tmp/commits_dump.json','w'), ensure_ascii=False, indent=1)
