# snapscore-pixel

Sends blank snaps from a real Android phone to a Snapchat **Shortcut**, over ADB.
Built and tuned for a **Pixel 7 (1080x2400)** and the Snapchat layout as of October 2026.

Based on [hassancodes/snapscore](https://github.com/hassancodes/snapscore), rewritten with
measured tap positions and on-screen checks so it never sends to the wrong place.

## How it works

Each round:

1. Gets Snapchat to the camera (or to an unsent snap) from whatever screen it's on:
   presses Back, and reopens Snapchat if that doesn't work.
2. Takes a snap, taps **Send To**, and selects your Shortcut.
3. Taps **Select All**, or ticks the one friend if the Shortcut only has one person.
4. Sends, and writes a row to `snapscore_log.csv`.

Before tapping anything that could send, it reads pixels from a screenshot:

- the Shortcut chip must be selected (blue), otherwise the taps would land on **My Story**;
- the blue send bar must be showing (someone is ticked);
- the Private Story circle must be unticked.

If a check fails it skips the round without sending. Three failed rounds in a row stops the script.

## Setup

1. Install [Android platform-tools](https://developer.android.com/tools/releases/platform-tools)
   to `%LOCALAPPDATA%\Android\platform-tools` (or change `ADB_PATH` in `snapscore.py`).
2. On the phone: enable **Developer options → USB debugging**, plug it in, and accept the prompt.
   `adb devices` should list it.
3. `pip install -r requirements.txt`
4. In Snapchat, create a **Shortcut** (Send To screen → **New +**) with the friends to send to.
   It must be the first Shortcut chip, right after **All**.

## Run

```
python snapscore.py        # 400 rounds
python snapscore.py 100    # 100 rounds
```

Stop with **Ctrl+C**. Don't use the phone while it runs.

## Log

`snapscore_log.csv` has one row per sent round:

| column | meaning |
|---|---|
| `time` | when the round was sent |
| `round` | round number within the run |
| `selected_by` | `select_all` (everyone in the Shortcut) or `single_friend` (one-person Shortcut) |

To measure points per snap: note your score before and after a run, wait a while for
Snapchat to catch up, then divide the gain by (rounds × people in the Shortcut).

## Other phones

All coordinates are for a 1080x2400 screen. On another phone, take screenshots with
`adb exec-out screencap -p > screen.png` and re-measure the constants at the top of `snapscore.py`.

## Notes

- Only send to people who are fine getting a lot of snaps. Friends who aren't will remove you.
- Automating Snapchat is against its Terms of Service; your account is your own risk.
