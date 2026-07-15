#!/usr/bin/env python3
"""
backfill_release_status.py — 每日回扫历史「已合并待发版」记录，判定其是否已随新 release 上线。

背景：某条更新合并进 main 时标为「已合并待发版」；之后若有新的正式 release 覆盖了它，
它就已经真正上线了。若不每天回扫，多维表会长期挂着大量假的「待发版」。

用法：
  python3 backfill_release_status.py            # dry-run，只打印将要变更的记录
  python3 backfill_release_status.py --apply     # 回写飞书多维表

判定：非 Skill 取该仓库最新正式 release tag（ecap-workspace: ecap-v*-release；agent-pack: v*-release 非 beta），
用 compare API 判 tag 是否包含该 PR 的 merge_commit_sha。包含=已上线，否则待发版。
Skill 类走 ClawHub，判不出标未知/需确认。
Token 从 zooclaw-updates git remote 提取；飞书凭据从 ~/.openclaw/openclaw.json。
"""
import json, re, subprocess, urllib.request, urllib.error, time, sys, os

HERE=os.path.dirname(os.path.abspath(__file__))
REPO_ROOT=os.path.join(HERE,"..")
APP="Iap1bcHgnaWlJqs8wRdcvcPcnye"; TBL="tbl3NTAENOKmW0mv"

def gh_token():
    t=os.environ.get("GITHUB_TOKEN")
    if t: return t
    remote=subprocess.check_output(["git","-C",REPO_ROOT,"remote","get-url","origin"]).decode().strip()
    return re.search(r'https://[^:/]+:([^@]+)@',remote).group(1)
TOK=gh_token()
def gh(p):
    for _ in range(3):
        req=urllib.request.Request("https://api.github.com"+p,headers={"Authorization":f"Bearer {TOK}","Accept":"application/vnd.github+json"})
        try: return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code in (403,429,502,503): time.sleep(2); continue
            return {"__err__":e.code}
    return {"__err__":"retry"}

def latest_release(repo, prefix_re):
    for r in gh(f"/repos/{repo}/releases?per_page=30"):
        if r["draft"] or r["prerelease"] or "beta" in r["tag_name"]: continue
        if re.match(prefix_re,r["tag_name"]): return r["tag_name"]
    return None

def feishu_token():
    c=json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))
    fa=c['channels']['feishu']['accounts']['default']
    d=json.dumps({'app_id':fa['appId'],'app_secret':fa['appSecret']}).encode()
    r=urllib.request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',data=d,headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))['tenant_access_token']

def fs(u,p,at,method="POST"):
    d=json.dumps(p).encode() if p is not None else None
    r=urllib.request.Request(u,data=d,method=method,headers={'Content-Type':'application/json','Authorization':f'Bearer {at}'})
    try: return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e: return {"__http__":e.code,"body":e.read().decode()[:300]}

def contains(repo,tag,sha):
    d=gh(f"/repos/{repo}/compare/{tag}...{sha}")
    if isinstance(d,dict) and d.get("__err__"): return None
    return d.get("status") in ("behind","identical")

def main():
    apply="--apply" in sys.argv
    at=feishu_token()
    WS=latest_release("SerendipityOneInc/ecap-workspace", r"^ecap-v\d")
    AP=latest_release("SerendipityOneInc/ecap-agent-pack", r"^v\d")
    print(f"latest releases: workspace={WS} agent-pack={AP}")
    # list all records
    recs=[]; pt=None
    while True:
        u=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records?page_size=500"
        if pt: u+="&page_token="+pt
        r=fs(u,None,at,"GET"); recs.extend(r["data"].get("items",[]))
        pt=r["data"].get("page_token")
        if not r["data"].get("has_more"): break
    def gettext(v):
        if isinstance(v,list): return "".join(x.get("text","") for x in v)
        if isinstance(v,dict): return v.get("text","")
        return v or ""
    pend=[x for x in recs if gettext(x["fields"].get("发布状态"))=="已合并待发版"]
    print(f"待复查(已合并待发版): {len(pend)}")
    sha_cache={}; updates=[]
    for x in pend:
        raw=gettext(x["fields"].get("原始内容"))
        title=gettext(x["fields"].get("标题"))
        if "ecap-agent-pack" in raw or "agent-studio" in raw:
            repo,tag="SerendipityOneInc/ecap-agent-pack",AP
        elif ("ecap-skills" in raw) and ("#" in raw):
            repo,tag="skills",None
        else:
            repo,tag="SerendipityOneInc/ecap-workspace",WS
        prs=re.findall(r'#(\d+)',raw)
        newst="未知/需确认"; note=""
        if repo=="skills":
            note="Skill 走 ClawHub 独立分发，需 openclaw skills verify 单独确认"
        elif prs and tag:
            pr=prs[0]; key=(repo,pr)
            if key not in sha_cache:
                d=gh(f"/repos/{repo}/pulls/{pr}")
                sha_cache[key]=d.get("merge_commit_sha") if isinstance(d,dict) and not d.get("__err__") else None
            sha=sha_cache[key]
            if sha:
                inc=contains(repo,tag,sha)
                newst = "已上线" if inc is True else ("已合并待发版" if inc is False else "未知/需确认")
        if newst!="已合并待发版":
            f={"发布状态":newst}
            if note: f["备注"]=note
            updates.append({"record_id":x["record_id"],"fields":f,"_t":title,"_s":newst})
        time.sleep(0.08)
    online=[u for u in updates if u["_s"]=="已上线"]
    print(f"将翻新为已上线: {len(online)} | 其他变更(未知): {len(updates)-len(online)}")
    for u in updates: print(f"   [{u['_s']}] {u['_t'][:45]}")
    if apply and updates:
        url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/batch_update"
        recs2=[{"record_id":u["record_id"],"fields":u["fields"]} for u in updates]
        ok=0
        for i in range(0,len(recs2),20):
            r=fs(url,{"records":recs2[i:i+20]},at); 
            if r.get("code")==0: ok+=len(r["data"]["records"])
            else: print("ERR",r); break
            time.sleep(0.3)
        print("已回写:",ok)
    elif not apply:
        print("(dry-run，加 --apply 回写)")

if __name__=="__main__": main()
