
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import time

OSM_FILE = "chicago.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Circle", "South Avenue", "North", "South","East","West","Lane","Route"]

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


def audit_street_type(street_types, street_name):
    # this function audit street name type
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    # this function if an attribute includes a street
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    #this function return all street name types
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    # this function update street name and make street name to be consistent
    name = name.replace(",", "")
    for word in name.split(" "):
        if word in mapping.keys():
            name = name.replace(word, mapping[word])

    return name


def output(osmfile):
    #This function print updated street name
    st_types = audit(osmfile)
    #assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
    print "Pass"
