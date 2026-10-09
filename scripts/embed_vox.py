# -*- coding: utf-8 -*-
"""Re-embed VOXSCENES (from scenes.py) and VOXLINES (from vo/*.txt) into course.html.
   Run after editing either source; the course never reads these files at runtime."""
import json, re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from scenes import SCENES

FILES = {'edge':'ch02_edge','agentic':'ch03_agentic','pricing':'ch04_toolkit','skills':'ch05_skills',
         'plumbing':'ch06_plumbing','research':'ch07_research','decks':'ch08_decks'}
scenes = {k:[list(x) for x in v] for k,v in SCENES.items()}
lines = {k:[l.strip() for l in open(HERE/'vo'/(f+'.txt'), encoding='utf-8') if l.strip()] for k,f in FILES.items()}

page = HERE.parent/'course.html'
s = page.read_text(encoding='utf-8')
pat_s = re.compile(r'var VOXSCENES = \{.*?\};\n')
pat_l = re.compile(r'var VOXLINES  = \{.*?\};\n')
assert len(pat_s.findall(s)) == 1 and len(pat_l.findall(s)) == 1, 'expected one VOXSCENES and one VOXLINES'
s = pat_s.sub(lambda m: 'var VOXSCENES = ' + json.dumps(scenes, ensure_ascii=False) + ';\n', s, count=1)
s = pat_l.sub(lambda m: 'var VOXLINES  = ' + json.dumps(lines, ensure_ascii=False) + ';\n', s, count=1)
page.write_text(s, encoding='utf-8')
print('embedded', sum(map(len, scenes.values())), 'scenes and', sum(map(len, lines.values())), 'transcript lines')
