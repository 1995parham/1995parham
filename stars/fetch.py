#!/usr/bin/env python3
"""Pull every starred repo and every star list into db.json.

    python3 fetch.py

Writes stars.json (raw REST), lists.json (lists + members) and db.json (the
joined view every other script reads). Needs no special scope -- reading is
fine with a default `gh auth login` token.
"""
import collections
import json
import subprocess


def gql(query, **variables):
    cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']
    for key, value in variables.items():
        cmd += ['-f', f'{key}={value}']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:400])
    return json.loads(result.stdout)


def fetch_stars():
    """Every starred repo, via the REST API (GraphQL has no `topics` shortcut)."""
    out = subprocess.run(
        ['gh', 'api', '--paginate', 'user/starred?per_page=100'],
        capture_output=True, text=True, check=True)
    stars = json.loads(out.stdout)
    json.dump(stars, open('stars.json', 'w'))
    print(f"stars.json  {len(stars)} repos")
    return stars


def fetch_lists():
    """Every star list and its members.

    There is no `user.list(slug:)` field, so members are paginated through
    node(id:) on each list.
    """
    data = gql('{ viewer{ lists(first:100){ nodes{ id name slug description isPrivate } } } }')
    lists = data['data']['viewer']['lists']['nodes']

    items_query = '''query($id:ID!,$c:String){ node(id:$id){ ... on UserList {
      items(first:100, after:$c){ pageInfo{hasNextPage endCursor}
        nodes{ ... on Repository { id nameWithOwner isArchived } } } } } }'''

    for entry in lists:
        items, cursor = [], ""
        while True:
            page = gql(items_query, id=entry['id'], c=cursor)['data']['node']['items']
            items += [n for n in page['nodes'] if n.get('nameWithOwner')]
            if not page['pageInfo']['hasNextPage']:
                break
            cursor = page['pageInfo']['endCursor']
        entry['items'] = items
        print(f"  {entry['slug']:26s} {len(items):4d}  {entry['name']}")

    json.dump(lists, open('lists.json', 'w'), indent=1)
    print(f"lists.json  {len(lists)} lists")
    return lists


def build_db(stars, lists):
    """Join the two into the flat record every other script reads."""
    membership = collections.defaultdict(list)
    for entry in lists:
        for item in entry['items']:
            membership[item['nameWithOwner']].append(entry['slug'])

    db = [dict(name=r['full_name'],
               id=r['node_id'],
               lang=r['language'],
               desc=(r['description'] or '')[:300],
               topics=r.get('topics') or [],
               archived=r['archived'],
               pushed=(r['pushed_at'] or '')[:7],
               stars=r['stargazers_count'],
               lists=sorted(membership.get(r['full_name'], [])))
          for r in stars]

    json.dump(db, open('db.json', 'w'))
    unlisted = sum(1 for x in db if not x['lists'])
    print(f"db.json     {len(db)} repos, {len(db) - unlisted} filed, {unlisted} unlisted")


if __name__ == '__main__':
    build_db(fetch_stars(), fetch_lists())
