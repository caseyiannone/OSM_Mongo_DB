#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'(^([a-z]|_)*):(([a-z]|_)*)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

mapping = {"St": "Street", "St.": "Street", "street": "Street","st": "Street",
           "Dr": "Drive", "Dr.": "Drive","Ct":"Court",
          "Blvd":"Boulevard","blvd":"Boulevard","Blvd.":"Boulevard",
           "Ct.":"Court","HWY":"Highway",
           "Ln":"Lane","Ter":"Terrace","Ave.":"Avenue","Ave":"Avenue",
           "road":"Road","rd":"Road","Rd.":"Road","Rd": "Road","place":"Place","US":"U.S.",
           "Pl":"Place","Rte":"Route","IL":"Illinois","W":"West","Trl":"Trail",
           "avenue":"Avenue","Pkwy":"Parkway","Cir":"Circle",
            "N":"North","N.":"North","E":"East","S":"South","S":"South","S.":"South",
           "W.":"West","E.":"East","W":"West"
          }
postcode_re = re.compile(r'\b\d{5}\b$', re.IGNORECASE)

def correctPostcode(value):
    match = re.search(r'\d{5}', value)
    if not match:
        return None
    else:
        new_postcode = match.group()
        return new_postcode

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag
        if element.tag == "node":
          node["pos"] = [float(element.attrib['lat']), float(element.attrib['lon'])]
          for attr in element.attrib:
            if attr in CREATED:
              if "created" not in node:
                node["created"] = {}
              node["created"][attr] = element.attrib[attr]
            elif attr not in ['lat','lon']:
              node[attr] = element.attrib[attr]

        elif element.tag == "way":
          node["node_refs"] = []
          for nd in element.iter("nd"):
            node["node_refs"].append(nd.attrib['ref'])

        for tag in element.iter("tag"):
            if ("k" not in tag.attrib):
              continue

            k = tag.attrib["k"]

            if (problemchars.search(k)):
                continue

            m = lower_colon.match(k)
            if (m and m.group(1) == "addr"):
                if 'address' not in node:
                    node['address'] = {};

                if ('street' == m.group(3)):
                    node['address']['street'] = update_name(tag.attrib['v'], mapping)
                elif ('postcode' == m.group(3) and tag.attrib['v'] != None):
                    node['address']['postcode'] = correctPostcode(tag.attrib['v'])
                else:
                    node['address'][m.group(3)] = tag.attrib['v']
            else:
                node[k] = tag.attrib['v']

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
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
    return data
