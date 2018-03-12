# coding:utf-8
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
        obj.select_set(action='DESELECT')
        # active应该一直都只有一个
        return C.active_object


# select object
def select_object(objectName, append=False):
    if not append:
        O.object.select_all(action='DESELECT')
    try:
        obj = D.objects[objectName]
    except (KeyError, TypeError):
        raise Exception("Input argv is error")
    else:
        obj.select_set(action='SELECT')
        return C.selected_objects
