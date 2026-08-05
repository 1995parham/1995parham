# CLAUDE.md — 1995parham

Parham Alvani's GitHub **profile README** repo. Because it is named after the
account, `README.md` renders on <https://github.com/1995parham>. There is no
build step — edit `README.md` and push.

## Layout

- `README.md` — the profile page: badge row, "About Me", the Go snippet,
  organizations list.
- `orgs/` — logos for the organizations Parham belongs to.
- `.github/workflows/snake.yml` — generates the contribution-snake SVG into the
  `output` branch. The README references that branch, not `main`.
- `languages.svg`, `streak.svg`, `logo-lg.png`, `bernard.gif` — README assets.

The badge row links to the resume release, LeetCode, Reddit, and Codeforces.
Those are the first thing a recruiter clicks, so a dead link here is expensive —
verify one before adding or keeping it. There is deliberately **no LinkedIn
badge**: Parham does not use LinkedIn, and the account the badge used to point at
is abandoned. Do not add one back.

## Cross-repo alignment (important)

`1995parham.pdf` is the **source of truth** for Parham's professional facts.
Three repos state the same information publicly and must agree:

| Repo | What it states |
|---|---|
| `1995parham.pdf` | Full resume — authoritative |
| `1995parham.github.io` | `src/pages/index.astro`, `experience.astro`, `education.astro`, `projects.astro` |
| `1995parham` (here) | `README.md` "About Me" |

Visa and sponsorship status belongs on the **resume only**, not here. This page
is read mostly by other developers, where that language reads as job-hunting
rather than as identity, and it goes stale once the move is done. Location is
fine and useful; work authorization is not.

The "About Me" opening must match the resume's headline and summary
(`src/shared/summary.typ` and `header_quote` in
`src/profile_spain/metadata.toml`) — same seniority, same positioning, same
location. This README is written in a deliberately informal voice; keep that
voice, but do not let it drift into describing a **different, more junior role**
than the resume claims. It previously opened with "I'm a Backend Developer"
while the resume said "Senior Software & Platform Engineer".
