# ADB monitoring snippets

How the device was watched live from a PC while games ran. All read-only.

## Connect over Wi-Fi (Android 11+)

Developer options → Wireless debugging → Pair device with pairing code.

```sh
adb pair <device-ip>:<pairing-port> <code>   # once
adb mdns services                            # finds the current connect port
adb connect <device-ip>:<connect-port>
adb -s <device-ip>:<connect-port> shell echo ok
```

- The connect port changes every time Wireless debugging is toggled or the device reboots. Re-run `adb mdns services`.
- Turn on "Disable adb authorization timeout", or Android forgets the pairing after 7 days.
- The device can show up twice (direct + mDNS). Pick one with `-s`.
- On Windows Git Bash, remote paths like `/sdcard/...` get rewritten into Windows paths. Prefix with `MSYS_NO_PATHCONV=1` or use PowerShell for `adb push/pull`.

## GameNative's own performance log

```sh
adb shell ls -t /sdcard/Android/data/app.gamenative/files/powercontrol/ | head -3
adb shell tail -n 5 /sdcard/Android/data/app.gamenative/files/powercontrol/metrics-<id>.jsonl
adb pull /sdcard/Android/data/app.gamenative/files/powercontrol ./powercontrol
python -I gn_metrics_summary.py ./powercontrol --last 1
```

## Memory (the usual killer on a 4 GB device)

```sh
adb shell cat /sys/class/kgsl/kgsl/page_alloc                 # GPU memory in bytes (Adreno); idle ~100 MB
adb shell grep -E 'MemAvailable|SwapFree' /proc/meminfo
adb shell top -b -n 1 -m 8                                   # who is using CPU / RES
adb shell logcat -d | grep -i -E 'lowmemorykiller|DEVICE LOST|guest_terminated'
```

- kgsl climbing steadily with swap heading to 0 = the game will be killed. `videoMemorySize` and `maxDeviceMemory` in the config did **not** cap it in testing.
- `lowmemorykiller ... critical pressure` followed by the launcher and keyboard dying = out of memory, not a crash.

## Which process is burning CPU (system services included)

```sh
adb shell top -b -n 1 -o PID,USER,%CPU,TIME+,ARGS -s 3 | head -15
```

Instant `%CPU` swings a lot. For a fair number, take `TIME+` twice and divide the delta by wall-clock seconds.

## Which files a game reads (toybox inotifyd)

```sh
adb shell inotifyd - "/storage/<sd>/GameNative/Steam/steamapps/common/<Game>/MUSIC:or"
```

- Prints `o` (open) / `r` (read) events live. A mask of `r` alone is rejected ("Invalid argument").
- Useful when ADB can't read another app's `/proc/<pid>/maps` (different uid): it shows whether a DLL or data file is actually loaded.

## Reading the symptoms

| What you see | Likely cause |
|---|---|
| fps 0, GPU busy | still working on GPU (shader compile, loading) |
| fps 0, CPU pegged, GPU 0, audio playing | software-decoded video, or a hot thread under translation |
| fps 0, CPU ~idle, GPU 0, no log progress | deadlock / waiting on something (network, Steam) |
| game dies, launcher restarts | out of memory (check kgsl + swap + lowmemorykiller) |
| black screen + `zink: DEVICE LOST` in logcat | GPU driver crash → try another Turnip build |
| static menu shows 0 fps | normal: only new frames are counted |
