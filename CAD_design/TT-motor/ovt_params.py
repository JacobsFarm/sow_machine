# =====================================================================
# Overseeder mini drop seeder, TT gear motor version - parameters
# A small, temporary test version of the rig of ../ovm_params.py: 80 mm wide inside, 120 mm high, no mounting
# flange, 4 mm end wall and motor plate, held together (and mountable) by one M8 x 100 bolt through a tube along
# the back. Driven by a yellow TT gear motor (1:48, double-flat shaft, ../../inspiration/KW-2628_4-1280x960.jpg)
# instead of the NEMA 17. Housing cross-section, cut-off rim and cam shapes stay as in the base design.
#   - the motor end of the roller is 2.8 mm longer (Ø35) and runs in a Ø35.4 x 2.8 bearing pocket in the inner face
#     of the plate, so the short TT shaft (8.7 mm) reaches into the roller through the 1.2 mm wall that is left; the
#     journal on the other end is 4.2 long and runs in the 4 mm end wall;
#   - the roller gets a double-D socket for the TT shaft (Ø5.4, 3.7 across the flats);
#   - the gearbox is bolted flat on the outer face of the plate with 2 x M3 through its own mounting holes and
#     located by its Ø4 peg in a hole in the plate.
# Same local frame as ovm_params: x = along the roller (+x = motor), y = forward, z = up, origin = roller axis.
# =====================================================================
import os
import sys

_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stepper_motor")
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

import ovm_params as P          # noqa: E402  (the base design, source of all other dimensions)

# ---------------------------------------------------------------------
# Changes to the base design. The base module is changed in memory here, so ovm_parts must be (re)loaded after
# this module (ovt_parts does that). The base run_in_freecad.py reloads ovm_params, so the base builds as before.
# ---------------------------------------------------------------------
width = 80.0                    # inside width = roller length + 2 x 0.5: the M8 x 100 bolt then fits (see bolt)
height = 120.0                  # body height, bottom of the end plates to the top of the hopper
end_t = 4.0                     # left end wall (base 3)
plate_t = 4.0                   # motor plate (base 6)

P.width = width
P.end_t = end_t
P.motor_plate_t = plate_t
P.flange = False
P.screw_columns = False         # the 2 M8 bolts clamp the motor plate; no M3 columns along the body
P.back_gap = 0.3                 # back housing wall to the roller (base 0.8): no room for seed behind the roller
P.y_back = -(P.roller_d / 2.0 + P.back_gap)
P.journal = (8.0, P.roller_end_gap + end_t - 0.3)    # Ø8 x 4.2: runs 3.7 mm in the 4 mm end wall (base 3 long)
P.roller_x = (-width / 2.0 + P.roller_end_gap, width / 2.0 - P.roller_end_gap)
P.rim_x = (-width / 2.0 + 0.2, width / 2.0 - 0.2)
P.tray_x = (-50.0, 50.0)
# lower hopper with the same wall angles (26 deg from vertical)
_tb, _tf = P.TAN_BACK, P.TAN_FRONT
P.z_top = P.plate_bottom + height                                 # 95
P.top_back = P.y_back - (P.z_top - P.z_throat) * _tb
P.top_front = P.y_front + (P.z_top - P.z_throat) * _tf
P.boss_z_high = P.z_top - 10.0
P.TAN_BACK = P.wall_slope(P.top_back, P.y_back)
P.TAN_FRONT = P.wall_slope(P.top_front, P.y_front)

# Cam rollers: fewer rings over the shorter length, at about the same ring pitch as the 150 mm rollers (143 mm of
# cams); the pitch stays at least cam length + height, so the 45 deg chamfers of neighbouring rings do not overlap.
_SPAN_BASE = 150.0 - 2 * P.roller_end_gap - 2 * P.flute_end
_SPAN = width - 2 * P.roller_end_gap - 2 * P.flute_end            # 73
for _k, _v in P.ROLLERS.items():
    if _v["kind"] == "studs":
        _base_rows = _v.get("rows_150", _v["rows"])
        _rows = int(round(_SPAN / (_SPAN_BASE / _base_rows)))
        assert _SPAN / _rows >= _v["stud"][0] + _v["stud"][2], _k
        _l, _w, _h = _v["stud"]
        P.ROLLERS[_k] = dict(_v, rows=_rows, rows_150=_base_rows,
                             label="cams %g x %g x %g, %d rings of %d" % (_l, _w, _h, _rows, _v["around"]))

# ---------------------------------------------------------------------
# 2 M8 through-bolts: along x, each through a tube on the outside of a housing wall (end wall to open end) and
# the motor plate. They clamp the plate on (no M3 screws) and locate it, and are the mounting points for the test;
# two bolts also stop the rig turning around one.
# ---------------------------------------------------------------------
bolt = (8.0, 100.0)             # M8 x 100 (length under the head)
bolt_hole = 8.3                 # close fit: the bolts locate the plate (and so the roller bearing) to about 0.15 mm
bolt_tube_d = 16.0              # tube outside diameter
# tube centres 6 mm outside the housing walls (2 mm overlap with the wall, hole 1.75 mm from it):
# back at z = 5, above the M3 column; front at z = 18, above the rim block (at z = 5 the hole would cut the rim slot)
bolt_positions = [(P.y_back - P.wall - 6.0, 5.0), (P.y_front + P.wall + 6.0, 18.0)]
bolt_head = (13.0, 5.3)         # hex head across corners (drawn round), height
washer = (16.0, 1.6)
nut = (13.0, 6.5)

