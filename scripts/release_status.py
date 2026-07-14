#!/usr/bin/env python3
"""
release_status.py — 判定 commit / PR 是否已随正式发布(release)上线。

用途：ZooClaw 每日同步的「发布状态」判定步骤。
判定逻辑：拿每条 commit 的 SHA/PR，去和对应仓库最新的【正式 release tag】(非 draft/非 prerelease)
比对——commit 被最新正式 release 包含 = 已上线；晚于 release = 已合并待发版。

关键规则（实操经验，勿改）：
  1. ecap-workspace（网页平台）：正式前端发布 tag 形如 `ecap-vX.Y.Z-release`，取最新那个做 HEAD 参照。
     后端是 `service-v*`，如需也可并入；但用户在网页上看到的以 `ecap-*` 为准。
  2. ecap-agent-pack：正式发布 tag 形如 `vX.Y.Z-release`（排除 `-beta.*`），取最新那个。
  3. ecap-skills：⚠️ Skill 走 ClawHub 独立分发，仓库 release tag 极不可靠（常年停在很旧版本）。
     Skill 类【不要】用本脚本的 release tag 判定，改用 ClawHub：
       openclaw skills verify <slug>  →  看返回 JSON 的 version + createdAt（发布时间）。
       若 ClawHub 最新发布时间 >= 该 commit 日期 且版本已含本次改动 → 已上线；否则 待发版。
     另外注意 PPT 这类 Skill 可能额外依赖【运行时镜像打包】(如 @zooclaw/web-search)，
     即使 ClawHub 发布了，也要等运行时镜像重建才真正生效——存疑时标「已合并待发版」并在备注注明。

用法：
  python3 release_status.py <owner/repo> <sha>
  → 打印 已上线 / 已合并待发版 / 未知

Token：从 zooclaw-updates 仓库的 git remote URL 里解析（user:token@github.com）。
"""
import json, urllib.request, urllib.error, subprocess, re, sys, os, time

def get_token():
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        remote = subprocess.check_output(
            ["git", "-C", os.path.join(here, ".."), "remote", "get-url", "origin"]
        ).decode().strip()
        m = re.search(r'https://[^:/]+:([^@]+)@', remote)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None

TOK = get_token()

def gh(path):
    for _ in range(3):
        req = urllib.request.Request(
            "https://api.github.com" + path,
            headers={"Authorization": f"Bearer {TOK}", "Accept": "application/vnd.github+json"},
        )
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                time.sleep(2); continue
            return {"__error__": e.code, "path": path}
    return {"__error__": "retry"}

def prod_ref_tag(repo):
    """返回该仓库当前正式发布 HEAD 的 tag（用于 shipped 判定）。"""
    rel = gh(f"/repos/{repo}/releases?per_page=50")
    if isinstance(rel, dict):
        return None
    prod = [x for x in rel if not x.get("draft") and not x.get("prerelease")]
    prod.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    if not prod:
        return None
    if repo.endswith("ecap-workspace"):
        for x in prod:
            if x["tag_name"].startswith("ecap-v"):
                return x["tag_name"]
    if repo.endswith("ecap-agent-pack"):
        for x in prod:
            if x["tag_name"].endswith("-release") and "-beta" not in x["tag_name"]:
                return x["tag_name"]
    return prod[0]["tag_name"]

def is_shipped(repo, sha):
    tag = prod_ref_tag(repo)
    if not tag or not sha:
        return None, tag
    cmp = gh(f"/repos/{repo}/compare/{sha}...{tag}")
    if isinstance(cmp, dict) and cmp.get("__error__"):
        return None, tag
    # tag 领先或等于 sha => tag 包含该 commit => 已上线
    return (cmp.get("status") in ("ahead", "identical")), tag

def label(repo, sha):
    if "ecap-skills" in repo:
        return "未知"  # skills 用 ClawHub 判，见脚本头注释
    shipped, tag = is_shipped(repo, sha)
    if shipped is True:
        return "已上线"
    if shipped is False:
        return "已合并待发版"
    return "未知"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: release_status.py <owner/repo> <sha>", file=sys.stderr)
        sys.exit(2)
    print(label(sys.argv[1], sys.argv[2]))
