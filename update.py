#!/usr/bin/env python3

import urllib.request, json 
from collections import OrderedDict

template = None
with open('template.json') as json_file:
    template = json.load(json_file, object_pairs_hook=OrderedDict)

# Read values from status.json
try:
    with urllib.request.urlopen('https://status.k4cg.org/status.json') as url:
        data = json.loads(url.read().decode())
        if data['door'] == 'open':
            template['state']['open'] = True
        elif data['door'] == 'closed':
            template['state']['open'] = False

        template['sensors']['temperature'][0]['value'] = data['temperature']
        template['sensors']['humidity'][0]['value'] = data['humidity']
        template['sensors']['network_connections'][0]['value'] = data['online']

except Exception as e:
    print(e)

with open('spacestatus.json', 'w') as outfile:
    json.dump(template, outfile, indent=4)
