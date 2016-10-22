# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pprint



# process the map file and find out not only what tags are there, but also how many

def get_element(filename):

    context = ET.iterparse(filename, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()


def count_tags (filename):
    tags_dict = defaultdict(int)
    for i, elem in enumerate(get_element(filename)):
        tags_dict[elem.tag] += 1
    return tags_dict
