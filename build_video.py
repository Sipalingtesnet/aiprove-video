"""Assemble the AIProve 60s explainer video:
6 x 10s segments (4 Ken Burns stills + 1 ffmpeg terminal/checklist card + 1 poster-mascot crop),
text overlays per storyboard, concat, mux narration fitted to exactly 60s.
Run: python3 build_video.py  (writes aiprove-explainer-60s.mp4 + segN.mp4 + video60.mp4)
"""
import json, subprocess, sys, os

D = "/home/hatch/workspace/aiprove/video"
STILLS = os.path.join(D, "stills")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
W, H, FPS, SEG = 1280, 720, 30, 10

def run(cmd, **kw):
    print("+", " ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        sys.exit(f"FAILED: {cmd[0]} {' '.join(cmd[1:4])}")
    return r

def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())

def overlay(text, y="h-110", fs=40):
    return (f"drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=black:"
            f"box=1:boxcolor=white@0.8:boxborderw=16:x=(w-text_w)/2:y={y}")

def still_seg(still, out, text):
    vf = (f"scale=2560:1440,"
          f"zoompan=z='1+0.1*on/299':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"format=yuv420p,{overlay(text)}")
    run(["ffmpeg", "-y", "-v", "error", "-i", still, "-vf", vf,
         "-frames:v", str(FPS * SEG), "-c:v", "libx264", "-preset", "medium", "-crf", "20", out])

# --- segments 1-4: Ken Burns stills ---
shots = [
    ("media-generation-aiprove-video-shot1-0-fa292fe5-6b0d-47f2-af1b-d23b12c54cad.webp", "WHO PAYS THE AGENT?"),
    ("media-generation-aiprove-video-shot2-0-fa65583c-917f-4513-abd2-e8a8661d0f9b.webp", "AIPROVE - OPEN BOUNTY ARENA"),
    ("media-generation-aiprove-video-shot3-0-2d4ac74a-b2de-40bb-b9c7-c1c59ab8309e.webp", "SIX STAGES - ALL VISIBLE"),
    ("media-generation-aiprove-video-shot4-0-b3b31ae7-02e2-4e53-b320-c282c1c42a33.webp", "100K PROVE = 1 CREDIT - RETURNED WIN OR LOSE"),
]
for i, (f, text) in enumerate(shots, 1):
    still_seg(os.path.join(STILLS, f), os.path.join(D, f"seg{i}.mp4"), text)

# --- segment 5: terminal + rubric card (pure ffmpeg) ---
def dt(text, x, y, fs=34, t0=0):
    en = f":enable='between(t,{t0},10)'" if t0 else ""
    return (f"drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=black:"
            f"x={x}:y={y}{en}")
vf5 = ",".join([
    overlay("GRADED IN THE OPEN", y="36"),
    "drawbox=x=636:y=120:w=4:h=520:color=black:t=4",
    dt("$ sandbox grade entry-042", 60, 140, t0=0.5),
    dt("run 1 - PASS", 60, 210, t0=1.5),
    dt("run 2 - PASS", 60, 280, t0=2.5),
    dt("score 1.42 - WINNER", 60, 350, t0=3.5),
    dt("RUBRIC", 700, 140, t0=4.5),
    dt("> explains hold-to-play", 700, 210, t0=5.5),
    dt("> reads human", 700, 280, t0=6.5),
    dt("> specific and accurate", 700, 350, t0=7.5),
    dt("7-day dispute window", 700, 420, t0=8.5),
])
run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
     "-i", f"color=c=0xf5f1e6:s={W}x{H}:r={FPS}:d={SEG}",
     "-vf", vf5, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
     os.path.join(D, "seg5.mp4")])

# --- segment 6: poster mascot crop + slow zoom ---
vf6 = (f"crop=1120:630:0:560,scale=1408:792,"
       f"zoompan=z='1+0.08*on/299':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
       f"format=yuv420p,{overlay('FREE TO ENTER IN BETA', y='36')},{overlay('AIPROVE.FUN', y='h-110')}")
run(["ffmpeg", "-y", "-v", "error", "-i", "/home/hatch/workspace/aiprove/art/poster.png",
     "-vf", vf6, "-frames:v", str(FPS * SEG), "-c:v", "libx264", "-preset", "medium",
     "-crf", "20", os.path.join(D, "seg6.mp4")])

# --- concat ---
lst = os.path.join(D, "segments.txt")
with open(lst, "w") as f:
    for i in range(1, 7):
        f.write(f"file 'seg{i}.mp4'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
     "-c", "copy", os.path.join(D, "video60.mp4")])

# --- narration: fit to exactly 60s ---
narr = os.path.join(D, "narration60.mp3")
dur = probe_dur(narr)
print(f"narration duration: {dur:.2f}s")
filt = []
if dur > 60.3:
    filt = [f"atempo={dur/60:.4f}"]
elif dur < 59.7:
    filt = [f"apad=whole_dur=60"]
# trim/pad precisely to 60.00s either way
af = ",".join(filt + ["atrim=0:60"]) if filt else "atrim=0:60"
run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(D, "video60.mp4"), "-i", narr,
     "-filter:a", af, "-map", "0:v", "-map", "1:a", "-t", "60",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
     os.path.join(D, "aiprove-explainer-60s.mp4")])

final = os.path.join(D, "aiprove-explainer-60s.mp4")
vd = probe_dur(final)
print(f"FINAL: {final} duration={vd:.2f}s size={os.path.getsize(final)} bytes")
for i in range(1, 7):
    p = os.path.join(D, f"seg{i}.mp4")
    print(f"seg{i}: {probe_dur(p):.2f}s {os.path.getsize(p)} bytes")
