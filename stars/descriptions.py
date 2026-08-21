#!/usr/bin/env python3
"""Set the description on each star list.

    python3 descriptions.py          # dry run, shows before -> after
    python3 descriptions.py --go     # write

Only the entries below are touched; any list not named here is left exactly as
it is. The house style is short, first-person and a little wry -- "It's the
way", "Why?", "No, please no!" -- so anything written here matches that rather
than reading like a product catalogue.
"""
import json
import subprocess
import sys

# slug -> description. Deliberately not a full inventory of every list: the
# hand-written ones that already read well are absent and stay untouched.
DESCRIPTIONS = {
    # --- were empty ---
    'iran':                    'Persian fonts, Jalali dates and code from home.',
    'llm':                     'Running the models locally, mostly.',

    # --- created by the filing pipeline, rewritten in the house voice ---
    'networking':              'Packets, proxies and everything between two hosts.',
    'observability':           'If it is not a metric, it did not happen.',
    'security':                'Keys, secrets and the people who want them.',
    'learning':                'Awesome lists and things I keep meaning to read.',
    'messaging-and-streaming': 'Someone publishes, someone else subscribes.',

    # --- same meaning and voice, tidied wording ---
    'golang':                  'Golang projects, libraries and everything else.',
    'services':                'Applications that run as a service, from Syncthing to Jira.',
    'just-for-having-fun':     'Nothing but funny repositories: useless applications, icons and the like.',
    'research':                'How we do the research, from tools to applications.',
}


def gql(query, **variables):
    cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']
    for key, value in variables.items():
        cmd += ['-f', f'{key}={value}']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:400])
    return json.loads(result.stdout)


def main(go):
    data = gql('{ viewer{ lists(first:100){ nodes{ id slug name description } } } }')
    lists = {n['slug']: n for n in data['data']['viewer']['lists']['nodes']}

    unknown = set(DESCRIPTIONS) - set(lists)
    if unknown:
        print(f"!! no such list: {sorted(unknown)}")
        return

    for slug, description in DESCRIPTIONS.items():
        entry = lists[slug]
        if (entry['description'] or '').strip() == description:
            print(f"  ok      {slug}")
            continue
        print(f"  {'set    ' if go else 'WOULD  '} {slug}")
        print(f"      was: {entry['description'] or '(empty)'}")
        print(f"      now: {description}")
        if go:
            # `name` is optional but sending it keeps the emoji title intact.
            gql('mutation($id:ID!,$n:String!,$d:String!){'
                ' updateUserList(input:{listId:$id,name:$n,description:$d}){ list{ slug } } }',
                id=entry['id'], n=entry['name'], d=description)

    if not go:
        print("\n(dry run -- re-run with --go)")


if __name__ == '__main__':
    main('--go' in sys.argv)
