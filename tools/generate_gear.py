import math, os
from panda3d.core import LPoint3d, LVector3d
from panda3d.egg import EggData, EggGroup, EggPolygon, EggVertex, EggVertexPool

def make_gear_egg(teeth=10, outer_r=1.0, inner_r=0.75, tooth_h=0.25,
                  thickness=0.3, out_path="models/gear.egg"):
    os.makedirs("models", exist_ok=True)
    egg  = EggData()
    pool = EggVertexPool("gear_verts")
    egg.addChild(pool)
    grp  = EggGroup("gear")
    egg.addChild(grp)

    def add_v(x, y, z, nx=0, ny=0, nz=1):
        v = EggVertex()
        v.setPos(LPoint3d(x, y, z))
        v.setNormal(LVector3d(nx, ny, nz))
        pool.addVertex(v)
        return v

    step   = 2 * math.pi / teeth
    fz, bz = thickness / 2, -thickness / 2

    for i in range(teeth):
        a0 = i * step
        a1, a2, a3 = a0+step*0.4, a0+step*0.6, (i+1)*step
        pts = [
            (math.cos(a0)*inner_r, math.sin(a0)*inner_r),
            (math.cos(a1)*inner_r, math.sin(a1)*inner_r),
            (math.cos(a1)*outer_r, math.sin(a1)*outer_r),
            (math.cos(a2)*outer_r, math.sin(a2)*outer_r),
            (math.cos(a2)*inner_r, math.sin(a2)*inner_r),
            (math.cos(a3)*inner_r, math.sin(a3)*inner_r),
        ]
        for j in range(1, len(pts)-1):
            for verts, z, nz in [([pts[0],pts[j],pts[j+1]], fz, 1),
                                   ([pts[0],pts[j+1],pts[j]], bz, -1)]:
                p = EggPolygon(); grp.addChild(p)
                for px, py in verts: p.addVertex(add_v(px, py, z, 0, 0, nz))
        for j in range(len(pts)):
            p1, p2 = pts[j], pts[(j+1)%len(pts)]
            nx = (p1[1]+p2[1])/2; ny = -(p1[0]+p2[0])/2
            p = EggPolygon(); grp.addChild(p)
            for (px,py),z in [(p1,fz),(p2,fz),(p2,bz),(p1,bz)]:
                p.addVertex(add_v(px, py, z, nx, ny, 0))

    egg.writeEgg(out_path)
    print(f"Gear model written to {out_path}")

if __name__ == "__main__":
    make_gear_egg()