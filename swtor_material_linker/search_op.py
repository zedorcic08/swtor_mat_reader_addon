# -*- coding: utf-8 -*-

import os
import fnmatch
import json
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

    # Initialize path values to None as default
    diffuse_path = None
    normal_path = None
    specular_path = None
    uses_reflective = None
    uses_emissive = None

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


    if diffuse_path is not None:
        diffuse_list = diffuse_path.split('\\')
        diffuse = diffuse_list[len(diffuse_list) - 1]
    else:
        diffuse = None
        print("No diffuse data found in the shader file.")

    if normal_path is not None:
        normal_list = normal_path.split('\\')
        normal = normal_list[len(normal_list) - 1]
    else:
        normal = None
        print("No normal data found in the shader file.")

    if specular_path is not None:
        specular_list = specular_path.split('\\')
        specular = specular_list[len(specular_list)-1]
    else:
        specular = None
        print("No specular data found in the shader file.")

    return [diffuse, normal, specular, uses_emissive, uses_reflective]

# Open the assets.json file created by the Character Creator
# Returns files associated with a specific model and the accompanying parameters

def get_xml_info(file_name, model_name, shader_type):

    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)

        for data_line in json_data :
            print(json.dumps(data_line, ident=2))




