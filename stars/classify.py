import json, re, collections

db=json.load(open('db.json'))

def ctx(x):
    return (x['name'].lower(), (x['desc'] or '').lower(), set(t.lower() for t in x['topics']), (x['lang'] or ''))

# rule = (list_slug, topics_set, name_regex, desc_regex, langs)
R = lambda s, t=(), n=None, d=None, l=(): (s, set(t), re.compile(n) if n else None, re.compile(d) if d else None, set(l))

RULES = [
 # --- highly specific editors / tools ---
 R('obsidian', ('obsidian','obsidian-plugin','obsidian-md'), r'obsidian'),
 R('vscode', ('vscode','vscode-extension','vscode-theme'), r'vscode|vs-code', r'\bvs ?code\b|visual studio code'),
 R('emacs', ('emacs','emacs-lisp','doom-emacs'), r'emacs|doom-|spacemacs', r'\bemacs\b', ('Emacs Lisp',)),
 R('neovim', ('neovim','nvim','vim','vim-plugin','vim-colorschemes','neovim-plugin','vim-script','tree-sitter'),
   r'(^|/)(n?vim[-.]|coc-|.*\.nvim$|.*-\.?nvim)|nvim|vimrc|tree-sitter-', r'\b(neovim|nvim|vim)\b', ('Vim Script','Vim script','VimL')),
 R('latex', ('latex','tex','bibtex','xelatex','typst'), r'latex|bibtex|xepersian|xetex|typst|beamer', r'\b(latex|bibtex|typesetting)\b', ('TeX',)),

 # --- domains ---
 R('mcp', ('mcp','model-context-protocol','mcp-server'), r'mcp[-_]|[-_]mcp', r'model context protocol|\bmcp server'),
 R('llm', ('llm','llms','ai','openai','gpt','chatgpt','langchain','rag','transformers','stable-diffusion',
           'generative-ai','agents','ollama','embeddings','prompt-engineering','anthropic','claude'),
   r'llama|gpt|openai|anthropic|claude|langchain', r'\b(llm|large language model|chatgpt|gpt-4|generative ai|ai agent|prompt)\b'),
 R('ml-pipeline', ('machine-learning','deep-learning','data-science','mlops','pytorch','tensorflow','spark',
                   'airflow','kubeflow','neural-network','nlp','computer-vision','data-engineering','pandas','jupyter'),
   r'kubeflow|mlflow|airflow', r'\b(machine learning|deep learning|neural net|data pipeline|dataframe)\b'),
 R('geolocation', ('gis','geospatial','geo','maps','openstreetmap','cartography','gdal','postgis','satellite','remote-sensing','geojson'),
   r'geo|gdal|osm|postgis|leaflet|mapbox', r'\b(geospatial|geographic|satellite|map tiles|coordinates|latitude)\b'),
 R('iot', ('iot','mqtt','lorawan','lora','embedded','arduino','esp32','raspberry-pi','zigbee','coap','modbus',
           'firmware','microcontroller','rtos','sensors','embedded-systems','can-bus','bluetooth','ble'),
   r'mqtt|lora|esp32|arduino|zigbee|modbus|coap', r'\b(iot|internet of things|embedded|firmware|microcontroller|sensor)\b'),
 R('android-iphone', ('android','ios','flutter','swift','swiftui','mobile','react-native','kotlin-android','android-app'),
   r'android|flutter|(^|/)ios', r'\b(android|ios app|iphone|flutter|mobile app)\b', ('Dart','Swift','Objective-C')),
 R('dapps', ('blockchain','ethereum','web3','smart-contracts','solidity','bitcoin','cryptocurrency','defi','nft'),
   r'ethereum|blockchain|web3|solidity', r'\b(blockchain|ethereum|smart contract|cryptocurrenc)\b'),

 R('ansible', ('ansible','ansible-role','ansible-collection','ansible-playbook'), r'ansible', r'\bansible\b'),
 # --- candidate NEW lists (measured, then decided) ---
 R('~observability', ('monitoring','observability','prometheus','grafana','tracing','opentelemetry','logging',
                      'metrics','apm','alerting','telemetry','jaeger','elk','loki','victoriametrics'),
   r'prometheus|grafana|opentelemetry|jaeger|victoria|thanos|loki|alertmanager',
   r'\b(monitoring|observability|metrics|tracing|distributed trace|alerting|log aggregat)\b'),
 R('~networking', ('networking','proxy','dns','vpn','tcp','udp','quic','http3','load-balancer','tunnel','wireguard',
                   'nginx','envoy','packet','pcap','tls','socks5','reverse-proxy','network','cdn','bgp','sdn','openflow'),
   r'proxy|tunnel|wireguard|envoy|haproxy|dnscrypt|v2ray|xray|shadowsocks|netstat|tcpdump|wireshark',
   r'\b(reverse proxy|load balanc|dns |vpn|packet|network protocol|tcp/ip|nat traversal|tunnel)\b'),
 R('~security', ('security','cryptography','pentesting','vulnerability','oauth','authentication','authorization',
                 'infosec','hacking','ctf','encryption','secrets','jwt','pki','sast','fuzzing'),
   r'vault|keycloak|sops|sealed-secrets|gopass|pass-|oauth2', r'\b(security|cryptograph|encrypt|vulnerabilit|penetration test|authentication|secret manage)\b'),
 R('~messaging', ('kafka','rabbitmq','nats','pulsar','amqp','message-queue','event-driven','streaming','event-sourcing','grpc','protobuf'),
   r'kafka|rabbitmq|nats-|pulsar|amqp|(^|/)grpc|protobuf', r'\b(message broker|message queue|event stream|pub/sub|publish.subscribe)\b'),
 R('~learning', ('awesome','awesome-list','books','book','tutorial','learning','roadmap','cheatsheet','education',
                 'course','interview-questions','system-design','algorithms','data-structures','computer-science'),
   r'^[^/]+/awesome|awesome-|-book$|^books|cheat.?sheet|roadmap|100-days|system-design|(^|/)learn',
   r'\b(awesome list|curated list|cheat.?sheet|roadmap|tutorial|learning resource|free books|study)\b'),
 R('interview', ('interview','coding-interview','tech-interview'), r'interview', r'\binterview\b'),
 R('iran', ('persian','iran','farsi','iranian','amirkabir-university','jalali','shamsi'),
   r'persian|iran|farsi|jalali|shamsi|amirkabir|tehran', r'\b(persian|iranian|farsi|jalali|shamsi)\b'),

 # --- infra ---
 R('kubernetes-and-cloud', ('kubernetes','k8s','helm','docker','containers','container','cloud','terraform','istio',
                           'operator','argocd','openshift','kubernetes-operator','service-mesh','gitops','aws','gcp',
                           'azure','serverless','crd','kubectl','containerd','podman','cri','oci','cloud-native'),
   r'kube|k8s|helm|istio|argo|terraform|docker|containerd|podman|crossplane|flux',
   r'\b(kubernetes|k8s|helm chart|container runtime|service mesh|gitops|cloud.native|terraform)\b'),
 R('database', ('database','sql','postgres','postgresql','mysql','mongodb','redis','nosql','clickhouse',
                'elasticsearch','orm','sqlite','migrations','timeseries','key-value','cassandra','etcd','tidb'),
   r'postgres|mysql|mongo|redis|sqlite|clickhouse|elastic|cassandra|(^|/)etcd|badger|leveldb|rocksdb',
   r'\b(database|sql |nosql|key.value store|time.series|orm\b|query engine)\b'),
 R('services', ('self-hosted','selfhosted','self-hosting','saas','groupware'),
   None, r'\b(self.hosted|runs as a service|web application|open.source alternative)\b'),
 R('desktop', ('linux','arch-linux','wayland','sway','i3','window-manager','macos','theme','dotfiles','gtk',
               'desktop','ricing','colorscheme','wm','x11','hyprland','fonts','font','icons','gnome','kde','compositor','statusbar'),
   r'sway|wayland|hypr|i3-|dotfiles|catppuccin|dracula|nord-|gruvbox|-theme$|waybar|rofi|dmenu|polybar',
   r'\b(wayland|window manager|desktop environment|color ?scheme|theme for|dotfiles|status bar|launcher)\b',
   ()),

 R('research', ('research','paper','simulation','academic','ns3','optimization','simulator'),
   r'mininet|ns-3|ns3|simul', r'\b(research|academic|paper|simulator|thesis)\b'),
 R('tools-and-actions', ('cli','command-line','terminal','github-actions','productivity','shell','bash','zsh',
                         'tui','git','automation','devops','linter','formatter','pre-commit','ci','ci-cd'),
   r'^actions/|-action$|action-|(^|/)gh-|cli$', r'\b(command.line|cli tool|github action|terminal|shell script)\b'),

 # --- language ecosystems (libraries) ---
 R('ansible', (), None, None, ('Jinja',)),
 R('php', ('php','laravel','symfony','composer','wordpress'), r'laravel|php', None, ('PHP',)),
 R('java', ('java','spring','spring-boot','gradle','maven','kotlin','jvm','scala'), r'gradle|maven|spring-', None, ('Java','Kotlin','Scala','Groovy','Clojure')),
 R('lua', (), None, None, ('Lua',)),
 R('c', ('c','cpp','c-plus-plus','assembly','systems-programming','compiler','kernel'), None, None, ('C','C++','Assembly','Zig','Ada','Fortran','Objective-C')),
 R('rust', (), None, None, ('Rust',)),
 R('golang', (), None, None, ('Go','Go Template')),
 R('python', (), None, None, ('Python','Jupyter Notebook','Cython')),
 R('nodejs-and-javascript', ('javascript','typescript','react','vue','angular','nodejs','node','frontend','css',
                             'html','webpack','svelte','nextjs','tailwindcss','bootstrap','web-components'),
   None, None, ('JavaScript','TypeScript','Vue','CSS','SCSS','HTML','Svelte','MDX','Astro')),

 # --- final-pass rules for the residual ---
 R('iran', (), r'^(aut-|aut$|ce-aut|1995parham-teaching|linuxfestival|querateam|aut-nlp|aut-icpc)', None),
 R('desktop', ('aur','archlinux','arch','homebrew','brew','packaging','distro','grub','bootloader','fonts'),
   r'(^|/)aur$|archlinux|homebrew-|-fonts?$|grub', r'\b(arch linux|aur |homebrew|font family|typeface|linux distro)\b', ('Ruby',)),
 R('research', (), None, None, ('VHDL','Verilog','SystemVerilog','Julia','Haskell','Erlang','Elixir','Coq','MATLAB','R')),
 R('tools-and-actions', (), None, None, ('Shell','Makefile','Perl','Awk','Dockerfile','Nix','Just','CMake','PowerShell','Batchfile')),
]


