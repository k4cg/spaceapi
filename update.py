#!/usr/bin/env python3

import time
import urllib.request
import json
import traceback
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

        template['sensors']['temperature'].append({
            'value': data['temperature'],
            'unit': '°C',
            'location': 'Inside'
        })

        template['sensors']['humidity'].append({
            'value': data['humidity'],
            'unit': '%',
            'location': 'Inside'
        })

        template['sensors']['network_connections'].append(
            {'value': data['online']}
        )

except Exception as e:
    traceback.print_exc()
    print(e)

# Last change
template['state']['lastchange'] = int(time.time())

with open('spaceapi.json', 'w') as outfile:
    json.dump(template, outfile, indent=4)
