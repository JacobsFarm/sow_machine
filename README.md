# Mini seed hopper for grass seed

A project to build a mini hopper for grass seed: a small, 3D-printable version of the drop seeder that you can
mount on the field robot or use on its own to test the metering roller. The roller is 150 mm long inside the
hopper and exchangeable: three fluted rollers and five cam rollers, with a fixed cut-off rim (no brush). A smaller
80 mm test version with a cheap TT gear motor is in `CAD_design/TT-motor/`.

## Repository layout

| Folder | Contents |
| --- | --- |
| [CAD_design/stepper_motor/](CAD_design/stepper_motor/README.md) | FreeCAD design of the mini hopper (FCStd, STEP, STL, scripts, previews) |
| [CAD_design/TT-motor/](CAD_design/TT-motor/README.md) | A small test version (80 mm wide, 120 mm high, two M8 × 100 bolts) with a TT gear motor, for short tests |
| [research/](research/README.md) | Research into the best way to meter grass seed (and herb mixtures), cam rollers and sealing |
| [inspiration/](inspiration/) | Photos of commercial cam rollers and seed boxes |

## Printing on a Bambu Lab A1

All parts are designed to print **without support** on a Bambu Lab A1 (only test roller I needs tree support
under its end face). The A1 has a build volume of
256 × 256 × 256 mm; the largest parts fit easily. There are two complete sets; print one of them.

### Base design: 150 mm, NEMA 17 (`CAD_design/stepper_motor/stl/`)

| Part | STL | Size (mm) | Material |
| --- | --- | --- | --- |
| Hopper body | `CAD_design/stepper_motor/stl/ovm_body.stl` | 133 × 164 × 153 | PETG |
| Motor plate | `CAD_design/stepper_motor/stl/ovm_motor_plate.stl` | 133 × 134 × 6 | PETG |
| Roller A (default, fluted) | `CAD_design/stepper_motor/stl/ovm_roller.stl` | 40 × 40 × 152 | PETG |
| Rollers B, C (helical flutes) and D to H (cam rollers) | `CAD_design/stepper_motor/stl/ovm_roller_B.stl` … `_H` | 40 × 40 × 152 | PETG |
| Cut-off rim | `CAD_design/stepper_motor/stl/ovm_rim.stl` | 150 × 10 × 3 | PETG |
| Lid | `CAD_design/stepper_motor/stl/ovm_lid.stl` | 159 × 130 × 5 | PETG |
| Catch tray | `CAD_design/stepper_motor/stl/ovm_tray.stl` | 170 × 85 × 40 | PETG |

### Test version: 80 mm, TT gear motor (`CAD_design/TT-motor/stl/`)

| Part | STL | Size (mm) | Material |
| --- | --- | --- | --- |
| Hopper body (2 M8 bolt tubes, no flange, no M3 columns) | `CAD_design/TT-motor/stl/ovt_body.stl` | 120 × 117 × 84 | PETG |
| Motor plate (TT motor, roller bearing) | `CAD_design/TT-motor/stl/ovt_motor_plate.stl` | 120 × 117 × 4 | PETG |
| Cam roller F (default) | `CAD_design/TT-motor/stl/ovt_roller_F.stl` | 40 × 40 × 86 | PETG |
| Cam rollers D, E, G, H | `CAD_design/TT-motor/stl/ovt_roller_D.stl`, `_E`, `_G`, `_H` | 40 × 40 × 86 | PETG |
| Cam roller I (F with the cams turned round; tree support under its end face) | `CAD_design/TT-motor/stl/ovt_roller_I.stl` | 40 × 40 × 86 | PETG |
| Cut-off rim | `CAD_design/TT-motor/stl/ovt_rim.stl` | 80 × 10 × 3 | PETG |
| Lid | `CAD_design/TT-motor/stl/ovt_lid.stl` | 88 × 117 × 5 | PETG |
| Catch tray | `CAD_design/TT-motor/stl/ovt_tray.stl` | 100 × 85 × 40 | PETG |

The parts of the two sets do not fit each other: use the `ovm_` files together, or the `ovt_` files together.
Bought parts for the test version: TT gear motor 1:48, 2 × M8 × 100 with 4 washers and 2 nuts, 2 × M3 × 25
socket head with 2 M3 nuts (see [CAD_design/TT-motor/README.md](CAD_design/TT-motor/README.md)).

**Steps in Bambu Studio:**

1. Import the STL files. They are already in the correct print orientation, so do not rotate them.
2. Use a **0.4 mm nozzle** and a **Textured PEI Plate** (the standard plate for PETG).
3. Settings: layer height **0.2 mm**, **6 walls**, **20 % infill**. With 6 walls the 2.4 mm thick walls are
   fully solid and seed-tight.
4. Material: **PETG for all parts**, including the cut-off rim. The A1 has an open frame, so do not use ABS or ASA
   (they can warp).

The bill of materials and the print overview are in [CAD_design/stepper_motor/README.md](CAD_design/stepper_motor/README.md) (base) and
[CAD_design/TT-motor/README.md](CAD_design/TT-motor/README.md) (test version).
