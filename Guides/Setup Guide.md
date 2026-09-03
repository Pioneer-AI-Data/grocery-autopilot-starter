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

## Running it with another AI assistant

The kit is Markdown, Python, and instructions, none of it Claude-only. What it needs is an AGENTIC assistant: one that reads and writes your local files and runs commands. That means the terminal agents (Claude Code first-class; OpenAI's Codex CLI and Google's Gemini CLI workable), never the chat apps: ChatGPT or Gemini in a browser cannot touch your pantry notes or run the Kroger scripts.

On a non-Claude CLI, two adjustments:

1. Automatic skill loading is Claude Code plumbing. Start each grocery session with "read `.claude/skills/grocery/SKILL.md` and follow it," or copy that file's contents into your agent's own context file (Codex reads this kit's `AGENTS.md` natively; Gemini CLI uses `GEMINI.md`).
2. Hold the safety rails yourself until you trust the setup: the "never check out, review every cart" rules are instructions, and different models follow instructions differently. Photo inventory also depends on your CLI's image support.

