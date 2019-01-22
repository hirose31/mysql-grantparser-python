# -*- coding: utf-8 -*-

# workaround for https://bugs.mysql.com/bug.php?id=89889
# at first load libcrypto.so and libssl.so from system library path.
import ssl  # noqa: F401
import mysql.connector
import re

re_numeric_part = re.compile(r'^(\d+)')


def numeric_part(s: str = None):
    m = re_numeric_part.match(s)
    if m:
        return int(m.group(1))
    return None


class Driver:
    def __init__(self, **kwargs: dict):
        if 'connection' in kwargs:
            self.connection = kwargs['connection']
        else:
            option = {
                'connect_timeout': 8,
                'user': 'root',
                'use_unicode': True,
                'charset': 'utf8',
            }
            option.update(kwargs)
            self.connection = mysql.connector.connect(**option)

        self.server_version = tuple([numeric_part(n)
                                     for n in self.connection.get_server_info().split('.')[:3]])

    def cursor(self, **args):
        return self.connection.cursor(**args)

    def each_user(self):
        cursor = self.cursor(dictionary=True)
        cursor.execute('SELECT user, host FROM mysql.user')
        for uh in cursor.fetchall():
            yield uh

    def show_grants(self,
                    user: str = None,
                    host: str = None,
                    ):
        cursor = self.cursor()
        cursor.execute('SHOW GRANTS FOR %s@%s', (user, host))
        for sg in cursor.fetchall():
            yield sg[0]

    def show_create_user(self,
                         user: str = None,
                         host: str = None,
                         ):
        if self.server_version < (5, 7, 6):
            return ''
        cursor = self.cursor()
        cursor.execute('SHOW CREATE USER %s@%s', (user, host))
        return cursor.fetchone()[0]
