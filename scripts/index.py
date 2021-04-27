#!/usr/bin/env python3

import os
import math
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def arch_linkgen(x):
    y = x.strip()
    return "[{}]({})  \n".format(remove_ext(y), "../archive/{}".format(y))


def idx_linkgen(x):
    y = x.strip()
    return "[{}]({})\n\n".format(remove_prefix(remove_ext(y)), y)


def remove_ext(fname):
    return fname.rsplit(".", maxsplit=1)[0]


def remove_prefix(fname):
    return fname.split("/")[-1]


def canonicalize(str):
    return str.lower().replace(" ", "_").strip()


def get_common_root(a, b):
    return os.path.commonprefix([canonicalize(a), canonicalize(b)])


def get_uniq_idx(previous, cur):
    a, b = canonicalize(remove_ext(previous)), canonicalize(remove_ext(cur))
    if previous is None or len(a) == 0:
        a = b
    le = len(os.path.commonprefix([a, b]))
    return b[: le + 1]


def main():
    files = sorted(filter(None, os.listdir("./archive/")))
    max_files = 1000 - 1
    lines_per_file = max(2048, math.ceil(len(files) / max_files))
    chunks = [chunk for chunk in grouper(files, lines_per_file, fillvalue="")]
    fnames = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        if i - 1 >= 0:
            prev_end = chunks[i - 1][-1]
        else:
            prev_end = ""
        if i + 1 < len(chunks):
            next_start = chunks[i + 1][0]
        else:
            next_start = ""
        start_idx = get_uniq_idx(prev_end, chunk[0])
        end_idx = get_uniq_idx(next_start, chunk[-1])
        dest_fname = "index/{}..{}.md".format(start_idx, end_idx)
        if os.path.isfile(dest_fname):
            # Just in case. This shouldn't happen.
            continuation = 2
            while os.path.isfile(dest_fname + " - " + str(continuation)):
                continuation += 1
            dest_fname += " - " + str(continuation)
        with open(dest_fname, "w") as idx_file:
            idx_file.writelines(map(arch_linkgen, chunk))
        fnames.append(dest_fname)
    with open("INDEX.md", "w") as readme:
        readme.writelines(map(idx_linkgen, fnames))


if __name__ == "__main__":
    main()
#  vim: set ts=4 sw=4 et :
