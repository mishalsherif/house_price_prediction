import sys
import json
from urllib.request import urlopen, Request

URL = 'http://127.0.0.1:5000/metadata'

try:
    req = Request(URL, headers={'User-Agent': 'metadata-check/1.0'})
    with urlopen(req, timeout=10) as resp:
        data = json.load(resp)
except Exception as e:
    print('ERROR: failed to fetch /metadata:', e)
    sys.exit(2)

meta = data.get('metadata')
if not meta:
    print('ERROR: metadata key missing in response')
    sys.exit(2)

district_localities = meta.get('district_localities', {})
locality_area_type = meta.get('locality_area_type', {})
area_types = set(meta.get('Area_Type', []))

ok = True

if not district_localities:
    print('ERROR: district_localities mapping is empty')
    ok = False

for district, localities in district_localities.items():
    if not localities:
        print(f'ERROR: district {district!s} has no localities')
        ok = False
    for loc in localities:
        if loc not in locality_area_type:
            print(f'ERROR: locality {loc!s} (in district {district}) missing area type mapping')
            ok = False
        else:
            area = locality_area_type[loc]
            if area not in area_types:
                print(f'ERROR: locality {loc!s} has area type {area!s} not listed in Area_Type')
                ok = False

if ok:
    print('OK: metadata mappings look consistent')
    sys.exit(0)
else:
    print('\nOne or more checks failed')
    sys.exit(1)
