# =====================================================================
# Overseeder, mini drop seeder for 3D printing - parameters
# A 150 mm wide test version of the metering of the drop seeder (../ovd_params.py): a printed hopper with an
# exchangeable fluted or cam roller in the throat, a rigid PETG cut-off rim on the front (no brush, no lip
# pressure), a NEMA 17 stepper on a bolt-on end plate and a catch tray for the calibration. To find the g per
# revolution of a roller shape and seed before the 1 m roller is made, and to test the on/off behaviour of the
# camera control on a single 150 mm row.
#
# Local coordinates (not robot coordinates, the rig stands on its own): x = along the roller (+x = motor side),
# y = forward (the top of the roller moves to +y, the front side moves down past the lip), z = up;
# origin = the roller axis. All parts are printable without support in the orientation given per part
# (see PRINT below).
# =====================================================================
import math

# ---------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------
bed = (256.0, 256.0, 256.0)     # Bambu Lab A1; every part must fit
nozzle = 0.4
wall = 2.4                      # 6 perimeters: seed-tight and stiff without infill
clear = 0.2                     # radial clearance of printed fits (hole = part + 2 * clear)
petg = 1.27e-3                  # g/mm3, PETG for every part
infill_eff = 0.55               # printed mass / solid mass at 6 perimeters and 20 % infill (estimated)
filament_eur_kg = 22.0

# ---------------------------------------------------------------------
# Roller: fluted, printed standing on its motor end. Flutes closed 3 mm before each end, so no seed runs out
# along the end gap.
# ---------------------------------------------------------------------
width = 150.0                   # inside width of the hopper = working width (roller 149 long)
roller_d = 40.0
roller_end_gap = 0.5            # each end to the end wall
roller_x = (-width / 2.0 + roller_end_gap, width / 2.0 - roller_end_gap)
flutes = 12
flute = (6.0, 5.0)              # width, depth: the same flute as the 1 m roller, so the catch test calibrates it
flute_end = 3.0                 # closed rim at each end
roller_fill = 0.8               # filling of the flutes (estimated, as ovd)

# Roller variants for the comparison on the rig (test plan in ../research/README.md section 4 and
# ../research/cam_roller_shape_and_sealing.md). All Ø40 x 149 with the same journal and D socket; flutes or cams
# end flute_end before each roller end. A is the default (the flute of the 1 m roller). 'lead' = angle of the flute
# to the roller axis; a helical flute is a circle of 'radius' (normal to the flute) swept along a helix through the
# roller surface, so the bottom is a semicircle.
# Cam rollers D to H (Nockenwalze, as the Zocon / APV ring rollers in ../inspiration/): rectangular cams
# 'stud' = (along x, around, radial height) on a core of Ø40 - 2 x height, 'rows' rings over the cam length,
# every second ring turned half a pitch around (brick pattern). From coarse (D, few tall cams: chaffy seed and
# mixtures) to very fine (H, many low cams: small seed). The row pitch is at least cam length + height, so the
# 45 deg chamfers of neighbouring rings do not overlap. The +x face of each cam and the -x end rim slope 45 deg,
# so the roller prints standing on its motor end without support. fill = filling of the cells (estimated: cams
# drag the seed rather than carry it in a closed pocket).
ROLLERS = {
    "A": {"kind": "straight", "flutes": flutes, "flute": flute, "fill": roller_fill,
          "label": "12 straight flutes 6 x 5"},
    "B": {"kind": "helical", "flutes": 14, "radius": 3.0, "lead": 10.0, "fill": roller_fill,
          "label": "14 helical flutes R3, 10 deg"},
    "C": {"kind": "helical", "flutes": 14, "radius": 2.0, "lead": 10.0, "fill": roller_fill,
          "label": "14 helical flutes R2, 10 deg"},
    "D": {"kind": "studs", "stud": (6.5, 9.0, 5.0), "around": 6, "rows": 12, "fill": 0.5,
          "label": "cams 6.5 x 9 x 5, 12 rings of 6 (coarse)"},
    "E": {"kind": "studs", "stud": (6.0, 7.0, 4.0), "around": 8, "rows": 14, "fill": 0.6,
          "label": "cams 6 x 7 x 4, 14 rings of 8"},
    "F": {"kind": "studs", "stud": (5.0, 6.0, 3.0), "around": 10, "rows": 17, "fill": 0.6,
          "label": "cams 5 x 6 x 3, 17 rings of 10"},
    "G": {"kind": "studs", "stud": (4.0, 5.0, 2.5), "around": 12, "rows": 21, "fill": 0.6,
          "label": "cams 4 x 5 x 2.5, 21 rings of 12 (fine)"},
    "H": {"kind": "studs", "stud": (4.0, 4.0, 1.5), "around": 16, "rows": 25, "fill": 0.6,
          "label": "cams 4 x 4 x 1.5, 25 rings of 16 (very fine)"},
}
ROLLER_DEFAULT = "A"
journal = (8.0, 3.0)            # left journal diameter, length (runs in a hole in the end wall)
d_socket = (5.0, 4.5, 22.0)     # motor side: D socket for the stepper shaft (diameter, across the flat, depth)

