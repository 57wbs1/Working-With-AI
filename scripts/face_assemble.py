# -*- coding: utf-8 -*-
"""Join generated presenter segments into one muted video per chapter, trimmed so it lines up
   with assets/audio/<chapter>.mp3 to the frame. Usage: python3 scripts/face_assemble.py SEGDIR chapter [prefix.mp4=seconds]
   FACE_SIZE=960 FACE_OUT=<dir> give a sharper master for edited explainers (default: 480px into assets/video/face)."""
import json, os, pathlib, subprocess, sys
SIZE = int(os.environ.get('FACE_SIZE', '480'))
ROOT = pathlib.Path(__file__).resolve().parent.parent
SEG = pathlib.Path(sys.argv[1]).resolve(); ch = sys.argv[2]
pre = [(pathlib.Path(a.split('=')[0]).resolve(), float(a.split('=')[1])) for a in sys.argv[3:]]
plan = json.load(open(SEG/'plan.json'))[ch]
parts = pre + [(SEG/'vid'/(pathlib.Path(s['file']).stem + '.mp4'), s['secs']) for s in plan]
tmp = SEG/f'tmp{SIZE}'; tmp.mkdir(exist_ok=True); lst = []
for i,(p,secs) in enumerate(parts):
    assert p.exists(), p
    o = tmp/f'{ch}_{i:02d}.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-t',f'{secs:.3f}','-an',
                    '-vf',f'scale={SIZE}:{SIZE},fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast' if SIZE>480 else 'slow','-crf','20' if SIZE>480 else '27',str(o)],check=True)
    lst.append(o)
(tmp/f'{ch}.txt').write_text(''.join(f"file '{o}'\n" for o in lst))
out = pathlib.Path(os.environ.get('FACE_OUT', ROOT/'assets'/'video'/'face')).resolve()/f'{ch}.mp4'; out.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(tmp/f'{ch}.txt'),
                '-c:v','libx264','-preset','slow','-crf','27','-movflags','+faststart',str(out)],check=True)
d = lambda f: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)],capture_output=True,text=True).stdout)
print(f'{ch}: video {d(out):.2f}s vs audio {d(ROOT/"assets"/"audio"/(ch+".mp3")):.2f}s, {out.stat().st_size//1024} KB')
