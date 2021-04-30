# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import search_op


class ObjectLinkUberItemMaterial(bpy.types.Operator):
    bl_idname = "object.uber_match"
    bl_label = "Item - Uber Material"
    bl_options = {'REGISTER', 'UNDO'}

    def create_material_from_template(self, mat):
        # Fetch Principled BDSF node and delete it
        material_name = mat.material.name
        material_data = mat.material
        print("--------------------")
        print("Processing material: " + material_name)

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
            print("Template set.")
            print("--------------------")
        else:
            print("Template not found.")


    def connect_diffuse(self, mat, diffuse_path, diffuse_name):
        # Fetch Diffuse node and connect file
        if "_d DiffuseMap" in mat.material.node_tree.nodes:
            diffuse_node = mat.material.node_tree.nodes["_d DiffuseMap"]
            if diffuse_name + ".dds" not in bpy.data.images:
                diffuse_node.image = bpy.data.images.load(diffuse_path)
            else:
                diffuse_node.image = bpy.data.images[diffuse_name + ".dds"]
            diffuse_node.image.colorspace_settings.name = 'Raw'
        else:
            print ("No Diffuse Node found.")

    def connect_specular(self, mat, specular_path, specular_name):
        # Fetch Specular Node and connect file
        if "_s GlossMap" in mat.material.node_tree.nodes:
            specular_node = mat.material.node_tree.nodes["_s GlossMap"]
            if specular_name + ".dds" not in bpy.data.images:
                specular_node.image = bpy.data.images.load(specular_path)
            else:
                specular_node.image = bpy.data.images[specular_name + ".dds"]
            specular_node.image.colorspace_settings.name = 'Raw'
        else:
            print("No Specular Node found.")

    def connect_normal(self, mat, normal_path, normal_name):
        # Fetch Normal node and connect file
        if "_n RotationMap" in mat.material.node_tree.nodes:
            normal_node = mat.material.node_tree.nodes["_n RotationMap"]
            if normal_name + ".dds" not in bpy.data.images:
                normal_node.image = bpy.data.images.load(normal_path)
            else:
                normal_node.image = bpy.data.images[normal_name + ".dds"]
            normal_node.image.colorspace_settings.name = 'Raw'
        else:
            print("No Normal Node found.")

    def execute(self, context):

        work_dir = context.preferences.addons[__package__].preferences.dirpath
        for obj in context.scene.objects:
            # Ignore camera and light objects
            if ("camera" not in obj.name.lower()) and ("light" not in obj.name.lower()):
                # Poll materials in an object
                for mat in obj.material_slots:
                    mat.material.use_nodes = True

                    component_list = search_op.find_file(work_dir, mat.name, 'shader')
                    if component_list is not None:
                        print("Creating material template...")
                        self.create_material_from_template(mat)

                        # Get path to diffuse image and load into slot
                        print("Material look-up and link started.")
                        diffuse_path = search_op.find_file(work_dir, component_list[0], 'texture')
                        if diffuse_path is not None:
                            self.connect_diffuse(mat, diffuse_path, component_list[0])
                        else:
                            print("No diffuse texture found.")

                        # Get path of normal image and load into slot
                        normal_path = search_op.find_file(work_dir, component_list[1], 'texture')
                        if normal_path is not None:
                            self.connect_normal(mat, normal_path, component_list[1])
                        else:
                            print("No normal texture found.")

                        # Get path to specular image and load into slot
                        specular_path = search_op.find_file(work_dir, component_list[2], 'texture')
                        if specular_path is not None:
                            self.connect_specular(mat, specular_path, component_list[2])
                        else:
                            print("No specular texture found.")
                    else:
                        print(" No shader found. ")

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

