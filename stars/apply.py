#!/usr/bin/env python3
"""Apply the star-organisation plan via the GitHub GraphQL API.

Requires the `user` scope:  gh auth refresh -h github.com -s user

  python3 apply.py lists            # create the 5 new lists
  python3 apply.py assign           # DRY RUN: file 1977 unlisted repos
  python3 apply.py assign --go      # actually do it
  python3 apply.py prune --go       # unstar the 610 dead repos
"""
import json, subprocess, sys, time, os

DONE = 'applied.log'          # resume marker: one repo id per line

def gql(q, **v):
    cmd = ['gh','api','graphql','-f',f'query={q}']
    for k,val in v.items():
        if isinstance(val,list):
            for item in val: cmd += ['-f', f'{k}[]={item}']
        else: cmd += ['-f', f'{k}={val}']
    for attempt in range(5):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0: return json.loads(r.stdout)
        if 'RATE_LIMIT' in r.stderr or 'was submitted too quickly' in r.stderr:
            time.sleep(20*(attempt+1)); continue
        raise RuntimeError(r.stderr.strip()[:400])
    raise RuntimeError('gave up after retries')

def list_ids():
    d = gql('{ viewer{ lists(first:100){ nodes{ id slug name } } } }')
    return {n['slug']: n['id'] for n in d['data']['viewer']['lists']['nodes']}

NEW = {
 '~networking':   ('🌐 Networking','Proxies, DNS, VPN, QUIC/HTTP, load balancers and packet tooling'),
 '~observability':('📈 Observability','Metrics, logs, traces and alerting — Prometheus, Grafana, OpenTelemetry'),
 '~security':     ('🔐 Security','Cryptography, secrets management, authn/authz and offensive tooling'),
 '~learning':     ('📚 Learning','Awesome lists, books, roadmaps and cheatsheets'),
 '~messaging':    ('📨 Messaging and Streaming','Kafka, NATS, RabbitMQ, gRPC and event streaming'),
}
SLUG = {'~networking':'networking','~observability':'observability','~security':'security',
        '~learning':'learning','~messaging':'messaging-and-streaming'}

def cmd_lists(go):
    have = list_ids()
    for key,(name,desc) in NEW.items():
        if SLUG[key] in have: print(f"  exists  {name}"); continue
        if not go: print(f"  CREATE  {name}  — {desc}"); continue
        gql('mutation($n:String!,$d:String!){ createUserList(input:{name:$n,description:$d,isPrivate:false}){ list{ slug name } } }',
            n=name, d=desc)
        print(f"  created {name}")

def cmd_assign(go):
    plan = json.load(open('plan.json'))
    ids  = list_ids()
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    resolved = {}
    for p in plan:
        s = p['proposed']
        resolved[s] = ids.get(SLUG.get(s, s))
    unresolved = sorted({s for s,v in resolved.items() if not v})
    if unresolved:
        print(f"!! lists not found (run `apply.py lists --go` first): {unresolved}"); return
    todo = [p for p in plan if p['id'] not in done]
    print(f"{len(todo)} to file ({len(done)} already done)")
    if not go:
        import collections
        for k,v in collections.Counter(p['proposed'] for p in todo).most_common():
            print(f"   {v:5d} -> {SLUG.get(k,k)}")
        print("\n(dry run — re-run with --go)"); return
    with open(DONE,'a') as log:
        for i,p in enumerate(todo,1):
            try:
                gql('mutation($item:ID!,$lists:[ID!]!){ updateUserListsForItem(input:{itemId:$item,listIds:$lists}){ item{ ... on Repository{ nameWithOwner } } } }',
                    item=p['id'], lists=[resolved[p['proposed']]])
                log.write(p['id']+'\n'); log.flush()
            except RuntimeError as e:
                print(f"  !! {p['name']}: {e}"); continue
            if i % 50 == 0: print(f"  {i}/{len(todo)}  last={p['name']}")
            time.sleep(0.35)
    print("done")

def cmd_prune(go):
    pr = json.load(open('prune.json'))
    print(f"{len(pr)} repos to unstar")
    if not go:
        for p in pr[:20]: print(f"   {p['stars']:6d}★ {p['pushed']}  {p['name']:44s} {p['reason']}")
        print(f"   ... and {len(pr)-20} more\n(dry run — re-run with --go)"); return
    for i,p in enumerate(pr,1):
        gql('mutation($id:ID!){ removeStar(input:{starrableId:$id}){ starrable{ id } } }', id=p['id'])
        if i % 50 == 0: print(f"  {i}/{len(pr)}")
        time.sleep(0.35)
    print("done")

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv)>1 else 'assign'
    go   = '--go' in sys.argv
    {'lists':cmd_lists,'assign':cmd_assign,'prune':cmd_prune}[what](go)