# ---------------------------------------------------------------------
# Hopper (body): one print, standing on its left end wall, every wall is then vertical. The right end is open
# for the roller and the lip and is closed by the motor plate.
# ---------------------------------------------------------------------
end_t = 3.0                     # left end wall
motor_plate_t = 6.0             # motor plate: the M3 heads of the motor sit in counterbores on its inner face
counterbore = (6.5, 3.2)        # for ISO 7380 button heads (1.65 high)
back_gap = 0.8                  # back housing wall to the roller (roller moves up here: no seed is wedged)
front_gap = 6.0                 # front housing wall to the roller, closed by the cut-off rim
y_back = -(roller_d / 2.0 + back_gap)          # inner face of the back housing wall
y_front = roller_d / 2.0 + front_gap           # inner face of the front housing wall
z_bottom = -14.0                # bottom of the housing walls (roller bottom at -20, as ovd: walls to about the axis)
z_throat = 28.0                 # knee: housing walls -> sloping walls (8 mm above the roller)
z_top = 108.0                   # top of the hopper
top_back = -60.0                # inner face at the top
top_front = 65.0
screw_columns = True            # False: no M3 columns (tt_motor/ clamps the plate with 2 M8 through-bolts)
boss_d = 7.0                    # 4 screw columns along x for the motor plate (M3 self-tapping, pilot 2.5)
boss_pilot = (2.5, 12.0)
boss_z_low = (-8.0, -10.0)      # back, front
boss_z_high = 98.0
screw_hole = 3.4
plate_bottom = -25.0             # the end plates reach below the housing for the lower motor screws

# Cut-off rim: a rigid PETG strip in a slot in the front housing wall at the axis height. It does not touch the
# roller: a fixed gap stops seed lying on the roller between the flutes / cams, without a brush or lip pressure.
# A strip with another gap is a cheap reprint (in steel: a flat bar). Gap 0.5 mm for ryegrass (literature
# 0.25 - 0.5 mm for small seed, about 2 mm for wheat: ../research/cam_roller_shape_and_sealing.md section 4).
rim_t = 3.0
rim_gap = 0.5                   # rim tip to the Ø40 of the roller
rim_slot = (rim_t + 2 * 0.1, 5.0)   # slot width (z, 0.1 clearance each side), depth into the wall (y)
rim_block = (8.0, 12.0)        # thickened front wall around the slot: thickness (y), height (z)
rim_x = (-width / 2.0 + 0.2, width / 2.0 - 0.2)

# Mounting flange at the back top: 2 x M10 at 50 mm (the hole grid of the robot beams, or a test board)
flange = True                   # False: no flange (tt_motor/ uses an M8 through-bolt instead)
flange_y = (-95.0, -61.5)
flange_z = (z_top - 6.0, z_top)
flange_holes_x = (-25.0, 25.0)
flange_hole_y = -80.0
flange_hole_d = 10.4

# Lid: plate with a short locating rim
lid_t = 2.0
lid_rim = (1.6, 3.0, 2.0)       # rim width, depth, inset from the inner face of the opening

# ---------------------------------------------------------------------
# Drive: NEMA 17 stepper (42 x 42 x 40, the motor of most 3D printers) directly on the roller, with a TMC2209 or
# A4988 driver. A 28BYJ-48 is cheaper but has no margin on the torque peak of a pinched seed (ovm_calc.torque).
# Shaft O5 with one flat (4.5 across), 24 long; 4 x M3 on a 31 mm square; centring boss O22 x 2 in the plate.
# ---------------------------------------------------------------------
stepper_body = (42.3, 40.0)     # square, length
stepper_holes = (31.0, 3.4)     # hole square, hole in the plate (M3 x 8 into the motor)
stepper_boss = (22.0, 2.0)      # centring boss diameter, height
stepper_shaft = (5.0, 4.5, 24.0)    # diameter, across the flat, length beyond the boss
stepper_connector = (16.0, 6.0, 12.0)   # width (y), height past the body (-z), length (x)
stepper_rpm_max = 60.0          # the flutes no longer fill above about 60 rpm (estimated); the motor can do more
stepper_torque = 0.25           # Nm usable at low speed (holding torque 0.40 Nm, 42 x 40 mm)
stepper_steps = 3200            # 200 full steps x 1/16 microstepping
stepper_kg = 0.28

# Catch tray for the calibration (under the roller)
tray_x = (-85.0, 85.0)
tray_y = (-40.0, 45.0)
tray_z = (-70.0, -30.0)
tray_t = 1.6

# ---------------------------------------------------------------------
# Seed and operation (ovm_calc), same seed values as the 1 m drop seeder
# ---------------------------------------------------------------------
seed_density = 0.35             # kg/l (estimated, 0.25 - 0.40)
seed_rate = 35.0                # g/m2
work_speed = 0.5                # m/s
calib_revs = 10                 # revolutions per catch test (fits the tray)
fall_h = 180.0                  # mm, drop height when the rig hangs at the height of the 1 m seeder
mu_journal = 0.3
seed_shear = 0.03               # Nm, seed cut or pinched between a flute edge or cam and the rigid rim (estimated
                                # peak; higher than with the TPU lip, the rim does not give way)


def wall_slope(top, knee):
    """tan of the angle from vertical of a sloping wall from the knee to the top."""
    return abs(top - knee) / (z_top - z_throat)


TAN_BACK = wall_slope(top_back, y_back)
TAN_FRONT = wall_slope(top_front, y_front)
ANGLE_BACK = math.degrees(math.atan(TAN_BACK))
ANGLE_FRONT = math.degrees(math.atan(TAN_FRONT))


def studded_span():
    """x range of the flutes or studs: flute_end in from each roller end."""
    return roller_x[0] + flute_end, roller_x[1] - flute_end


def stud_rows(v):
    """(x of the -x face of the tip, angle offset in degrees) of each row of studs of a stud variant: rows evenly
    over the studded length, every second row turned half a pitch around."""
    a, b = studded_span()
    pitch = (b - a) / v["rows"]
    tip = v["stud"][0]
    return [(a + (i + 0.5) * pitch - tip / 2.0, (i % 2) * 180.0 / v["around"]) for i in range(v["rows"])]
