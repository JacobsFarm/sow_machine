# Cam (studded) roller: how makers do it, best shape, and sealing

Follow-up to [README.md](README.md) §2 and variant D in the test plan. Question: how do manufacturers build the cam
roller (German *Nockenrad*, "stud roller", "peg roller"), which shape is best for grass seed, and how is the
roller sealed against seed leaking past it?

Compiled 19 October 2026. Web research found **little hard geometry**: makers do not publish tooth or stud
dimensions. Statements marked *[judgement]* are engineering reasoning, not sourced. They must be checked on the
mini rig.

## 1. Short answer

1. A **cam / stud roller is not the best shape for ryegrass.** For free-flowing grass seed the helical fluted
   roller (variants B, C) stays the first choice. The cam roller is the right tool for **coarse, chaffy or mixed
   seed** (cocksfoot, brome, unhulled sainfoin, burnet) and for mixtures with large and small seeds.
2. If a cam roller is built, use **low, wide, round-tipped studs in staggered rows** (not tall sharp pins), with
   a **row pitch that is not a multiple of the seed length**. Stud height about 1.5 to 2 × the seed width for
   the bulk seed, so the roller picks up a layer, not a heap *[judgement]*.
3. **Sealing decides the accuracy more than the roller shape.** Three leaks matter: past the outlet edge (cut-off
   gap), past the roller ends (end seals) and after the motor stops (trickle). In PETG the practical answer is a
   **rigid cut-off edge with a small, fixed gap plus a bought brush strip**, and **a labyrinth of closed roller
   ends in a close-fit bore**.

## 2. How makers do it

| Maker / source | What they use | Take-away |
| --- | --- | --- |
| European drills in general (DEULA, course notes): *stud type roller*, "widely used in European design seed drills", studs around the circumference, rate set by a multi-speed gearbox [1][2] | Stud roller + gearbox | Studs are the classic European answer to a wide range of rates and seed sizes. |
| Maschio Gaspardo in-line drills: interchangeable rollers from fine grass to cereals, **a small peg roller recommended for small seeds** [3] | Peg roller changed per seed size | The roller is swapped per seed group, not made adjustable. |
| Einböck, APV: **fine and coarse toothed rollers**, one segment per hose; APV also **flex rollers** with flexible cell edges for mixes of large and small seed [see step 2 dossier, Part B2] | Teeth/cells, rubber edges | Rubber-edged cells avoid crushing and blocking. Not possible in PETG. |
| Vredo overseeders: "cam wheel" in a pneumatic hopper that keeps the roller well filled, also on slopes (step 2 dossier, B1) | Cam wheel | A full, well-fed roller matters more than the stud shape. |
| Truax FLEXII grass drills: **separate small-seed and fluffy-seed boxes, metal row dividers keep the seed in contact with the metering wheels** [4] | Picker wheels + dividers | For fluffy seed the contact with the wheel is the problem, not the wheel. |
| Old Kverneland/Accord-type and combined coarse/fine wheels (patents): a **coarse wheel with slanted ribs, alternately high and low**, on one shaft with a fine wheel [5] | Slanted, alternating-height ribs | Slanted and staggered ribs smooth the pulse. This is the same idea as the helical flute. |
| Pin-roller DEM study (wheat and fertilizer): **16 lines of 4 pins** was optimal; simulated CV about **37 %** against **96 %** for a 12-flute roller [6] | Pin roller | Pins can beat flutes at **low rotation speed and high dose**. Simulation only, other seed, and the CV values are high in absolute terms. |

Reading across these: the cam / stud / peg roller is chosen for **range and robustness**, not for the lowest CV.
The studies that measure evenness well (helical flutes at 20 to 40 rpm, see README §2) are about fluted rollers.

## 3. Which shape is best

