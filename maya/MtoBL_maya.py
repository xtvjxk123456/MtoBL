# coding:utf-8
import sys

sys.path.insert(0, r'D:\pythonSource\scriptInCompany')

import LocalSocket as ls
# import maya.cmds as mc
# import maya.utils as util
import pymel.core as pm
import math


def mesh_data(mesh):
    maya_bl_world_rotate = pm.dt.Matrix([1.0, 0, 0, 0,
                                         0, math.cos(math.radians(-90)), math.sin(math.radians(-90)), 0,
                                         0, -math.sin(math.radians(-90)), math.cos(math.radians(-90)), 0,
                                         0, 0, 0, 1])
    mesh = pm.PyNode(mesh)
    # face_vert_index
    face_data = [f.getVertices() for f in mesh.faces]
    # face_uv_index
    face_uv_count, face_uv_index = pm.PyNode('pCubeShape1').getAssignedUVs()
    face_uv_data = []
    current_index = 0
    for i, v in enumerate(face_uv_count):
        face_uv_data.append(face_uv_index[current_index:current_index + v])
        current_index = current_index + v

        # vert_position
        verts_data = [list(maya_bl_world_rotate * v.getPosition('world')) for v in mesh.verts]
        # vert_normal_value
        # normal_data = [list(maya_bl_world_rotate*v.getNormal('world')) for v in mesh.verts]

        # face_normal
        face_normal_data = [map(lambda x: list(maya_bl_world_rotate * x), f.getNormals('world')) for f in mesh.faces]

        # uv_data
        uv_data = zip(*mesh.getUVs())

        # origin pivot
        pivot_data = list(maya_bl_world_rotate * pm.PyNode('pCube1').getPivots(worldSpace=True)[0])

        return {'f': face_data,
                'fn': face_normal_data,
                'v': verts_data,
                # 'n':normal_data,
                'uv': uv_data,
                'origin': pivot_data,
                'fuv': face_uv_data
                }


def run():
    with ls.TcpClient() as s:
        s.send({'type': 'MESH', 'data': mesh_data('pCubeShape1')})
