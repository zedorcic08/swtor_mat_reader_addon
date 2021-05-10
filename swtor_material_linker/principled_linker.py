# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import search_op


class ObjectLinkMaterials(bpy.types.Operator):
    bl_idname = "object.material_match"
    bl_label = "Item - Principled BDSF"
    bl_options = {'REGISTER', 'UNDO'}

    def connect_diffuse(self, mat, diffuse_path, diffuse_name):

        # Create texture node if Principled BSDF is found
        if "Principled BSDF" in mat.material.node_tree.nodes:
            diffuse_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
            diffuse_node.location = [-500, 400]
            if diffuse_name+".dds" not in bpy.data.images:
                diffuse_node.image = bpy.data.images.load(diffuse_path)
            else:
                diffuse_node.image = bpy.data.images[diffuse_name+".dds"]

            # Connect texture node to Diffuse Node on the Principled BSDF (default spawning shader)
            principled_node = mat.material.node_tree.nodes["Principled BSDF"]
            mat.material.node_tree.links.new(principled_node.inputs['Base Color'], diffuse_node.outputs['Color'])
        else:
            print("Shader node not found.")

    def connect_specular(self, mat, specular_path, specular_name):

        # Create texture node
        if "Principled BSDF" in mat.material.node_tree.nodes:
            specular_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
            specular_node.location = [-500, 200]
            if specular_name + ".dds" not in bpy.data.images:
                specular_node.image = bpy.data.images.load(specular_path)
            else:
                specular_node.image = bpy.data.images[specular_name + ".dds"]

            # Connect texture node to Specular Node on the Principled BSDF (default spawning shader)
            principled_node = mat.material.node_tree.nodes["Principled BSDF"]
            mat.material.node_tree.links.new(principled_node.inputs['Specular'], specular_node.outputs['Color'])
        else:
            print("Shader node not found.")

    def connect_normal(self, mat, normal_path, normal_name):

        if "Principled BSDF" in mat.material.node_tree.nodes:

            # Create texture node
            normal_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
            normal_node.location = [-500, -100]
            if normal_name + ".dds" not in bpy.data.images:
                normal_node.image = bpy.data.images.load(normal_path)
            else:
                normal_node.image = bpy.data.images[normal_name + ".dds"]

            # Create splitter node
            split_rgb_node = mat.material.node_tree.nodes.new("ShaderNodeSeparateRGB")
            split_rgb_node.location = [-250, -50]

            # Create inversion node
            invert_node = mat.material.node_tree.nodes.new("ShaderNodeInvert")
            invert_node.location = [-200, -100]

            # Create RGB node
            rgb_node = mat.material.node_tree.nodes.new("ShaderNodeRGB")
            rgb_node.location = [-300, -200]
            rgb_node.outputs[0].default_value = [255, 255, 255, 255]

            # Create composition node
            compose_node = mat.material.node_tree.nodes.new("ShaderNodeCombineRGB")
            compose_node.location = [-150, -100]

            # Grab Principled Node
            principled_node = mat.material.node_tree.nodes["Principled BSDF"]

            # Invert Green channel
            mat.material.node_tree.links.new(split_rgb_node.inputs['Image'], normal_node.outputs['Color'])
            mat.material.node_tree.links.new(invert_node.inputs['Color'], split_rgb_node.outputs['G'])

            # Connect Alpha, Inverted Green, and white to recompose normal
            mat.material.node_tree.links.new(compose_node.inputs['R'], normal_node.outputs['Alpha'])
            mat.material.node_tree.links.new(compose_node.inputs['G'], invert_node.outputs['Color'])
            mat.material.node_tree.links.new(compose_node.inputs['B'], rgb_node.outputs['Color'])

            mat.material.node_tree.links.new(principled_node.inputs['Normal'], compose_node.outputs['Image'])
        else:
            print("Shader node not found.")


    def execute(self, context):

        work_dir = context.preferences.addons[__package__].preferences.dirpath
        for obj in context.scene.objects:
            # Ignore camera and light objects
            if obj.type not in ['CAMERA', 'LIGHT']:
                # Poll materials in an object
                for mat in obj.material_slots:
                    mat.material.use_nodes = True

                    print("Retrieving texture list...")
                    component_list = search_op.find_file(work_dir, mat.name, 'shader')

                    if component_list is not None:
                        print("Linking textures... ")

                        if component_list[0] is not None:
                            diffuse_path = search_op.find_file(work_dir, component_list[0], 'texture')
                            if diffuse_path is not None:
                                self.connect_diffuse(mat, diffuse_path, component_list[0])
                            else:
                                print("No diffuse texture found.")
                        else:
                            print("No diffuse data.")

                        if component_list[1] is not None:
                            normal_path = search_op.find_file(work_dir, component_list[1], 'texture')
                            if normal_path is not None:
                                self.connect_normal(mat, normal_path, component_list[1])
                            else:
                                print("No normal texture found.")
                        else:
                            print("No normal data.")

                        if component_list[2] is not None:
                            specular_path = search_op.find_file(work_dir, component_list[2], 'texture')
                            if specular_path is not None:
                                self.connect_specular(mat, specular_path, component_list[2])
                            else:
                                print("No specular texture found.")
                        else:
                            print("No specular data found.")
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