| Question | Finding | Basis |
| --- | --- | --- |
| Studs or flutes for ryegrass? | Flutes (helical, round bottom). Studs fill less predictably with elongated seed. | README §2, [6] vs. [7] |
| Studs for chaffy or mixed seed? | Yes. Studs push seed over the edge instead of relying on a pocket that chaff cannot fill. | [3][4], step 2 dossier |
| Number of rows | Many narrow rows, staggered, so the dose is spread over the turn. The pin study found number of lines and pins per line the main factors, with 16 lines × 4 pins optimal [6]. | [6] |
| Stud height | Low for small seed (shallower, more ridges), higher for large seed. A patent states the same for flutes: deeper and fewer for large seed, shallower and more for small seed [8]. | [8] |
| Stud tip | Rounded or flat top with a **chamfer**. A sharp pin damages seed and pricks into the cut-off. In steel a 45° chamfer is simple to mill. | *[judgement]* |
| Stud flank | Slanted, not radial: the seed slides off instead of jamming at the root. | *[judgement]*, as the slanted ribs in [5] |
| Free-flowing small seed (clover, timothy) | Runs past the studs [see DEULA note, README §2]. Do not use a stud roller for these. | README §2 |

### Proposed variant D2 (not built yet)

| Parameter | Value | Why |
| --- | --- | --- |
| Roller Ø | 40 mm (as A to D) | Same journal, D socket and housing. |
| Rows | 16 around the circumference | From [6]. |
| Studs per row | 4 over 113 mm, staggered by half a pitch per row | Spreads the dose; from [6] scaled to the active length. |
| Stud | 6 wide (along the axis) × 4 long × 3 high, 1 mm chamfer on top | Low profile for ryegrass-size seed (about 6 mm long, 1.5 mm wide). |
| Ends | closed 3 mm each end (as now) | End seal, see §4. |

Filament about the same as variant D (82 to 97 g). Change `ROLLERS` in `ovm_params.py` only after the test of
variant D shows the stud principle works with your seed.

## 4. Sealing

### 4.1 Where seed escapes

| Leak | Cause | Effect |
| --- | --- | --- |
| A. At the **cut-off edge** under the roller | gap between roller and the lip/flap too large, or seed wedged in it | Extra seed per turn, uneven. Too small a gap crushes seed. |
| B. At the **roller ends** | gap between the roller and the end walls | Seed grinds in the gap, adds friction and a rate error. Grass seed is light, but it gets in. |
| C. After **stopping** | seed trickles out of open flutes/gaps | Seed on the ground when the robot stops. |

### 4.2 What is known

- **Cut-off gap by seed size** (patent text [9]): about 0.25 to 0.5 mm (0.01 to 0.02 in) for small seed such as kale
  or mustard, about 2 mm (0.08 in) for wheat or barley. A smooth roller surface helps avoid carry-through of fine
  seed. Grass seed is between the two, so start at **0.5 mm** for ryegrass and test.
- **A fluted meter has three parts:** roller, sliding cut-off and adjustable flap. The flap position sets the
  gap for seed size and can open fully for cleaning [10]. In the mini rig the gap is fixed, which is fine for one
  seed, but it should be easy to change (see 4.3).
- **End sealing in industry**: the roller runs through a **rotary sealing ring** whose opening matches the
  flute profile, so it seals against the side wall without rubbing. Dust gets out through notches in the outer
  ring [11]. Older patent: roller and slider must seal very well against the side plates, otherwise seed leaks
  under hopper pressure and grinds [12].
- **Wear** opens the cut-off gap and makes the rate drop below calibration [13] (vendor source). A printed PETG
  edge wears and creeps: re-check the gap now and then.
- **Brush**: Einböck, patents and the helical roller study use a brush to strip excess seed off the roller and as a
  seal [see step 2 dossier, B2, and 14]. A brush gives way to a seed in the flute instead of crushing it.

### 4.3 Recommendation for the mini rig (PETG, Bambu A1)

**Built (19 October 2026):** the rig now uses the rigid rim **without a brush** (simplest), gap 0.5 mm, with five
cam rollers D to H after the ring rollers in `../inspiration/`. See `../CAD_design/stepper_motor/README.md`. The table below
stays as the fallback if the rim alone trickles or crushes seed.