# ---------------------------------------------------------------------
# TT gear motor (datasheet drawing in ../../inspiration/; shaft and mounting holes from the user's measurement)
# Gearbox lying on the plate: its thickness along x, its length along z (motor up), its width along y.
# ---------------------------------------------------------------------
tt_gearbox = (37.0, 22.44, 18.6)    # length (z), width (y), thickness (x)
tt_shaft_to_end = 9.25              # shaft axis to the gearbox end on the tab side (that end points down)
tt_tab = (4.8, 8.0, 2.8)            # tab beyond the gearbox end: length (z), width (y), thickness (x)
tt_motor = (28.2, 22.4, 19.0)       # motor can beyond the gearbox: length (z), width (y), thickness (x)
tt_shaft = (5.4, 3.7)               # double-flat shaft: round diameter, across the two flats
tt_shaft_out = (8.7, 9.3)           # shaft beyond the gearbox faces: plate side (the shorter one, worst case), back
tt_holes = (19.85, 17.6, 3.0)       # 2 mounting holes: distance from the shaft along z (measured; = 11.25 + 8.6
                                    # on the drawing), spacing in y, diameter
tt_peg = (4.0, 1.92, 11.25)         # locating peg on the face: diameter, height, distance from the shaft along z
tt_rpm_6v = 200.0                   # no-load speed at 6 V, 1:48 (typical, not measured)
tt_stall_nm = 0.08                  # stall torque at 6 V (typical, not measured)

# ---------------------------------------------------------------------
# Motor plate: the base outline (plus the bolt tubes), 4 mm, a bearing pocket for the roller end
# ---------------------------------------------------------------------
roller_end_d = 35.0                 # the roller end in the pocket is Ø35, not Ø40: the counterbored M3 heads at 19.85
                                    # from the shaft (head to r = 18.95) then keep a 1.25 mm wall to the pocket
pocket = (roller_end_d + 0.4, 2.8)  # the bearing of the motor end: Ø35.4 x 2.8 in the inner face of the plate, 0.2 mm
                                    # clearance per side; the roller end runs 2.3 mm in it (2.0 mm cylinder after the
                                    # chamfer). The roller runs in the plates at both ends; the TT shaft only drives it
                                    # (socket with clearance, so the two do not fight)
wall_left = plate_t - pocket[1]     # 1.2 mm wall (6 layers) between the pocket and the gearbox face
shaft_hole = tt_shaft[0] + 0.6      # through the wall, the shaft does not touch it
peg_hole = tt_peg[0] + 0.2          # locates the gearbox to 0.1 mm, so its shaft lines up with the bearing
peg_groove = (0.6, 0.4)             # the Ø4 peg (1.92) sticks 0.72 through the 1.2 wall: ring groove in the roller
                                    # end face at the peg radius so it clears while turning (depth, radial clearance)
end_chamfer = 0.3                   # 45 deg on the bed-side edge of the Ø35 end: no elephant's foot in the bearing
motor_bolt = (3.0, 5.5, 3.0)        # 2 x M3 x 25 socket head from the inside: through hole, counterbore for the head
                                    # (Ø5.5, the head size) in the inner face, so the head is flush and out of the way
                                    # of the roller; nut on the outer face of the gearbox.
                                    # Length: 1.0 wall + 18.6 gearbox + 2.4 nut = 22, M3 x 25 leaves 3
                                    # The outer face is flat: no recess under the motor can (not needed on the real
                                    # motor; the can is drawn flush with the gearbox face on the plate side)

# ---------------------------------------------------------------------
# Roller: the base roller variants with a 2.8 mm longer motor end and a double-D socket
# ---------------------------------------------------------------------
roller_ext = pocket[1]              # extra length at the motor end (plain Ø35, no cams), 0.5 from the pocket bottom;
                                    # the Ø40 end face covers the pocket mouth, 0.5 from the plate (seed-tight as
                                    # the base end gap). Printed standing on this end: a 2.5 mm overhang ring.
socket_clear = 0.2                  # per side on the TT shaft: takes up the 0.1 motor location and print tolerance
socket_depth = 10.0                 # the shaft enters 8.7 - 1.2 - 0.5 = 7.0 mm
# Roller I (this version only): roller F turned round: the cams (and the 45 deg end rim step) are mirrored, so the
# chamfer of every cam is on the bearing (-x) side and the steep face on the motor side. Journal and TT motor end
# as F. It prints standing on the journal end, so all chamfers face down; the end face around the journal needs
# support from the plate: use the tree support of the slicer (see README.md).
P.ROLLERS["I"] = dict(P.ROLLERS["F"], chamfer="-x",
                      label=P.ROLLERS["F"]["label"] + ", cams turned round")

VARIANTS = ["D", "E", "F", "G", "H", "I"]   # the cam rollers; any key of P.ROLLERS works
DEFAULT = "F"
