# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import time
from audit import *


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    #node = defaultdict(set)
    node = {}
    if element.tag == "node" or element.tag == "way" :
        #create the dictionary based on exaclty the value in element attribute.
        node = {'created':{}, 'type':element.tag}
        for k in element.attrib:
            try:
                v = element.attrib[k]
            except KeyError:
                continue
            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
        try:
            node['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
        except KeyError:
            pass

        if 'address' not in node.keys():
            node['address'] = {}
        #Iterate the content of the tag
        for stag in element.iter('tag'):
            #Init the dictionry

            k = stag.attrib['k']
            v = stag.attrib['v']
            #Checking if indeed prefix with 'addr' and no ':' afterwards
            if k.startswith('addr:'):
                if len(k.split(':')) == 2:
                    content = addresschars.search(k)
                    if content:
                        node['address'][content.group(1)] = v
            else:
                node[k]=v
        if not node['address']:
            node.pop('address',None)
        #Special case when the tag == way,  scrap all the nd key
        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])

# This section of code iterates over the second level 'k' and 'v' tags, checks for problem
# characters, and assembles the node dict with specific boolean criteria. Note that to assemble
# the address dict properly it has to be initialized above this code block, otherwise you
# reset it with every tag iteration.
        for tag in element.iter('tag'):

            tagk = tag.attrib['k']
            tagv = tag.attrib['v']
            m = problemchars.search(tagk)
            if not m:
                if tagk == "addr:street":
				    address['street'] = update_name(tagv,mapping)

                elif tagk == 'addr:housenumber':
                    address['housenumber'] = tagv
                    node['address'] = address

                elif 'addr' not in tagk:
                    node[tagk] = tagv
                else:
                    pass

        return node
# if element.tag != to 'node' or 'way', bypass the other loops, and return none.
    else:
        return None

def process_map(file_in, pretty = False):
    """
    Process the osm file to json file to be prepared for input file to monggo
    """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
            root.clear()
# return data
# OSM_data = process_map(OSM_FILE)
