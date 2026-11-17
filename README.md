# gamenative-air-x

14 Windows PC games running on a [Mangmi Air X](https://mangmi.com/products/mangmi-air-x) through GameNative, plus the configs, tools and troubleshooting notes that got them there.

## Contents

- [The device and the problem](#the-device-and-the-problem)
- [Results](#results)
- [How it was done](#how-it-was-done)
  - [1. Live telemetry over Wi-Fi](#1-live-telemetry-over-wi-fi)
  - [2. A firmware bug was eating half the CPU](#2-a-firmware-bug-was-eating-half-the-cpu)
  - [3. Game by game](#3-game-by-game)
    - [Spidersaurs](#spidersaurs)
    - [Sine Mora EX](#sine-mora-ex)
    - [Cave Story+](#cave-story)
    - [Bad North](#bad-north)
    - [Kingdom: New Lands](#kingdom-new-lands)
    - [Gravity Circuit](#gravity-circuit)
    - [Swords & Bones](#swords--bones)
    - [Mago](#mago)
    - [Megabonk](#megabonk)
    - [Retro City Rampage DX](#retro-city-rampage-dx)
    - [Star Wars Jedi Knight: Dark Forces II](#star-wars-jedi-knight-dark-forces-ii)
    - [Cast n Chill](#cast-n-chill)
    - [Wizordum](#wizordum)
    - [Undertale](#undertale)
  - [4. Knowing when to stop](#4-knowing-when-to-stop)
- [What's next](#whats-next)
- [What's here](#whats-here)
- [Caveats](#caveats)
- [Credits](#credits)
- [Try it yourself with Claude Code](#try-it-yourself-with-claude-code)

## The device and the problem

The Air X is an Android handheld built for retro emulation: Snapdragon 662, Adreno 610 GPU, **4 GB RAM shared by everything**, Android 14. [GameNative](https://github.com/utkarshdalal/GameNative) runs Steam and Epic games on Android by stacking several layers:
- Wine/Proton
- an x86→ARM translator (FEX or Box64)
- DXVK (DirectX→Vulkan)
- Turnip (an open Vulkan driver for Adreno)

GameNative is designed for more powerful Android devices than the Mangmi Air X. Out of the box, most games ran badly or not at all on this hardware.

Done over about a week (Nov 11-17, 2026) with Claude Code. I held the device, tested and made the calls. Claude Code watched the device live over wireless ADB, read logs and game files, built configs and wrote things down.

## Results

**Working**

- <a href="https://store.steampowered.com/app/688420/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/688420/header.jpg" width="120" alt="Bad North: Jotunn Edition"></a> [Bad North: Jotunn Edition](https://store.steampowered.com/app/688420/)
- <a href="https://store.steampowered.com/app/3483740/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/3483740/header.jpg" width="120" alt="Cast n Chill"></a> [Cast n Chill](https://store.steampowered.com/app/3483740/)
- <a href="https://store.steampowered.com/app/200900/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/200900/header.jpg" width="120" alt="Cave Story+"></a> [Cave Story+](https://store.steampowered.com/app/200900/)
- <a href="https://store.steampowered.com/app/858710/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/858710/header.jpg" width="120" alt="Gravity Circuit"></a> [Gravity Circuit](https://store.steampowered.com/app/858710/)
- <a href="https://store.steampowered.com/app/496300/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/496300/header.jpg" width="120" alt="Kingdom: New Lands"></a> [Kingdom: New Lands](https://store.steampowered.com/app/496300/)
- <a href="https://store.steampowered.com/app/1098280/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1098280/header.jpg" width="120" alt="Mago"></a> [Mago](https://store.steampowered.com/app/1098280/)
- <a href="https://store.steampowered.com/app/3405340/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/3405340/header.jpg" width="120" alt="Megabonk"></a> [Megabonk](https://store.steampowered.com/app/3405340/)
- <a href="https://store.steampowered.com/app/204630/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/204630/header.jpg" width="120" alt="Retro City Rampage DX"></a> [Retro City Rampage DX](https://store.steampowered.com/app/204630/)
- <a href="https://store.steampowered.com/app/606730/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/606730/header.jpg" width="120" alt="Sine Mora EX"></a> [Sine Mora EX](https://store.steampowered.com/app/606730/)
- <a href="https://store.steampowered.com/app/1191620/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1191620/header.jpg" width="120" alt="Spidersaurs"></a> [Spidersaurs](https://store.steampowered.com/app/1191620/)
- <a href="https://store.steampowered.com/app/32380/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/32380/header.jpg" width="120" alt="Star Wars Jedi Knight: Dark Forces II"></a> [Star Wars Jedi Knight: Dark Forces II](https://store.steampowered.com/app/32380/)
- <a href="https://store.steampowered.com/app/1534700/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1534700/header.jpg" width="120" alt="Swords & Bones"></a> [Swords & Bones](https://store.steampowered.com/app/1534700/)
- <a href="https://store.steampowered.com/app/391540/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/391540/header.jpg" width="120" alt="Undertale"></a> [Undertale](https://store.steampowered.com/app/391540/)
- <a href="https://store.steampowered.com/app/1715590/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1715590/header.jpg" width="120" alt="Wizordum"></a> [Wizordum](https://store.steampowered.com/app/1715590/)

**Parked**

- <a href="https://store.steampowered.com/app/296970/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/296970/header.jpg" width="120" alt="Renowned Explorers: International Society"></a> [Renowned Explorers: International Society](https://store.steampowered.com/app/296970/)
- <a href="https://store.steampowered.com/app/389140/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/389140/header.jpg" width="120" alt="Horizon Chase Turbo"></a> [Horizon Chase Turbo](https://store.steampowered.com/app/389140/)
- <a href="https://store.steampowered.com/app/1264280/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1264280/header.jpg" width="120" alt="Slipways"></a> [Slipways](https://store.steampowered.com/app/1264280/)
- <a href="https://store.steampowered.com/app/249590/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/249590/header.jpg" width="120" alt="Teslagrad"></a> [Teslagrad](https://store.steampowered.com/app/249590/)
- <a href="https://store.steampowered.com/app/418620/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/418620/header.jpg" width="120" alt="The TakeOver"></a> [The TakeOver](https://store.steampowered.com/app/418620/)

Cave Story+, Gravity Circuit, Kingdom: New Lands and Horizon Chase Turbo were played from my Epic library; the links go to their Steam pages.

Per-game configs, results and manual steps: **[configs/](configs/README.md)**.

## How it was done

### 1. Live telemetry over Wi-Fi

The PC connected to the handheld with wireless ADB. During play it read:
- GameNative's own per-session performance log: fps, frame times, CPU/GPU %, temperatures
- GPU memory straight from the kernel (`kgsl`)
- swap and free memory
- `top`
- logcat, for which process Android's low-memory killer took

Every change was judged on numbers from before and after. Snippets: [tools/monitor](tools/monitor/adb-snippets.md).

### 2. A firmware bug was eating half the CPU

Before launching any game, the handheld's own system service used 300-600% CPU, about 4 of its 8 cores. Mangmi support sent a diagnostic script. Its thread dumps pointed at a recursive file scan, and decompiling the service showed the scan's logic.

While the [ES-DE (EmulationStation Desktop Edition)](https://www.patreon.com/es_de) front end is on screen, the service rescans ES-DE's themes folder every 2 seconds. That folder held 3.5 GB in 17,140 files. The service never waits for the last scan to finish, so the scans pile up.

Trimming the themes cut the service from ~519% to ~101%. Carrion went from 6.4 to 13.2 fps. Follow-up logs went to Mangmi for a firmware fix. Full write-up: [docs/es-de-themes-cpu-bug.md](docs/es-de-themes-cpu-bug.md).

### 3. Game by game

I imported a config, played, and exported it back. Claude Code diffed the export, read the metrics, and proposed the next single change. Most fixes had a different root cause.

Prices are Steam US list prices (before sales) as of November 2026. Field names are GameNative's container settings / config JSON keys. Banners are Steam's store images, linked to each store page.

#### Spidersaurs

<a href="https://store.steampowered.com/app/1191620/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1191620/header.jpg" width="231" alt="Spidersaurs"></a>

*Co-op run-and-gun shooter: dinosaur-spider hybrids, Saturday-morning-cartoon style. $19.99*

**Root cause:** The intro video is decoded in software, far too slow under translation. It wasn't a RAM problem, as first thought.

**What didn't work:**

- July verdict "needs 8 GB RAM" (disproved: memory to spare)
- Box64 Performance
- DXVK 2.7.1
- Proton 11 + Box64 0.4.4 + Turnip v27
- Renaming the video pak (the game quits after the logo)

**Fix:**

- My idea: swap in a short clip. Claude Code worked out the undocumented `.pak` format, proved a rebuild matched the original byte for byte, then rebuilt `movie_intro.pak` and `wf_splash_screen.pak` with ~1 s clips (originals kept as `.orig`)
- Config: Proton 11 + Box64 + DXVK 2.7.1 + Turnip v27
- Details: [docs/spidersaurs-intro.md](docs/spidersaurs-intro.md)

#### Sine Mora EX

<a href="https://store.steampowered.com/app/606730/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/606730/header.jpg" width="231" alt="Sine Mora EX"></a>

*Side-scrolling shoot 'em up where time is your health bar; dieselpunk war story. $9.99*

**Root cause:** The 32-bit game runs out of *address space*: it quit while 520 MB of RAM was still free.

**What didn't work:**

- GameNative's known config (DXVK 1.11.1-sarek, `videoMemorySize` 2048): logos, then quits ~30 s in

**Fix:**

- `dxwrapperConfig` version `1.11.1-sarek` → `2.7.1-1-gplasync-0` (DXVK 2.x unmaps textures in 32-bit games)
- `videoMemorySize` 2048 → 512
- Game folder `sinemoraex.settings`: `videomode=1`, `force_width=640`, `force_shadow=256`, `force_aa=1`, `skip_logos=1`

#### Cave Story+

<a href="https://store.steampowered.com/app/200900/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/200900/header.jpg" width="231" alt="Cave Story+"></a>

*Action-platformer / Metroidvania: a robot wakes in a cave on a floating island. $14.99*

**Root cause:** The game folder ships its own `opengl32.dll`, Microsoft's *software* renderer, which loads instead of the GPU path.

**What didn't work:**

- FEXCore Performance (still ~35 fps on every setting)
- Left stick mapped to arrow keys (keys got stuck "held")
- XInput Mapper (stick still stuck)

**Fix:**

- Rename `opengl32.dll` → `opengl32.dll.bak` in the game folder
- Controls: keyboard keys on the D-pad (Z jump, X shoot, A/S weapons, Q inventory, W map, Esc pause), left stick unmapped
- DirectInput API off

#### Bad North

<a href="https://store.steampowered.com/app/688420/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/688420/header.jpg" width="231" alt="Bad North"></a>

*Minimalist real-time tactics roguelite: defend tiny islands from Viking raids. $14.99*

**Root cause:** Its controller library (Rewired) ignored the pad, and the menus broke below 720 px tall.

**What didn't work:**

- Standard DirectInput mapper (no input; mouse emulation as a stopgap)
- 960x540: the Play button opens nothing
- 1024x768: works, but 4:3 with black bars
- Plain 1280x720: swap ran down to ~10 MB
- `videoMemorySize` 512: no measurable effect

**Fix:**

- DirectInput Mapper Type: Standard → **XInput Mapper**
- `screenSize` 1280x720 + exec args `-screen-width 1024 -screen-height 576` (Unity renders smaller, the menus keep their 720p layout)
- In-game anti-aliasing off (GPU 91-99% → 63-72%)

#### Kingdom: New Lands

<a href="https://store.steampowered.com/app/496300/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/496300/header.jpg" width="231" alt="Kingdom: New Lands"></a>

*Side-scrolling kingdom-building strategy on horseback: build by day, defend by night. $14.99*

**Root cause:** Unity garbage-collector crash under the Box64 translator.

**What didn't work:**

- Known config (x86_64 Proton + FEXCore mismatch): exits after ~6 s
- Box64 Performance and Box64 Stability/Unity: "Fatal error in GC: Collecting from unknown thread"

**Fix:**

- Proton `proton-11.0-2-arm64ec-9`, DXVK 2.7.1, Turnip v27
- `emulator` Box64 → **FEXCore** (preset Intermediate)
- DirectInput Mapper Type → XInput Mapper

#### Gravity Circuit

<a href="https://store.steampowered.com/app/858710/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/858710/header.jpg" width="231" alt="Gravity Circuit"></a>

*Fast 2D action platformer: a robot hero punching and grappling through a 16-bit-style future. $16.99*

**Root cause:** GPU driver crash: logcat showed `zink: DEVICE LOST` seconds after start.

**What didn't work:**

- Known config: exits after ~6 s
- July settings (exe path, Box64/FEX Performance, `BOX64_AVX`) on Turnip 26.2.0: black screen

**Fix:**

- July settings + `graphicsDriverConfig` version → **Turnip v27.0.0-R1**

#### Swords & Bones

<a href="https://store.steampowered.com/app/1534700/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1534700/header.jpg" width="231" alt="Swords & Bones"></a>

*Retro 16-bit action-adventure: sword and shield against undead hordes and demons. $4.99*

**Root cause:** DXVK presented frames badly through gamescope: flashing or a black screen.

**What didn't work:**

- Known config: all-black window
- DXVK 2.7.1 + Turnip v27: flashing
- DXVK async off (`async=0`, `DXVK_ASYNC=0`)
- fifo present mode
- `numBackBuffers=1`
- WineD3D: no flashing, but 11-15 fps
- WineD3D on Vulkan, FEXCore Performance: no gain

**Fix:**

- DXVK 2.7.1 + `displayServer` gamescope → **X11** + display renderer Vulkan → **OpenGL** (set by hand; X11 + Vulkan was black)
- envVars `DXVK_CONFIG=dxvk.enableGraphicsPipelineLibrary=False;d3d9.numBackBuffers=1;dxgi.numBackBuffers=1`, `DXVK_ASYNC=0`, `MESA_VK_WSI_PRESENT_MODE=fifo`

#### Mago

<a href="https://store.steampowered.com/app/1098280/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1098280/header.jpg" width="231" alt="Mago"></a>

*Retro 2D platformer: a wizard rescues a princess from a gourmet villain's dinner menu. $14.99*

**Root cause:** Old DXVK + Turnip used too much memory at load, so Android killed it. Then a stray debug overlay.

**What didn't work:**

- Nov-12 config (DXVK async-1.10.3, Turnip 25.3): GPU memory ~910 MB → killed ~20 s in
- Debug setting in the game's `options.ini` (wasn't the overlay; restored)

**Fix:**

- `dxwrapperConfig` version → `2.7.1-1-gplasync-0`, Turnip → v27.0.0-R1, `videoMemorySize` → 512
- Remove `DXVK_HUD=fps,frametimes,gpuload` from envVars (hidden on old DXVK, visible on 2.7.1)
- Result: locked ~60 fps

#### Megabonk

<a href="https://store.steampowered.com/app/3405340/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/3405340/header.jpg" width="231" alt="Megabonk"></a>

*3D roguelike survivor: auto-attack hordes, stack absurd builds. $9.99*

**Root cause:** GPU-bound on the Adreno 610.

**What didn't work:**

- DXVK 2.7.1 + Turnip v27: hangs on "Loading..." (twice)
- Unity launch args `-screen-width 1024 -screen-height 576`: ignored (10.2 fps)

**Fix:**

- Keep the original stack (DXVK 1.11.1-sarek + Turnip 26.0.0_R4)
- In-game: grass Low; shadows, AA, soft particles, bloom, motion blur and ambient occlusion off → 10 → ~17 fps

#### Retro City Rampage DX

<a href="https://store.steampowered.com/app/204630/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/204630/header.jpg" width="231" alt="Retro City Rampage DX"></a>

*8-bit open-world crime parody: carjacking and missions through '80s pop culture. $14.99*

**Root cause:** The game's own "Select controller" prompt ignored the pad.

**What didn't work:**

- XInput Mapper: no effect

**Fix:**

- At that prompt, open GameNative's on-screen keyboard and press Enter once; the controller works from then on
- Config unchanged; locked 60 fps

#### Star Wars Jedi Knight: Dark Forces II

<a href="https://store.steampowered.com/app/32380/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/32380/header.jpg" width="231" alt="Star Wars Jedi Knight: Dark Forces II"></a>

*1997 first-person shooter: Kyle Katarn, lightsabers and Force powers. $5.99*

**Root cause:** The pause menu is drawn with old Windows GDI, which never reaches the screen on X11. DXVK doesn't apply (the game renders through WineD3D).

**What didn't work:**

- `WINE_D3D_CONFIG` `csmt=0`, `renderer=vulkan`, `OffscreenRenderingMode=backbuffer`
- Display renderer OpenGL
- DX wrapper WineD3D and Cnc ddraw
- Screen sizes 640x480 / 854x480 / 1280x720
- `-windowgui`
- gamescope: menu visible, but small in a corner with ~10 s stalls

**Fix:**

- `displayServer` → X11, `screenSize` → 1024x768
- Quick Save (F9) mapped to a spare button
- Hidden level-start autosaves made loadable with [`jk_autosave_visible.py`](tools/jk_autosave_visible.py)
- Details: [docs/jedi-knight.md](docs/jedi-knight.md)

#### Cast n Chill

<a href="https://store.steampowered.com/app/3483740/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/3483740/header.jpg" width="231" alt="Cast n Chill"></a>

*Relaxing fishing game: lakes, rivers and a dog companion. $14.99*

**Root cause:** Nothing broken; uncapped 36-40 fps ran hot and uneven.

**Fix:**

- In-game FPS limit 30 + VSync off → steady 29.5 fps and cooler (54-57 °C)

#### Wizordum

<a href="https://store.steampowered.com/app/1715590/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/1715590/header.jpg" width="231" alt="Wizordum"></a>

*Retro fantasy first-person shooter: a mage fighting with spells. $19.99*

**Root cause:** Nothing broken.

**Fix:**

- GameNative's known config as is: menus 33-37 fps, levels 17-22

#### Undertale

<a href="https://store.steampowered.com/app/391540/"><img src="https://cdn.akamai.steamstatic.com/steam/apps/391540/header.jpg" width="231" alt="Undertale"></a>

*Cult-classic indie RPG where you never have to kill anyone. $9.99*

**Root cause:** The face buttons sent nothing, and it opened windowed.

**What didn't work:**

- Looking for a fullscreen launch flag (the game has none)

**Fix:**

- Keyboard remap: A → Z (confirm), B → X (cancel), Y → C (menu), D-pad → arrows
- F4 on a button toggles fullscreen
- Box64 + FEXCore Performance, Turnip 25.1.0, DXVK, `maxDeviceMemory` 512

### 4. Knowing when to stop

Games that didn't come together were parked with a reason and a next step:
- **Renowned Explorers:** looks light but isn't. Loading to the menu takes ~1:45, bound by file I/O. It waits forever on a Steam leaderboard unless offline. The first expedition load ran out of memory at 720p. On identical settings it then deadlocks intermittently, which points at translation-layer timing.
- **Horizon Chase Turbo, Slipways:** GPU memory climbs until Android kills them. Measured from the kernel and reported upstream: [GameNative Discussion #2443](https://github.com/utkarshdalal/GameNative/discussions/2443).
- **Teslagrad:** old Unity with one main thread pinned under translation.
- **The TakeOver:** controller confusion; parked by choice.
- **Jedi Knight's music:** the CD-audio shim loads, but the game never asks for a track. The next step is in the doc.

## What's next

- **Jedi Knight music:** a Wine MCI debug log is next.
- **Renowned Explorers, Horizon Chase Turbo:** retest after the next GameNative update.
- **Mangmi firmware fix:** once it ships, put the ES-DE themes back and recheck the service CPU.

I'll update this repo as those land.

## What's here

```
configs/            GameNative exports: working/, parked/, untested/, with a table of results and manual steps
docs/
  lessons-low-ram.md      17 lessons for GameNative on low-RAM devices (start here)
  es-de-themes-cpu-bug.md the Mangmi system service bug
  spidersaurs-intro.md    the intro video swap and the .pak format
  jedi-knight.md          save workaround, black menu, music investigation
tools/
  shorten_pak.py          rebuild/trim WayForward .pak archives (--verify = byte-identical rebuild)
  jk_autosave_visible.py  make Jedi Knight level-start autosaves appear in Load Game
  build_esde_media.py     fill missing ES-DE box art / screenshots / logos / trailers from Steam's public store data, and compose miximages
  monitor/                gn_metrics_summary.py + ADB monitoring snippets
claude-code-prompt.md     starter prompt for debugging your own device with Claude Code
```

The tools are Python 3. `build_esde_media.py` needs Pillow; the rest use only the standard library. No game files, art or videos are included.

## Caveats

- Tested on one device, on GameNative 1.4.0 and Air X firmware 1.1.14. Results will shift with updates.
- "Working" includes playable-but-modest: Megabonk ~17 fps, Sine Mora EX 18-28 fps, Wizordum 17-22 fps in levels.
- GameNative isn't my software, and I didn't modify it. Game files that were edited (Spidersaurs paks, Cave Story+'s DLL, Jedi Knight's exe import for the music test) were backed up first and are reversible.

## Credits

- [GameNative](https://github.com/utkarshdalal/GameNative): the app that makes any of this possible
- [OpenJKDF2](https://github.com/shinyquagsire23/OpenJKDF2): the open re-implementation of Jedi Knight whose source explained the menus, the save format and the hidden autosaves
- [Mesa Turnip](https://docs.mesa3d.org/drivers/freedreno.html), [FEX-Emu](https://github.com/FEX-Emu/FEX), [Box64](https://github.com/ptitSeb/box64), [DXVK](https://github.com/doitsujin/dxvk), [Wine](https://www.winehq.org/)/Proton
- [ES-DE](https://es-de.org/) front end, and ogg-winmm (the CD-audio shim shipped with Jedi Knight's Steam release)
- Mangmi support, for the diagnostic script

## Try it yourself with Claude Code

[`claude-code-prompt.md`](claude-code-prompt.md) is a starter prompt for doing the same kind of debugging on your own Air X (or a similar low-RAM Android handheld) with Claude Code. Paste it into a new session, then name the game you want to fix.
