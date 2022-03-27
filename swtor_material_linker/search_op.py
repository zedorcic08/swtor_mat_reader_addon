# -*- coding: utf-8 -*-

import bpy
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


# Function to erase the Principled BSDF node and then copy over the material template for the Uber Shade in its place
def create_material_from_template(mat):
    # Fetch Principled BDSF node and delete it
    material_name = mat.material.name
    material_data = mat.material
    print("--------------------")
    print("Copying template for: " + material_name)

    if "Principled BSDF" in material_data.node_tree.nodes:
        print("Deleting default shader...")
        principled_node = mat.material.node_tree.nodes["Principled BSDF"]
        mat.material.node_tree.nodes.remove(principled_node)
    else:
        print("Principled Shader not present.")

    # Get Uber template and copy it to current material
    print("Copying template...")
    if "Template: Uber Shader" in bpy.data.materials:
        shader_template = bpy.data.materials["Template: Uber Shader"]
        mat.material = shader_template.copy()
        mat.material.name = material_name
        print("Template name: " + mat.material.name)
        print("Template set.")
        print("--------------------")
    else:
        print("Template not found.")


#Function to delete the Principled BSDF node present and spawn a new SWTOR Uber Shader node.
def create_material_node(mat):

    # Fetch Principled BDSF node and delete it
    material_name = mat.material.name
    material_data = mat.material
    print("--------------------")
    print("Copying template for: " + material_name)

    if "Principled BSDF" in material_data.node_tree.nodes:
        print("Deleting default shader...")
        principled_node = mat.material.node_tree.nodes["Principled BSDF"]
        mat.material.node_tree.nodes.remove(principled_node)
    else:
        print("Principled Shader not present.")

    print("Linking node...")

    uber_node = mat.material.node_tree.nodes.new('ShaderNodeHeroEngine')
    uber_node.derived = 'UBER'
    uber_node.location = [-200, 100]

    # Get output node already present
    output_node = mat.material.node_tree.nodes["Material Output"]

    # Link the two nodes
    mat.material.node_tree.links.new(output_node.inputs['Surface'],uber_node.outputs['Shader'])


def connect_diffuse(mat, diffuse_path, diffuse_name, operation_type):
    # Fetch Diffuse node and connect file
    if operation_type == 'legacy':
        if "_d DiffuseMap" in mat.material.node_tree.nodes:
            diffuse_node = mat.material.node_tree.nodes["_d DiffuseMap"]
            if diffuse_name + ".dds" not in bpy.data.images:
                diffuse_node.image = bpy.data.images.load(diffuse_path)
            else:
                diffuse_node.image = bpy.data.images[diffuse_name + ".dds"]
            diffuse_node.image.colorspace_settings.name = 'Raw'
        else:
            print ("No Diffuse Node found.")
    elif operation_type == 'node':
        if 'SWTOR' in mat.material.node_tree.nodes:
            material_node = mat.material.node_tree.nodes['SWTOR']
            if diffuse_name + ".dds" not in bpy.data.images:
                material_node.diffuseMap = bpy.data.images.load(diffuse_path)
            else:
                material_node.diffuseMap = bpy.data.images[diffuse_name + ".dds"]
        else:
            print("No node found.")
    else:
        print("Invalid Operation. ")


def connect_specular(mat, specular_path, specular_name, operation_type):
    # Fetch Specular Node and connect file
    if operation_type == 'legacy':
        if "_s GlossMap" in mat.material.node_tree.nodes:
            specular_node = mat.material.node_tree.nodes["_s GlossMap"]
            if specular_name + ".dds" not in bpy.data.images:
                specular_node.image = bpy.data.images.load(specular_path)
            else:
                specular_node.image = bpy.data.images[specular_name + ".dds"]
            specular_node.image.colorspace_settings.name = 'Raw'
        else:
            print("No Specular Node found.")
    elif operation_type == 'node':
        if 'SWTOR' in mat.material.node_tree.nodes:
            material_node = mat.material.node_tree.nodes['SWTOR']
            if specular_name + ".dds" not in bpy.data.images:
                material_node.glossMap = bpy.data.images.load(specular_path)
            else:
                material_node.glossMap = bpy.data.images[specular_name + ".dds"]
        else:
            print("No node found.")
    else:
        print("Invalid Operation. ")


def connect_normal(mat, normal_path, normal_name, operation_type):
    # Fetch Normal node and connect file
    if operation_type == 'legacy':
        if "_n RotationMap" in mat.material.node_tree.nodes:
            normal_node = mat.material.node_tree.nodes["_n RotationMap"]
            if normal_name + ".dds" not in bpy.data.images:
                normal_node.image = bpy.data.images.load(normal_path)
            else:
                normal_node.image = bpy.data.images[normal_name + ".dds"]
            normal_node.image.colorspace_settings.name = 'Raw'
        else:
            print("No Normal Node found.")
    elif operation_type == 'node':
        if 'SWTOR' in mat.material.node_tree.nodes:
            material_node = mat.material.node_tree.nodes['SWTOR']
            if normal_name + ".dds" not in bpy.data.images:
                material_node.rotationMap = bpy.data.images.load(normal_path)
            else:
                material_node.rotationMap = bpy.data.images[normal_name + ".dds"]
        else:
            print("No node found.")
    else:
        print("Invalid Operation. ")


def connect_textures(mat, work_dir, component_list, operation_type):
    if component_list[0] is not None:
        diffuse_path = find_file(work_dir, component_list[0], 'texture')
        if diffuse_path is not None:
            connect_diffuse(mat, diffuse_path, component_list[0], operation_type)
        else:
            print("No diffuse texture found.")
    else:
        print("No diffuse data.")

        # Get path of normal image and load into slot
    if component_list[1] is not None:
        normal_path = find_file(work_dir, component_list[1], 'texture')
        if normal_path is not None:
            connect_normal(mat, normal_path, component_list[1], operation_type)
        else:
            print("No normal texture found.")
    else:
        print("No normal data.")

        # Get path to specular image and load into slot
    if component_list[2] is not None:
        specular_path = find_file(work_dir, component_list[2], 'texture')
        if specular_path is not None:
            connect_specular(mat, specular_path, component_list[2], operation_type)
        else:
            print("No specular texture found.")
    else:
        print("No specular data.")




