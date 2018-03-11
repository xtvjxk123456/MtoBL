# coding:utf-8
# 这个模块是在blender 2.8 py3里用的
import bpy

C = bpy.context
D = bpy.data
O = bpy.ops


# set object to be active for operator
def set_object_active(objectName):
    try:
        obj = D.objects[objectName]
    except (KeyError, TypeError):
        raise Exception("Input argv is error")
    else:
        obj.select_set(action='SELECT')
        # active应该一直都只有一个
        return C.active_object

