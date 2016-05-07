#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RepeatedFile

if __name__ == "__main__":
    rf = RepeatedFile.RepeatedFile('/home/lbp/work')
    rf.get_files()
    print rf.file_dict