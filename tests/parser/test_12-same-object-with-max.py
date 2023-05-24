# -*- coding: utf-8 -*-

from mysql_grantparser.parser import parse
from mysql_grantparser.exporter import Exporter
from utils import dump_json

tests = [
    [
        [
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'scott'@'%'",
            r"CREATE USER 'scott'@'%' IDENTIFIED WITH 'mysql_native_password'  REQUIRE NONE WITH MAX_USER_CONNECTIONS 5 PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': 'MAX_USER_CONNECTIONS 5',
                    },
                },
                'options': {
                    'identified': '',
                    'required': '',
                },
            },
        },
        'several privs no password',
    ],
]


class TestParserBasic:
    def test_parser_basic(self):
        for test in tests:
            stmts = test[0]
            expect = test[1]
            label = test[2]

            create_user = ''
            for i, stmt in enumerate(stmts):
                if stmt.startswith('CREATE USER '):
                    create_user = stmts.pop(i)

            grants = []
            for stmt in stmts:
                grants.append(parse(stmt, create_user))
            packed = Exporter.pack(grants)
            # dump_json('PACKED: ', packed)
            # dump_json('EXPECTED: ', expect)
            assert packed == expect, label
