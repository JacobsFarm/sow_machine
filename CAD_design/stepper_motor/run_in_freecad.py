import importlib
import os
import sys

sys.dont_write_bytecode = True

try:
    FOLDER = os.path.dirname(os.path.abspath(__file__))
except NameError:
    FOLDER = r"F:\veldrobot\mini doseerbak\CAD_design\stepper_motor"

if FOLDER not in sys.path:
    sys.path.insert(0, FOLDER)

import ovm_params
import ovm_parts
import ovm_calc
import build_ovm

for module in (ovm_params, ovm_parts, ovm_calc, build_ovm):
    importlib.reload(module)

doc = build_ovm.build()
ovm_calc.report()
print("interference", build_ovm.check_interference())
print("does not fit the bed", build_ovm.check_fit())
print("print sizes", build_ovm.print_sizes())
print("filament", build_ovm.mass_properties())
print("roller variants", build_ovm.roller_variants())

try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass
