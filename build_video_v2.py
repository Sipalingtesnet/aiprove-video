"""Re-render the AIProve explainer with the jitter fix:
- Every still segment: pre-upscale 6x Lanczos (7680 wide) BEFORE zoompan,
  so zoompan's integer rounding happens at 7680px and is invisible at 1280x720.
- Subtle zoom 1.00 -> 1.06 (seg2: 1.00 -> 1.05, starting full-frame so the
  AIPROVE headline is never clipped).
- Segment 5 (terminal/rubric card) is reused unchanged; same voiceover.
- Output: 1280x720, 30fps, yuv420p, crf 18, exactly 60.00s.
Run: python3 build_video_v2.py  (writes aiprove-explainer-60s-v2.mp4)
"""
import os, subprocess, sys

D = "/home/hatch/workspace/aiprove/video"
STILLS = os.path.join(D, "stills")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
W, H, FPS, SEG = 1280, 720, 30, 10
FRAMES = FPS * SEG  # 300

def run(cmd):
    print("+", " ".join(cmd[:6]), "...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        sys.exit(f"FAILED: {' '.join(cmd[:8])}")
    return r

def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())

def overlay(text, y="h-110", fs=40):
    return (f"drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=black:"
            f"box=1:boxcolor=white@0.8:boxborderw=16:x=(w-text_w)/2:y={y}")

def zoompan_filter(zoom_end, out="1280x720"):
    # deterministic frame-index interpolation, centered floating-point coords
    return (f"zoompan=z='1+{zoom_end}*(on/{FRAMES})':d={FRAMES}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={out}:fps={FPS}")

def still_seg(still, out, text, zoom_end=0.06):
    vf = (f"scale=7680:-1:flags=lanczos,{zoompan_filter(zoom_end)},"
          f"format=yuv420p,{overlay(text)}")
    run(["ffmpeg", "-y", "-v", "error", "-i", still, "-vf", vf,
         "-frames:v", str(FRAMES), "-c:v", "libx264", "-preset", "medium", "-crf", "18", out])

# --- segments 1-4: supersampled Ken Burns stills ---
shots = [
    ("media-generation-aiprove-video-shot1-0-fa292fe5-6b0d-47f2-af1b-d23b12c54cad.webp",
     "WHO PAYS THE AGENT?", 0.06),
    ("media-generation-aiprove-video-shot2-0-fa65583c-917f-4513-abd2-e8a8661d0f9b.webp",
     "AIPROVE - OPEN BOUNTY ARENA", 0.05),  # seg2: gentler zoom, starts full-frame
    ("media-generation-aiprove-video-shot3-0-2d4ac74a-b2de-40bb-b9c7-c1c59ab8309e.webp",
     "SIX STAGES - ALL VISIBLE", 0.06),
    ("media-generation-aiprove-video-shot4-0-b3b31ae7-02e2-4e53-b320-c282c1c42a33.webp",
     "100K PROVE = 1 CREDIT - RETURNED WIN OR LOSE", 0.06),
]
for i, (f, text, zend) in enumerate(shots, 1):
    still_seg(os.path.join(STILLS, f), os.path.join(D, f"v2-seg{i}.mp4"), text, zend)

# --- segment 5: REUSE the existing clean terminal/rubric animation ---
run(["cp", os.path.join(D, "seg5.mp4"), os.path.join(D, "v2-seg5.mp4")])

# --- segment 6: poster mascot crop, upscaled 6x, then zoompan ---
vf6 = (f"crop=1120:630:0:560,scale=7680:-1:flags=lanczos,{zoompan_filter(0.06)},"
       f"format=yuv420p,{overlay('FREE TO ENTER IN BETA', y='36')},{overlay('AIPROVE.FUN', y='h-110')}")
run(["ffmpeg", "-y", "-v", "error", "-i", "/home/hatch/workspace/aiprove/art/poster.png",
     "-vf", vf6, "-frames:v", str(FRAMES), "-c:v", "libx264", "-preset", "medium",
     "-crf", "18", os.path.join(D, "v2-seg6.mp4")])

# --- concat ---
lst = os.path.join(D, "v2-segments.txt")
with open(lst, "w") as f:
    for i in range(1, 7):
        f.write(f"file 'v2-seg{i}.mp4'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
     "-c", "copy", os.path.join(D, "v2-video60.mp4")])

# --- narration: fit to exactly 60s (same track as v1) ---
narr = os.path.join(D, "narration60.mp3")
dur = probe_dur(narr)
print(f"narration duration: {dur:.2f}s", flush=True)
filt = []
if dur > 60.3:
    filt = [f"atempo={dur/60:.4f}"]
elif dur < 59.7:
    filt = [f"apad=whole_dur=60"]
af = ",".join(filt + ["atrim=0:60"]) if filt else "atrim=0:60"
run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(D, "v2-video60.mp4"), "-i", narr,
     "-filter:a", af, "-map", "0:v", "-map", "1:a", "-t", "60",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
     os.path.join(D, "aiprove-explainer-60s-v2.mp4")])

final = os.path.join(D, "aiprove-explainer-60s-v2.mp4")
print(f"FINAL: {final} duration={probe_dur(final):.2f}s size={os.path.getsize(final)} bytes")
for i in range(1, 7):
    p = os.path.join(D, f"v2-seg{i}.mp4")
    print(f"v2-seg{i}: {probe_dur(p):.2f}s {os.path.getsize(p)} bytes")
