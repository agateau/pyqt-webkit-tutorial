# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import os
import re

def _to_utf8(line):
    return unicode(line, "utf-8")

def _split_file(fl):
    def add_entry(key, content):
        # Remove trailing empty lines
        while len(content) > 0 and content[-1].strip() == u"":
            del content[-1]
        dct[key] = u"".join(content)

    dct = {}
    content = []
    key = None
    rx = re.compile("^\s*/// ([-a-zA-Z0-9/]+)$")
    for line in fl.readlines():
        line = _to_utf8(line)
        result = rx.match(line)
        if result is None:
            content.append(line)
        else:
            if key is not None:
                add_entry(key, content)
            content = []
            key = result.group(1)
            continue
    add_entry(key, content)
    return dct

class TextFileCache(object):
    def __init__(self, txt_dir):
        self._cache = {}
        self._dir = txt_dir

    def __contains__(self, name):
        return self.has_key(name)

    def __getitem__(self, name):
        if not name in self._cache:
            self._read_file(name)

        return self._cache[name]

    def has_key(self, name):
        if name in self._cache:
            return True

        file_name, absolute_name, is_splitted = self._parse_name(name)
        if not os.path.exists(absolute_name):
            return False

        if is_splitted:
            # File is splitted, we need to read it to know whether the requested
            # fragment exists
            self._read_file(name)
            return name in self._cache
        else:
            return True

    def _read_file(self, name):
        file_name, absolute_name, is_splitted = self._parse_name(name)
        fl = open(absolute_name)
        if is_splitted:
            dct = _split_file(fl)
            for key, value in dct.items():
                self._cache[file_name + "#" + key] = value
        else:
            self._cache[name] = _to_utf8(fl.read())

    def _parse_name(self, name):
        """
        Return a tuple of the form (name, absolute_name, is_splitted)
        """
        lst = name.split("#")
        if len(lst) == 2:
            name = lst[0]
            is_splitted = True
        else:
            is_splitted = False
        absolute_name = os.path.join(self._dir, name)
        return name, absolute_name, is_splitted
# vi: ts=4 sw=4 et
