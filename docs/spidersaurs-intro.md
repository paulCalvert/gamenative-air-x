# Spidersaurs: swapping the intro video

**Outcome:** the game went from frozen at launch to fully playable at 35-39 fps.

## Symptom

After launch: music, a dark screen, no progress. Months earlier this had been written off as "needs more than 4 GB of RAM". Live monitoring disproved that:

- RAM use 360-840 MB with memory to spare
- 3+ CPU cores pegged
- GPU at 0%

When audio plays, the GPU is idle and the CPU is pegged, something is being decoded in software.

## Cause

The intro is a VP8/VP9 video (`data/movie_intro.pak` → `intro.ivf` + `intro.mp3`). The game decodes it on the CPU, and under x86→ARM translation that is far too slow. Changing translators (Box64, FEXCore), DXVK versions and GPU drivers didn't help. Renaming the pak made the game quit after the logo.

## Fix

Paul proposed swapping the video the game loads for a short, black clip. To do that the pak had to be rebuilt, and its format wasn't documented, so it was worked out from the file:

```
u32 directory size, u32 entry count
per entry: "FILELINK_____END", u32 offset (from data start), u32 size, name ("movie_intro:intro.ivf")
data: each file preceded by a 64-byte "MANAGEDFILE_DATABLOCK..." marker, padded with '?' to 16 bytes
trailer: 48 x '?'
```

[`tools/shorten_pak.py`](../tools/shorten_pak.py) rebuilds a pak. With `--verify` it rebuilds unchanged and checks the result is byte-identical to the original. That check passed for both paks before anything was trimmed. Without `--verify` it keeps the first ~1 s of each `.ivf` (30 frames) and `.mp3` (40 frames).

```sh
python -I shorten_pak.py movie_intro.pak movie_intro.pak.check --verify   # prints identical: True
python -I shorten_pak.py movie_intro.pak movie_intro.short.pak
```

Both video paks were trimmed: `movie_intro.pak` and `wf_splash_screen.pak` (the studio logo). A scan of all 259 pak manifests found no other videos, since the cutscenes are drawn by the engine. The originals were kept as `.orig` next to the game files.

## Notes

- A Steam "verify files" or reinstall restores the long intro. Run the tool again afterwards.
- The general lesson, reused later: **audio playing + black screen + CPU pegged + GPU 0** → look for a software-decoded video (`.ivf`, `.webm`, `.bik`) and shorten it.
- Config: [`configs/working/spidersaurs.json`](../configs/working/spidersaurs.json).
