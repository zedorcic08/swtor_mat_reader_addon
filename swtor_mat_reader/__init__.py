# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import xml_operations

bl_info = {
    "name": "SWTOR Material Linker",
    "author": "Silver Ranger",
    'version': (0, 0, 1),
    "blender": (2, 80, 0),
    "category": "Import-Export",
}

class LinkerAddonPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    dirpath: bpy.props.StringProperty(
        name="Work Directory",
        subtype='DIR_PATH',
        maxlen=1024,
        default='D:\\',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'dirpath')


class ObjectLinkMaterials(bpy.types.Operator):
    bl_idname = "object.material_match"
    bl_label = "Link Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scene = context.scene
        work_dir = bpy.context.preferences.addons[__name__].preferences.dirpath
        print(work_dir)
        for obj in scene.objects:
            if (("camera" not in obj.name.lower()) and ("light" not in obj.name.lower())):
                for mat in obj.material_slots:
                    print('Material: ', mat.name)
          #          xml_operations.material_search(mat.name,work_dir)

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def register():
    bpy.utils.register_class(ObjectLinkMaterials)
    bpy.utils.register_class(LinkerAddonPreferences)


def unregister():
    bpy.utils.unregister_class(ObjectLinkMaterials)
    bpy.utils.unregister_class(LinkerAddonPreferences)