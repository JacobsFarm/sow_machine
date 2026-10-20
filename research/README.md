# Research: the best way to meter grass seed and herb mixtures out of the hopper

Question: what roller shape (or other metering device) is best to dose seed from the hopper of the drop seeder
([../](../README.md)) and its printable test rig ([../CAD_design/](../CAD_design/stepper_motor/README.md)), for **perennial
ryegrass** and for **herb mixtures** (herbal leys, flower/herb lawn mixtures)?

Short answer:
1. **Perennial ryegrass**: a fluted roller is right, but with **helical (spiral) flutes with a round bottom**,
   more and smaller than now, so the roller runs at **20 … 40 rpm** at the normal rate instead of 10 rpm. That
   removes most of the pulsing of straight flutes. A brush strip instead of a stiff lip.
2. **Herb mixtures**: do not meter them with one roller out of one box. The seeds differ 100× in weight and 4× in
   bulk density, so they **segregate** in the hopper and one roller cannot dose them all well. Use **two
   compartments, each with its own roller and motor** (grass / small seeds), as grass drills do, and set the
   ratio in software. Chaffy parts (cocksfoot, unhulled sainfoin, burnet) need an **agitator** and a coarser
   roller (studs or picker wheel).
3. Test it on the mini rig: print 3 … 4 roller variants and measure the evenness (CV) per variant, at a full,
   half and quarter-full hopper.

## 1. What the seeds are like

Bulk density from the weight per bushel, thousand-seed weight (TSW) from seeds per pound of the Pennington forage
guide [1]; the values marked * are typical literature values, not verified here: weigh your own seed lot.

| Seed | TSW (g) | Bulk density (kg/l) | Flow class |
| --- | --- | --- | --- |
| Perennial ryegrass | 1.4 (diploid; tetraploid 3 … 4*) | 0.31 | elongated, hulled, flows fairly well |
| Tall fescue | 2.0 | 0.32 | as ryegrass |
| Cocksfoot (orchardgrass) | 1.1 | 0.18 | **chaffy**, bridges |
| Smooth brome | 3.4 | 0.18 | **chaffy**, bridges |
| Timothy | 0.39 | 0.58 | small, round, free flowing |
| Kentucky bluegrass | 0.31 | 0.27 | very small, a bit fluffy |
| White clover | 0.59 | 0.77 | small, round, smooth: **sinks through grass** |
| Red clover | 1.7 | 0.77 | as white clover |
| Birdsfoot trefoil | 1.2 | 0.77 | as clover |
| Chicory* | 1.2 … 1.5 | ≈ 0.5 | small, angular, flows well |
| Ribwort plantain* | 1.5 … 2 | ≈ 0.6 | glossy, slippery, flows very well |
| Yarrow* | 0.1 … 0.2 | ≈ 0.3 | tiny and light: needs a carrier or a very fine roller |
| Burnet (small)* | 5 … 8 | ≈ 0.3 | large, corky: coarse |
| Sainfoin, unhulled (pods)* | 15 … 25 | ≈ 0.3 | large, rough pods: coarse and chaffy; hulled seed flows well |

Conversions: 24 lb/bu × 0.4536 / 35.24 l = 0.31 kg/l; 330 000 seeds/lb → 453.6 g / 330 = 1.37 g per 1000.

What this means for the metering:
- Ryegrass and fescue have a low density (0.31 kg/l) and elongated seeds: a fluted roller fills well, but
  rectangular flutes can wedge a seed at the edge (the torque peak in `ovm_calc.torque()`).
- Clover, plantain and timothy are 2 … 2.5× denser and much smaller: in a box with ryegrass they **trickle down
  through the grass seed** whenever the box vibrates (the robot drives over a lawn). That is segregation; seed
  machine makers offer an agitator against it [6].
- Cocksfoot, brome and sainfoin pods are chaffy: they **bridge** above the throat. The classic study on fluffy
  grass seed [2] measured that the seeding rate of a standard grass seed box dropped by 99 % before three quarters
  of the seed was out; a semicircular box with an agitator and a picker wheel reduced the rate variation by 84 percentage points.

## 2. Metering devices compared

