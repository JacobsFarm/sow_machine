# Overseeder, mini drop seeder for 3D printing: why it is built like this

## A test rig, not a smaller machine

The g per revolution of a fluted roller depends on the seed (size, chaff, density) and on how well the flutes fill,
and that can only be measured. A 150 mm piece of the metering, with the **same flute (6 × 5 mm)** as the 1 m roller,
gives the calibration factor for the big roller for about € 8 of filament. Per mm of roller it carries 0.095 g per
revolution against 0.101 g on the Ø50 roller. The flute volume per length is nearly the same. The difference comes
from the closed 3 mm ends (143 of 150 mm fluted), and from `ovm_calc` taking the real flute section under the Ø40 arc
(29.6 mm²), where `ovd_calc` takes 6 × 5 = 30 mm². Use the factor on the flute volume, not on the g per mm.

## Roller variants A to H

The research (`../../research/README.md`) expects helical round-bottom flutes at 20 … 40 rpm to meter ryegrass more
evenly than straight rectangular flutes at 10 rpm, and cams to suit chaffy mixtures. That can only be settled by
catch tests, so the rig takes eight rollers with the same outside, journal and D socket. Only the metering surface
differs, and the rest of the rig (rim, gaps, motor) stays the same for all of them.

- **A stays the default**: it has the flute of the 1 m roller, so its catch test calibrates that roller.
- **B, 14 flutes R 3, 10° lead**: the DEM optimum (14 flutes, 10°) with the round bottom proposed for ryegrass.
  It carries 0.55× the volume of A and runs at 20 rpm at the normal rate, just inside the even range. With 10° over
  143 mm the flute turns 72° around, so each flute spans 2.8 flute pitches. There is always flute under the rim and
  the outflow has no pulses.
- **C, R 2**: the same helix with a smaller section (0.25× A, 45 rpm at 35 g/m²). It is meant for small seed and low
  rates. Clover at 3 … 5 g/m² (at the grass bulk density) runs at about 1 … 1.6 rpm on A and at 4 … 6.5 rpm on C:
  4× better, but still below 20 rpm. For the small-seed compartment the research proposes a shorter active length
  as well. The catch test shows whether C at a few rpm is even enough.
- **D to H, cam rollers** (the ring rollers of Zocon / APV in `../../inspiration/`): rectangular cams in rings, every
  second ring turned half a pitch around (brick pattern), so seed cannot run straight through between them. A
  series from coarse to very fine, because the photos show the makers do the same: one roller per seed group, not
  one adjustable roller.

  | Variant | Cam (along × around × high) | Rings × cams | Core | For |
  | --- | --- | --- | --- | --- |
  | D | 6.5 × 9 × 5 | 12 × 6 | Ø30 | chaffy seed, mixtures with coarse parts |
  | E | 6 × 7 × 4 | 14 × 8 | Ø32 | grass mixtures |
  | F | 5 × 6 × 3 | 17 × 10 | Ø34 | ryegrass |
  | G | 4 × 5 × 2.5 | 21 × 12 | Ø35 | ryegrass at low rates, fine grasses |
  | H | 4 × 4 × 1.5 | 25 × 16 | Ø37 | clover and small seed |

  The cam tips make the same Ø40 as the other rollers, so the rim gap and back gap stay valid. The ring pitch is
  at least cam length + height, so the 45° chamfers of neighbouring rings never touch: each cam is its own simple
  block, which in steel is a milled ring on a shaft.
- **Geometry of a helical flute**: a circle of the flute radius, square to the flute, swept (Frenet) along a helix
  through the roller surface, then cut off square to the axis 3 mm from the ends. The cross-section normal to the
  flute is then exactly the stated semicircle (less the small part outside the Ø40 arc). The volume is
  lens area × length / cos(lead), checked against the solid within 0.1 %.
- **Printing standing**: a helical flute leans only 10° from vertical, and its closed top end bridges 2 R (6 / 4 mm)
  like the 6 mm flutes of A. Horizontal cam undersides and the top rim step of D to H would be 1.5 … 5 mm overhangs,
  so they slope 45° towards the motor end, which is down when printed. The rim at the motor end needs no slope.
- **STL resolution**: the swept faces mesh to 11 … 14 MB at 0.02 mm. At 0.05 mm / 0.2 rad they are about 3 MB and
  the volume changes by 0.1 %, far below what a 0.4 mm nozzle resolves.

## Printable without support

- The hopper is one profile (housing walls, sloping walls, rim block, screw columns, flange) extruded along the
  roller. Printed standing on its left end wall, all walls are vertical: no support, no overhang, and the layer lines
  run along the seed flow, so seed slides down smoothly.
- The right end is open so the roller and the rim go in from the side; the motor plate closes it.
- The roller stands on its motor end; the flutes stop 3 mm before the ends (a 6 mm bridge at the top) so no seed runs
  out through the 0.5 mm end gap.
- Every part fits the Bambu Lab A1 bed of 256 × 256 × 256 mm (`build_ovm.check_fit()`); the tallest are the body
  (153 mm) and the rollers (152 mm).

## Sizes

- **Walls 2.4 mm** (6 perimeters at 0.4): solid, seed-tight and stiff enough for 0.3 kg of seed.
- **Walls 26° from vertical**: lawn seed slides at a wall angle up to about 45° from horizontal; 64° from horizontal
  leaves a margin for chaffy mixtures.
- **Back gap 0.8 mm**: the roller moves up on the back, so seed is carried out of the gap, never pulled into it.
- **Front gap 6 mm, closed by a rigid cut-off rim** at the height of the axis: a flat PETG strip 3 mm thick in a
  slot, its square tip **0.5 mm** from the Ø40 of the roller. It strips off the seed that lies on the roller between
  the flutes or cams, and the flutes or cells carry their contents down past it. No brush and no TPU: the rim never
  touches the roller, so there is no wear, no lip pressure and nothing to adjust. The 0.5 mm comes from the
  literature range for small seed (0.25 … 0.5 mm; wheat about 2 mm, `../../research/cam_roller_shape_and_sealing.md`).
  If seed is crushed or trickles, print a rim with another `rim_gap`: 3 g of filament. In steel the rim is a sawn
  flat bar.
- **Ø8 journal** in a printed hole on the left, the motor shaft carries the right end: the roller weighs 95 … 122 g,
  the stepper bearings take that easily, and there is no second bearing to align.

## NEMA 17, not a 28BYJ-48

The 28BYJ-48 is cheaper and smaller, but its 0.03 Nm is less than the estimated peak of 0.032 Nm when a seed is pinched
at the rigid rim (`ovm_calc.torque()`), and it reaches only about 15 rpm. A NEMA 17 (which most people with a printer
have lying around) gives 0.25 Nm usable, margin 7.8, directly on the roller without a gearbox. As a stepper it also gives
the exact number of revolutions for the catch test and holds the roller still when stopped (no trickle).
The 6 mm motor plate takes the M3 button heads in counterbores, so they stay clear of the roller end.

## Mounting

Two M10 holes at 50 mm in a flange at the back top fit the hole grid of the robot beams or a board on a test
stand. The rig then hangs with the bottom of the roller about where the big seeder has it.
