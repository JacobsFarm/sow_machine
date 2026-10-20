# CAD design

Two versions of the mini seed hopper. Each has its own folder with the model, STL files, previews and scripts.

| Folder | Version | Drive | Width |
| --- | --- | --- | --- |
| [stepper_motor/](stepper_motor/README.md) | Base design, with eight exchangeable rollers | NEMA 17 stepper | 150 mm |
| [TT-motor/](TT-motor/README.md) | Small, cheap test version | TT gear motor | 80 mm |

The TT-motor scripts (`ovt_*.py`) import the dimensions and shared parts (rim, lid, tray) from
`stepper_motor/ovm_*.py`. Change shared dimensions in `stepper_motor/` and rebuild both versions.
