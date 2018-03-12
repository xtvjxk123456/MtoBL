# coding:utf-8
import bpy
import bmesh as bm

C = bpy.context
D = bpy.data
O = bpy.ops


def is_future_version():
    version = bpy.app.version
    if version[0] > 2:
        return True
    if version[0] == 2 and version[1] >= 80:
        return True
    else:
        return False


# set object to be active for operator
def set_object_active(objectName):
    try:
        obj = D.objects[objectName]
    except (KeyError, TypeError):
        raise Exception("Input argv is error")
    else:
        if is_future_version():
            obj.select_set(action='SELECT')
            obj.select_set(action='DESELECT')
            # active应该一直都只有一个
            return C.active_object
        else:
            C.scene.objects.active = obj
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
        if is_future_version():
            obj.select_set(action='SELECT')
            return C.selected_objects
        else:
            # 2.80以前有层概念，注意当前层
            obj.select = True
            return C.selected_objects


def vertexs_position(meshObjectName, is_global=True):
    obj = set_object_active(meshObjectName)
    mesh_obj = obj.data

    # #set mesh_obj edit
    # O.object.mode_set(mode='EDIT')
    # O.mesh.select_all(action='DESELECT')
    mesh_bm = bm.new()
    mesh_bm.from_mesh(mesh_obj)

    verts = mesh_bm.verts
    if not is_future_version():
        verts.ensure_lookup_table()
    if is_global:
        for v in verts:
            yield (obj.matrix_world * v.co).to_tuple()
    else:
        for v in verts:
            yield v.co.to_tuple()
