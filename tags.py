# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re

# Before you process the data and add it into MongoDB, you should
# check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
# as well as see if there are any other potential problems.

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#determine if a tag matches one of the regular expression conditions above
# and add a count to the dict for that condition

def key_type(element, keys):
    if element.tag == "tag":

        for tag in element.iter('tag'):
            tagk = tag.attrib['k']
            if lower.match(tagk):
                keys['lower'] += 1
            elif problemchars.match(tagk):
                keys['problemchars'] += 1
            elif lower_colon.match(tagk):
                keys['lower_colon'] += 1
            #if none of the searches as true add a count to 'other'
            else:
                keys['other'] += 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