# --- owner prior: learn from Parham's own past list decisions ---
import collections as _c
_owner=_c.defaultdict(_c.Counter)
for _x in db:
    if len(_x['lists'])==1:
        _owner[_x['name'].split('/')[0].lower()][_x['lists'][0]]+=1
OWNER_PRIOR={}
for _o,_cnt in _owner.items():
    _top,_n=_cnt.most_common(1)[0]
    if _n>=2 and _n/sum(_cnt.values())>=0.6: OWNER_PRIOR[_o]=_top

def classify(x):
    name, desc, tops, lang = ctx(x)
    o=name.split('/')[0]
    if o in OWNER_PRIOR: return OWNER_PRIOR[o], 'owner'
    if re.search(r'[\u0600-\u06FF]{4,}', x['desc'] or ''): return 'iran', 'persian'
    for slug, T, N, D, L in RULES:
        if T & tops: return slug, 'topic'
        if N and N.search(name): return slug, 'name'
        if D and D.search(desc): return slug, 'desc'
        if L and lang in L: return slug, 'lang'
    return None, None

# ---------------------------------------------------------------- outputs
# Lists retired in favour of the five new ones; their members are rehomed by
# rehome.py before migrate.py deletes them.
REMAP = {'mcp':'llm', 'lua':'neovim', 'dapps':'golang', 'interview':'~learning'}
# Never propose unstarring anything filed here. These are kept as an archive
# rather than for being actively maintained -- students' projects are mostly
# dead by design, and a staleness rule would happily delete all of them.
PROTECT = {'students', 'iran', 'research'}

