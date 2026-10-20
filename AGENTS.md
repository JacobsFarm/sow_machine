# Agents: project rules

These rules apply to every AI agent working in this repository. They take precedence over personal preferences.

## Project

Mini seed metering hopper (drop seeder) for grass seed: a small, 3D-printable version of the seeder for the
field robot. See [README.md](README.md) for an overview and [CAD_design/stepper_motor/README.md](CAD_design/stepper_motor/README.md) for the
design.

## Hard rules

1. **Never commit.** Do not create a git commit, push, branch or merge unless the user explicitly asks for it in
   the chat message. Leave changes in the working tree.
2. **Printable in PETG.** Every part must be printable in PETG. No TPU or other material, including for the
   wiper lip. Design wall thickness and shape so PETG prints them well.
3. **Printable on a Bambu Lab A1.** Build volume is 256 × 256 × 256 mm. Every part must print without support
   or with minimal support, and must fit inside the build volume. Watch overhangs (max. about 45°) and keep walls
   thin enough to fill properly.
4. **Design as if it will be made in metal.** Model parts so they can be reproduced in iron or steel by milling,
   sawing or welding. That means realistic dimensions, simple geometry and no unnecessary detail.
5. **No unnecessary rounded corners.** Use rounded corners only where they have a function (for example, seed
   that must not get stuck, or a smooth roller transition). Otherwise use sharp corners or a simple chamfer.
6. **Simple and robust, but working.** Choose the simplest solution that works. No unnecessary parts and no
   fancy mechanisms, but design for strength and seed tightness.

## CAD: FreeCAD 1.1 via MCP

- Use the **FreeCAD 1.1 MCP connection** (the `mcp__freecad__*` tools) for all CAD work. It is the first choice;
  do not use a separate script outside FreeCAD.
- The existing scripts in [CAD_design/stepper_motor/](CAD_design/stepper_motor/) (`ovm_params.py`, `ovm_parts.py`, `build_ovm.py`) remain the
  source of dimensions. Change dimensions there and rebuild the model in FreeCAD.
- After every change, export the STL files to `CAD_design/<version>/stl/` and keep the previews in `CAD_design/<version>/previews/`
  up to date.
- After every change, check that all parts fit inside the A1 build volume.

## Print settings (Bambu Studio, Bambu Lab A1)

- Nozzle 0.4 mm, layer height 0.2 mm, 6 walls, 20 % infill.
- Bed: Textured PEI Plate.
- Material: PETG for all parts. Do not use ABS or ASA (the A1 is an open frame and they can warp).
- Parts are already in print orientation. Do not rotate them without a reason.

## Open points

- The TPU wiper lip is replaced by a rigid PETG cut-off rim with a 0.5 mm gap (no brush). Test on the printer
  whether 0.5 mm crushes seed or lets seed run through; change `rim_gap` if needed.

## Documentation

- Write all documentation (README files, notes, file names) in English.
- Keep dimensions and materials in the README files up to date with the CAD source.
- Use short, clear sentences and tables for dimensions.