| Device | How it works | Good for | Weak points | For the Bruut |
| --- | --- | --- | --- | --- |
| **Straight fluted roller** (now: 12 × 6 × 5 rectangular) | flutes fill in the hopper and empty at the bottom | free-flowing seed, wide range of rates [3] | pulses (one dose per flute), rate drifts with hopper fill and with roller length in seed [4]; rectangular edges pinch seeds | works, but not the best |
| **Helical fluted roller** | flutes as a spiral: a flute empties gradually, the next one starts before the previous one is empty | the same seeds, more even | slightly more complex to make (no problem when printed) | **best for ryegrass** |
| **Studded / cam roller** (Nockenrad, "European" drills) | studs on the roller push seed over a lip; rate by speed | coarse and mixed seed; Vredo overseeders use a cam wheel with a flap [8] | free-flowing small seed can run past the cams [7]; less exact at very low rates | for the coarse compartment |
| **Cell roller** (APV-style rollers per seed size) | rows of small cells with a set volume | small seed at low rates (clover, mustard, phacelia, grass with a fine roller) [5] | a cell roller per seed group; chaffy seed does not fill cells | **best for the small-seed compartment** |
| **Picker wheel / brush + agitator** (Truax, Brillion fluffy box) | toothed wheel or brush pulls seed out of a slot, agitator keeps it moving | chaffy, fluffy native grass and mixtures [2][9] | less precise for small round seed | only when chaffy species are in the mix |
| **Air (pneumatic)** | roller doses into an air stream, outlets spread it | spreading over a width | needs a fan and hoses; the dose is still made by a roller | not needed for a 1 m drop seeder |

What the measurements say about fluted rollers:
- For small seed (alfalfa, close to clover), a flute diameter of **6 … 8 mm** gave the most even flow; the CV of the
  flow drops strongly with more roller length in seed and with more speed, recommended range **20 … 40 rpm** [3].
  CVs of 7 … 13 % are normal for alfalfa in fluted rollers [3].
- A DEM optimisation of a helical fluted roller found the lead (helix) angle and the number of flutes have more
  influence on evenness than speed; optimum around **14 flutes, 10° lead, ≈ 40 rpm** [4]. That is a simulation
  with grain, not grass, but it points the same way as the measurements.
- On a wheat flute roller the CV was 9 % at constant speed and 13 % at changing speed; a closed loop on a flow
  sensor brought it down to 7 … 11 % [10]. The Bruut already controls the roller speed from the driving speed, so
  the speed part is solved; the roller itself must stop pulsing.
- Makers solve "one roller for everything" with **exchangeable rollers per seed group** (APV: coarse roller for
  grass, fine roller for grass and mustard, fine-blind for phacelia, extra-fine for poppy [5]) and **separate boxes**
  for small and chaffy seed (Brillion: small seed box with fluted cups plus an agitator box for chaffy seed [9];
  Truax/Great Plains: a native grass box with agitator and picker wheels plus a small fluted box [2]).

## 3. Recommendation

### Perennial ryegrass (and fescue, festulolium, timothy)

A helical fluted roller, printed:
- **14 flutes, lead 10°, semicircular bottom R 3 … 4 mm** (Ø 6 … 8 mm): no sharp edges to pinch the seed, and
  easier to clean than rectangular flutes;
- flute volume so that the normal rate needs **20 … 40 rpm**. Now the 1 m roller does 101 g/rev and runs at 10 rpm at
  35 g/m² and 0.5 m/s, below the range where flow is even; with 14 semicircular flutes R 3 (14 × 14 mm² instead of
  12 × 30 mm²) it carries about 0.55× as much and runs at about 18 rpm, with R 2.5 (0.38×) at about 26 rpm;
- the flutes end before the roller ends (as the mini already does);
- a **brush strip** instead of the TPU lip: it wipes off seed between the flutes but gives way to a seed in a flute,
  which the 1 m seeder already has.

### Herb mixtures

The mixture parts behave too differently for one roller. Recommended:
1. **Two compartments with their own roller and stepper**, as on the simple slit seeder (`ovs`: 41 + 18 l):
   - grass compartment: the helical roller above;
   - small-seed compartment (clover, chicory, plantain, trefoil, yarrow): a **fine cell roller or a fine helical
     roller** (6 … 8 mm flutes, short active length), running at 20 … 40 rpm at the low rate of these species
     (2 … 5 kg/ha each in a herbal ley).
   The ratio is then set in the controller, not in the bag, and it no longer changes when the box vibrates.
2. **Chaffy parts** (cocksfoot, brome, unhulled sainfoin, burnet): either buy them hulled/cleaned, or give the
   grass compartment a **slow agitator** (a finger shaft at a few rpm just above the throat) and a **studded roller**.
   Do not run an agitator for free-flowing seed: it makes segregation worse instead of better.
3. **Very fine seed** (yarrow, wildflowers): mix it with a carrier (dry sand, or bran) so the volume is large
   enough to dose; supplier advice is 1 … 5 parts carrier to 1 part seed [11]. Calibrate with the carrier in it.
4. Keep the small-seed compartment **shallow and narrow** (little seed above the roller), so the fill level changes
   the rate as little as possible [2][10].

## 4. Test plan on the mini rig

The mini rig (`../CAD_design/stepper_motor/`) has an exchangeable roller, so roller variants are cheap to compare (≈ 75 g PETG
each). Proposed variants, all Ø40 × 119:

| Variant | Flutes | Expected |
| --- | --- | --- |
| A, now | 12 straight, rectangular 6 × 5 | reference |
| B | 14 helical, 10° lead, semicircular R 3 | evenest for ryegrass |
| C | 14 helical, 10° lead, semicircular R 2 | small seed / clover |
| D | studs 6 × 6 × 4 in staggered rows | chaffy seed, mixtures |

