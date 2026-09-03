# Windows Setup

The kit runs on Windows with Claude Code; the notes, the skill, and all the Kroger scripts are cross-platform Python. Three things work differently from the Mac, and each has a Windows path.

## 1. Credentials (instead of the Mac Keychain)

Pick one, in order of preference:

- **Environment variables** (cleanest): set `KROGER_CLIENT_ID` and `KROGER_CLIENT_SECRET` as user environment variables (Settings, "Edit environment variables for your account"). The cart login stores its token the same way automatically if `KROGER_REFRESH_TOKEN` is set, or falls through to:
- **The credentials file**: `%USERPROFILE%\.grocery-autopilot\kroger-credentials.json`, shaped like `{"client_id": "...", "client_secret": "..."}`. The scripts create and update this file themselves during `auth`. It sits in your user profile, outside the vault, so it never syncs or gets committed; still, treat the folder as private.

Everything else in `Guides/Kroger API Setup.md` (developer account, store setup, auth login, cart) is identical; run the same `python kroger.py ...` commands in PowerShell or Terminal.

## 2. The shared list (instead of Apple Reminders)

The skill's list output on Windows is the note `Household/Shopping List.md`: clean item names, store sections, notes per line. From there, two good patterns:

- **iPhone family, Windows computer** (very common): keep using a shared Apple Reminders list on the phones. Anyone still adds by Siri; whoever runs the weekly plan copies the note's list into Reminders from their phone in under a minute, and tells Claude what the family added so the plan sweeps it in.
- **Any shared list app** (Microsoft To Do, AnyList, Google Keep): same idea. The app is the family's front door; the note is the system's copy. Say what the family added during the weekly plan and nothing gets lost.

## 3. The weekly nudge and alerts (instead of iMessage and launchd)

- **Weekly nudge**: Task Scheduler. Create a weekly task for your planning morning that shows a message or opens the vault folder. Quick version in PowerShell (run once, adjust day/time):

```
schtasks /create /tn "Grocery plan day" /sc weekly /d MON /st 10:00 /tr "msg %username% Plan the week: snap fridge, freezer, pantry pics, then tell Claude to plan the week"
```

- **Cart-ready alert**: on Windows the alert is the plan session itself telling you, plus the shared list app's own notifications if it has them. Text-message alerts are a Mac feature (they send through Messages).

## What is identical on both platforms

Everything that matters: the notes, the skill, the planning conversation, photo inventory, receipt logging, live Kroger prices, the cart push, and the safety rails. The AI still never checks out on either platform.
