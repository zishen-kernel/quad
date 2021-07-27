
def load(obj_file):
    obj = []

    f = open(obj_file)
    lines = f.readlines()

    for i in range(10):
        print len(lines[i].split())

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
    #load('11803_Airplane_v1_l1.obj')
    show_struct('11803_Airplane_v1_l1.obj')

