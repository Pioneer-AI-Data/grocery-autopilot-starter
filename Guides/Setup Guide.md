# Setup Guide

The long version of Start Here, for when you want the why.

## What runs where

- **Your notes** (`Household/`): plain Markdown. The AI reads and writes them; you can too, any time.
- **The skill** (`.claude/skills/grocery/`): instructions Claude Code follows, plus the Kroger scripts. Open this folder in Claude Code and the skill is live automatically.
- **The shared Reminders list**: the family's front door. The AI writes the shopping list there and sweeps in whatever the family added.
- **Nothing leaves your machine** except the API calls you configure (Kroger, and Claude itself).

## The first session, in order

1. Fill in `Household/Grocery System.md`. Every bracket. The calendar list is the one that matters most: only calendars with real typed-in commitments.
2. Photos of fridge, freezer, pantry → "update the pantry."
3. Tell it your family's ten real dinners → they become Meal Library cards.
4. **Log two or three old receipts** (photos or store-account order history) → "log this receipt." This builds your baseline: what shopping cost BEFORE the system. Every month after gets measured against it. Ours showed a third of spend was snacks; yours will show something.
5. "Plan the week" → correct it out loud → approve the list.

## Family rollout

- Share the Reminders list with everyone; show them the Siri phrase once.
- Fill in `Household/How the Grocery List Works.md` (the family guide) and send it to the household.
- Optional: copy `notify-family.sh.example` to `notify-family.sh`, add your numbers, and set up the plan-day text with the launchd template beside it. First run pops a macOS prompt to allow Messages automation; click OK.

## Disruptions are normal

"We're out of milk" any day; "we skipped tacos" any night; a photo of the receipt whenever. The system absorbs all three and stays current. The weekly loop is a rhythm, not a cage.
