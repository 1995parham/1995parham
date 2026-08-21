# stars

Tooling that files the account's starred repositories into GitHub star lists.

This is a maintenance pipeline, not part of the profile page — nothing here is
rendered by `README.md`. It exists because the star count outgrew what anyone
can curate by hand.

## The API, and its limits

Star lists have **no REST API** and `gh` has no porcelain for them, but they are
fully scriptable over GraphQL: `createUserList`, `updateUserList`,
`deleteUserList` and `updateUserListsForItem`. Three constraints shape every
script here:

- **The mutations need the `user` scope**, which a default `gh auth login` token
  does not carry. Grant it once with `gh auth refresh -h github.com -s user`.
  Reading (`fetch.py`) works without it.
- **`updateUserListsForItem` replaces** a repo's entire list set rather than
  adding to it. Always send the full desired set, or you will silently drop the
  memberships you did not mention. This is why `apply.py assign` only touches
  repos that are in *no* list — their "before" set is empty, so nothing can be
  clobbered.
- **GitHub caps an account at 32 lists.** Adding a list means retiring one, so
  `migrate.py` deletes before it creates, and `rehome.py` moves the retired
  lists' members somewhere else first.

Unstarring a repo also removes it from every list, so `prune` must run *after*
`assign` — or, better, prune first and drop those repos from the plan, since
filing something you are about to unstar is wasted work.

## Pipeline

```sh
python3 fetch.py                 # stars + lists -> db.json
python3 classify.py              # db.json -> plan.json, prune.json
python3 atlas.py                 # -> star-atlas.html, to eyeball the plan

python3 apply.py lists           # dry run; --go to create the new lists
python3 rehome.py                # move retired lists' members to their absorbers
python3 migrate.py               # delete retired lists, create the new ones

python3 apply.py assign          # dry run; --go to file everything
python3 apply.py prune           # dry run; --go to unstar the dead
```

Every `apply.py` verb dry-runs unless given `--go`. `assign` is resumable: each
completed repo id is appended to `applied.log` and skipped on the next run, so
an interrupted run is safe to restart.

## How the classifier decides

`classify.py` learns the existing conventions rather than imposing new ones:

- **One list per repo.** The hand-curated lists are overwhelmingly single-listed,
  so the classifier assigns exactly one.
- **Domain beats language.** `cilium` is filed under kubernetes-and-cloud, not
  golang; `k9s` under tools-and-actions, not golang. Language lists are for
  libraries and language-ecosystem tooling, and the rule order encodes that —
  purpose rules run before the language fallbacks.
- **Owner priors beat everything.** If an owner already has two or more repos
  filed, and 60% of them agree on a list, a new repo from that owner inherits
  it. This is the single strongest signal, because it replays decisions already
  made by hand.

`PROTECT` in `classify.py` keeps `students`, `iran` and `research` out of the
prune set entirely. Those lists are an archive, not a set of dependencies —
students' projects are mostly dead by design, and a staleness rule would happily
delete every one of them.

Roughly 4% of repos match no rule at all, usually because they have neither a
description nor topics. They are left unfiled rather than guessed at, and show
up under "Need a look" in the atlas.
