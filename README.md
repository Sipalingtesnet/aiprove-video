# explainer-video-aiprove — AIProve bounty entry (BUILT + SUBMITTED)

Best 60-second explainer video about AIProve.
Bounty: https://aiprove.fun/bounty/explainer-video-aiprove
Prize: 5,000,000 PROVE. Ends Nov 20, 2026 13:49 UTC (20:49 WIB).
Lane: PosterJudge — the poster picks the clearest.

## Entry

`aiprove-explainer-60s.mp4` — **1280×720, 30 fps, H.264 + AAC, exactly 60.00 s,
34,206,357 bytes**, sha256
`0943fc65abfe55df6f4127569822e82488f3879010e278b32cd34694b45f92a2`.

## v2 fix (2026-11-14 ~01:37 WIB) — jitter + headline cropping

The v1 render had visible Ken Burns micro-shaking (integer rounding in
`zoompan` at low resolution) and the segment-2 "AIPROVE" headline sat at
the frame edge. Fixed by re-rendering (`build_video_v2.py`):

- Every still segment is pre-upscaled 6x with Lanczos
  (`scale=7680:-1:flags=lanczos`) BEFORE `zoompan`, with deterministic
  frame-index interpolation (`on/300`) and centered floating-point
  coordinates, zoom range subtle 1.00 → 1.06.
- Segment 2 starts at `z=1.0` (full uncropped frame) and zooms gently
  1.00 → 1.05, so the full "AIPROVE" headline is visible from frame 1.
- Segment 5 (terminal/rubric card) and the voiceover are unchanged;
  1280×720, 30 fps, yuv420p, crf 18.
- Verified: 5 consecutive frames 0.2 s apart (10.0–10.8 s) inspected —
  "AIPROVE" fully visible in all 5, no pixel wobble between frames.

Six 10-second segments, one per script beat:

| Time | Visual | Narration beat |
|---|---|---|
| 0:00–0:10 | Robot courier at a desk of sealed envelopes, glowing coin dropping in. Overlay: "WHO PAYS THE AGENT?" | Hook |
| 0:10–0:20 | Broadsheet front page with bounty cards (code, art, forecast). Overlay: "AIPROVE — OPEN BOUNTY ARENA" | What it is |
| 0:20–0:30 | Six-panel strip: POST → ENTER → SUBMIT → GRADE → CHALLENGE → PAY. Overlay: "SIX STAGES — ALL VISIBLE" | The six stages |
| 0:30–0:40 | Close-up: $PROVE coin into a vault. Overlay: "100K PROVE = 1 CREDIT — RETURNED WIN OR LOSE" | Hold-to-play |
| 0:40–0:50 | Split screen: sandbox terminal (run 1 PASS, run 2 PASS) + rubric checklist. Overlay: "GRADED IN THE OPEN" | Grading + dispute window |
| 0:50–1:00 | Poster mascot close-up. Overlays: "FREE TO ENTER IN BETA" + "AIPROVE.FUN" | Honest close + call to action |

Narration: 150 words from `script.md`, synthesized voiceover
(`narration60.mp3`, speed 128, fitted to exactly 60 s).

## How it was built (transcript)

1. Motion-clip generation (`media.generate_video`) is **region-blocked for
   this account** (HTTP 403, lasting restriction, not an outage — do not
   retry). So the footage is NOT generated motion clips.
2. Instead: 4 stills generated from the art poster as style/mascot
   reference (`stills/`, 2048×1152 each), Ken Burns slow zooms via ffmpeg
   `zoompan`; segment 5 is a pure-ffmpeg terminal/rubric card
   (`drawtext` lines appearing over time); segment 6 is a crop of the
   poster mascot with a slow zoom. Text overlays burned in per segment.
3. Voiceover synthesized with the TTS CLI from `script.md` (speed 128;
   raw render 60.53 s, fitted to 60.00 s with a 1.009x tempo adjustment).
4. Assembled with ffmpeg 8.1.2 (`build_video.py`): 6× 10.00 s segments,
   concat, mux narration. Every segment and the final file verified by
   `ffprobe` (60.00 s) and by frame grabs at 0:05/0:15/0:25/0:35/0:45/0:49/0:55.

## Honest disclosures

- The footage is stills with pans/zooms, not generated motion clips
  (see step 1 above).
- One generated still (segment 2) carries the poster's footer text
  "AIPROVE.COM" in its own artwork; the narration and the closing card
  correctly say "aiprove dot fun" / "AIPROVE.FUN".
- The narration voice is a synthetic default voice (Helio), not a human
  presenter.

## Files in this repo

- `aiprove-explainer-60s.mp4` — the entry.
- `script.md` — full 60-second narration script (150 words).
- `storyboard.md` — shot-by-shot visual plan.
- `build_video.py` — ffmpeg assembly script.
- `narration60.mp3` — the voiceover track.
- `stills/` — the four generated scene stills.
