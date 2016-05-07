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

    def get_all_files(self, path=None):
        if path is None:
            path = self._search_path
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                file_full_path = os.path.join(dirpath, filename)
                sha1value = self.calc_sha1(file_full_path)
                if sha1value not in self.file_dict:
                    self.file_dict[sha1value] = []
                self.file_dict[sha1value].append(file_full_path)

                # for dirname in dirnames:
                #     self.get_all_files(dirpath + '/' + dirname)

    def calc_sha1(self, filepath):
        lenth = 1024 * 1024
        with open(filepath, 'rb') as f:
            sha1obj = hashlib.sha1()
            # file_size=os.path.getsize(filepath)
            # if file_size<lenth:
            #     file_size
            sha1obj.update(f.read(lenth))
            hash = sha1obj.hexdigest()
            return hash

    def get_repeate_file(self, key_word=None):
        self.get_all_files()
        has_key_word = isinstance(key_word, (list, tuple))
        filetoreserve = 0
        noask = False
        for sha1, filenames in self.file_dict.items():
            if len(filenames) > 1:

                if has_key_word:
                    filetoreserve = self.get_reserve_index(filenames, key_word)

                if noask:
                    for index, file in enumerate(filenames):
                        if index != filetoreserve:
                            os.remove(file)
                else:
                    for index, file in enumerate(filenames):
                        if index == filetoreserve:
                            print 'reserve [{0}] {1}'.format(index, file)
                        else:
                            print 'delete [{0}] {1}'.format(index, file)
                    r = raw_input('is it right ? Yes:Y no:n just_do_it_no_ask_again:doit :')
                    r = r.lower()
                    if r == 'y' or r == 'yes' or r == '':
                        self.remove_files(filenames, filetoreserve)
                    elif isinstance(r, int) and len(filenames) > int(r):
                        filetoreserve = int(r)
                        self.remove_files(filenames, filetoreserve)
                    elif r == 'doit':
                        noask = True
                        self.remove_files(filenames, filetoreserve)
                    else:
                        print 'do nothing'

    def remove_files(self, filenames, reserve_index):
        for index, file in enumerate(filenames):
            if index != reserve_index:
                print 'remove file {0}'.format(file)
                os.remove(file)

    def get_reserve_index(self, filenames, key_word):
        filetodel = []
        for index, file in enumerate(filenames):
            for w in key_word:
                if w in file:
                    filetodel.append(index)
        len_file_list = len(filenames)
        if len_file_list <= len(filetodel):
            return 0
        for i in xrange(len_file_list):
            if (i not in filetodel):
                return i
