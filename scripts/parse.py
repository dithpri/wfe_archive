#!/usr/bin/env python3

import lxml.etree as ET
import gzip
from pathlib import Path
import io
import sys


def fast_iter(context, func, *args, **kwargs):
    """
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    for event, elem in context:
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath("ancestor-or-self::*"):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context

def process_element(elem):
    region = {
        # region name
        "name": elem.find("NAME").text.lower().replace(" ", "_"),
        # wfe
        # encode to a bytes object, as we read the factbook files in
        # binary mode, because the daily dumps contain "\r\n" pairs.
        # Reading/writing them as text would transform "\r\n"s into the
        # platform specific newline, which can cause the
        # `latest_wfe.read() == region["factbook"]`
        # comparison to always fail...
        # Trust me, I ran out of disk space due to this.
        "factbook": (elem.find("FACTBOOK").text or "").encode("utf-8"),
    }

    # Testing only
    # if region["name"] != "the_north_pacific":
    #     return

    region_file = "./archive/{}.txt".format(region['name'])

    with io.open(region_file, "wb") as f:
        f.write(region["factbook"])


if __name__ == "__main__":
    with gzip.open(sys.argv[1], "rb") as f:
        context = ET.iterparse(f, tag="REGION")
        fast_iter(context, process_element)
#  vim: set ts=4 sw=4 et :
