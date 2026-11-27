#!/usr/bin/env python3
"""Inspect source reels read-only, write only to workstream qa directory.
Usage: python3 [local render path] [exact/input.mp4 ...]
Reports actual streams, duration, SHA256, sampled decoded frame hashes and
whole-frame luma changes. Creates 270px view proof frames and an optional
safe-area guide; use human review for readability and platform UI preview.
"""
import argparse, hashlib, json, math, os, pathlib, re, shutil, statistics, subprocess, sys
Q=pathlib.Path(__file__).resolve().parent
BASE=Q.parent
EXT={'.mp4','.mov','.m4v','.webm'}
FRACTIONS=[.03,.14,.28,.42,.56,.70,.84,.96]
def run(args,data=None):
 r=subprocess.run(args,input=data,capture_output=True,timeout=70)
 if r.returncode: raise RuntimeError(r.stderr.decode(errors='replace').strip()[-1600:])
 return r.stdout,r.stderr
def probe(p):
 raw,_=run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate,pix_fmt,channels,sample_rate,duration:stream_side_data=rotation','-of','json',str(p)])
 return json.loads(raw)
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def inspect(p):
 data=probe(p)
 v=next((x for x in data.get('streams',[]) if x.get('codec_type')=='video'),None)
 a=[x for x in data.get('streams',[]) if x.get('codec_type')=='audio']
 if not v:raise ValueError("no video stream")
 f=data.get('format',{}); duration=float(v.get('duration') or f.get('duration') or 0)
 if not math.isfinite(duration) or duration<=0:raise ValueError("no positive duration")
 flags=[]; w,h=v['width'],v['height']; rot=next((x.get('rotation',0) for x in v.get('side_data_list',[]) if 'rotation' in x),0)
 dw,dh=(h,w) if abs(rot)%180==90 else (w,h)
 if (dw,dh)!=(1080,1920):flags.append('display is not 1080×1920')
 if v.get('codec_name')!='h264':flags.append('not H.264; verify native platform ingestion')
 if v.get('pix_fmt')!='yuv420p':flags.append('not 8-bit yuv420p; verify native preview')
 if duration<3:flags.append('duration under 3 seconds; verify hold time')
 srcsha=digest(p); out=Q/(re.sub('[^a-zA-Z0-9_.-]','-',p.stem)+'-'+srcsha[:8]);out.mkdir(exist_ok=True)
 frames=[]; prev=None
 for i,fraction in enumerate(FRACTIONS,1):
  t=min(max(0,duration-.15),duration*fraction)
  encoded,pngerr=run(['ffmpeg','-hide_banner','-loglevel','error','-ss',f'{t:.3f}','-i',str(p),'-map','0:v:0','-frames:v','1','-vf','scale=270:-2:flags=lanczos','-f','image2pipe','-c:v','png','-threads','1','pipe:1'])
  if not encoded:raise ValueError(f'no decoded video frame at {t:.3f}s')
  target=out/f'{i:02}-{t:.3f}s.png';target.write_bytes(encoded)
  pixels,_=run(['ffmpeg','-hide_banner','-loglevel','error','-i','pipe:0','-frames:v','1','-vf','scale=90:160:flags=area,format=gray','-f','rawvideo','-threads','1','pipe:1'],encoded)
  if len(pixels)!=90*160:raise ValueError('unexpected luma buffer size')
  changes=[abs(x-y) for x,y in zip(prev,pixels)] if prev else []
  frames.append({'at_seconds':round(t,3),'frame':str(target),'decoded_sha256':hashlib.sha256(encoded).hexdigest(),
   'mean_absolute_luma_delta':round(statistics.mean(changes),2) if changes else None,'pct_pixels_changed_ge_10':round(100*sum(x>=10 for x in changes)/len(changes),2) if changes else None})
  prev=pixels
 unique=len(set(x['decoded_sha256'] for x in frames))
 if unique<=1:flags.append('sampled frames identical; no motion evidence')
 else:
  n=sum((x['pct_pixels_changed_ge_10'] or 0)>=2 for x in frames)
  if n<2:flags.append('few substantial sampled changes; inspect motion and holds')
 # Assumed visual inspection guide only; never describes a specific app overlay.
 # 10% horizontal sides, 15% top, 19% bottom at 270x480 proof.
 if (dw,dh)==(1080,1920):
  for i in (0,3,6):
   if i>=len(frames):break
   s=frames[i]; guide=out/(pathlib.Path(s['frame']).stem+'-safe-guide.png')
   x,y=27,72; bx,by=243,389
   filt=f'drawbox=x={x}:y={y}:w={bx-x}:h={by-y}:color=yellow@0.9:t=2'
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',s['frame'],'-vf',filt,'-frames:v','1','-threads','1',str(guide)])
   s['safe_guide']=str(guide)
 volume=None
 if a:
  _,stderr=run(['ffmpeg','-hide_banner','-nostats','-loglevel','info','-i',str(p),'-map','0:a:0','-af','volumedetect','-vn','-f','null','-'])
  st=stderr.decode(errors='replace')
  volume={k:v for k,v in re.findall(r'(mean_volume|max_volume): ([-+\d.inf]+) dB',st)}
 return {'source':str(p),'source_sha256':srcsha,'bytes':p.stat().st_size,'duration_seconds':round(duration,3),'display_dimensions':[dw,dh],
 'video_stream':v,'audio_streams':a,'audio_measurement_first_track':volume,'sampled_unique_frames':unique,'frame_samples':frames,'flags':flags,
 'visual_QA_required':'Review proof at 270px and actual device; verify text reads quickly, labels remain on screen, motion communicates versus static-only, and safe area excludes controls. Audio presence/level is not licensing proof.'}
def main():
 par=argparse.ArgumentParser(description=__doc__);par.add_argument('files',nargs='*');a=par.parse_args()
 if not all(shutil.which(x) for x in ('ffmpeg','ffprobe')):raise SystemExit('ffmpeg and ffprobe are required')
 sources=[pathlib.Path(s).resolve() for s in a.files] if a.files else sorted(p for p in BASE.rglob('*') if p.is_file() and p.suffix.lower() in EXT and Q not in p.parents)
 reports=[]
 for p in sources:
  try:reports.append(inspect(p))
  except Exception as e:reports.append({'source':str(p),'error':str(e)})
 summary={'state':'checked' if reports else 'waiting_for_source_files','files':len(sources),'results':reports}
 (Q/'latest.json').write_text(json.dumps(summary,indent=2)+'\n')
 for r in reports:
  print(r.get('source'),r.get('display_dimensions'),r.get('duration_seconds'),'audio=',len(r.get('audio_streams',[])),'frames=',r.get('sampled_unique_frames'),r.get('flags',r.get('error')))
 if not reports:print('WAITING: no source reel files yet.')
 return int(any('error' in r for r in reports))
if __name__=='__main__':sys.exit(main())
