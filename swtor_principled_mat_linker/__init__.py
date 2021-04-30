# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import xml_operations

bl_info = {
    "name": "SWTOR Material Linker",
    "author": "Silver Ranger",
    'version': (0, 5, 0),
    "blender": (2, 80, 0),
    "category": "Import-Export",
}

class LinkerAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    dirpath: bpy.props.StringProperty(
        name="Work Directory",
        subtype='DIR_PATH',
        maxlen=1024,
        default='C:\\',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'dirpath')


class ObjectLinkMaterials(bpy.types.Operator):
    bl_idname = "object.material_match"
    bl_label = "Link Materials"
    bl_options = {'REGISTER', 'UNDO'}

    # Draw the clickable menu item
    def draw_menu(self, context):
        layout = self.layout
        layout.separator()
        layout.operator("object.material_match", text="Link Materials")

    def connect_diffuse(self, mat, diffuse_path):
        # Create texture node
        diffuse_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
        diffuse_node.location = [-500, 400]
        diffuse_node.image = bpy.data.images.load(diffuse_path)

        # Connect texture node to Diffuse Node on the Principled BSDF (default spawning shader)
        principled_node = mat.material.node_tree.nodes["Principled BSDF"]
        mat.material.node_tree.links.new(principled_node.inputs['Base Color'], diffuse_node.outputs['Color'])

    def connect_specular(self, mat, specular_path):
        # Create texture node
        specular_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
        specular_node.location = [-500, 200]
        specular_node.image = bpy.data.images.load(specular_path)

        # Connect texture node to Specular Node on the Principled BSDF (default spawning shader)
        principled_node = mat.material.node_tree.nodes["Principled BSDF"]
        mat.material.node_tree.links.new(principled_node.inputs['Specular'], specular_node.outputs['Color'])

    def connect_normal(self, mat, normal_path):

        # Create texture node
        normal_node = mat.material.node_tree.nodes.new("ShaderNodeTexImage")
        normal_node.location = [-400, -100]
        normal_node.image = bpy.data.images.load(normal_path)

        # Create splitter node
        split_rgb_node = mat.material.node_tree.nodes.new("ShaderNodeSeparateRGB")
        split_rgb_node.location = [-200, -50]

        # Create inversion node
        invert_node = mat.material.node_tree.nodes.new("ShaderNodeInvert")
        invert_node.location = [-200, -100]

        # Create RGB node
        rgb_node = mat.material.node_tree.nodes.new("ShaderNodeRGB")
        rgb_node.location = [-300, -150]
        rgb_node.outputs[0].default_value = [255, 255, 255, 255]

        # Create composition node
        compose_node = mat.material.node_tree.nodes.new("ShaderNodeCombineRGB")
        compose_node.location = [-150, -100]

        principled_node = mat.material.node_tree.nodes["Principled BSDF"]

        # Invert Green channel
        mat.material.node_tree.links.new(split_rgb_node.inputs['Image'], normal_node.outputs['Color'])
        mat.material.node_tree.links.new(invert_node.inputs['Color'], split_rgb_node.outputs['G'])

        # Connect Alpha, Inverted Green, and white to recompose normal
        mat.material.node_tree.links.new(compose_node.inputs['R'], normal_node.outputs['Alpha'])
        mat.material.node_tree.links.new(compose_node.inputs['G'], invert_node.outputs['Color'])
        mat.material.node_tree.links.new(compose_node.inputs['B'], rgb_node.outputs['Color'])

        mat.material.node_tree.links.new(principled_node.inputs['Normal'], compose_node.outputs['Image'])


    def execute(self, context):

        work_dir = bpy.context.preferences.addons[__name__].preferences.dirpath
        for obj in context.scene.objects:
            # Ignore camera and light objects
            if ("camera" not in obj.name.lower()) and ("light" not in obj.name.lower()):
                # Poll materials in an object
                for mat in obj.material_slots:
                    mat.material.use_nodes = True

                    component_list = xml_operations.find_file(work_dir, mat.name ,'shader')
                    if component_list is not None:

                        diffuse_path = xml_operations.find_file(work_dir,component_list[0], 'texture')
                        if diffuse_path is not None:
                            self.connect_diffuse(mat, diffuse_path)
                        else:
                            print("No diffuse texture found.")

                        normal_path = xml_operations.find_file(work_dir, component_list[1], 'texture')
                        if normal_path is not None:
                            self.connect_normal(mat, normal_path)
                        else:
                            print("No normal texture found.")

                        specular_path = xml_operations.find_file(work_dir, component_list[2], 'texture')
                        if specular_path is not None:
                            self.connect_specular(mat, specular_path)
                        else:
                            print("No specular texture found.")
                    else:
                        print(" No shader found. ")

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def register():
    bpy.utils.register_class(LinkerAddonPreferences)
    bpy.utils.register_class(ObjectLinkMaterials)
    bpy.types.NODE_MT_context_menu.append(ObjectLinkMaterials.draw_menu)


def unregister():
    bpy.types.NODE_MT_context_menu.remove(ObjectLinkMaterials.draw_menu)
    bpy.utils.unregister_class(ObjectLinkMaterials)
    bpy.utils.unregister_class(LinkerAddonPreferences)