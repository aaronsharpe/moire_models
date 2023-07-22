import numpy as np
import ezdxf

def gen_hexagon(l, x, y):
    """
    Create a hexagon centered on (x, y)
    l: length of the hexagon's edge
    x: x-coordinate of the hexagon's center
    y: y-coordinate of the hexagon's center
    """
    poly = [[x + np.cos(np.radians(angle)) * l, y + np.sin(np.radians(angle)) * l] for angle in range(0, 360, 60)]
    poly.append([x + np.cos(np.radians(0)) * l, y + np.sin(np.radians(0)) * l])
    return np.array(poly)

def gen_lattice_site(poly, lattice_vecs, i, j):
    return poly + i*lattice_vecs[0] + j*lattice_vecs[1]

def gen_lattice_circ(poly, lattice_vecs, radius=10):
    """
    Create a lattice with lattice sites indicated by poly, bounded by a circle
    poly: list of ordered pairs (list) that will be centered at each lattice site
    lattice_vecs: list of ordered pairs (lists) that will serve as the lattice vectors

    """
    i_max = int(2*radius/np.sqrt(lattice_vecs[0][0]**2 + lattice_vecs[0][1]**2))

    polys = []
    for i in range(-i_max, i_max):
        for j in range(-i_max, i_max):
            vec_x = i*lattice_vecs[0][0] + j*lattice_vecs[1][0]
            vec_y = i*lattice_vecs[0][1] + j*lattice_vecs[1][1]
            if np.sqrt(vec_x**2 + vec_y**2) <= radius:
                polys.append(gen_lattice_site(poly, lattice_vecs, i, j))
            else:
                pass
    return polys

def export_lattice(lattice, fname='export.dxf', ):
    doc = ezdxf.new(dxfversion='R2010', setup=True)
    msp = doc.modelspace()
    doc.layers.new(name='1', dxfattribs={'color': 1})
    for poly in lattice:
        msp.add_lwpolyline(poly, dxfattribs={'layer': '1'})
    doc.saveas(fname)
