#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2016, Rohan Garg <rohan@garg.io>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares
import os
from time import gmtime, strftime, sleep
import MySQLdb

NEXTCLOUD_DB = 'nextcloud'
OCC_PATH = '/var/www/nextcloud/occ'

def create_nextcloud_db(username, password):
    con = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="")
    with con:
        cur = con.cursor()
        cur.execute('create database %s', (NEXTCLOUD_DB))
        cur.execute("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s'",
                    (username, password))
        cur.execute("grant all on %s.* to '%s'@'localhost'",
                    (NEXTCLOUD_DB, username))

def setup_nextcloud(username, password, hostname):
    cmds = [
           ['sudo', '-u', 'www-data', OCC_PATH, 'maintenance:install',
           '--database-name', NEXTCLOUD_DB, '--database-user', username,
           '--admin-user', username, '--admin-pass', password,
           '--database', 'mysqldb', "--database-pass='%s'" % password],
           ['sudo', '-u', 'www-data', OCC_PATH, 'config:system:set',
            'trusted_domains', '0', "--value=%s.local" % hostname],
           ['sudo', '-u', 'www-data', OCC_PATH, 'config:system:set',
            'trusted_domains', '1', "--value=%s" % hostname]
           ]

    for cmd in cmds:
        libcalamares.utils.target_env_call(cmd)

def run():
    libcalamares.utils.target_env_call
    password = str(libcalamares.utils.obscure(libcalamares.globalstorage.value('password')))
    username = str(libcalamares.globalstorage.value('username'))
    hostname = str(libcalamares.globalstorage.value('hostname'))
    create_nextcloud_db(username, password)
    setup_nextcloud(username, password, hostname)
    return None
