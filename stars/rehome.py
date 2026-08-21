import json, sys
sys.argv=['x']
exec(open('apply.py').read().split("if __name__")[0])
ids=list_ids()
for p in json.load(open('rehome.json')):
    tgt=[ids[SLUG.get(s,s)] for s in p['to']]
    gql('mutation($item:ID!,$lists:[ID!]!){ updateUserListsForItem(input:{itemId:$item,listIds:$lists}){ item{ ... on Repository{ nameWithOwner } } lists{ slug } } }',
        item=p['id'], lists=tgt)
    print(f"  {p['name']:44s} -> {[SLUG.get(s,s) for s in p['to']]}")
print("rehomed", len(json.load(open('rehome.json'))))
