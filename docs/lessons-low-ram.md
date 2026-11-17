# GameNative on a low-RAM device: lessons

Learned on a 4 GB Snapdragon 662 / Adreno 610 handheld, roughly in the order to try them. Each one fixed at least one real game.

## Start here

1. **Try DXVK 2.7.1-gplasync + Turnip v27.0.0-R1 first.** This stack revived most of the community "known configs". Exceptions: Megabonk hangs on it, and Teslagrad runs worse. Keep their original stacks.
2. **Set `videoMemorySize` to 512.** Known configs ship with 2048, which doesn't fit 3.7 GB of shared RAM. Real GPU memory isn't capped by `videoMemorySize` or `maxDeviceMemory`, though. Watch `/sys/class/kgsl/kgsl/page_alloc`.
3. **Imports skip `screenSize`, `videoMemorySize` and `displayServer`** (sometimes the display renderer too). Set them by hand, then export and compare to confirm.

## By symptom

4. **Unity game, menus break at lower resolutions:** keep screenSize 1280x720 and shrink the render with exec args `-screen-width W -screen-height H`. This worked for Bad North and Slipways; Megabonk ignores the args. Keep the desktop ≥720 px tall.
5. **Unity game ignores the controller:** check `Managed/` for `Rewired_*.dll`. If it's there, set DirectInput Mapper Type to XInput Mapper.
6. **Unity "Fatal error in GC: Collecting from unknown thread" under Box64:** switch the emulator to FEXCore.
7. **Black screen, and logcat shows `zink: DEVICE LOST`:** the GPU driver crashed. Try another Turnip build (v27).
8. **DXVK flashing or black screen:** displayServer X11 + a non-Vulkan display renderer (OpenGL).
9. **Mystery on-screen overlay:** look for `DXVK_HUD` in envVars. It does nothing on old DXVK builds and shows up after an upgrade.
10. **Game folder ships its own `opengl32.dll` or `d3d*.dll`:** it overrides Wine. Rename it to `.bak`. Cave Story+ bundled Microsoft's software OpenGL renderer.
11. **Audio plays, screen black, CPU pegged, GPU at 0:** a software-decoded intro video. Shorten it (see [spidersaurs-intro.md](spidersaurs-intro.md)).
12. **32-bit DX9 game quits during loading with RAM still free:** out of address space, not memory. Use DXVK 2.x, which unmaps textures in 32-bit processes.
13. **FEXCore Performance preset stops a multithreaded renderer** (logic runs, GPU at 0): step back to Intermediate.
14. **Game sits on a loading screen waiting on Steam** (leaderboards etc.): set `steamOfflineMode: true`.
15. **DirectDraw / D3D ≤7 games:** DXVK doesn't apply, and WineD3D is always used. Tune WineD3D through `WINE_D3D_CONFIG`. GDI menus may be black on X11 but visible on gamescope.
16. **Change controller mappings before launching, never during a load.** One game exited when the mapping screen opened mid-load.
17. **Buttons stop working after a resolution change:** revert screenSize first. A lower resolution can push menu panels off-screen.

## Habits that made it work

- **One change per test, and measure before and after.** Use fps, p95 frame time, CPU/GPU %, GPU memory, swap. See [tools/monitor](../tools/monitor).
- **Classify the failure first.** Slow and hung look the same on screen. CPU/GPU/memory numbers tell you which, and point to completely different fixes.
- **Back up any game file before editing it**, as `.orig`/`.bak` next to it plus a PC copy.
- **Export the config after every good run.** Import is lossy, so the export is the record.
- **Park games with a written reason and a next step** instead of tinkering forever.
- **Each installed game costs ~0.4-1 GB of internal storage** for its Wine container, even when the game sits on the SD card. Uninstall failures inside GameNative to get it back.
- After a device reboot: re-enable wireless debugging. GameNative may silently lose its Steam login ("No CDN servers available"); sign out and back in, then check the download location didn't reset to internal storage.
