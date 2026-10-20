# TT motor control (ESP32 + L298N)

Run the TT gear motor of the [80 mm test version](../../CAD_design/TT-motor/README.md) from the PC, with variable
speed. A web page sends the speed over USB to an ESP32; the ESP32 drives the motor through an L298N. Next to the
controls, the page shows the CAD model with the roller turning at the estimated speed.

| Folder / file | Contents |
| --- | --- |
| `connections.txt` | wiring as built |
| `firmware/tt_motor/tt_motor.ino` | ESP32 sketch (Arduino core esp32 3.x) |
| `app/index.html` | control page with 3D view (Chrome or Edge, Web Serial) |
| `app/server.js`, `app/start.bat` | small local web server (Node.js, no packages) |
| `app/seeding.html` | spot seeding sync: the overseeder animation drives the real motor |
| `app/seeding/` | `timeline.json` and `frames/` from the overseeder animation, `export_seeding.py` |
| `app/models/*.stl` | parts in assembly position (frame of `build_ovt.py`: x along the roller, y forward, z up, origin = roller axis) |

## Wiring

| ESP32 | L298N | Note |
| --- | --- | --- |
| GPIO2 | IN1 | channel A (OUT1/OUT2); GPIO2 is also the blue LED on most boards |
| GPIO14 | IN2 | channel A |
| GPIO15 | IN3 | channel B (OUT3/OUT4) |
| GPIO13 | IN4 | channel B |
| GND | GND | common ground, needed |
| 5V | 5V | see below |

- Keep the **ENA and ENB jumpers on**. The speed is PWM (1 kHz) on IN1/IN2 (or IN3/IN4).
- Put the TT motor on **OUT1/OUT2** (channel A). If it is on OUT3/OUT4, choose channel B on the page.
- **5V to 5V**: with its 5V jumper on, the L298N makes 5 V from its own supply and feeds the ESP32 through this
  wire. With USB also connected, the two 5 V sources are joined. Most boards have a diode on USB, so it usually
  works, but it is safer to remove the 5V–5V wire while the ESP32 is on USB. Keep GND connected.
- A TT motor is rated 3 … 6 V. The L298N drops about 2 V, so with a 7 … 8 V supply 100 % gives about 5 … 6 V on
  the motor. With a higher supply, keep the duty lower.

## Flash the firmware

The board is an ESP32-D0WD-V3 with a CH340 USB chip (COM3 on this PC).

1. Arduino IDE 2: open `firmware/tt_motor/tt_motor.ino`, board **ESP32 Dev Module**, port **COM3**, Upload.
2. Or from the command line:

```bash
arduino-cli compile --upload -p COM3 --fqbn esp32:esp32:esp32 firmware/tt_motor
```

## Run the program

1. Close the Arduino serial monitor (only one program can use COM3).
2. Double-click `app/start.bat`, or run `node server.js` in `app/` and open <http://localhost:8080> in Chrome or Edge.
3. Click **Connect ESP32** and choose the CH340 port (COM3).
4. Move the slider. Space = stop, arrow up/down = ±5 %.

| Control | What it does |
| --- | --- |
| Speed −100 … +100 % | PWM duty; + = top of the roller moves forward (towards the rim), the correct seeding direction |
| Reverse motor direction | tick it if the roller turns the wrong way (instead of swapping the motor wires) |
| Ramp | how fast the duty changes (%/s), so the gears get no shock |
| Start kick | full power for a short time when starting from standstill, so the motor starts at low duty |
| Roller, rpm at 100 %, dead band | model for the 3D view and the rpm and g/min estimate |

The 3D view follows the duty that the ESP32 reports back. Without a connection it simulates the slider.

## Spot seeding sync

`seeding.html` (link at the top of the control page) plays the animation of the
[overseeder with Cambridge roll](../../../aanbouwdelen/overseeding/overseeder%20with%20cambridge%20roll/README.md)
on the robot in real time. Whenever the seeder motor in the animation is on, the TT motor runs; on full grass it
stops. So the mini hopper shows in real life what the seeder does in the field.

| | |
| --- | --- |
| Run | 45 s: pass north, headland turn, pass south; 6 bare patches, the motor is on about 6 s in total |
| Mini roller speed | follows the robot speed: `rpm at 0.5 m/s` × v / 0.5 (default 28 rpm, roller F at 35 g/m²) |
| rpm → duty | dead band + rpm / (TT rpm at 100 %) × (100 − dead band); use the values you measured |
| Timeline bar | green = motor on; click to jump |
| Loop | on: the run starts again, so the robot keeps driving passes |
| Speed | 0.5 ×, 1 × (real time), 2 ×; the caption in the frames says "2 x speed" because the GIF plays at 2 × |

The motor state comes from the same process model as the animation (`osr_ground.simulate()`): it includes the
motor start time and the fall time, so the motor starts before the patch reaches the drop line. The page sets a
fast ramp (1000 %/s) on the ESP32 for this reason.

To update after a change to the animation: render the GIF again (see that README), then run

```bash
"/c/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" code/TT-motor/app/seeding/export_seeding.py
```

## Safety: watchdog

The page resends the speed every 0.3 s. When the ESP32 gets no line for 1.5 s, it stops the motor. So the motor
stops when the page is closed, the PC sleeps or the USB cable comes out.

## Serial commands

115200 baud, one command per line. Usable from any serial terminal.

| Command | Meaning |
| --- | --- |
| `S <-100..100>` | speed in % duty, sign = direction |
| `C <A\|B>` | L298N channel of the motor (stops the motor) |
| `X` | stop now, no ramp |
| `R <%/s>` | ramp rate, default 200, 0 = off |
| `K <ms>` | start kick, default 60 ms, 0 = off |
| `?` | status |

Status line every 100 ms: `T <target %> <actual %> <channel> <kick 0/1>`.

## Calibrate the speed

The rpm in the page is an estimate: a DC motor has no speed feedback. Defaults: 200 rpm at 100 % (TT 1:48,
typical at 6 V) and a dead band of 15 %. To measure:

1. Put a tape flag on the shaft end at the back of the motor.
2. Set for example 50 %, count the turns in 60 s.
3. Find the lowest duty where the roller still turns under seed: that is the dead band.
4. Fill in **rpm at 100 %** so the page shows the measured rpm at 50 %.

Roller F needs about 28 rpm at 35 g/m² and 0.5 m/s ([CAD README](../../CAD_design/TT-motor/README.md)).

## Update the 3D models

`app/models/` is exported from `CAD_design/TT-motor/Overseeder_Mini_TT.FCStd` (body, motor plate, rim, TT motor,
shaft) and from `ovt_parts.roller(k)` (rollers D to I), in the assembly frame, not the print orientation. Export
them again after a change to the CAD (with FreeCAD 1.1):

```bash
"/c/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" code/TT-motor/app/models/export_assembly.py
```
