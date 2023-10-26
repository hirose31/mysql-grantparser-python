# -*- coding: utf-8 -*-


from mysql_grantparser.parser import parse
from mysql_grantparser.exporter import Exporter
from utils import dump_json

# MySQL 5.7 style
tests = [
    [
        [
            r"CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
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
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': '',
                },
            },
        },
        'root',
    ],

    [
        [
            r"CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
            r"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE, CREATE ROLE, DROP ROLE ON *.* TO `root`@`%` WITH GRANT OPTION",
            r"GRANT APPLICATION_PASSWORD_ADMIN,AUDIT_ABORT_EXEMPT,AUDIT_ADMIN,AUTHENTICATION_POLICY_ADMIN,BACKUP_ADMIN,BINLOG_ADMIN,BINLOG_ENCRYPTION_ADMIN,CLONE_ADMIN,CONNECTION_ADMIN,ENCRYPTION_KEY_ADMIN,FIREWALL_EXEMPT,FLUSH_OPTIMIZER_COSTS,FLUSH_STATUS,FLUSH_TABLES,FLUSH_USER_RESOURCES,GROUP_REPLICATION_ADMIN,GROUP_REPLICATION_STREAM,INNODB_REDO_LOG_ARCHIVE,INNODB_REDO_LOG_ENABLE,PASSWORDLESS_USER_ADMIN,PERSIST_RO_VARIABLES_ADMIN,REPLICATION_APPLIER,REPLICATION_SLAVE_ADMIN,RESOURCE_GROUP_ADMIN,RESOURCE_GROUP_USER,ROLE_ADMIN,SENSITIVE_VARIABLES_OBSERVER,SERVICE_CONNECTION_ADMIN,SESSION_VARIABLES_ADMIN,SET_USER_ID,SHOW_ROUTINE,SYSTEM_USER,SYSTEM_VARIABLES_ADMIN,TABLE_ENCRYPTION_ADMIN,TELEMETRY_LOG_ADMIN,XA_RECOVER_ADMIN ON *.* TO `root`@`%` WITH GRANT OPTION",
            r"GRANT PROXY ON ``@`` TO `root`@`%` WITH GRANT OPTION",
        ],
        {
            'root@%': {
                'user': 'root',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': [
                            'SELECT',
                            'INSERT',
                            'UPDATE',
                            'DELETE',
                            'CREATE',
                            'DROP',
                            'RELOAD',
                            'SHUTDOWN',
                            'PROCESS',
                            'FILE',
                            'REFERENCES',
                            'INDEX',
                            'ALTER',
                            'SHOW DATABASES',
                            'SUPER',
                            'CREATE TEMPORARY TABLES',
                            'LOCK TABLES',
                            'EXECUTE',
                            'REPLICATION SLAVE',
                            'REPLICATION CLIENT',
                            'CREATE VIEW',
                            'SHOW VIEW',
                            'CREATE ROUTINE',
                            'ALTER ROUTINE',
                            'CREATE USER',
                            'EVENT',
                            'TRIGGER',
                            'CREATE TABLESPACE',
                            'CREATE ROLE',
                            'DROP ROLE',
                            'APPLICATION_PASSWORD_ADMIN',
                            'AUDIT_ABORT_EXEMPT',
                            'AUDIT_ADMIN',
                            'AUTHENTICATION_POLICY_ADMIN',
                            'BACKUP_ADMIN',
                            'BINLOG_ADMIN',
                            'BINLOG_ENCRYPTION_ADMIN',
                            'CLONE_ADMIN',
                            'CONNECTION_ADMIN',
                            'ENCRYPTION_KEY_ADMIN',
                            'FIREWALL_EXEMPT',
                            'FLUSH_OPTIMIZER_COSTS',
                            'FLUSH_STATUS',
                            'FLUSH_TABLES',
                            'FLUSH_USER_RESOURCES',
                            'GROUP_REPLICATION_ADMIN',
                            'GROUP_REPLICATION_STREAM',
                            'INNODB_REDO_LOG_ARCHIVE',
                            'INNODB_REDO_LOG_ENABLE',
                            'PASSWORDLESS_USER_ADMIN',
                            'PERSIST_RO_VARIABLES_ADMIN',
                            'REPLICATION_APPLIER',
                            'REPLICATION_SLAVE_ADMIN',
                            'RESOURCE_GROUP_ADMIN',
                            'RESOURCE_GROUP_USER',
                            'ROLE_ADMIN',
                            'SENSITIVE_VARIABLES_OBSERVER',
                            'SERVICE_CONNECTION_ADMIN',
                            'SESSION_VARIABLES_ADMIN',
                            'SET_USER_ID',
                            'SHOW_ROUTINE',
                            'SYSTEM_USER',
                            'SYSTEM_VARIABLES_ADMIN',
                            'TABLE_ENCRYPTION_ADMIN',
                            'TELEMETRY_LOG_ADMIN',
                            'XA_RECOVER_ADMIN',
                        ],
                        'with': 'GRANT OPTION',
                    },
                    '``@``': {
                        'privs': [
                            'PROXY'
                        ],
                        'with': 'GRANT OPTION'
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': '',
                },
            },
        },
        'root',
    ],

    [
        [
            r"CREATE USER 'scott'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
            r"GRANT USAGE ON *.* TO 'scott'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott'@'%' WITH GRANT OPTION",
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
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': '',
                },
            },
        },
        'several privs',
    ],
    [
        [
            r"CREATE USER 'scott2'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE SSL WITH MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 2 MAX_CONNECTIONS_PER_HOUR 3 MAX_USER_CONNECTIONS 4 PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
            r"GRANT USAGE ON *.* TO 'scott2'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott2'@'%' WITH GRANT OPTION",
        ],
        {
            'scott2@%': {
                'user': 'scott2',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                        'with': 'MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 2 MAX_CONNECTIONS_PER_HOUR 3 MAX_USER_CONNECTIONS 4',
                    },
                    'orcl.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': 'GRANT OPTION MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 2 MAX_CONNECTIONS_PER_HOUR 3 MAX_USER_CONNECTIONS 4',
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': 'SSL',
                },
            },
        },
        'long with, require SSL',
    ],
    [
        [
            r"CREATE USER 'scott3'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL demo client certificate/CN=client/emailAddress=client@example.com' ISSUER '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL/CN=CA/emailAddress=ca@example.com' PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
            r"GRANT USAGE ON *.* TO 'scott3'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `orcl`.* TO 'scott3'@'%' WITH GRANT OPTION",
        ],
        {
            'scott3@%': {
                'user': 'scott3',
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
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': r"SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL demo client certificate/CN=client/emailAddress=client@example.com' ISSUER '/C=SE/ST=Stockholm/L=Stockholm/O=MySQL/CN=CA/emailAddress=ca@example.com'",
                },
            },
        },
        'require issuer and subject',
    ],
    [
        [
            r"CREATE USER 'scott4'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*0380BEA27363E56C37F0BFDA438F429080848051' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK",
            r"GRANT USAGE ON *.* TO 'scott4'@'%'",
            r"GRANT SELECT, INSERT, UPDATE, DELETE ON `t`.* TO 'scott4'@'%'",
            r"GRANT SELECT (c1), INSERT (c2, c1), DELETE ON `t`.`t1` TO 'scott4'@'%'",
        ],
        {
            'scott4@%': {
                'user': 'scott4',
                'host': '%',
                'objects': {
                    '*.*': {
                        'privs': ['USAGE'],
                        'with': '',
                    },
                    't.*': {
                        'privs': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
                        'with': '',
                    },
                    't.t1': {
                        'privs': ['SELECT (c1)', 'INSERT (c2, c1)', 'DELETE'],
                        'with': '',
                    },
                },
                'options': {
                    'identified': r"PASSWORD '*0380BEA27363E56C37F0BFDA438F429080848051'",
                    'required': '',
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
