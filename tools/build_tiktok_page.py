#!/usr/bin/env python3
"""Build the phone page that lists the TikTok queue: each clip with a player, a Download button and a
one-tap "Copy caption" button. Reads <dir>/clips.json: [{"file","caption","streamer","score","added","post_at"}]
(newest first) and writes <dir>/index.html."""
import html
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
clips = json.loads((d / "clips.json").read_text())
cards = []
for i, c in enumerate(clips):
    cap = html.escape(c["caption"])
    cards.append(f"""
<div class="card">
  <div class="meta"><b>{html.escape(c.get('streamer', ''))}</b> · score {c.get('score', '?')}/10 · added {html.escape(c.get('added', ''))}
  {f"· <span class='when'>post at {html.escape(c['post_at'])}</span>" if c.get('post_at') else ''}</div>
  <video src="{html.escape(c['file'])}" controls playsinline preload="metadata"></video>
  <div class="row">
    <a class="btn dl" href="{html.escape(c['file'])}" download>⬇️ Download video</a>
    <button class="btn cp" onclick="cp({i}, this)">📋 Copy caption</button>
  </div>
  <textarea id="c{i}" readonly>{cap}</textarea>
</div>""")
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>ThViceCity · TikTok queue</title>
<style>
body{{margin:0;background:#120a24;color:#f3eaff;font:16px -apple-system,system-ui,sans-serif}}
h1{{font-size:20px;margin:16px}} p.note{{margin:0 16px 12px;color:#bfb3d9;font-size:14px}}
.card{{background:#1e1236;margin:12px;border-radius:16px;padding:12px;box-shadow:0 2px 10px #0006}}
.meta{{font-size:14px;color:#d6c8f5;margin-bottom:8px}} .when{{color:#ff8fd0}}
video{{width:100%;max-height:70vh;border-radius:12px;background:#000}}
.row{{display:flex;gap:8px;margin:10px 0}}
.btn{{flex:1;text-align:center;padding:12px;border-radius:12px;border:0;font-size:16px;font-weight:600;text-decoration:none}}
.dl{{background:#ff2e97;color:#fff}} .cp{{background:#2ee6ff;color:#120a24}}
textarea{{width:100%;box-sizing:border-box;min-height:84px;border-radius:10px;border:0;padding:8px;font-size:15px;background:#2a1a4a;color:#f3eaff}}
</style></head><body>
<h1>🌴 TikTok queue ({len(clips)} clips)</h1>
<p class="note">Newest first. Tap Download, then post the video in TikTok and paste the caption. Updated automatically every hour.</p>
{''.join(cards) if cards else '<p class="note">No clips yet — check back after the next run.</p>'}
<script>
function cp(i,b){{const t=document.getElementById('c'+i);t.select();t.setSelectionRange(0,99999);
navigator.clipboard?navigator.clipboard.writeText(t.value).then(()=>ok(b),()=>{{document.execCommand('copy');ok(b)}}):(document.execCommand('copy'),ok(b));}}
function ok(b){{const o=b.textContent;b.textContent='✅ Copied';setTimeout(()=>b.textContent=o,1500)}}
</script></body></html>"""
(d / "index.html").write_text(page)
print(f"built {d / 'index.html'} with {len(clips)} clips")
