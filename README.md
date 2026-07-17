# Sales KPI Dashboard

A small full-stack ops app — a sales performance dashboard. Add sales, filter
them, and read back the key finance KPIs (revenue, orders, average order value,
target attainment) plus revenue breakdowns by category and channel.

This repository is the starting point for a technical exercise — see the
**[exercise brief](Technical-Exercise-Sales-KPI-Dashboard.md)** for what you'll be doing.

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite (plain JS) |
| Backend  | Python + FastAPI (asyncpg, raw SQL — no ORM) |
| Database | PostgreSQL 16 |
| Runtime  | Docker Compose |

## Setup

You need two things: **Docker Desktop** (to run the app) and **Claude Code +
VS Code** (to do the exercise). The steps differ slightly by operating system —
follow your OS below, then the shared Claude Code + VS Code steps.

### 🪟 Windows — WSL2 + Docker Desktop

On Windows, run everything inside **WSL2** (a real Linux environment). Docker,
git, and Claude Code all run from the Ubuntu shell, not PowerShell.

1. **Install WSL2.** Open **PowerShell as Administrator** and run:
   ```powershell
   wsl --install
   ```
   This installs WSL2 and Ubuntu. Reboot if prompted, then set your Ubuntu
   username/password on first launch. Verify with `wsl -l -v` (your distro
   should show **VERSION 2**).
2. **Install Docker Desktop for Windows** from
   <https://www.docker.com/products/docker-desktop/>. During/after install:
   - Settings → General → enable **Use the WSL 2 based engine**.
   - Settings → Resources → **WSL Integration** → enable your Ubuntu distro.
3. **Verify inside the Ubuntu (WSL) terminal:**
   ```bash
   docker --version && docker compose version
   ```
4. **Clone into the Linux filesystem** (e.g. `~/projects`), **not** `/mnt/c/...`
   — the Windows-mounted path is much slower for Docker bind mounts.

### 🍎 macOS — Docker Desktop

1. **Install Docker Desktop for Mac** from
   <https://www.docker.com/products/docker-desktop/>. Pick the build for your
   chip (**Apple Silicon** for M1/M2/M3+, **Intel** otherwise), drag it to
   Applications, and launch it once so the engine starts.
2. **Verify in Terminal:**
   ```bash
   docker --version && docker compose version
   ```

### 🤖 Claude Code + VS Code (Windows & macOS)

You'll use **Claude Code** as your AI coding assistant for this exercise.

1. **Install VS Code** from <https://code.visualstudio.com/>.
   - **Windows only:** also install the **WSL** extension (Microsoft) so VS Code
     runs against your Ubuntu distro — then launch the editor by typing `code .`
     from inside WSL.
2. **Install Node.js 18+** (Claude Code needs it). Check with `node --version`.
   - **macOS:** `brew install node`, or download from <https://nodejs.org/>.
   - **Windows/WSL:** install inside Ubuntu, e.g. via
     [nvm](https://github.com/nvm-sh/nvm) (`nvm install --lts`).
3. **Install Claude Code:**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
   (On Windows, run this in the **WSL/Ubuntu** terminal.)
4. **Sign in.** From the project folder, run `claude`, then use `/login` and
   follow the browser prompt.
5. **Use it in VS Code:** open the project in VS Code and run `claude` in the
   integrated terminal (or install the **Claude Code** extension from the
   Marketplace). More docs: <https://docs.claude.com/en/docs/claude-code>.

## Run it

Once Docker Desktop is running, from the project folder (on **Windows, use the
WSL/Ubuntu terminal**):

```bash
docker compose up --build
```

Then open:

| Service | URL |
|---------|-----|
| Web app | http://localhost:5173 |
| API     | http://localhost:8010 (e.g. http://localhost:8010/api/summary) |
| Postgres | localhost:5442 (user/pass/db: `sales` / `sales` / `sales`) |

The database is seeded automatically on first start with ~75 days of sample
sales and monthly targets. Sample dates are relative to *today*, so the current
month is always partially elapsed.

## Reset the data

Seeding runs only when the database is empty, so your own added/edited sales
survive restarts. To wipe everything and re-seed fresh (dated to today):

```bash
docker compose down -v && docker compose up --build
```

## Project layout

```
backend/
  main.py            FastAPI app (CORS, DB lifecycle, router wiring)
  db.py              Pool, schema, seed data, and all queries + KPI math
  sales/routes.py    HTTP routes (/api/...)
frontend/
  src/App.jsx        Dashboard shell + data loading
  src/api.js         Tiny fetch client
  src/components/    FilterBar, KpiCards, Breakdown, AddSaleForm, SalesTable
docker-compose.yml   db + api + web
```

## API quick reference

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/summary?month=&category=&channel=` | KPI totals + breakdowns |
| GET | `/api/sales?month=&category=&channel=` | List sales |
| POST | `/api/sales` | Create a sale (JSON body) |
| DELETE | `/api/sales/{id}` | Delete a sale |
| GET | `/api/filters` | Distinct months / categories / channels |
| GET | `/api/targets` | Monthly targets |
