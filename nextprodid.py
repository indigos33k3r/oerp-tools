#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014  Sebastian Endres <basti.endres@fablab.fau.de>
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <http://www.gnu.org/licenses/>.

from oerphelper import *
import sys
from ConfigParser import ConfigParser
import locale
import codecs

# get reserved ids from config file
locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
cfg = ConfigParser({})
cfg.readfp(codecs.open('config.ini', 'r', 'utf8'))
res = cfg.get('nextprodid', 'reserved_ids').replace(' ', '').replace('[[', '').replace(']]', '')
reserved = []
if not res.replace('[', '').replace(']', '').replace(',', '') == '':
    res = res.split('],[')
    for i in res:
        reserved = reserved + range(int(i.split(',')[0]), int(i.split(',')[1]))

# get ids dictionary from oerp
# ('active','>=',False) so that also deactivated products are found
id_dict_list = oerp.read('product.product', oerp.search('product.product', [('active', '>=', False)]), ['default_code'])

# extract default_code from dict
ids = []
for id_dict in id_dict_list:
    if str.isdigit(str(id_dict['default_code'])) and not int(id_dict['default_code'] in reserved):
        ids.append(int(id_dict['default_code']))

# ids = sorted(ids)

# get next unused default_code
i = 0
foundIds = []
while len(foundIds) < 5:
    i += 1
    if i in reserved or i in ids:
        continue
    foundIds.append(i)

for i in foundIds:
    print("%04d" % i)
sys.exit(0)
