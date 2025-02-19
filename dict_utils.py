from typing import List, Dict
import json

def appendIfNotExists(src:List[dict], dest:List[dict]):
    for s in src:
        d = [x for x in dest if x['id'] == s['id']]
        if len(d) == 1:
            continue
        else:
            print(f"add {json.dumps(s)}")
            dest += [s]
    return dest