# Technical Exercise — Sales KPI Dashboard

Welcome, and thanks for taking the time. This exercise is about **working
effectively with an AI coding assistant (Claude Code)** while genuinely
**understanding** the code you ship — not just producing it.

You'll work in the provided repository — a small but real full-stack app
(React + FastAPI + Postgres). **Clone it and follow the setup in its README:**

```bash
git clone https://github.com/WFH-Holding-Group/technical_test_ops_app.git
```

**Get it running first** and click around so you understand what it does.

There are **four parts**. Use Claude Code freely throughout. We care as much
about *how you think and explain* as about the final diff.

**Suggested time:** ~2–3 hours for Parts A–C, then ~20–30 minutes to prepare
Part D. Commit your work as you go so we can follow your progress.

**Questions?** If you get stuck or need any clarification, reach out to Jeremy at
[jeremy@findyourtribe.co](mailto:jeremy@findyourtribe.co) — we're happy to help.

---

## Part A — Fix the bugs 🐞

This dashboard has **several correctness bugs**: some of the numbers it reports
are wrong. We won't tell you where they are or how many — finding them is part
of the exercise.

- Explore the app, compare what it shows against what the data *should* produce,
  and track down the causes.
- Fix them cleanly.
- For each bug, be ready to explain in Part D: **what was wrong, why it produced
  the wrong result, and how your fix addresses it.**

> Tip: the sample data is deterministic, so you can reason about expected totals
> by hand or with a quick script.

## Part B — Build an enhancement ✨

Add a **"Pace to Target"** panel that forecasts whether the selected month will
hit its sales target, based on the pace so far.

For the selected month, show:

| Metric | Meaning |
|--------|---------|
| **Month-to-date revenue** | net revenue from completed sales so far this month |
| **Days elapsed / days in month** | how far into the month we are |
| **Projected month-end revenue** | run-rate forecast = `MTD ÷ days elapsed × days in month` |
| **Target** | the month's target |
| **Pace vs target** | projected vs target (RM and %), with an **on-track / at-risk** indicator |

**Handle these cases correctly** (this is the point of the exercise):

- A **past** (already finished) month → there is no remainder to project;
  projected should equal the actual month total.
- A **future** month → nothing has happened yet (0 days elapsed) → must not
  divide by zero; show a sensible "N/A".
- Months have **28/29/30/31** days (February in a leap year is 29).
- Use the **correct calendar date for "today"** (this project's timezone is
  Malaysia, UTC+8).
- No `NaN` / `Infinity` when a target is missing or 0 days have elapsed.

You may add a backend endpoint and a frontend panel, in whatever shape you think
is clean. Be ready to explain your edge-case handling.

## Part C — Innovation 💡

Add **one improvement of your own choosing** — something you think makes the
product genuinely better. Scope it so you can finish and explain it.

Some directions (you are **not** limited to these): CSV export, a revenue trend
sparkline, a refund-rate metric, a "top products" ranking, inline editing,
keyboard shortcuts, dark mode, better empty/loading states, tests.

Be ready to explain *why* you picked it and what it adds.

## Part D — Present it 🎤

Prepare a **short slide deck** (≈5–8 slides) and walk us through it. Use Claude
to help you design/generate the slides quickly — that's encouraged.

Cover:

1. **Bugs** — what you found, why each was wrong, how you fixed it.
2. **Enhancement** — how your Pace-to-Target feature works and how you handled
   the tricky cases.
3. **Innovation** — what you built and why.

Also touch briefly on **how you used Claude Code** — where it helped, and where
you had to steer or correct it.

---

## Submitting your work

When you're finished, share your work as a **GitHub repository** and reply to our
email with the link.

- **Commit as you go** in small, meaningful steps — we like to see how your work
  progressed, not just the final state (please don't squash or force-push over
  your history).
- Push everything to **your own public GitHub repo** (you won't have push access
  to the original).
- Include your **Part D slides** in the repo (or a link to them) alongside the code.
- **Reply to our email with the GitHub repository link** once you're done.

## What we're evaluating

- **Correctness** — are the numbers right, and are the edge cases handled?
- **Understanding** — can you clearly explain *why*, not just *what*?
- **Code quality** — clean, readable, consistent with the existing code.
- **Effective AI use** — using Claude Code to move fast *and* stay in control.
- **Communication** — a clear, confident walkthrough.

Good luck — have fun with it!
