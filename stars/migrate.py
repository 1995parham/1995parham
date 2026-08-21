import json, sys
sys.argv=['x']
exec(open('apply.py').read().split("if __name__")[0])
DYING=['canada','lua','mcp','interview','dapps']
ids=list_ids()
print("== deleting retired lists ==")
for s in DYING:
    if s not in ids: print(f"  gone     {s}"); continue
    gql('mutation($id:ID!){ deleteUserList(input:{listId:$id}){ user{ login } } }', id=ids[s])
    print(f"  deleted  {s}")
print("\n== creating new lists ==")
cmd_lists(True)
