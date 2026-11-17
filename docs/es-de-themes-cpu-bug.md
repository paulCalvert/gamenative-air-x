# The ES-DE themes CPU bug (Mangmi system service)

**Outcome:** the handheld's own system service dropped from ~519% CPU to ~101% (an 8-core CPU tops out at 800%), and the fan turned off. CPU-bound games roughly doubled: Carrion went from 6.4 to 13.2 fps.

## Symptom

`top` over ADB showed `com.handheld.systemservice`, Mangmi's controller/fan/performance-mode service, using more CPU than the game, even with no game running. Typical readings were 300-600%, or about 4 of the 8 cores busy before launching anything. Battery drained fast and games stuttered.

## Ruled out, one at a time

Each test measured the service's CPU time (`TIME+` delta ÷ wall-clock seconds), because the instant `%CPU` swings a lot.

| Test | Result |
|---|---|
| Reboot, and a full power-off + overnight charge | still 300%+ within 4 minutes of boot |
| Quick-panel toggles: ambient light, force landscape, performance mode, fan mode, trigger mode, button layout | no change |
| Wireless ADB (in case monitoring caused it) | CPU kept climbing while ADB was off |
| Force-stopping the ES-DE launcher | no change (misleading: see below) |
| Ejecting the SD card | still ~606% |
| Screen-off sleep | the spin mostly stops, then resumes on wake |
| Firmware updater | already on the latest (1.1.14) |

## Finding it

1. Mangmi support sent a diagnostic script. It was reviewed first (read-only, writes to `/sdcard/tmp`) and run as root through Mangmi's own settings app.
2. Its Java thread dumps showed every busy worker thread inside `TopActivityTrigger.scanDir`: a recursive file walk.
3. Decompiling the system app (`SystemService.apk`, with androguard) showed the logic. **While ES-DE is the foreground app, every 2 seconds it starts a new recursive walk of ES-DE's `themes` folder** (looking for files ending in `lock` to delete) and never waits for the previous walk to finish.
4. The themes folder held 13 themes: 3.5 GB in 17,140 files. Each walk took longer than 2 seconds, so walks piled up until the CPU was saturated.

Force-stopping ES-DE had looked like it ruled the launcher out. Most likely the walks already queued kept running, so the test measured the backlog, not new scans.

## Workaround

Keep only the theme in use. The files belong to ES-DE's app folder, so the deletion ran as root through Mangmi's "Run script" option. The folder went from 17,140 entries (3.5 GB) to 2,350 (846 MB), and the service from ~519% to ~101%.

Every theme added brings the drain back until Mangmi fixes the service. The follow-up logs and the finding went to Mangmi support.

## Before / after

| | Before | After |
|---|---|---|
| System service, ES-DE on screen | ~519% | ~101% |
| Carrion | 6.4 fps, CPU 98% | 13.2 fps, CPU 65% |
| Megabonk | 11 fps | 12.7 fps, "a lot more responsive" (GPU-bound, so smaller gain) |
| Fan | always on | off at idle |

About one core of service load remains even with a game in front, so something else in the service still runs.
