# -*- coding: utf-8 -*-

from .driver import Driver
from .parser import parse


class Exporter:
    def __init__(self, **kwargs: dict):
        self.driver = Driver(**kwargs)

    def export(self):
        grants = []

        for uh in self.driver.each_user():
            user = uh['user']
            host = uh['host']

            create_user = self.driver.show_create_user(user, host)

            for stmt in self.driver.show_grants(user, host):
                grants.append(parse(stmt, create_user))

        return self.pack(grants)

    @classmethod
    def pack(cls, grants: list = None):
        packed = {}
        for grant in grants:
            user = grant.pop('user')
            host = grant.pop('host')
            user_host = '@'.join([user, host])
            obj = grant.pop('object')
            identified = grant.pop('identified')
            required = grant.pop('required')

            if user_host not in packed:
                packed[user_host] = {
                    'user': user,
                    'host': host,
                    'objects': {},
                    'options': {
                        'identified': '',
                        'required': '',
                    },
                }

            packed[user_host]['objects'][obj] = grant
            if required:
                packed[user_host]['options']['required'] = required
            if identified:
                packed[user_host]['options']['identified'] = identified

        return packed
