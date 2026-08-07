#!/usr/bin/env python3
"""
backfill_tob.py — 回填多维表「toB相关」列（是/否）。

范围：来源日期 >= 指定时间戳（默认近一个月 2026-07-01 UTC）且「toB相关」为空的记录。
判断：信息类型=后端功能 → 是；否则命中 toB 关键词（渠道接入/计费/迁移运维/开发者API/组织多租户/后台合规）→ 是；其余 → 否。

用法：
  python3 backfill_tob.py            # dry-run
  python3 backfill_tob.py --apply    # 回写
  可选：--since <ms>  指定起始来源日期毫秒（默认 1782864000000 = 2026-07-01 UTC）
"""
import json, re, urllib.request, urllib.error, time, sys, os

APP="Iap1bcHgnaWlJqs8wRdcvcPcnye"; TBL="tbl3NTAENOKmW0mv"
DEFAULT_SINCE=1782864000000  # 2026-07-01 00:00 UTC

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

def gettext(v):
    if isinstance(v,list): return "".join(x.get("text","") for x in v if isinstance(x,dict))
    if isinstance(v,dict): return v.get("text","")
    return v or ""

# toB 判定：只看 enterprise 家族词（用户指定口径 2026-07-31）——命中即是，否则否。
# 昦 commit scope + 原始内容全文（中英文，大小写不敏感）。
TOB_PATTERNS=[
    r"enterprise-admin",
    r"enterprise-app",
    r"enterprise-package",
    r"enterprise\s+package",   # enterprise package / packages
    r"enterprise\s+account",
    r"enterprise\s+payment",
    r"zoowork",
    # 中文
    r"企业管理后台",
    r"企业套餐",
    r"线下订单",
    r"线下企业支付",
    r"线下付费企业",
]
TOB_RE=re.compile("|".join(TOB_PATTERNS), re.I)

# 否定上下文：仅"提及"而非主体的误命中，排除
# 1) "Enterprise Package and ... retain their existing guards" —— 主体是 personal plan，enterprise 只是“保持不变”
# 2) "ZooWork Figma" —— ZooWork 仅为设计稿来源，改的是别的 UI
NEG_PATTERNS=[
    r"enterprise\s+package\s+and\s+ecap\s+pack\s+subscriptions\s+retain",
    r"zoowork\s+figma",
]
NEG_RE=re.compile("|".join(NEG_PATTERNS), re.I)

def judge(f):
    # 只看 enterprise 家族词：扫全文（标题 + 原始内容含 commit scope + 核心宣传点）
    text=(gettext(f.get("标题"))+"\n"+gettext(f.get("原始内容"))+"\n"+gettext(f.get("核心宣传点")))
    m=TOB_RE.search(text)
    if not m:
        return "否",""
    # 命中了，但如果仅命中“仅提及”语境且无其他实体词，则排除
    # 具体判断：去掉否定语境后重新搜，若仍命中才算
    cleaned=NEG_RE.sub(" ", text)
    m2=TOB_RE.search(cleaned)
    if m2:
        return "是",f"命中:{m2.group(0)}"
    return "否",""  # 仅命中了“仅提及”语境，判否

def main():
    apply="--apply" in sys.argv
    since=DEFAULT_SINCE
    if "--since" in sys.argv:
        since=int(sys.argv[sys.argv.index("--since")+1])
    at=feishu_token()
    recs=[]; pt=None
    while True:
        u=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records?page_size=500"
        if pt: u+="&page_token="+pt
        r=fs(u,None,at,"GET")
        recs.extend(r["data"].get("items",[]))
        pt=r["data"].get("page_token")
        if not r["data"].get("has_more"): break
    print(f"全表记录: {len(recs)}")

    inscope=[]
    for x in recs:
        f=x["fields"]
        d=f.get("来源日期")
        try: d=int(d)
        except: d=0
        if d<since: continue
        inscope.append(x)  # 重判范围内全部（覆盖旧值）
    print(f"近一个月(>= {since}) 待重判: {len(inscope)}")

    updates=[]
    cnt_yes=cnt_no=0
    for x in inscope:
        val,reason=judge(x["fields"])
        if val=="是": cnt_yes+=1
        else: cnt_no+=1
        updates.append({"record_id":x["record_id"],"fields":{"toB相关":val},
                        "_t":gettext(x["fields"].get("标题")),"_v":val,"_r":reason})
    print(f"判定: 是={cnt_yes} 否={cnt_no}")
    for u in updates:
        print(f"   [{u['_v']}] {u['_t'][:40]:<40} {u['_r']}")

    if apply and updates:
        url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/batch_update"
        recs2=[{"record_id":u["record_id"],"fields":u["fields"]} for u in updates]
        ok=0
        for i in range(0,len(recs2),20):
            r=fs(url,{"records":recs2[i:i+20]},at)
            if r.get("code")==0: ok+=len(r["data"]["records"])
            else: print("ERR",r); break
            time.sleep(0.3)
        print("已回写:",ok)
    elif not apply:
        print("(dry-run，加 --apply 回写)")

if __name__=="__main__": main()
