# GameNative configs

Exported from GameNative 1.4.0 on a Mangmi Air X (Snapdragon 662, Adreno 610, 4 GB RAM, Android 14). Import them through the game's container settings in GameNative.

## Read before importing

- **The import skips some fields.** In testing it ignored `screenSize`, `videoMemorySize` and `displayServer` (sometimes the display renderer too). After importing, set those by hand and check them against the JSON.
- `drives` contains this device's paths, with the SD card id replaced by `XXXX-XXXX`. GameNative fills in its own paths for your install; fix them if a game can't find its folder.
- `extraData.configMatchedGpu` is left over from GameNative's community "known config" the file started from. It isn't this device's GPU.
- Controller key mappings are **not** in these files. Where a game needs a mapping, it is listed below.

## Working

| Game | Config | Result on the Air X | Manual steps / quirks |
|---|---|---|---|
| Bad North: Jotunn Edition | [bad-north.json](working/bad-north.json) | ~25 fps, full missions | screenSize 1280x720 + exec args `-screen-width 1024 -screen-height 576`. Keep the desktop ≥720 px tall (lower and the menus break). In-game AA off. Controller → DirectInput Mapper Type = XInput Mapper (Rewired) |
| Cast n Chill | [cast-n-chill.json](working/cast-n-chill.json) | steady 30 fps | GameNative known config unchanged. In-game FPS limit 30 + VSync off |
| Cave Story+ (Epic) | [cave-story-plus.json](working/cave-story-plus.json) | smooth (not measured after the fix; ~35 fps before) | Rename the game folder's `opengl32.dll` → `opengl32.dll.bak` (it's Microsoft's software renderer). FEXCore preset Performance. Keyboard mapping on the D-pad (Z jump, X shoot, A/S weapons, Q inventory, W map, Esc pause), left stick unmapped, DirectInput API off |
| Gravity Circuit (Epic) | [gravity-circuit.json](working/gravity-circuit.json) | 25-29 fps | Turnip v27.0.0-R1. On v26 the driver crashed (`zink: DEVICE LOST`) |
| Kingdom: New Lands (Epic) | [kingdom-new-lands.json](working/kingdom-new-lands.json) | ~31 fps | Emulator FEXCore (Intermediate). Box64 → Unity "Collecting from unknown thread" crash. XInput Mapper |
| Mago | [mago.json](working/mago.json) | locked ~60 fps | DXVK 2.7.1-gplasync + Turnip v27, VRAM 512. GPU memory sits at ~700-900 MB; watch long sessions |
| Megabonk | [megabonk.json](working/megabonk.json) | ~17 fps, GPU-bound | Keep the original stack (DXVK 1.11.1-sarek + Turnip 26.0.0_R4): DXVK 2.7.1 + Turnip v27 hangs on "Loading...". In-game: grass Low, shadows/AA/soft particles/bloom/motion blur/AO off |
| Retro City Rampage DX | [retro-city-rampage-dx.json](working/retro-city-rampage-dx.json) | locked 60 fps | At the game's "Select controller" prompt, open GameNative's on-screen keyboard and press Enter once |
| Sine Mora EX | [sine-mora-ex.json](working/sine-mora-ex.json) | 18-28 fps, playable | DXVK 2.x is required (32-bit game runs out of address space on 1.11). Edit `sinemoraex.settings` in the game folder: `videomode=1`, `force_width=640`, `force_shadow=256`, `force_aa=1`, `skip_logos=1` |
| Spidersaurs | [spidersaurs.json](working/spidersaurs.json) | 35-39 fps | Needs the shortened intro videos: see [docs/spidersaurs-intro.md](../docs/spidersaurs-intro.md). A Steam verify restores the long intro |
| Star Wars Jedi Knight: Dark Forces II | [jedi-knight-dark-forces-ii.json](working/jedi-knight-dark-forces-ii.json) | ~60 fps in levels | displayServer X11 (set by hand), screenSize 1024x768. Esc menu is black on X11 → map Quick Save (F9) to a spare button; level-start saves made loadable. No music. See [docs/jedi-knight.md](../docs/jedi-knight.md) |
| Swords & Bones | [swords-and-bones.json](working/swords-and-bones.json) | ~120 fps counter | displayServer X11 **and display renderer OpenGL, set by hand** (the file doesn't carry the renderer). On gamescope / Vulkan display the screen flashes or stays black |
| Undertale | no export | working | July setup: Box64 Performance, FEXCore Performance, Turnip 25.1.0, DXVK, maxDeviceMemory 512. Keyboard map A→Z, B→X, Y→C, D-pad → arrows. F4 toggles fullscreen |
| Wizordum | [wizordum.json](working/wizordum.json) | menus 33-37, levels 17-22 fps | GameNative known config unchanged. Long level loads |

## Parked (best attempt so far)

| Game | Config | What happens |
|---|---|---|
| Renowned Explorers | [renowned-explorers.json](parked/renowned-explorers.json) | Reaches menus at ~30-40 fps with: DXVK 2.7.1, FEXCore Intermediate (Performance stops the renderer), `steamOfflineMode` (otherwise it waits forever on a Steam leaderboard), 960x540 + VRAM 512 set by hand, and `r_uselcdfilter = false` in the game's `settings.ini` (fixes missing UI text). Still fails intermittently on identical settings: ~1:45 file-bound load to the menu, an out-of-memory kill on the first expedition load at 720p, then deadlocks/livelocks at the loading bar. Retest after a GameNative update |
| Horizon Chase Turbo (Epic) | [horizon-chase-turbo.json](parked/horizon-chase-turbo.json) | Runs at 54-59 fps for ~45 s, but GPU memory climbs past 850 MB, swap hits 0 and Android kills it. Neither `videoMemorySize` nor `maxDeviceMemory` capped it. Reported upstream: GameNative Discussion #2443 |
| Slipways | [slipways.json](parked/slipways.json) | Same rising GPU memory pattern; long stalls waiting on swap |
| Teslagrad | [teslagrad.json](parked/teslagrad.json) | Old Unity, one main thread pinned under translation: smooth stretches at 31-35 fps, then drops to 2-15 |

## Untested

[carrion.json](untested/carrion.json), [hollow-knight.json](untested/hollow-knight.json), [wizordum-v1-asynccache-fexperf.json](untested/wizordum-v1-asynccache-fexperf.json): built, never confirmed on the device.
