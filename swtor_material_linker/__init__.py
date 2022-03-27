# -*- coding: utf-8 -*-

import bpy
import bpy.types
import bpy.props
from . import principled_linker
from . import uber_linker

bl_info = {
    "name": "SWTOR Material Linker",
    "author": "Silver Ranger",
    'version': (2, 0, 0),
    "blender": (2, 80, 0),
    "category": "Import-Export",
}


class LinkerAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    dirpath: bpy.props.StringProperty(
        name="Work Directory",
        subtype='DIR_PATH',
        maxlen=1024,
        default='C:\\',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'dirpath')


class OBJECT_MT_SubMenu(bpy.types.Menu):
    bl_label = 'Link Type'
    bl_idname = 'object.link_submenu'

    def draw(self, context):
        layout = self.layout

        layout.operator("object.material_match", text="Scene - Principled Shader (Legacy)")
        layout.operator("object.uber_material_scene_match", text="Scene - Uber Material (Legacy)")
        layout.operator("object.uber_material_active_match", text="Selected item - Uber Material (Legacy)")
        layout.operator("object.uber_node_scene_match", text="Scene - Uber Material (Node)")
        layout.operator("object.uber_node_active_match", text="Selected item - Uber Material (Node)")


class OBJECT_MT_MainMenu(bpy.types.Menu):
    # Main menu drawing
    bl_label = 'Material Linker'
    bl_idname = 'object.main_menu'

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.menu(OBJECT_MT_SubMenu.bl_idname)


def register():
    bpy.utils.register_class(LinkerAddonPreferences)
    bpy.utils.register_class(principled_linker.ObjectLinkMaterials)
    bpy.utils.register_class(uber_linker.ObjectSceneUberMaterialLinker)
    bpy.utils.register_class(uber_linker.ObjectActiveUberMaterialLinker)
    bpy.utils.register_class(uber_linker.ObjectSceneUberNodeLinker)
    bpy.utils.register_class(uber_linker.ObjectActiveUberNodeLinker)
    bpy.utils.register_class(OBJECT_MT_SubMenu)
    bpy.utils.register_class(OBJECT_MT_MainMenu)
    bpy.types.NODE_MT_context_menu.append(OBJECT_MT_MainMenu.draw)


def unregister():
    bpy.types.NODE_MT_context_menu.remove(OBJECT_MT_MainMenu.draw)
    bpy.utils.unregister_class(OBJECT_MT_MainMenu)
    bpy.utils.unregister_class(OBJECT_MT_SubMenu)
    bpy.utils.unregister_class(uber_linker.ObjectActiveUberNodeLinker)
    bpy.utils.unregister_class(uber_linker.ObjectSceneUberNodeLinker)
    bpy.utils.unregister_class(uber_linker.ObjectActiveUberLinker)
    bpy.utils.unregister_class(uber_linker.ObjectSceneUberLinker)
    bpy.utils.unregister_class(principled_linker.ObjectLinkMaterials)
    bpy.utils.unregister_class(LinkerAddonPreferences)