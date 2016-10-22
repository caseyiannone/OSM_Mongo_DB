# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re


def get_user(element):
    return

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node':
            for node in element.iter('node'):
                userid = node.attrib['uid']
                users.add(userid)

    return users
