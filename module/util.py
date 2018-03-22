# coding:utf-8
import itertools
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


# 暂时没有更新法线
def update_mesh(meshShapeName, data=None):
    """
    数据例子
    {'f': [[0, 1, 3, 2],
       [2, 3, 5, 4],
       [4, 5, 7, 6],
       [6, 7, 1, 0],
       [1, 7, 5, 3],
       [6, 0, 2, 4]],
 'fn': [[[0.0, -1.0, 6.123233995736766e-17],
         [0.0, -1.0, 6.123233995736766e-17],
         [0.0, -1.0, 6.123233995736766e-17],
         [0.0, -1.0, 6.123233995736766e-17]],
        [[0.0, 6.123233995736766e-17, 1.0],
         [0.0, 6.123233995736766e-17, 1.0],
         [0.0, 6.123233995736766e-17, 1.0],
         [0.0, 6.123233995736766e-17, 1.0]],
        [[0.0, 1.0, -6.123233995736766e-17],
         [0.0, 1.0, -6.123233995736766e-17],
         [0.0, 1.0, -6.123233995736766e-17],
         [0.0, 1.0, -6.123233995736766e-17]],
        [[0.0, -6.123233995736766e-17, -1.0],
         [0.0, -6.123233995736766e-17, -1.0],
         [0.0, -6.123233995736766e-17, -1.0],
         [0.0, -6.123233995736766e-17, -1.0]],
        [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
        [[-1.0, 0.0, 0.0],
         [-1.0, 0.0, 0.0],
         [-1.0, 0.0, 0.0],
         [-1.0, 0.0, 0.0]]],
 'fuv': [[0, 1, 3, 2],
         [2, 3, 5, 4],
         [4, 5, 7, 6],
         [6, 7, 9, 8],
         [1, 10, 11, 3],
         [12, 0, 2, 13]],
 'uv': [(0.375, 0.0),
        (0.625, 0.0),
        (0.375, 0.25),
        (0.625, 0.25),
        (0.375, 0.5),
        (0.625, 0.5),
        (0.375, 0.75),
        (0.625, 0.75),
        (0.375, 1.0),
        (0.625, 1.0),
        (0.875, 0.0),
        (0.875, 0.25),
        (0.125, 0.0),
        (0.125, 0.25)],
 'v': [[-0.4219123581960016,
        -0.8774453469943295,
        1.7685093998569443e-08,
        0.0],
       [0.6200289269373602, -0.8774453469943295, 1.7685093998569443e-08, 0.0],
       [-0.4219123581960016, -0.8774453469943294, 1.0177453933183336, 0.0],
       [0.6200289269373602, -0.8774453469943294, 1.0177453933183336, 0.0],
       [-0.4219123581960016, 0.7162097624111882, 1.0177453933183336, 0.0],
       [0.6200289269373602, 0.7162097624111882, 1.0177453933183336, 0.0],
       [-0.4219123581960016, 0.7162097624111881, 1.7685093900986212e-08, 0.0],
       [0.6200289269373602, 0.7162097624111881, 1.7685093900986212e-08, 0.0]]}

    :param meshShapeName:
    :param data: {'f':[],'v':[]}
    :return:
    """
    if data:
        # 使用mesh shape name
        mesh = bpy.data.meshes[meshShapeName]

        mesh_bm = bm.new()
        faces_data = data['f']
        verts_data = data['v']
        # 这里不使用点法线,毕竟点法线是每个面的点相加的
        face_normal_data = data['fn']
        uv_data = data['uv']
        face_uv_index_data = data['fuv']

        # create verts
        verts = [mesh_bm.verts.new(tuple(v[:3])) for v in verts_data]
        if not is_future_version():
            mesh_bm.verts.ensure_lookup_table()

        # create faces
        faces = [mesh_bm.faces.new(tuple(map(lambda x: verts[x], f))) for f in faces_data]
        if not is_future_version():
            mesh_bm.faces.ensure_lookup_table()

        # face_uv
        uv_layer = bm.loops.layers.uv.verify()
        for f, fuv in zip(faces, face_uv_index_data):
            f.loops.index_update()
            for i, loop in enumerate(f.loops):
                try:
                    uv_index = fuv[i]
                except IndexError:
                    pass
                else:
                    loop[uv_layer].uv = uv_data[uv_index]

        mesh_bm.to_mesh(mesh)
        # 显性更新好像不容易崩溃
        bm.clear()
        mesh.update()

        #    obj.data.calc_normals_split()
        #    for loop,normal in zip(obj.data.loops,itertools.chain(*face_normal_data)):
        #        loop.normal = normal
        #    obj.data.free_normals_split()
        # 这种操作不对劲

        # 设置法线，界面也可以识别到
        mesh.normals_split_custom_set(list(itertools.chain(*face_normal_data)))
        # can link ui
        mesh.use_auto_smooth = True  # custom normal split需要auto smooth
        mesh.update()


def create_mesh(transfomrName, data=None):
    # create mesh
    if D.objects.find(transfomrName) < 0 and D.meshes.find(transfomrName + 'Shape') < 0:
        mesh = D.meshes.new(transfomrName + 'Shape')
        obj = D.objects.new(transfomrName, mesh)
        if not is_future_version():
            C.scene.objects.link(obj)
        else:
            C.scene_collection.objects.link(obj)
        update_mesh(mesh, data)
        return obj
    else:
        raise Exception('Input transform name is illegal.')

# C.scene_collection为当前collection
# 现阶段2.8没有D.scene_collection 故无法创建collection
# 不知如何select/active collection
