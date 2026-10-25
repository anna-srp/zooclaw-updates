#!/usr/bin/env python3
"""Write updates/<date>/ files + insert sections into index.md / updates/index.md / changelog.md.
Usage: backfill_write.py YYYY-MM-DD YYYY-MM-DD
Reads /tmp/cls/<date>.json (classification) and /tmp/bf/<date>.json (raw commit data).
"""
import json, os, sys, datetime, re

ROOT = '/tmp/zu'
NL = chr(10)

TYPE_FM = {
    '新功能上线': '新功能',
    'Bug Fix': 'Bug Fix',
    '体验优化': '体验优化',
    '产品基础功能更新': '产品基础功能更新',
    'Skill 上架/更新': 'Skill 上架/更新',
    'Agent 上架/更新': 'Agent 上架/更新',
    '后端功能': '后端功能',
    '其他公告': '其他公告',
}
CHG_GROUP = {
    '新功能上线': '🆕 新功能',
    'Bug Fix': '🐛 Bug 修复',
    '体验优化': '✨ 体验优化',
    '产品基础功能更新': '🧩 产品基础功能更新',
    'Skill 上架/更新': '🛠 Skill 上架/更新',
    'Agent 上架/更新': '🤖 Agent 上架/更新',
    '后端功能': '🔧 基础能力',
    '其他公告': '📢 其他公告',
}
GROUP_ORDER = ['🆕 新功能', '✨ 体验优化', '🧩 产品基础功能更新', '🛠 Skill 上架/更新',
               '🤖 Agent 上架/更新', '🔧 基础能力', '📢 其他公告', '🐛 Bug 修复']
PRIO = {'P0': '高', 'P1': '高', 'P2': '中', 'P3': '低'}


def load(path, default=None):
    if not os.path.exists(path):
        return default
    return json.load(open(path))


def commit_index(bf):
    m = {}
    for repo, commits in bf['repos'].items():
        for c in commits:
            m[c['sha']] = (repo, c)
    return m


def write_day(date):
    cls = load('/tmp/cls/%s.json' % date)
    bf = load('/tmp/bf/%s.json' % date)
    if cls is None or bf is None:
        return None
    cmap = commit_index(bf)
    base = os.path.join(ROOT, 'updates', date)
    os.makedirs(base, exist_ok=True)
    written = []
    for item in cls:
        if item.get('internal_only'):
            continue
        sha = item['sha']
        if sha not in cmap:
            print('  WARN sha not in raw: %s' % sha[:10], file=sys.stderr)
            continue
        repo, c = cmap[sha]
        pr = item.get('pr_number') or c.get('pr_number')
        suffix = pr if pr else sha[:8]
        fname = '%s-%s.md' % (item['slug'], suffix)
        title = item['title']
        itype = item['info_type']
        parts = []
        parts.append('---')
        parts.append('title: "%s"' % title.replace('"', "'"))
        parts.append('type: "%s"' % TYPE_FM.get(itype, itype))
        parts.append('priority: "%s"' % PRIO.get(item['internal'], '中'))
        parts.append('date: "%s"' % date)
        parts.append('status: "待审核"')
        parts.append('channels: ""')
        parts.append('---')
        parts.append('')
        parts.append('# ' + title)
        parts.append('')
        parts.append('## 核心宣传点')
        parts.append('')
        parts.append(item['pitch'])
        parts.append('')
        parts.append('## 分级')
        parts.append('')
        parts.append('- 内部：%s' % item['internal'])
        parts.append('- 外部：%s' % item['external'])
        parts.append('- toB 相关：%s' % item['tob'])
        parts.append('- 发布状态：已合并待发版')
        if item.get('note'):
            parts.append('')
            parts.append('## 备注')
            parts.append('')
            parts.append(item['note'])
        parts.append('')
        parts.append('## 原始内容')
        parts.append('')
        parts.append('- 仓库：%s' % repo)
        parts.append('- SHA: `%s`' % sha)
        parts.append('- PR: %s' % ('#' + pr if pr else '（无）'))
        parts.append('- 作者：%s' % c['author'])
        parts.append('- 日期：%s' % c['date'])
        parts.append('')
        parts.append('### Commit Message')
        parts.append('')
        parts.append('```')
        parts.append(c['message'])
        parts.append('```')
        parts.append('')
        open(os.path.join(base, fname), 'w').write(NL.join(parts) + NL)
        written.append({'file': fname, 'title': title, 'type': itype,
                        'external': item['external'], 'pr': pr, 'pitch': item['pitch']})
    return written


def insert_section(path, date, body_lines, anchor_prefix='## '):
    """Insert a dated section into a newest-first file at the right chronological spot."""
    text = open(path).read()
    lines = text.split(NL)
    marker = anchor_prefix + date
    if marker in text:
        print('  section %s already in %s, skip' % (date, os.path.basename(path)))
        return False
    positions = [(i, l[len(anchor_prefix):].strip()) for i, l in enumerate(lines)
                 if l.startswith(anchor_prefix) and re.fullmatch(r'2026-\d\d-\d\d', l[len(anchor_prefix):].strip())]
    insert_at = None
    for i, d in positions:
        if d < date:
            insert_at = i
            break
    if insert_at is None:
        insert_at = len(lines)
    new = lines[:insert_at] + body_lines + [''] + lines[insert_at:]
    open(path, 'w').write(NL.join(new))
    return True


def main():
    start = datetime.date.fromisoformat(sys.argv[1])
    end = datetime.date.fromisoformat(sys.argv[2])
    cur = start
    total_files = 0
    while cur <= end:
        date = cur.isoformat()
        written = write_day(date)
        if written is None:
            print('%s: 缺 /tmp/cls 或 /tmp/bf，跳过' % date)
            cur += datetime.timedelta(days=1)
            continue
        total_files += len(written)
        print('%s: updates 写入 %d 条' % (date, len(written)))

        # --- root index.md ---
        if written:
            body = ['## ' + date, '']
            for w in written:
                label = '%s (#%s)' % (w['title'], w['pr']) if w['pr'] else w['title']
                body.append('- [%s](updates/%s/%s) — %s / 外部 %s'
                            % (label, date, w['file'], w['type'], w['external']))
        else:
            body = ['## ' + date, '', '- 当日无用户可感知更新']
        insert_section(os.path.join(ROOT, 'index.md'), date, body)

        # --- updates/index.md ---
        if written:
            ubody = ['## ' + date, '']
            for w in written:
                ubody.append('- [%s](%s/%s)' % (w['title'], date, w['file']))
        else:
            ubody = ['## ' + date, '', '- 当日无用户可感知更新']
        insert_section(os.path.join(ROOT, 'updates', 'index.md'), date, ubody)

        # --- changelog.md ---
        if written:
            groups = {}
            for w in written:
                groups.setdefault(CHG_GROUP.get(w['type'], '📢 其他公告'), []).append(w)
            cbody = ['## ' + date, '']
            for g in GROUP_ORDER:
                if g not in groups:
                    continue
                cbody.append('### ' + g)
                cbody.append('')
                for w in groups[g]:
                    label = '%s (#%s)' % (w['title'], w['pr']) if w['pr'] else w['title']
                    cbody.append('**%s**' % label)
                    cbody.append('')
                    cbody.append(w['pitch'] + '（已合并待发版）')
                    cbody.append('')
        else:
            cbody = ['## ' + date, '', '当日两仓无用户可感知更新。', '']
        insert_section(os.path.join(ROOT, 'changelog.md'), date, cbody)

        cur += datetime.timedelta(days=1)
    print('合计写入 updates 文件 %d 个' % total_files)


main()
