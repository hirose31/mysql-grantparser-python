# -*- coding: utf-8 -*-

import re
import logging

logger = logging.getLogger(__name__)


def parse(stmt: str = None,
          create_user: str = None,
          ) -> list:
    parsed = {
        'with': '',
        'required': '',
        'identified': '',
        'privs': [],
        'object': '',
        'user': '',
        'host': '',
    }

    # grant
    matched = re.search(r'\s+WITH\s+(.+?)$', stmt)
    if matched:
        parsed['with'] = matched.group(1).strip()

    # require
    matched = re.search(r'\s+REQUIRE\s+(.+?)(?:\s+WITH\s+.+)?$', stmt)
    required = ''
    if matched:
        required = matched.group(1)
    if create_user:
        matched = re.search(r"\s+REQUIRE\s+(.+?)\s+(?:WITH|PASSWORD)\s+", create_user)
        if matched:
            required = matched.group(1)

        matched = re.search(r"\s+REQUIRE\s+.+\s+WITH\s+(.+)\s+PASSWORD", create_user)
        if matched:
            resource_option = matched.group(1)
            parsed['with'] = (parsed['with'] + ' ' + resource_option).strip()

    if required != 'NONE':
        parsed['required'] = required.strip()

    # identified
    matched = re.search(r'\s+IDENTIFIED BY\s+(.+?)(?:\s+REQUIRE\s+.+)?$', stmt)
    identified = ''
    if matched:
        identified = matched.group(1)
    if create_user:
        matched = re.search(r"\s+IDENTIFIED\s+WITH\s+'[^']+'\s+AS\s+('[^']+')", create_user)
        if matched:
            identified = matched.group(1)
            if identified:
                identified = 'PASSWORD %s' % identified
    if identified:
        parsed['identified'] = identified.strip()

    # main
    matched = re.search(r"^GRANT\s+(.+?)\s+ON\s+(.+?)\s+TO\s+['`](.*)['`]@['`](.+?)['`]", stmt)
    if matched:
        parsed['privs'] = parse_privs(matched.group(1).strip())
        parsed['object'] = matched.group(2).replace('`', '').strip()
        parsed['user'] = matched.group(3).strip()
        parsed['host'] = matched.group(4).strip()

    logger.debug('parsed: %s', parsed)
    return parsed


def parse_privs(privs: str = None):
    privs += ','
    priv_list = []

    priv_list = [priv.strip() for priv in re.findall(r'([^,(]+(?:\([^)]+\))?)\s*,\s*', privs)]

    return priv_list
