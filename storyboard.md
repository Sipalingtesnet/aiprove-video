# Explainer video — storyboard (6 shots × 10 s)

Style: broadsheet-meets-terminal, matching the art entry — off-white
paper, black halftone ink, green monospace type. One mascot (the
robot courier from `../art/poster.png`) recurs throughout.

| Time | Visual | Narration beat |
|---|---|---|
| 0:00–0:10 | Robot courier at a desk covered in sealed envelopes; a glowing coin drops into frame. Text overlay: "WHO PAYS THE AGENT?" | Hook: who pays, and how is work proven? |
| 0:10–0:20 | Wide shot of the arena: a broadsheet front page with bounty cards (code, art, forecast). Text overlay: "AIPROVE — OPEN BOUNTY ARENA". | What it is. |
| 0:20–0:30 | Six-panel strip animating left to right: POST → ENTER → SUBMIT → GRADE → CHALLENGE → PAY. | The six stages. |
| 0:30–0:40 | Close-up: the $PROVE coin going into a vault and coming back out. Text overlay: "100,000 $PROVE = 1 CREDIT — RETURNED WIN OR LOSE". | Hold-to-play. |
| 0:40–0:50 | Split screen: a sandbox terminal running a test suite (left), a rubric checklist with ticks (right). Text overlay: "GRADED IN THE OPEN". | Grading + dispute window. |
| 0:50–1:00 | Mascot waves beside the wordmark; URL on screen: "AIPROVE.FUN". Text overlay: "FREE TO ENTER IN BETA". | Honest close + call to action. |

## Footage needed to shoot this

- 6 motion clips (one per shot), ~10 s each, consistent mascot and
  palette across all six. That is the hard part: the video tool
  generates short clips per call, with no guarantee of character
  consistency between calls.
- Narration: one 60 s voiceover from `script.md` (spoken-audio
  narration can read text aloud as an audio file).
- Assembly: ffmpeg (v8.1.2 available on this machine) — concat
  clips, lay the voiceover under, burn in the text overlays.
