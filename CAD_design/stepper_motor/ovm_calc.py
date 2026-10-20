"""Calculations for the mini drop seeder (pure Python, no FreeCAD): hopper, g per revolution, stepper speed and
torque, catch test, comparison with the 1 m drop seeder.

    python ovm_calc.py
"""
import math
import os
import sys

import ovm_params as P

FOLDER = os.path.dirname(os.path.abspath(__file__))
OVD_FOLDER = os.path.dirname(os.path.dirname(FOLDER))
G = 9.81


def hopper_litres():
    """Seed space: the sloping part plus the housing above the axis (the roller itself subtracted)."""
    slope = ((P.y_front - P.y_back) + (P.top_front - P.top_back)) / 2.0 * (P.z_top - P.z_throat)
    housing = (P.y_front - P.y_back) * P.z_throat - math.pi * (P.roller_d / 2.0) ** 2 / 2.0
    return (slope + housing) * P.width / 1e6


def flute_length():
    return P.roller_x[1] - P.roller_x[0] - 2 * P.flute_end


def chord_area(rho, half):
    """Area under the circle of radius rho over |y| <= half: integral of sqrt(rho^2 - y^2) dy."""
    return half * math.sqrt(rho * rho - half * half) + rho * rho * math.asin(half / rho)


def lens_area(r, rho):
    """Part of a circle of radius r, centred on a circle of radius rho, that lies inside that circle (the
    cross-section of a round flute normal to the flute)."""
    return (r * r * math.acos(r / (2.0 * rho)) + rho * rho * math.acos(1.0 - r * r / (2.0 * rho * rho))
            - 0.5 * r * math.sqrt(4.0 * rho * rho - r * r))


def flute_area(variant=P.ROLLER_DEFAULT):
    """Cross-section of one flute in a plane square to the roller axis (mm2)."""
    v = P.ROLLERS[variant]
    R = P.roller_d / 2.0
    if v["kind"] == "straight":
        fw, fd = v["flute"]
        return chord_area(R, fw / 2.0) - fw * (R - fd)          # the outer edge is the arc of the roller
    if v["kind"] == "helical":
        return lens_area(v["radius"], R) / math.cos(math.radians(v["lead"]))
    raise ValueError("studs have cells, not flutes")


def cell_volume_studs(v, steps=2000):
    """Free volume between the cams of a cam roller D to H (mm3): the annulus core..R between the end rims, minus the 45 deg
    step of the -x rim and the chamfered studs (tip length + (R - r) long at radius r, 2 r asin(w / 2r) wide)."""
    R = P.roller_d / 2.0
    length, width, h = v["stud"]
    rc = R - h
    a, b = P.studded_span()
    rows = P.stud_rows(v)
    vol, dr = 0.0, h / steps
    for k in range(steps):
        r = rc + (k + 0.5) * dr
        xa = a + (R - r)                                        # the -x rim slope
        free = b - xa
        for xs, _ in rows:
            free_studs = max(0.0, min(b, xs + length + (R - r)) - max(xa, xs))
            free -= v["around"] * free_studs * 2.0 * r * math.asin(width / 2.0 / r) / (2.0 * math.pi * r)
        vol += 2.0 * math.pi * r * dr * free
    return vol


def volume_per_rev(variant=P.ROLLER_DEFAULT):
    """Flute (or cell) volume that passes the rim per revolution (mm3), before the filling."""
    v = P.ROLLERS[variant]
    if v["kind"] == "studs":
        return cell_volume_studs(v)
    return v["flutes"] * flute_area(variant) * flute_length()


def ml_per_rev(variant=P.ROLLER_DEFAULT):
    return volume_per_rev(variant) * P.ROLLERS[variant]["fill"] / 1000.0


def g_per_rev(variant=P.ROLLER_DEFAULT):
    return ml_per_rev(variant) * P.seed_density


def rpm_for(speed=P.work_speed, rate=P.seed_rate, variant=P.ROLLER_DEFAULT):
    """Roller speed for a rate (g/m2) at a driving speed (m/s), the strip is the roller width."""
    g_per_s = rate * speed * P.width / 1000.0
    return g_per_s / g_per_rev(variant) * 60.0


def variants():
    """Per roller variant: volume, ml and g per revolution, rpm and microsteps/s at seed_rate and work_speed."""
    out = {}
    for k, v in P.ROLLERS.items():
        rpm = rpm_for(variant=k)
        out[k] = {"label": v["label"], "cm3_per_rev": volume_per_rev(k) / 1000.0, "fill": v["fill"],
                  "ml_per_rev": ml_per_rev(k), "g_per_rev": g_per_rev(k), "rpm": rpm, "steps_s": steps_per_s(rpm),
                  "in_20_40": 20.0 <= rpm <= 40.0}
    return out


def max_speed(rate=P.seed_rate):
    return P.stepper_rpm_max / rpm_for(1.0, rate)


def steps_per_s(rpm):
    return rpm / 60.0 * P.stepper_steps


