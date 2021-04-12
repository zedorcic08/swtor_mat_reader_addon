# -*- coding: utf-8 -*-

import os
import fnmatch
import xml.etree.ElementTree as xml_tree


def find_file(working_dir,filename,filetype):

# Function to find files across a given directory.
# Takes: directory path, file name, file type
# File type is either 'shader' or 'texture'

    for root, dir_list, file_list in os.walk(working_dir, topdown=False):
        if filetype == 'shader':
            for entry in file_list:
                if fnmatch.fnmatch(entry, shader_name + '.mat'):
                    components = get_shader_info(root+entry)


def get_shader_info(filename):

    data_tree = xml_tree.parse(filename)


