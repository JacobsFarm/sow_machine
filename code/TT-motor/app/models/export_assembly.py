import sys, os
import FreeCAD as App, MeshPart
TT = r"F:\veldrobot\mini doseerbak\CAD_design\TT-motor"
OUT = r"F:\veldrobot\mini doseerbak\code\TT-motor\app\models"
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, TT); sys.path.insert(1, os.path.join(os.path.dirname(TT), "stepper_motor"))
doc = App.openDocument(os.path.join(TT, "Overseeder_Mini_TT.FCStd"))

def save(shape, name):
    m = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.15)
    m.write(os.path.join(OUT, name + ".stl"))
    bb = shape.BoundBox
    print("wrote", name, m.CountFacets, "x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax))

for n in ("body", "motor_plate", "rim", "tt_motor", "tt_shaft"):
    o = doc.getObject(n)
    s = o.Shape.copy()
    s.Placement = o.getGlobalPlacement()
    save(s, n)

import ovt_params as T
import ovt_parts as G
for k in T.VARIANTS:
    save(G.roller(k), "roller_" + k)
print("default", T.DEFAULT)
