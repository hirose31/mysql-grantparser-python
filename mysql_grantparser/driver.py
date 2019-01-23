# -*- coding: utf-8 -*-

# workaround for https://bugs.mysql.com/bug.php?id=89889
# at first load libcrypto.so and libssl.so from system library path.
import ssl  # noqa: F401
import mysql.connector
import re
import logging

re_numeric_part = re.compile(r'^(\d+)')
logger = logging.getLogger(__name__)


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
            # skip mysql.infoschema, mysql.session@localhost, mysql.sys
            if uh['user'].startswith('mysql.') and uh['host'] == 'localhost':
                continue
            logger.debug('each_user: %s@%s', uh['user'], uh['host'])
            yield uh

    def show_grants(self,
                    user: str = None,
                    host: str = None,
                    ):
        cursor = self.cursor()
        cursor.execute('SHOW GRANTS FOR %s@%s', (user, host))
        for sg in cursor.fetchall():
            logger.debug('show_grants: %s', sg[0])
            yield sg[0]

    def show_create_user(self,
                         user: str = None,
                         host: str = None,
                         ):
        if self.server_version < (5, 7, 6):
            return ''
        cursor = self.cursor()
        cursor.execute('SHOW CREATE USER %s@%s', (user, host))
        scu = cursor.fetchone()[0]
        logger.debug('show_create_user: %s', scu)
        return scu
