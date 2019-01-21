# -*- coding: utf-8 -*-

import json


def dump_json(label, data):
    print(label)
    print(json.dumps(data, ensure_ascii=True, sort_keys=True, indent=4))
