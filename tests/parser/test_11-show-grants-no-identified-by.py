# -*- coding: utf-8 -*-

from mysql_grantparser.parser import parse
from mysql_grantparser.exporter import Exporter
from utils import dump_json

tests = [
    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott'@'%' WITH GRANT OPTION",
            r"CREATE USER 'scott'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                        'with': '',
                    },
                    'orcl.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': 'GRANT OPTION',
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40'",
                    'required': '',
                },
            },
        },
        'several privs',
    ],
    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott'@'%' WITH GRANT OPTION",
            r"CREATE USER 'scott'@'%' IDENTIFIED WITH 'mysql_native_password'  REQUIRE NONE WITH MAX_USER_CONNECTIONS 5 PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                        'with': 'MAX_USER_CONNECTIONS 5',
                    },
                    'orcl.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': 'GRANT OPTION MAX_USER_CONNECTIONS 5',
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
