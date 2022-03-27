# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import search_op


class ObjectSceneUberMaterialLinker(bpy.types.Operator):
    bl_idname = "object.uber_material_scene_match"
    bl_label = "Scene - Uber Material (Material)"
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

                        search_op.connect_textures(mat, work_dir, component_list, 'legacy')
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class ObjectActiveUberMaterialLinker(bpy.types.Operator):
    bl_idname = "object.uber_material_active_match"
    bl_label = "Item - Uber Material (Material)"
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

                        search_op.connect_textures(mat, work_dir, component_list, 'legacy')
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class ObjectSceneUberNodeLinker(bpy.types.Operator):
    bl_idname = "object.uber_node_scene_match"
    bl_label = "Scene - Uber Material (Node)"
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
                        if 'SWTOR' not in mat.material.node_tree.nodes:
                            search_op.create_material_node(mat)

                            # Get path to diffuse image and load into slot
                            print("Material look-up and link started.")
                            search_op.connect_textures(mat, work_dir, component_list, 'node')
                        else:
                            print("Node already present.")
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class ObjectActiveUberNodeLinker(bpy.types.Operator):
    bl_idname = "object.uber_node_active_match"
    bl_label = "Item - Uber Material (Node)"
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
                        if 'SWTOR' not in mat.material.node_tree.nodes:
                            search_op.create_material_node(mat)

                            # Get path to diffuse image and load into slot
                            print("Material look-up and link started.")
                            search_op.connect_textures(mat, work_dir, component_list, 'node')
                        else:
                            print("Node already present.")
                    else:
                        print(" No shader found. ")

        print("--------------------")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.