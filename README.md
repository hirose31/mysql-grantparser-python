# NAME

mysql_grantparser - parse MySQL SHOW GRANTS

# SYNOPSIS

``` python
import mysql_grantparser

grants = mysql_grantparser.Exporter(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='pa55w0rd',
).export()

```

# DESCRIPTION

mysql_grantparser is SHOW GRANTS parser for MySQL, inspired by Ruby's [Gratan](https://github.com/codenize-tools/gratan).

This module returns privileges for all users as following dict.

``` python
{
    'USER@HOST': {
        'user': USER,
        'host': HOST,
        'objects': {
            'DB_NAME.TABLE_NAME': {
                'privs': [ PRIV_TYPE, PRIV_TYPE, ... ],
                'with': 'GRANT OPTION',
            },
            ...
        },
        'options': {
            'identified': '...',
            'required': '...',
        },
    },
    ...
}
```

For example, this GRANT statement

``` sql
GRANT SELECT, INSERT, UPDATE, DELETE ON orcl.* TO 'scott'@'%' IDENTIFIED BY 'tiger' WITH GRANT OPTION;
```

is represented as following.

``` python
{
    'scott@%': {
        'user': 'scott',
        'host': '%',
        'objects': {
            '*.*': {
                privs: [
                    'USAGE'
                ],
            },
            'orcl.*': {
                'privs': [
                    'SELECT',
                    'INSERT',
                    'UPDATE',
                    'DELETE',
                ],
                'with': 'GRANT OPTION',
            }
        },
        'options': {
            'identified': "PASSWORD XXX",
            'required': '',
        },
    },
}
```

# SEE ALSO

- Documentation: https://github.com/hirose31/mysql-grantparser-python/blob/master/README.md
- Changelog: https://github.com/hirose31/mysql-grantparser-python/blob/master/CHANGELOG.md
- Repository: https://github.com/hirose31/mysql-grantparser-python
- Test status: fixme