un = [x for x in db if not x['lists']]
res, why, out = collections.Counter(), collections.Counter(), []
for x in un:
    s, w = classify(x)
    s = REMAP.get(s, s)
    res[s or '**UNMATCHED**'] += 1
    why[w or 'none'] += 1
    out.append(dict(x, proposed=s, via=w))
json.dump(out, open('proposed.json','w'), indent=0)

plan = [x for x in out if x['proposed']]
json.dump(plan, open('plan.json','w'), indent=1)

prop = {x['name']: x['proposed'] for x in out}
prune = []
for x in db:
    bucket = x['lists'][0] if x['lists'] else (prop.get(x['name']) or '').lstrip('~')
    if bucket in PROTECT:
        continue
    if x['archived']:
        reason = 'archived upstream'
    elif (x['pushed'] or '9999') < '2021-01' and x['stars'] < 100:
        reason = f"no commits since {x['pushed']}, {x['stars']} stars"
    else:
        continue
    prune.append({'name':x['name'], 'id':x['id'], 'reason':reason, 'stars':x['stars'],
                  'pushed':x['pushed'], 'lists':x['lists'], 'desc':x['desc']})
json.dump(prune, open('prune.json','w'), indent=1)

print(f"classified {len(plan)}/{len(un)} unlisted repos")
print("\n=== proposed distribution ===")
for k, v in res.most_common():
    print(f"  {v:5d} {k}")
print("\nsignal:", dict(why))
print(f"\nplan.json  {len(plan)} assignments")
print(f"prune.json {len(prune)} unstar candidates ({', '.join(sorted(PROTECT))} protected)")