| Leak | Measure | Print and metal note |
| --- | --- | --- |
| A. cut-off edge | Rigid PETG edge in the housing (replaces the TPU lip) with a **0.5 mm gap**, plus a **bought bristle brush strip** behind it. Add a **second hole row or slot** so the lip can be moved 0 … 1 mm. | In steel: a bent plate. The brush is a stock part (nylon bristles in a strip); it is not printed, so the "PETG only" rule applies to the printed parts. Say so in the BOM. |
| B. roller ends | Keep the **3 mm closed ends** and make the bore a **running fit of 0.3 mm** per side. Add a **groove (labyrinth) of 1 × 1 mm** in the end wall. A ring of the same profile as the roller end, as in [11], is not needed at this scale. | Groove is a lathe cut in steel. |
| C. trickle after stop | Use the **brush** plus the **stepper hold torque** (the roller stays put). Optional: a slide plate under the outlet that closes when the robot is off. | Test with the brush first. |

Because the A1 prints at ±0.1 mm, the 0.5 mm gap is the tightest practical value. Print the roller and cut-off
edge in the orientation already used and measure the real gap with a feeler gauge before the first test.

## 5. Test plan additions

On top of the plan in [README.md](README.md) §4:

1. **Gap sweep**: 0.25 / 0.5 / 1.0 mm cut-off gap with roller B and ryegrass. Note g/rev and CV for each.
2. **Brush on/off** with the same gap: does the brush lower trickle after stop and the CV?
3. **End leak**: roller with and without the end groove. Weigh seed found at the roller ends after 50 revolutions.
4. **Cam roller D2** against D and B, with ryegrass and a chaffy mix (cocksfoot, 50 / 50). The cam roller is
   only worth keeping if it wins on the chaffy mix.

## 6. Not found / not verified

- No public stud or tooth dimensions for Vredo, Einböck, Gaspardo or APV rollers (they are in manuals and
  parts books).
- No independent study of **stud rollers with grass seed**. The pin-roller study [6] is a simulation on wheat and
  fertilizer, and its absolute CV is poor.
- No data on **brush vs. rigid lip** for grass seed. The gap values in [9] are from a patent text, not from
  tests with grass.
- Stud height, tip and flank rules in §3 marked *[judgement]* are not sourced.
- The Gaspardo leaflet and the ACIAR manual could only be read through search summaries, not in full.

## Sources

1. DEULA, *Sämaschinen*: https://www.deula.de/fileadmin/Redakteure/Stammsitz/extranet/600-699/616_-_i_-_1_-_B1_-_Saemaschinen.pdf
2. Seed metering devices (lecture slides, stud type roller): https://www.slideshare.net/slideshow/seed-metering-devices/249874473
3. Maschio Gaspardo, in-line direct seed drills leaflet (peg roller for small seed): https://www.maschiogaspardo.com/media/assets/upload/attachments/u0t6afxpw2/Leaflet%20SODO%2022%20(2025-05%5EW00227258R%5EEN).pdf
4. Truax FLEXII grass drill: https://www.truaxcomp.com/flexii-series-grass-drill/
5. Combined coarse and fine seed wheel, slanted ribs of alternating height (patent listing): https://agri.nais.net.cn/patentdetails/0ECA7E68-0469-4AA5-9693-0BACB356B8F8.html and https://patents.google.com/patent/DE837022C/en
6. Adilet et al., *Investigation of the pin-roller metering device and tube effect for wheat seeds and granular
   fertilizers based on DEM*, IJABE 16(2), 2023: https://ijabe.org/index.php/ijabe/article/view/7721
7. Güler (2005) and the DEM helical roller study, see [README.md](README.md) sources 3 and 4.
8. Variable geometry meter roller (patent): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9609804
9. Metering gaps by seed size and smooth roller surface: a patent text returned by the search; the exact patent
   was not identified (the search listed several, see also 12). Treat the numbers as indicative.
10. ACIAR, seed metering manual (fluted roller, sliding cut-off, adjustable flap, peg/studded roller): https://www.aciar.gov.au/sites/default/files/legacy/node/714/Part%203%20MN121.pdf
11. US 4928858, *Metering device for seed or fertilizer* (rotary sealing ring): https://patents.google.com/patent/US4928858A/en
12. US 4254897, *Seed and fertilizer metering mechanism for agricultural drilling machines*: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4254897
13. National Agro, fluted roller wear and seed slippage (vendor blog): https://nationalagro.com/blog/5-signs-your-seed-drills-fluted-rollers-need-replacement-before-the-season-peak
14. Helical fluted roller with seed-cleaning brush, see [README.md](README.md) source 4: https://www.mdpi.com/2077-0472/13/7/1400
