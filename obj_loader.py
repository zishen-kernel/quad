import load_mtl
import numpy
from OpenGL.GL import *
from PIL import Image

def get_triangles(vs, vts, fs):
    vbo_data = []

    for face in fs:
        if len(face) == 3:
            for v in (face[0], face[1], face[2]):
                v_i, vt_i, vn_i = v.split('/')
                if vt_i == "":
                    vt_i = "1"
                vbo_data.extend(vs[int(v_i)])
                vbo_data.extend(vts[int(vt_i)])

        elif len(face) == 4:
            for v in (face[0], face[1], face[2], face[0], face[2], face[3]):
                v_i, vt_i, vn_i = v.split('/')
                if vt_i == "":
                    vt_i = 1
                vbo_data.extend(vs[int(v_i)])
                vbo_data.extend(vts[int(vt_i)])

        else:
            print 'face len error %s' % face

    vbo_data = numpy.array(vbo_data, dtype=numpy.float32) 
    return vbo_data

def get_groups(obj_path, obj_file):
    f = open('%s/%s' %(obj_path, obj_file))
    lines = f.readlines()

    groups = []
    # index in face start from 1 not 0
    vs = [[]]
    vts = [[]]
    fs = None

    mtls = None
    mtl_name = ''

    for line in lines:
        es = line.split()
        if len(es) < 1:
            continue
        if es[0] == '#':
            continue

        if es[0] == 'mtllib':
            mtls = load_mtl.load('%s/%s' % (obj_path, es[1]))

        if es[0] == 'v':
            vs.append(es[1:4])

        if es[0] == 'vt':
            vts.append(es[1:3])

        if es[0] == 'f':
            fs.append(es[1:])

        if es[0] == 'usemtl':
            if fs is None:
                fs = []
            else:
                triangles = get_triangles(vs, vts, fs)
                fs = []

                texture_file = mtls[mtl_name]['map_Ka']
                groups.append({'triangles': triangles,
                               'texture_file': texture_file})
            mtl_name = es[1]


    triangles = get_triangles(vs, vts, fs)
    texture_file = mtls[mtl_name]['map_Ka']
    groups.append({'triangles': triangles,
                   'texture_file': texture_file})
        

    return groups

def add_vao_texture(obj_path, group):
    # vao
    vbo_data = group['triangles']

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vbo_data.nbytes, vbo_data, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))

    group['vao'] = vao
    group['vbo'] = vbo
    group['vbo_data'] = vbo_data

    # texture

    texture = glGenTextures(1)
    image = Image.open('%s/%s' % (obj_path, group['texture_file']))
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGB").tobytes()

    group['texture'] = texture
    group['image'] = image
    group['image_data'] = image_data


def load(obj_path, obj_file):
    groups = get_groups(obj_path, obj_file)

    for group in groups:
        add_vao_texture(obj_path, group)

    return groups

def show_struct(obj_file):
    f = open(obj_file)
    lines = f.readlines()

    curr = ''
    count = 0

    polygon_n = 0
    triangle_n = 0

    for i in range(len(lines)):
        line = lines[i]
        es = line.split()
        if len(es) < 1:
            continue

        if es[0] == '#':
            print lines[i]
            continue

        if es[0] == 's':
            continue

        if es[0] == 'f':
            if len(es) == 5:
                polygon_n += 1

            elif len(es) == 4:
                triangle_n += 1
            else:
                print line

        if es[0] != curr:
            print '%d %d %s' % (i, count, curr)
            curr = es[0]
            count = 1
        else:
            count += 1
    print '%d %d %s' % (i, count, curr)
    print '%d %d' % (polygon_n, triangle_n)

if __name__ == '__main__':
    #groups = load('object', '11803_Airplane_v1_l1.obj')
    show_struct('object/11803_Airplane_v1_l1.obj')