Per variant and seed (ryegrass, white clover, a herbal ley mixture):
1. **Rate**: g per revolution from 10 revolutions into the tray (as in the mini README), 3 repeats.
2. **Evenness**: run at constant rpm over a slowly moving strip (paper with spray glue or a grease belt) or catch
   in 2 s portions; weigh per portion; CV = standard deviation / mean. Target: CV < 10 % (alfalfa in fluted
   rollers: 7 … 13 % [3]).
3. **Fill level**: repeat at full, half and a quarter full hopper; the rate should change less than 5 % [2].
4. **Segregation** (mixture only): sieve the first and the last portion and count clover in them; the share
   should stay the same from a full to a nearly empty hopper.
5. **Stop**: does seed trickle out after the motor stops (brush vs. TPU lip)?
6. **Damage**: look at seed after 50 revolutions for split or broken seeds (germination test if in doubt).

## Sources

1. Pennington, *Weight per bushel and number of seed per pound of selected forage crops*:
   https://www.pennington.com/-/media/Project/OneWeb/Pennington/Files/Tips_Guides/ForageCropWeightGuide.pdf
2. Wiedemann, Brock, Fisher, Cross (1979), *Seed metering and placement devices for rangeland seeder*,
   Transactions of the ASAE: https://revegetation.greatbasinfirescience.org/wp-content/uploads/2021/01/Wiedemann1979_SeedMeteringPlacement.pdf
   and the Australian follow-up for chaffy grasses: https://www.publish.csiro.au/an/EA98019
3. Güler (2005), *Effects of flute diameter, fluted roll length, and speed on alfalfa seed flow*, Applied
   Engineering in Agriculture: https://www.researchgate.net/publication/274539824_Effects_of_flute_diameter_fluted_roll_length_and_speed_on_alfalfa_seed_flow
   (values as quoted in reviews, e.g. https://jast.modares.ac.ir/article_15002_5496f40877a2ded20411a2266e86f523.pdf);
   Purdue, *Grain drill metering systems and the need for calibration*: https://www.extension.purdue.edu/extmedia/abe/abe-126-w.pdf
4. *Optimization of the fluted force-feed seeder meter with the helical roller using DEM and response surface
   analysis*, Agriculture 13 (2023) 1400: https://www.mdpi.com/2077-0472/13/7/1400
5. APV pneumatic seeders, metering rollers per seed: https://en.apv.at/products/seeding-spreading/pneumatic-seeders
   and the seeding shaft configurator: https://en.apv.at/news/news/detail/apv-seeding-shaft-configurator
6. Pöttinger Vitasem, agitator shaft for grass seed that segregates or flows poorly:
   https://www.poettinger.at/landtechnik/download/232.01.0311_Vitasem_ADD_de.pdf and
   https://www.poettinger.at/en_uk/produkte/detailtexthl/VSEM/th/2/seed-box
7. DEULA, *Sämaschinen* (cam wheel and fine seed wheel):
   https://www.deula.de/fileadmin/Redakteure/Stammsitz/extranet/600-699/616_-_i_-_1_-_B1_-_Saemaschinen.pdf;
   field remark on cam wheels and grass seed: https://www.tractorfan.de/topics/5047 (forum, anecdotal)
8. Vredo overseeder metering (fluted metering with a flap, cam wheel): https://www.pitchcare.com/blogs/news/more-good-news-from-campeys
   and https://www.farmtrader.co.nz/a-proud-milestone-for-vredo/
9. Brillion seeders (fluted seed cups for small seed, agitator box for chaffy seed):
   https://www.generalimp.com/userdocs/documents/brillionseedersag226.pdf and
   https://landoll.com/wp-content/uploads/2024/06/FPS6_FoodPlotSeeder_OM_2P102-2405.pdf
10. *An adaptive roller speed control method based on monitoring value of real-time seed flow rate for flute-roller
    type seed-metering device* (wheat): https://pmc.ncbi.nlm.nih.gov/articles/PMC7796428/
11. Carrier for small seed: https://www.theseedcollection.com.au/mixing-seeds-with-sand-for-easier-sowing and
    https://www.applewoodseed.com/planting-information/how-to-sow-wildflower-seeds/
12. Herbal ley composition and seed rates: https://defrafarming.blog.gov.uk/create-and-maintain-herbal-leys and
    https://www.fwi.co.uk/livestock/grassland-management/7-top-tips-on-establishing-herbal-leys

## Not verified

- TSW and bulk density of chicory, plantain, yarrow, burnet and sainfoin (marked *): typical values, weigh the lot.
- The DEM optimum (14 flutes, 10°, 40 rpm) is a simulation with other seed; the test plan checks it for grass.
- The flow-rate factor 0.55× of semicircular R 3 flutes is a cross-section ratio; filling of round flutes may
  differ from rectangular ones. The catch test gives the real value.
