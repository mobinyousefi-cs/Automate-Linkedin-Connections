# LinkedIn Connections Automator (Educational)

Automate **limited and careful** LinkedIn connection flows using Python + Selenium with a clean CLI.
This project is designed for **learning automation patterns** (waiting, selectors, CLI structure, CI, etc.).
It defaults to **dry-run** mode for safety.

> ⚠️ **Disclaimer**
> Automating LinkedIn may violate LinkedIn’s Terms of Service and can lead to account restrictions.
> Use this repository for **educational purposes** only. If you ever switch off dry-run, proceed cautiously,
> at low volume, and at your own risk.

---

## Features

* ✅ Typer CLI (`python -m linkedin_auto …`)
* ✅ Dry-run mode (default) — safe simulation
* ✅ Login check command
* ✅ Connect via:

  * a list of profile URLs, or
  * people search results for a query (with per-page caps)
* ✅ Optional personalized note (≤280 chars)
* ✅ Human-like randomized delays + explicit waits
* ✅ `src/` layout, tests with pytest, Ruff + Black, GitHub Actions CI

---

## Quickstart

### 1. Python

Python 3.9+ recommended.

### 2. Install

```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Edit LI_EMAIL, LI_PASSWORD, keep LI_DRY_RUN=true at first
```

### 4. Try login (non-intrusive)

```bash
python -m linkedin_auto login-check
```

### 5. Dry-run on a list of profiles

```bash
echo "https://www.linkedin.com/in/someone/" > profiles.txt
python -m linkedin_auto connect-urls -f profiles.txt --note "Hi, enjoyed your post about X!"
```

### 6. Dry-run on a search query

```bash
python -m linkedin_auto connect-search "Data Scientist Milan" --pages 1
```

---

## Environment Variables

| Variable                   | Default | Description                                                 |
| -------------------------- | ------- | ----------------------------------------------------------- |
| `LI_EMAIL`                 | —       | LinkedIn account email                                      |
| `LI_PASSWORD`              | —       | LinkedIn account password                                   |
| `LI_DRY_RUN`               | `true`  | If `true`, simulates actions without clicking *Send*        |
| `LI_HEADLESS`              | `true`  | Run Chrome headless                                         |
| `LI_PROFILE_DIR`           | —       | Optional Chrome user profile dir (retains sessions/cookies) |
| `LI_IMPLICIT_WAIT`         | `1.0`   | Selenium implicit wait (s)                                  |
| `LI_PAGE_LOAD_TIMEOUT`     | `45.0`  | Page load timeout (s)                                       |
| `LI_MAX_CONNECTS_PER_PAGE` | `10`    | Cap invites sent per search page                            |
| `LI_HUMAN_DELAY_MIN`       | `1.0`   | Lower bound for random sleep (s)                            |
| `LI_HUMAN_DELAY_MAX`       | `2.75`  | Upper bound for random sleep (s)                            |
| `LI_NOTE_TEMPLATE`         | —       | Optional default note text (≤280 chars)                     |

---

## Notes on Selectors

LinkedIn’s DOM changes over time. The provided XPaths are **best-effort** and may need adjustments.
Use browser devtools to confirm button labels and structure (`Connect`, `More`, `Send`, etc.).

---

## Development

* **Lint:** `ruff check .`
* **Format:** `black .`
* **Test:** `pytest -q`

CI runs Ruff, Black (check), and pytest on every push/PR.

---

## Legal & Ethics

* Respect platform rules and user consent.
* Prefer manual, meaningful networking over automation.
* Keep volumes low and avoid spammy behavior.
* This software is provided **as-is**, without warranty (MIT License).

