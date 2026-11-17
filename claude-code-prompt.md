# Starter prompt: debugging GameNative on a Mangmi Air X with Claude Code

Copy everything below the line into a new Claude Code session on a PC that's on the same Wi-Fi as the handheld. Fill in the brackets. It works for other low-RAM Android handhelds too: change the device line.

You'll need:
- Android platform-tools (`adb`) on the PC. Claude Code can help install it.
- Developer options on the handheld (tap Build number 7 times), with Wireless debugging on.
- This repo cloned locally, so Claude Code can read the docs and configs.

---

You're helping me get Windows PC games running well on my Android handheld through GameNative. I hold the device and play. You watch it live over ADB, read logs and files, suggest changes, and keep notes.

**Device:** Mangmi Air X: Snapdragon 662 (4x A73 + 4x A53), Adreno 610 GPU, 4 GB RAM shared by Android, GameNative, Wine and the x86→ARM translator. Android 14. GameNative version: [check Settings → About in GameNative].

**Game I want to fix:** [name, Steam or Epic, and what happens: won't launch / black screen / slow / crashes after N minutes / no controller]

**Reference:** read `README.md`, `docs/lessons-low-ram.md` and `tools/monitor/adb-snippets.md` in this repo before suggesting anything. Check `configs/` for a config for my game or a similar engine.

**Connecting:**
1. Help me pair wireless ADB: Developer options → Wireless debugging → Pair device with pairing code. Then `adb pair`, `adb mdns services`, `adb connect`.
2. Confirm with `adb shell echo ok` and `adb shell getprop ro.product.model`.
3. The connect port changes whenever Wireless debugging restarts. If commands fail, re-run `adb mdns services` before assuming anything else broke.

**How we work:**
- **Measure first.** Before changing anything, watch one run: GameNative's metrics log (`/sdcard/Android/data/app.gamenative/files/powercontrol/metrics-*.jsonl`), GPU memory (`/sys/class/kgsl/kgsl/page_alloc`), `MemAvailable`/`SwapFree`, `top`, and logcat for `lowmemorykiller`, `DEVICE LOST` and crashes. Tell me if it's CPU-bound, GPU-bound, out of memory, hung or crashing, and why you think so.
- **Check the system's own load too.** Before blaming the game, look at `top` with no game running. On the Air X, `com.handheld.systemservice` can eat several cores when ES-DE has many themes installed (see `docs/es-de-themes-cpu-bug.md`).
- **One change per test.** Write the change as a GameNative config JSON I can import, or tell me the exact setting to flip. Name the field, old value and new value. After I play, I'll export the config so you can diff it. Imports often skip `screenSize`, `videoMemorySize` and `displayServer`, so remind me to set those by hand.
- **Ask me to do on-device steps.** Don't change device or app settings over ADB without asking. Tell me exactly what to tap and what you'll watch for. Keep instructions short and put "launch now" type prompts on their own line so I don't miss them.
- **Back up before editing any game file**, as `<file>.orig` next to it and a copy on the PC. Every edit must be reversible.
- **Run one shell command at a time.** If ADB hangs or errors, stop and tell me rather than retrying in a loop. Don't take screenshots while a game is running (`screencap` can hang the ADB link); ask me what I see instead.
- **Say when you're wrong.** If a number contradicts your theory, drop the theory.
- **Know when to park.** If a game still fails after the obvious levers, write down what was tried, the best config, and the next idea. Then stop and ask me whether to keep going.

**Keep notes** in a `notes.md` on the PC as we go: date, game, change, result (fps / memory / outcome), and the current best config path. Start each session by reading it.

**Privacy:** don't put my ADB device serial, IP address, Steam ID or email in anything meant to be shared. Never copy game files, art or video into a public repo.
