"""Summarize GameNative per-session performance logs (metrics-*.jsonl).

GameNative 1.4+ writes one file per game session to
  /sdcard/Android/data/app.gamenative/files/powercontrol/metrics-<epoch ms>.jsonl
Each line: timestampMs, fps, frameTimeP50Ms, frameTimeP95Ms, frameTimeMaxMs,
slowFrameCount, totalFrameCount, cpuUsagePercent, gpuUsagePercent, cpuTempC, gpuTempC.

Pull the folder first:
  adb pull /sdcard/Android/data/app.gamenative/files/powercontrol ./powercontrol
Then:
  python -I gn_metrics_summary.py ./powercontrol [--last N]

Note: fps only counts new frames, so a static menu reads 0 fps. Stats below use
samples with fps > 0 for fps/frame time and all samples for CPU/GPU/temps.
"""
import glob, json, os, sys, datetime, statistics as st


def spread(vals):
    if not vals:
        return '-'
    vals = sorted(vals)
    p10 = vals[int(len(vals) * 0.1)]
    return f'p10 {p10:.0f} / med {st.median(vals):.0f} / max {vals[-1]:.0f}'


def summarize(path):
    rows = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line.startswith('{'):
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass  # a session killed mid-write can leave a partial last line
    if not rows:
        return
    t0 = datetime.datetime.fromtimestamp(rows[0]['timestampMs'] / 1000)
    mins = (rows[-1]['timestampMs'] - rows[0]['timestampMs']) / 60000
    live = [r for r in rows if r.get('fps', 0) > 0]
    col = lambda k, rs: [r[k] for r in rs if k in r]
    print(f'{os.path.basename(path)}  {t0:%Y-%m-%d %H:%M}  {mins:.1f} min  '
          f'{len(rows)} samples ({len(live)} with frames)')
    print(f'  fps          {spread(col("fps", live))}')
    print(f'  p95 frame ms {spread(col("frameTimeP95Ms", live))}')
    print(f'  CPU %        {spread(col("cpuUsagePercent", rows))}')
    print(f'  GPU %        {spread(col("gpuUsagePercent", rows))}')
    print(f'  CPU / GPU temp max (C) {max(col("cpuTempC", rows) or [0])} / {max(col("gpuTempC", rows) or [0])}')
    if len(live) >= 9:  # does it degrade over the session (heat, memory)?
        n = len(live) // 3
        thirds = [round(st.median(col('fps', live[i * n:(i + 1) * n])), 1) for i in range(3)]
        print(f'  fps median by thirds of the session: {thirds}')
    # quick read of the bottleneck
    gpu = st.median(col('gpuUsagePercent', rows) or [0])
    cpu = st.median(col('cpuUsagePercent', rows) or [0])
    if live:
        hint = 'GPU-bound' if gpu >= 90 else 'CPU-bound (likely one hot thread)' if cpu >= 70 else 'neither pegged: check memory/swap or I/O'
    else:
        hint = 'no frames: hung/loading. GPU busy = GPU work; CPU busy + GPU 0 = software decode, shader compile or a stuck thread'
    print(f'  hint: {hint}')


if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(sys.argv[1], '**', 'metrics-*.jsonl'), recursive=True))
    if '--last' in sys.argv:
        files = files[-int(sys.argv[sys.argv.index('--last') + 1]):]
    for f in files:
        summarize(f)
