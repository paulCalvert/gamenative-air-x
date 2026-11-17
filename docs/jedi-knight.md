# Star Wars Jedi Knight: Dark Forces II (1997)

**Outcome:** playable at ~60 fps in levels. The pause menu is black, so progress runs on Quick Save plus loadable level-start saves. No in-game music yet.

Config: [`configs/working/jedi-knight-dark-forces-ii.json`](../configs/working/jedi-knight-dark-forces-ii.json). Set displayServer X11 and screenSize 1024x768 by hand after importing.

## Why the usual fixes don't apply

- JK draws with DirectDraw / Direct3D 3. DXVK starts at D3D8/9, so **JK always renders through WineD3D** whatever the DX wrapper says. WineD3D options go in the `WINE_D3D_CONFIG` environment variable (GameNative shows no settings gear for it).
- The menus switch the display to plain GDI drawing (`Video_SwitchToGDI` in [OpenJKDF2](https://github.com/shinyquagsire23/OpenJKDF2)'s source). Under X11 that layer never reaches the screen, so **the in-game Esc menu is black**. The game is still drawing it, but nothing is presented. The startup main menu does work.
- It renders 640x480 only.

## Black Esc menu: tried

All of these failed on X11 and were reverted:
- `WINE_D3D_CONFIG`: `csmt=0`; `renderer=vulkan` (hangs at launch); `OffscreenRenderingMode=backbuffer`
- display renderer OpenGL
- DX wrapper WineD3D and Cnc ddraw
- screen sizes 640x480, 854x480, 1280x720
- the `-windowgui` launch flag

gamescope does show the menu, but draws the game small in a corner and stalls ~10 s on every menu load. Paul chose X11 and a workaround.

## Workaround: saves without the pause menu

1. **Quick Save is F9** (from OpenJKDF2's input table). It is one slot, `quicksave.jks`, overwritten each time. Paul mapped it to a spare button (Start/Select are unused now that Esc is useless).
2. **There is no quick-load key.** Loading only happens from Load Game, and that works from the startup main menu.
3. To recover from a bad quick save: JK silently auto-saves each level start as `_JKAUTO_<level>.jks`, but Load Game hides those files. OpenJKDF2's `jkGUISaveLoad.c` shows why: the list skips names starting `_JKAUTO_` and only shows saves whose name field contains `~`, displaying the text after it.
4. [`tools/jk_autosave_visible.py`](../tools/jk_autosave_visible.py) copies an autosave to a normal slot and rewrites the name field (UTF-16 at byte offset 1068), so the level start appears as "START 01 - Double-Cross on Nar Shaddaa", and so on. The first version showed every copy as "Level start", and zero-padding the numbers made them sort in order. Its output matches the saves tested in-game byte for byte.

```sh
python -I jk_autosave_visible.py info player/<profile>/_JKAUTO_01narshadda.jks
python -I jk_autosave_visible.py make player/<profile>/_JKAUTO_01narshadda.jks player/<profile>/save0101.jks "START 01 - Double-Cross on Nar Shaddaa" --title "1 - Double-Cross on Nar Shaddaa"
```

## Black bars

The bars at the sides are the game's 4:3 shape. The bar at the bottom, with the HUD in the corners, is JK's own view size: press `=`/`-` with the map closed.

## Music: parked

Sound effects and cutscene audio work; level music doesn't.

- The Steam release replaces CD audio with **ogg-winmm**, a `winmm.dll` shim that plays `MUSIC\TrackNN.ogg`.
- Wine kept loading its own winmm. So the exe's import name was patched (`WINMM.dll` → `WINMX.dll`, one string), with the shim copied as `winmx.dll`. The patched exe and the original were both backed up, and the change is reversible.
- Watching file access live (`inotifyd`) showed the shim now loads and scans all 18 tracks at launch. **No track is ever opened when a level starts**, so the game's play request never arrives or asks for track numbers that don't exist.
- Next step: a Wine debug log (`WINEDEBUG=+mci,+winmm,+mcicda`) to see the actual MCI calls.
