#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, hashlib


class RepeatedFile:
    file_dict = dict()
    _search_path = None

    fileList = []

    def __init__(self, search_path=None):
        if search_path is None:
            self._search_path = os.getcwd()
        elif os.path.isabs(search_path):
            self._search_path = search_path
        else:
            self._search_path = os.path.abspath(search_path)

    def get_files(self, path=None):
        if path is None:
            path = self._search_path
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                file_full_path = dirpath + '/' + filename
                self.file_dict[self.calc_sha1(file_full_path)]= file_full_path

            for dirname in dirnames:
                self.get_files(dirpath + '/' + dirname)
            break

    def calc_sha1(self, filepath):
        with open(filepath, 'rb') as f:
            sha1obj = hashlib.sha1()
            sha1obj.update(f.read())
            hash = sha1obj.hexdigest()
            return hash