def torque():
    """Torque on the roller (Nm): journal friction of the roller and seed weight (the rim does not touch the
    roller), and a peak when a seed is pinched between a flute edge or cam and the rim."""
    roller_kg = 0.12                                        # build_ovm.roller_variants: 95 ... 120 g
    seed_on_roller = 0.06                                   # kg resting on the roller top (estimated)
    steady = P.mu_journal * (roller_kg + seed_on_roller) * G * P.journal[0] / 2000.0
    return {"steady": steady, "peak": steady + P.seed_shear, "motor": P.stepper_torque,
            "margin_peak": P.stepper_torque / (steady + P.seed_shear)}


def catch_test(revs=P.calib_revs):
    """Expected catch of a calibration run: N revolutions into the tray."""
    g = revs * g_per_rev()
    tray_ml = ((P.tray_x[1] - P.tray_x[0] - 2 * P.tray_t) * (P.tray_y[1] - P.tray_y[0] - 2 * P.tray_t)
               * (P.tray_z[1] - P.tray_z[0] - P.tray_t) / 1000.0)
    return {"revs": revs, "g": g, "ml": g / P.seed_density, "tray_ml": tray_ml,
            "time_s_at_10rpm": revs / 10.0 * 60.0}


def fall_time():
    return math.sqrt(2.0 * P.fall_h / 1000.0 / G)


def compare_ovd():
    """g per revolution per mm of roller length against the 1 m roller; the same calibration factor
    (g measured / g calculated) holds for both when the flute shape is the same."""
    if OVD_FOLDER not in sys.path:
        sys.path.insert(0, OVD_FOLDER)
    try:
        import ovd_calc
        import ovd_params as O
    except Exception:
        return None
    big = ovd_calc.g_per_rev() / O.width
    return {"ovd_g_per_rev_mm": big, "ovm_g_per_rev_mm": g_per_rev() / P.width,
            "ovd_flute": O.flute, "ovm_flute": P.flute, "ovd_d": O.roller_d, "ovm_d": P.roller_d}


def bed_fit(sizes):
    """sizes = {part: (x, y, z) in the print orientation}; returns the parts that do not fit the bed."""
    bx, by, bz = P.bed
    return [k for k, (x, y, z) in sizes.items() if not (sorted((x, y))[0] <= min(bx, by)
                                                        and sorted((x, y))[1] <= max(bx, by) and z <= bz)]


def report():
    print("Overseeder, mini drop seeder (3D print)")
    print("  hopper %.2f l = %.0f g seed at %.2f kg/l; walls %.0f / %.0f deg from vertical"
          % (hopper_litres(), hopper_litres() * P.seed_density * 1000, P.seed_density, P.ANGLE_BACK, P.ANGLE_FRONT))
    print("  roller O%d x %d, %d flutes %gx%g over %.0f mm: %.1f ml = %.2f g per revolution"
          % (P.roller_d, P.width, P.flutes, P.flute[0], P.flute[1], flute_length(), ml_per_rev(), g_per_rev()))
    for v in (0.2, 0.3, P.work_speed):
        rpm = rpm_for(v)
        print("    %.1f m/s: %.1f rpm = %.0f microsteps/s for %.0f g/m2" % (v, rpm, steps_per_s(rpm), P.seed_rate))
    print("  roller variants at %.0f g/m2 and %.1f m/s (DEM / literature range for even flow: 20 - 40 rpm):"
          % (P.seed_rate, P.work_speed))
    for k, r in variants().items():
        print("    %s %-44s %5.1f cm3/rev x %.1f = %5.1f ml = %5.2f g/rev -> %5.1f rpm = %4.0f microsteps/s%s"
              % (k, r["label"], r["cm3_per_rev"], r["fill"], r["ml_per_rev"], r["g_per_rev"], r["rpm"],
                 r["steps_s"], "" if r["in_20_40"] else "  (outside 20 - 40)"))
    print("  roller up to %.0f rpm (flute filling) -> up to %.2f m/s at %.0f g/m2" % (P.stepper_rpm_max, max_speed(), P.seed_rate))
    t = torque()
    print("  torque %.3f Nm steady, %.3f Nm peak; stepper %.3f Nm -> margin %.1f"
          % (t["steady"], t["peak"], t["motor"], t["margin_peak"]))
    c = catch_test()
    print("  catch test %d rev: %.0f g = %.0f ml (tray %.0f ml), %.0f s at 10 rpm"
          % (c["revs"], c["g"], c["ml"], c["tray_ml"], c["time_s_at_10rpm"]))
    print("  fall %.2f s from %.0f mm" % (fall_time(), P.fall_h))
    o = compare_ovd()
    if o:
        print("  per mm of roller: mini %.3f g/rev, 1 m seeder %.3f g/rev (flute %gx%g vs %gx%g, O%d vs O%d)"
              % (o["ovm_g_per_rev_mm"], o["ovd_g_per_rev_mm"], o["ovm_flute"][0], o["ovm_flute"][1],
                 o["ovd_flute"][0], o["ovd_flute"][1], o["ovm_d"], o["ovd_d"]))


if __name__ == "__main__":
    report()
