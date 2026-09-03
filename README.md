# Grocery Autopilot Starter

A complete starter kit that turns Claude Code into your family's grocery manager: a weekly dinner plan built around your actual calendar, a shopping list that prices itself at your Kroger, and a cart that loads itself for pickup. You approve one list a week; the system does the rest.

Built by [Pioneer AI & Data](https://pioneeraidata.com). Free to use, copy, and share.

## What it does

- **One shared list.** Your existing Apple Reminders grocery list becomes the family's front door. Anyone adds items by Siri or typing; the weekly plan sweeps everything in.
- **A dinner week that fits your life.** It reads the calendars you tell it to, gives busy nights quick meals, keeps variety rules (nothing repeats, no two same-cuisine nights in a row), and always includes a path for the picky eater.
- **Real prices before you shop.** With a free Kroger developer account, every list is priced at your actual store, promos flagged, aisle numbers included, and the order lands in your real Kroger cart for pickup. You just pick the slot and pay.
- **A budget that trends down.** Receipts get logged, off-list spending gets visible, and the month is measured against your target. Our own first month found 36% of spend was snacks and desserts; the first system order came in at $54 against a $136 in-store average.
- **Plain text you own.** Everything lives in Markdown notes on your machine. No subscription beyond the Claude you already use, no new apps for the family.

## What you need

- A Mac or Windows computer with [Claude Code](https://claude.com/claude-code) (text alerts and Apple Reminders integration are Mac extras; `Guides/Windows Setup.md` has the Windows equivalents). Built for Claude Code; other agentic CLIs (OpenAI's Codex CLI, Google's Gemini CLI) can run it too, see the note in `Guides/Setup Guide.md`
- A shared grocery list your family already uses (Apple Reminders on Mac gets deep integration; any shared list app works)
- Optional power-up: a free [Kroger developer account](https://developer.kroger.com) for live prices and cart loading
- Obsidian if you like nice note viewing; plain text editors work fine

## How to start

1. Open this folder in Claude Code.
2. Read `Start Here.md` and follow the 20-minute checklist.
3. Fill in `Household/Grocery System.md`: your budget target, your stores, which calendars count, who eats what.
4. Take photos of your fridge, freezer, and pantry, drop them into the chat, and say **"update the pantry."**
5. Say **"plan the week."** You're running.

## Structure

```
Start Here.md               Front door and setup checklist
Why This Exists.md          The idea, with our real numbers
AGENTS.md                   Safety rails for the AI (read it, it matters)
Household/                  Your data: rules, pantry, staples, meals, plans, spending log
Guides/                     Setup, the Kroger API power-up, and the weekly rhythm
.claude/skills/grocery/     The skill Claude Code runs, plus the Kroger scripts
```

House rules inherited from the design: plain English, no em dashes, your family's names and numbers never leave your machine.
