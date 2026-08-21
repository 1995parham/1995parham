#!/usr/bin/env python3
"""Build star-atlas.html -- the browsable index of every star and its filing.

    python3 atlas.py

Reads db.json, plan.json and prune.json; stitches templates/head.html and
templates/body.html around an embedded JSON payload.
"""
import json
import os

SLUG = {'~networking': 'networking', '~observability': 'observability',
        '~security': 'security', '~learning': 'learning',
        '~messaging': 'messaging-and-streaming'}
NEW = set(SLUG.values())


def build_payload():
    db = json.load(open('db.json'))
    plan = {x['name']: (x['proposed'], x['via']) for x in json.load(open('plan.json'))}
    prune = {p['name']: p['reason'] for p in json.load(open('prune.json'))}

    rows = []
    for x in db:
        current = x['lists'][0] if x['lists'] else ''
        proposed, via = plan.get(x['name'], ('', ''))
        rows.append([x['name'], x['lang'] or '', x['desc'], x['stars'], x['pushed'],
                     current, SLUG.get(proposed, proposed), via or '',
                     1 if x['archived'] else 0, prune.get(x['name'], '')])

    meta = dict(total=len(db),
                listed=sum(1 for r in rows if r[5]),
                assigned=sum(1 for r in rows if r[6]),
                review=sum(1 for r in rows if not r[5] and not r[6]),
                prune=len(prune),
                newlists=sorted(NEW))
    return {'meta': meta, 'rows': rows}


def main():
    payload = json.dumps(build_payload(), separators=(',', ':'))
    # The payload is embedded in a <script type="application/json"> block, so a
    # literal `</script>` anywhere in a repo description would end the tag early
    # and break the parse. Escaping `<` avoids that; U+2028/9 are not valid raw
    # in a JS string literal either.
    payload = (payload.replace('<', '\\u003c')
                      .replace(' ', '\\u2028')
                      .replace(' ', '\\u2029'))

    here = os.path.dirname(os.path.abspath(__file__))
    head = open(os.path.join(here, 'templates', 'head.html')).read()
    body = open(os.path.join(here, 'templates', 'body.html')).read()

    with open('star-atlas.html', 'w') as fh:
        fh.write(head + body.replace('__PAYLOAD__', payload))
    print(f"star-atlas.html  {os.path.getsize('star-atlas.html') // 1024}KB")


if __name__ == '__main__':
    main()
