# -*- coding: utf-8 -*-

import os
import fnmatch
import xml.etree.ElementTree as xml_tree


# Function to find files across a given directory.
# Input: directory path, file name, file type
# Output: list of material components (reading from shader) or file path to texture
# File type is either 'shader' or 'texture'


def find_file(working_dir, file_name, filetype):

    if os.path.exists(working_dir):
        print("File directory found. Starting file search...")

        for root, dir_list, file_list in os.walk(working_dir, topdown=False):

            if filetype == "shader":
                for entry in file_list:
                    if fnmatch.fnmatch(entry, file_name + ".mat"):
                        print("Shader found. Starting shader read...")
                        components = get_shader_info(root + "\\" + entry)
                        print("Components found.")
                        return components

            if filetype == "texture":
                for entry in file_list:
                    if fnmatch.fnmatch(entry, file_name + ".dds"):
                        print("Texture " + entry + " found.")
                        return root + '\\' + entry
    else:
        print('Directory does not exist.')
        return None


# Open the MAT file and read the contents to grab the Diffuse, Normal and Specular files.
# Return a list with the file names and whether Emissive and Reflective are used in the shader


def get_shader_info(filename):

    data_tree = xml_tree.parse(filename)
    data_root = data_tree.getroot()

    for data_node in data_root:
        if data_node.tag == 'input':
            if data_node[0].text == 'DiffuseMap':
                diffuse_path = data_node[2].text
            elif data_node[0].text == 'RotationMap1':
                normal_path = data_node[2].text
            elif data_node[0].text == 'GlossMap':
                specular_path = data_node[2].text
            elif data_node[0].text == 'UsesReflection':
                uses_reflective = eval(data_node[2].text)
            elif data_node[0].text == 'UsesEmissive':
                uses_emissive = eval(data_node[2].text)

    diffuse_list = diffuse_path.split('\\')
    normal_list = normal_path.split('\\')
    specular_list = specular_path.split('\\')

    diffuse = diffuse_list[len(diffuse_list)-1]
    normal = normal_list[len(normal_list)-1]
    specular = specular_list[len(specular_list)-1]

    return [diffuse, normal, specular, uses_emissive, uses_reflective]


