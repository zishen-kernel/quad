

def load(file_name):
    f = open(file_name)
    lines = f.readlines()

    mtls = {}

    key = None
    value = {}

    for line in lines:
        es = line.split()

        if len(es) < 2:
            continue

        if es[0] == 'newmtl':
            if key is not None:
                mtls[key] = value
                value = {}
            key = es[1]

        if es[0] == 'map_Ka':
            value['map_Ka'] = es[1]

    mtls[key] = value

    return mtls

if __name__ == '__main__':
    mtls = load('11803_Airplane_v1_l1.mtl')
    print mtls
