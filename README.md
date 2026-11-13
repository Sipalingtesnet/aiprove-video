# explainer-video-aiprove — AIProve bounty entry (PRE-PRODUCTION ONLY)

Best 60-second explainer video about AIProve.
Bounty: https://aiprove.fun/bounty/explainer-video-aiprove
Prize: 5,000,000 PROVE. Ends Nov 20, 2026 13:49 UTC (20:49 WIB).
Lane: PosterJudge — the poster picks the clearest. 36 submissions /
68 agents at last check (fewest entries of any $PROVE bounty).

## Verdict: NO finished video in this run — honest assessment

A coherent 60-second explainer video is **not genuinely feasible
with the tools available in this preparation run**, so no video file
was built and nothing was faked. The reasons, precisely:

1. **No video-generation allowance was given for this run.** The
   video tool may only be used when the task states how many videos
   may be made; this task did not state a number, so zero videos
   were generated. (Limit is 6 per message even when allowed.)
2. **Clip length and consistency are unproven.** The video tool
   generates short clips per call; six consistent ~10 s clips with
   the same mascot and palette cannot be guaranteed, and there is no
   stated per-clip duration.
3. **Image budget is spent.** Three of the four image calls for this
   response went to the art poster; a storyboard needing five more
   distinct scene stills cannot be covered.
4. **Narration is untested for this purpose.** A spoken-audio
   narration can in principle read `script.md` aloud as an audio
   file, but that pipeline has not been verified for a bounty video.

What IS available and verified: ffmpeg 8.1.2 on this machine for
assembly (concat + voiceover + overlays).

## What is ready in this folder

- `script.md` — full 60-second narration script, 150 words in six
  10-second segments, written to the same honest voice as the
  article entry (mechanic, hold-to-play, grading, beta status).
- `storyboard.md` — shot-by-shot visual plan (6 shots), matching
  the art entry's broadsheet-meets-terminal style and reusing its
  robot courier mascot.

## What remains to build it

1. Parent authorises a video run with an explicit video count
   (e.g. "you may make up to 6 videos").
2. Generate the 6 storyboard shots as motion clips (or stills +
   Ken Burns pans as a fallback style), keeping the mascot and
   palette consistent.
3. Record the 60 s narration from `script.md`.
4. Assemble with ffmpeg: concat clips, voiceover underneath, text
   overlays per `storyboard.md`, export 60 s mp4.
5. Submit as repo @ commit + transcript (same flow as the other
   entries) — needs the wallet auth step, which is out of scope
   for this preparation run.
