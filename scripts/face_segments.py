# -*- coding: utf-8 -*-
"""Split each chapter's narration at natural pauses into segments of at most MAXS seconds,
   for audio-driven presenter video (Wan 2.7 takes 2-15 s). Writes the cut audio and a plan.
   Usage: python3 scripts/face_segments.py OUTDIR [chapter[=start_seconds] ...]
   A start offset skips audio that already has presenter video (e.g. ch02-edge=13.0)."""
import json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
PICK = dict((a.split('=')[0], float(a.split('=')[1]) if '=' in a else 0.0) for a in sys.argv[2:])
MAXS, MINS = 15.0, 4.0
CH = ['ch02-edge','ch03-agentic','ch04-toolkit','ch05-skills','ch06-plumbing','ch07-research','ch08-decks']

def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
def pauses(p):
    e = subprocess.run(['ffmpeg','-hide_banner','-i',p,'-af','silencedetect=noise=-35dB:d=0.2','-f','null','-'],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', e)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', e)]
    return [(a+b)/2 for a,b in zip(st,en) if a > 0.5]          # cut in the middle of each pause

plan = {}
for c in [c for c in CH if not PICK or c in PICK]:
    src = str(ROOT/'assets'/'audio'/(c+'.mp3')); D = dur(src); cuts = [PICK.get(c, 0.0)]
    mids = pauses(src)
    while D - cuts[-1] > MAXS:
        ok = [m for m in mids if MINS <= m - cuts[-1] <= MAXS]
        cuts.append(max(ok) if ok else cuts[-1] + MAXS)         # latest pause that keeps the segment legal
    cuts.append(D)
    segs = []
    for i,(a,b) in enumerate(zip(cuts, cuts[1:])):
        f = OUT/f'{c}_{i:02d}.mp3'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{a:.3f}','-to',f'{b:.3f}','-i',src,'-c:a','libmp3lame','-b:a','128k',str(f)],check=True)
        segs.append({'file': str(f), 'start': round(a,3), 'end': round(b,3), 'secs': round(b-a,3)})
    plan[c] = segs
old = json.load(open(OUT/'plan.json')) if (OUT/'plan.json').exists() else {}
old.update(plan); json.dump(old, open(OUT/'plan.json','w'), indent=1)
import math
tot = sum(math.ceil(s['secs']) for v in plan.values() for s in v)
print({c: len(v) for c,v in plan.items()}, 'segments; billed seconds', tot, '-> credits at 1.5/s:', tot*1.5)
