import re, subprocess, json, urllib.request, datetime, os, sys

url = subprocess.check_output(['git','-C','/home/node/.openclaw/workspace/tmp/zooclaw-updates','remote','get-url','origin']).decode().strip()
m = re.search(r'https://[^:/]+:([^@]+)@', url)
TOKEN = m.group(1)
def api(path):
    req = urllib.request.Request('https://api.github.com'+path, headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','User-Agent':'zooclaw'})
    return json.load(urllib.request.urlopen(req))

DAY = '2026-08-19'
since = DAY+'T00:00:00Z'; until = '2026-08-20T00:00:00Z'
repos = ['SerendipityOneInc/ecap-skills','SerendipityOneInc/ecap-workspace']
out = {}
for r in repos:
    try:
        commits = api(f'/repos/{r}/commits?since={since}&until={until}&per_page=100')
    except Exception as e:
        print('ERR', r, e); commits=[]
    items=[]
    for c in commits:
        sha=c['sha']
        full = api(f'/repos/{r}/commits/{sha}')
        msg = full['commit']['message']
        title = msg.split('\n')[0]
        pr_body=None; pr_num=None
        pm = re.search(r'\(#(\d+)\)', title)
        if pm:
            pr_num=pm.group(1)
            try:
                pr = api(f'/repos/{r}/pulls/{pr_num}')
                pr_body = pr.get('body')
            except Exception as e:
                pr_body='(fetch failed: %s)'%e
        items.append({'sha':sha,'author':full['commit']['author']['name'],'date':full['commit']['author']['date'],'message':msg,'pr_number':pr_num,'pr_body':pr_body,'files':[f['filename'] for f in full.get('files',[])][:50]})
    out[r]=items
    print(r, len(items))
json.dump(out, open('tmp/commits_%s.json'%DAY,'w'), ensure_ascii=False, indent=1)
