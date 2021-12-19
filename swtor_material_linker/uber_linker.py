# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import search_op

# TODO: refactor code to remove redundancy

class ObjectSceneUberLinker(bpy.types.Operator):
    bl_idname = "object.uber_scene_match"
    bl_label = "Scene - Uber Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        work_dir = context.preferences.addons[__package__].preferences.dirpath
        for obj in context.scene.objects:
            # Ignore camera and light objects
            if obj.type not in ['CAMERA', 'LIGHT']:
                # Poll materials in an object
                for mat in obj.material_slots:
                    mat.material.use_nodes = True

                    # Provision against copied materials: material name will always end up as 'name'+'.00x'
                    # At the start of the iteration, pull the actual name from the string
                    material_name = mat.name.split(".")[0]
                    print("--------------------")
                    print("Processing " + material_name + ".")
                    print("--------------------")

                    component_list = search_op.find_file(work_dir, material_name, 'shader')
                    if component_list is not None:
                        print("Creating material template...")
                        search_op.create_material_from_template(mat)

                        # Get path to diffuse image and load into slot
                        print("Material look-up and link started.")
                        if component_list[0] is not None:
                            diffuse_path = search_op.find_file(work_dir, component_list[0], 'texture')
                            if diffuse_path is not None:
                                search_op.connect_diffuse(mat, diffuse_path, component_list[0])
                            else:
                                print("No diffuse texture found.")
                        else:
                            print("No diffuse data.")

                        # Get path of normal image and load into slot
                        if component_list[1] is not None:
                            normal_path = search_op.find_file(work_dir, component_list[1], 'texture')
                            if normal_path is not None:
                                search_op.connect_normal(mat, normal_path, component_list[1])
                            else:
                                print("No normal texture found.")
                        else:
                            print("No normal data.")

                        # Get path to specular image and load into slot
                        if component_list[2] is not None:
                            specular_path = search_op.find_file(work_dir, component_list[2], 'texture')
                            if specular_path is not None:
                                search_op.connect_specular(mat, specular_path, component_list[2])
                            else:
                                print("No specular texture found.")
                        else:
                            print("No specular data.")
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

class ObjectActiveUberLinker(bpy.types.Operator):
    bl_idname = "object.uber_active_match"
    bl_label = "Item - Uber Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        work_dir = context.preferences.addons[__package__].preferences.dirpath
        for obj in context.selected_objects:
            # Ignore camera and light objects
            if obj.type not in ['CAMERA', 'LIGHT']:
                # Poll materials in an object
                for mat in obj.material_slots:
                    mat.material.use_nodes = True

                    # Provision against copied materials: material name will always end up as 'name'+'.00x'
                    # At the start of the iteration, pull the actual name from the string
                    material_name = mat.name.split(".")[0]
                    print("--------------------")
                    print("Processing " + material_name + ".")
                    print("--------------------")

                    component_list = search_op.find_file(work_dir, material_name, 'shader')
                    if component_list is not None:
                        print("Creating material template...")
                        search_op.create_material_from_template(mat)

                        # Get path to diffuse image and load into slot
                        print("Material look-up and link started.")
                        if component_list[0] is not None:
                            diffuse_path = search_op.find_file(work_dir, component_list[0], 'texture')
                            if diffuse_path is not None:
                                search_op.connect_diffuse(mat, diffuse_path, component_list[0])
                            else:
                                print("No diffuse texture found.")
                        else:
                            print("No diffuse data.")

                        # Get path of normal image and load into slot
                        if component_list[1] is not None:
                            normal_path = search_op.find_file(work_dir, component_list[1], 'texture')
                            if normal_path is not None:
                                search_op.connect_normal(mat, normal_path, component_list[1])
                            else:
                                print("No normal texture found.")
                        else:
                            print("No normal data.")

                        # Get path to specular image and load into slot
                        if component_list[2] is not None:
                            specular_path = search_op.find_file(work_dir, component_list[2], 'texture')
                            if specular_path is not None:
                                search_op.connect_specular(mat, specular_path, component_list[2])
                            else:
                                print("No specular texture found.")
                        else:
                            print("No specular data.")
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

