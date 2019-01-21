# -*- coding: utf-8 -*-

from mysql_grantparser.parser import parse
from mysql_grantparser.exporter import Exporter
from utils import dump_json

tests = [
    [
        [
            r"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION",
        ],
        {
            'root@%': {
                'user': 'root',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['ALL PRIVILEGES'],
                        'with': 'GRANT OPTION',
                    },
                },
                'options': {
                },
            },
        },
        'root',
    ],

    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'%' IDENTIFIED BY PASSWORD '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott'@'%' WITH GRANT OPTION",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                    },
                    'orcl.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': 'GRANT OPTION',
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40'",
                },
            },
        },
        'several privs',
    ],
    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'localhost' IDENTIFIED BY PASSWORD '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40' REQUIRE SSL WITH GRANT OPTION MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 2 MAX_CONNECTIONS_PER_HOUR 3 MAX_USER_CONNECTIONS 4",
        ],
        {
            'scott@localhost': {
                'user': 'scott',
                'host': 'localhost',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                        'with': 'GRANT OPTION MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 2 MAX_CONNECTIONS_PER_HOUR 3 MAX_USER_CONNECTIONS 4',
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*F2F68D0BB27A773C1D944270E5FAFED515A3FA40'",
                    'required': 'SSL',
                },
            },
        },
        'long with, require SSL',
    ],
    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'%' REQUIRE ISSUER '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL/CN=CA/emailAddress=ca@example.com'' SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL demo client certificate/CN=client/emailAddress=client@example.com'",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                    },
                },
                'options': {
                    'required': r"ISSUER '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL/CN=CA/emailAddress=ca@example.com'' SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL demo client certificate/CN=client/emailAddress=client@example.com'",
                },
            },
        },
        'require issuer and subject',
    ],
    [
        [
            r"GRANT USAGE ON *.* TO 'scott'@'%' IDENTIFIED BY PASSWORD '*5BCB3E6AC345B435C7C2E6B7949A04CE6F6563D3'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `t`.* TO 'scott'@'%'",
            r"GRANT SELECT (c1), INSERT (c2, c1), DELETE ON `t`.`t1` TO 'scott'@'%'",
        ],
        {
            'scott@%': {
                'user': 'scott',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                    },
                    't.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                    },
                    't.t1': {
                        'privs': ['SELECT (c1)', 'INSERT (c2, c1)', 'DELETE'],
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*5BCB3E6AC345B435C7C2E6B7949A04CE6F6563D3'",
                },
            },
        },
        'column privileges',
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
