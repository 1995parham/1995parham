# CLAUDE.md — 1995parham

Parham Alvani's GitHub **profile README** repo. Because it is named after the
account, `README.md` renders on <https://github.com/1995parham>. There is no
build step — edit `README.md` and push.

## Layout

- `README.md` — the profile page: header + badge rows, "About Me", tech-stack
  badges, a "Things I've Built" table, the organizations tables, the Go snippet.
- `orgs/` — logos for the organizations Parham belongs to.
- `.github/workflows/snake.yml` — generates the contribution-snake SVG into the
  `output` branch. The README references that branch, not `main`.
- `logo-lg.png`, `bernard.gif`, `she-said-yes.jpg` — README assets. `languages.svg`
  and `streak.svg` used to live here too; they were leftovers of the deleted
  metrics workflow, went stale, and are gone. Do not re-add generated stat
  widgets — they were removed on purpose.

The badge rows link to the homepage, the resume release, `@elaheh-dastan`,
LeetCode, Codeforces, Reddit, WakaTime, and 16personalities. Those are the first
thing a recruiter clicks, so a dead link here is expensive — verify one before
adding or keeping it. Note that LeetCode, Reddit, Codeforces and 16personalities
all answer `403` to `curl`; that is bot-blocking, not a dead link. Check them
through their APIs (`codeforces.com/api/user.info`, `leetcode.com/graphql`) or in
a browser rather than concluding from the status code.

The partner badge and the `inLove(...)` line in the Go snippet must point at the
same handle. It is **`@elaheh-dastan`** — the older `@elahe-dastan` spelling 404s
and sat broken in this README for a long time.

There is deliberately **no LinkedIn badge**: Parham does not use LinkedIn, and the
account the badge used to point at is abandoned. Do not add one back.

Repo cards in "Things I've Built" use live `img.shields.io/github/stars/...`
badges rather than hardcoded counts, so the numbers cannot rot. Org rows use
`avatars.githubusercontent.com/u/<id>` — the same panda art tracked in `orgs/`,
served by GitHub instead of committed twice. Accent color is `#A1E477`, the
background token from `orgs/README.md`, so the README and the avatars read as one
set.

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
