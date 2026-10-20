import importlib
import os
import sys

sys.dont_write_bytecode = True

try:
    FOLDER = os.path.dirname(os.path.abspath(__file__))
except NameError:
    FOLDER = r"F:\veldrobot\mini doseerbak\CAD_design\TT-motor"
BASE = os.path.join(os.path.dirname(FOLDER), "stepper_motor")

for p in (BASE, FOLDER):
    if p not in sys.path:
        sys.path.insert(0, p)

import ovm_params
import ovm_parts
import build_ovm
import ovt_params
import ovt_parts
import build_ovt

for module in (ovm_params, ovm_parts, build_ovm, ovt_params, ovt_parts, build_ovt):
    importlib.reload(module)

doc = build_ovt.build()
print("interference", build_ovt.check_interference())
print("shaft engagement", build_ovt.check_engagement())
print("does not fit the bed", build_ovt.check_fit())
print("print sizes", build_ovt.print_sizes())
print("filament", build_ovt.mass_properties())
