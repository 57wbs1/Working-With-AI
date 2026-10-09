# -*- coding: utf-8 -*-
"""WebVTT captions for a chapter: wording from scripts/vo/<chapter>.txt, timing from whisper word stamps.
   Usage: python3 scripts/make_vtt.py <chapter-id> <whisper.json>   e.g. ch03-agentic .work/.../ch03-agentic.json"""
import difflib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {'ch02-edge':'ch02_edge','ch03-agentic':'ch03_agentic','ch04-toolkit':'ch04_toolkit','ch05-skills':'ch05_skills',
         'ch06-plumbing':'ch06_plumbing','ch07-research':'ch07_research','ch08-decks':'ch08_decks'}
ch, wj = sys.argv[1], sys.argv[2]
script = ' '.join(l.strip() for l in open(ROOT/'scripts'/'vo'/(FILES[ch]+'.txt')) if l.strip()).split()
heard = [w for s in json.load(open(wj))['segments'] for w in s['words']]
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
a, b = [norm(w) for w in script], [norm(w['word']) for w in heard]
times = [None]*len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag in ('equal', 'replace'):            # spread the heard span over the script span
        for k in range(i1, i2):
            j = j1 + min(j2-j1-1, int((k-i1)*(j2-j1)/max(1, i2-i1))) if j2 > j1 else None
            if j is not None: times[k] = (heard[j]['start'], heard[j]['end'])
# fill gaps (inserted script words the ear missed) from neighbours
for k in range(len(times)):
    if times[k] is None:
        prev = next((times[p] for p in range(k-1, -1, -1) if times[p]), (0, 0))
        nxt = next((times[n] for n in range(k+1, len(times)) if times[n]), prev)
        times[k] = (prev[1], max(prev[1], nxt[0]))
cues, cur = [], []
for k, w in enumerate(script):
    cur.append(k)
    text = ' '.join(script[i] for i in cur)
    end_here = re.search(r'[.?!,:;]$', w) and len(text) > 18
    if len(text) > 40 or end_here or k == len(script)-1:
        cues.append((times[cur[0]][0], times[cur[-1]][1], text)); cur = []
fmt = lambda t: '%02d:%02d:%06.3f' % (t//3600, (t%3600)//60, t%60)
out = ROOT/'assets'/'video'/'explainer'/f'{ch}.vtt'
with open(out, 'w', encoding='utf-8') as f:
    f.write('WEBVTT\n\n')
    for i, (s, e, t) in enumerate(cues, 1):
        e = max(e, s + 0.6)
        if i < len(cues): e = min(e, cues[i][0])
        f.write(f'{i}\n{fmt(s)} --> {fmt(e)}\n{t}\n\n')
print(ch, len(cues), 'cues ->', out.relative_to(ROOT))
