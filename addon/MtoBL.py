# coding:utf-8
# 主要是为了预览
import bpy


class MayaPreview(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Maya Preview'
    bl_label = 'Maya Preview'
    bl_context = 'object'

    def draw(self, context):
        self.layout.label(text='This tool connect to maya ')
        self.layout.separator()
        self.layout.label(text='there are some button in future')


def register():
    bpy.utils.register_class(MayaPreview)


def unregister():
    bpy.utils.unregister_class(MayaPreview)
