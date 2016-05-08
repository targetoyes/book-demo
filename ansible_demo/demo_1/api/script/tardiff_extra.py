#!/usr/bin/python
# -*- coding: utf-8 -*-

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import sys
import tarfile
import time
from difflib import Differ

def tardiff(a, b, xa=0, xb=0):
    text = ''

    ta = tarfile.open(a)
    tb = tarfile.open(b)

    na = [(i.name, i.type, i.size) for i in ta]
    nb = [(i.name, i.type, i.size) for i in tb]

    for i in nb:
        if i[1] == '5':
            continue
        if i[0] in [j[0] for j in na]:
            for x in na:
                if i[0] == x[0] and i[2] != x[2]:
                    text += i[0] + ' is modified\n'
        else:
            text += i[0] + ' is increased\n'
    print text
    return text

if __name__ == '__main__':
    tardiff('/data/tar_home/use-for-test/test_service/test_234567_2015_10_27_16_56_0.tar.gz', '/temp/test.tar.gz')

