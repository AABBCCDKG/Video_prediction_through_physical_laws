from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,csv,shutil,subprocess,hashlib
import numpy as np
import cv2
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'website/public'
EXPERIMENTS=ROOT/'experiments'
METHODS=['persistence','linear','quadratic','physics_constant_velocity','physics_constant_velocity_no_contacts','physics_deceleration','convlstm_seed0','convlstm_seed1','convlstm_seed2']

def encode(frames,path,fps):
 height,width=frames.shape[1:3]
 command=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(path)]
 process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 _,err=process.communicate(frames.tobytes())
 if process.returncode:raise RuntimeError(err.decode())
 cap=cv2.VideoCapture(str(path));count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));ok,first=cap.read();cap.release()
 assert ok and count==len(frames),(path,count,len(frames))
 return {'file':path.name,'frames':count,'width':width,'height':height,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
 (PUBLIC/'media').mkdir(parents=True,exist_ok=True);(PUBLIC/'data').mkdir(exist_ok=True);(PUBLIC/'downloads').mkdir(exist_ok=True)
 manifest=json.loads((EXPERIMENTS/'data/video_manifest.json').read_text())
 label_manifest={f"{r['scene_group']}_{r['variant']}":r for r in json.loads((EXPERIMENTS/'data/labels/manifest.json').read_text())}
 metrics=list(csv.DictReader((EXPERIMENTS/'results/formal/metrics.csv').open()))
 report=json.loads((EXPERIMENTS/'results/formal/report.json').read_text())
 scenes=[];tasks=[]
 for group in [9,10]:
  for variant in [1,2]:
   key=f'{group}_{variant}';row=next(r for r in manifest if r['scene_group']==group and r['variant']==variant)
   T=row['input_frames_in_repository'];H=60
   cap=cv2.VideoCapture(str(EXPERIMENTS/f'original/data/{group}/{variant}.mp4'));frames=[]
   while len(frames)<T+H:
    ok,frame=cap.read()
    if not ok:break
    frames.append(cv2.cvtColor(cv2.resize(frame,(640,360),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2RGB))
   cap.release();frames=np.stack(frames);H=len(frames)-T
   observed=frames[:T]
   with np.load(EXPERIMENTS/f'results/formal/rgb_forecasts_{key}.npz') as z:forecasts={m:z[m][:H] for m in METHODS}
   assets={'recorded':f'{key}-recorded.mp4'}
   tasks.append((frames,PUBLIC/'media'/assets['recorded'],row['fps']))
   for method in METHODS:
    future=np.stack([cv2.resize(f,(640,360),interpolation=cv2.INTER_NEAREST) for f in forecasts[method]])
    assets[method]=f'{key}-{method}.mp4';tasks.append((np.concatenate([observed,future]),PUBLIC/'media'/assets[method],row['fps']))
   cv2.imwrite(str(PUBLIC/f'media/{key}-poster.jpg'),cv2.cvtColor(frames[T-1],cv2.COLOR_RGB2BGR))
   events=[{'frame':e['frame'],'objects':e['objects'],'uncertainty':e.get('uncertainty_frames',2)} for e in label_manifest[key]['candidate_events'] if T<=e['frame']<T+H]
   per_metrics={}
   for item in metrics:
    if item['clip']==key:
     per_metrics.setdefault(item['horizon'],{})[item['method']]={k:float(item[k]) if item[k] else None for k in ['ADE_px','FDE_px','moving_ADE_px','RGB_MSE','PSNR_dB','label_coverage','prediction_miss_rate','overlap_pair_time_rate']}
   scenes.append({'id':key,'group':group,'variant':variant,'fps':row['fps'],'prefixFrames':T,'futureFrames':H,'totalFrames':T+H,'videos':assets,'poster':f'{key}-poster.jpg','events':events,'metrics':per_metrics,'source':f'https://github.com/AABBCCDKG/Video_prediction_through_physical_laws/blob/b596d003f737f40a62ea74a98adba001243bc9cb/data/{group}/{variant}.mp4'})
 with ThreadPoolExecutor(max_workers=4) as executor:encoded=list(executor.map(lambda args:encode(*args),tasks))
 (PUBLIC/'data/site-data.json').write_text(json.dumps({'scenes':scenes,'report':report,'assets':encoded,'dataset':{'groups':10,'videos':20,'frames':2499,'seconds':41.69,'train':[1,2,3,4,5,6],'validation':[7,8],'test':[9,10]},'revision':'b596d003f737f40a62ea74a98adba001243bc9cb','author':{'name':'Dong Wang','affiliation':'Purdue University','email':'wang6213@purdue.edu'}},indent=2))
 for source,target in [('paper/main.pdf','paper.pdf'),('paper/purdue-motion-neurips-source.zip','paper-source.zip'),('experiments/purdue-motion-experiments.zip','experiments.zip')]:shutil.copy2(ROOT/source,PUBLIC/'downloads'/target)
 (PUBLIC/'downloads/metrics.csv').write_text((EXPERIMENTS/'results/formal/metrics.csv').read_text())
 shutil.copy2(EXPERIMENTS/'results/formal/RESULTS.md',PUBLIC/'downloads/RESULTS.md')
 print(f'Generated and decoded {len(encoded)} H.264 videos; {sum(x["bytes"] for x in encoded)/1048576:.2f} MiB. Every comparison has the same observed prefix and 60 future frames.')
if __name__=='__main__':main()
