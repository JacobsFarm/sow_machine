"""Parts of the TT gear motor version of the mini drop seeder. The hopper body, cut-off rim, lid and tray come
unchanged from ../ovm_parts.py; this module adds the motor plate with the roller pocket, the roller with the
longer motor end and the double-D socket, and the TT gear motor itself (bought part, for the checks and images).
Local frame of ovm_params (x = along the roller, +x = motor; y = forward; z = up; origin = roller axis).
"""
import importlib
import math

import ovt_params as T          # first: puts the base folder on sys.path and sets the 100 mm width

import Part
from FreeCAD import Vector as V

import ovm_params as P
import ovm_parts as G

importlib.reload(G)             # its module constants (X_IN, ...) must follow the width set by ovt_params

R = P.roller_d / 2.0
X_IN = P.width / 2.0                    # inner face of the motor plate
X_MOT = X_IN + T.plate_t                # outer face of the motor plate = face of the gearbox
X_POCKET = X_IN + T.pocket[1]           # bottom of the roller pocket
X1 = P.roller_x[1] + T.roller_ext       # motor end of the roller (0.5 from the pocket bottom)

X_OUT = G.X_OUT                         # outer face of the left end wall
rim, lid, tray = G.rim, G.lid, G.tray


def end_profile():
    """Outline of the end wall and motor plate: the base outline grown around the M8 bolt tubes."""
    r = T.bolt_tube_d / 2.0
    ring = [(y + r * math.cos(a * math.pi / 16), z + r * math.sin(a * math.pi / 16))
            for y, z in T.bolt_positions for a in range(32)]
    return G.convex_hull(G.end_profile() + ring)


def body():
    """Hopper body of the base design (no flange, 4 mm end wall), with the end wall grown around the bolt tubes and
    an M8 tube along the back and the front wall (PETG, one print, standing on the end wall: the tubes are
    vertical)."""
    tubes = [G.cyl_x(T.bolt_tube_d, -X_OUT, X_IN, y, z) for y, z in T.bolt_positions]
    s = G.body().fuse([G.prism(end_profile(), -X_OUT, -X_IN)] + tubes)
    for y, z in T.bolt_positions:
        s = s.cut(G.cyl_x(T.bolt_hole, -X_OUT - 1, X_IN + 1, y, z))
    s = s.cut(G.cyl_x(P.journal[0] + 2 * P.clear, -X_OUT - 1, -X_IN + 1))
    return s.removeSplitter()


def double_d(d, flat, x0, x1):
    """Shaft (or socket) along x: circle d with two flats 'flat' apart, normal to z."""
    return G.cyl_x(d, x0, x1).common(G.box_span((x0 - 1, x1 + 1), (-d, d), (-flat / 2.0, flat / 2.0)))


def motor_holes():
    """(y, z) of the 2 gearbox mounting holes (motor up)."""
    z, dy, _ = T.tt_holes
    return [(-dy / 2.0, z), (dy / 2.0, z)]


def motor_plate():
    """Right end wall (PETG, printed flat, outer face down): the base outline, the Ø35.4 x 2.8 bearing pocket in the
    inner face for the roller end, shaft and peg holes through the 1.2 mm wall, M8 bolt holes, and 2 Ø3 through
    holes for the gearbox bolts with Ø5.5 counterbores for their heads in the inner face."""
    s = G.prism(end_profile(), X_IN, X_MOT)
    cuts = [G.cyl_x(P.screw_hole, X_IN - 1, X_MOT + 1, y, z) for y, z in G.boss_positions()] if P.screw_columns else []
    cuts += [G.cyl_x(T.bolt_hole, X_IN - 1, X_MOT + 1, y, z) for y, z in T.bolt_positions]
    cuts.append(G.cyl_x(T.pocket[0], X_IN - 1, X_POCKET))
    cuts.append(G.cyl_x(T.shaft_hole, X_IN, X_MOT + 1))
    cuts.append(G.cyl_x(T.peg_hole, X_IN, X_MOT + 1, 0.0, T.tt_peg[2]))
    d, cb, cbd = T.motor_bolt
    for y, z in motor_holes():      # M3 from the inside: through hole, head in a counterbore in the inner face
        cuts += [G.cyl_x(d, X_IN - 1, X_MOT + 1, y, z), G.cyl_x(cb, X_IN - 1, X_IN + cbd, y, z)]
    for c in cuts:
        s = s.cut(c)
    return s.removeSplitter()


def roller(variant=T.DEFAULT):
    """Metering roller variant (P.ROLLERS) for the TT motor: the base flutes or cams, journal on the left, a plain
    Ø35 motor end 2.8 mm long (it runs in the plate pocket) and a double-D socket for the TT shaft (PETG, printed
    standing on the motor end). Roller I has its cams and end rims mirrored (chamfers on the bearing side); it
    prints standing on the journal end, with tree support from the slicer under its end face."""
    v = P.ROLLERS[variant]
    x0, x1 = P.roller_x
    if v["kind"] == "studs":
        s = G.studded_core(v)
        if v.get("chamfer") == "-x":    # the cam length is symmetric about x = 0: mirror cams and end rims
            s = s.mirror(V(0, 0, 0), V(1, 0, 0))
    else:
        s = G.cyl_x(P.roller_d, x0, x1)
        for g in (G.straight_flutes(v) if v["kind"] == "straight" else G.helical_flutes(v)):
            s = s.cut(g)
    s = s.fuse([G.cyl_x(P.journal[0], x0 - P.journal[1], x0 + 1), G.cyl_x(T.roller_end_d, x1 - 1, X1)])
    c = 2 * T.socket_clear
    s = s.cut(double_d(T.tt_shaft[0] + c, T.tt_shaft[1] + c, X1 - T.socket_depth, X1 + 1))
    re, ch = T.roller_end_d / 2.0, T.end_chamfer
    s = s.cut(G.revolve_x([(X1 - ch, re + 1), (X1 - ch, re), (X1, re - ch), (X1 + 1, re - ch), (X1 + 1, re + 1)]))
    gd, gc = T.peg_groove
    r0, r1 = T.tt_peg[2] - T.tt_peg[0] / 2.0 - gc, T.tt_peg[2] + T.tt_peg[0] / 2.0 + gc
    s = s.cut(G.revolve_x([(X1 - gd, r0), (X1 + 1, r0), (X1 + 1, r1), (X1 - gd, r1)]))
    return s.removeSplitter()


def tt_motor():
    """TT gear motor on the outer face of the plate: gearbox (tab end down), motor can up, peg into the plate."""
    gl, gw, gt = T.tt_gearbox
    z0 = -T.tt_shaft_to_end
    box = G.box_span((X_MOT, X_MOT + gt), (-gw / 2.0, gw / 2.0), (z0, z0 + gl))
    for y, z in motor_holes():
        box = box.cut(G.cyl_x(T.tt_holes[2], X_MOT - 1, X_MOT + gt + 1, y, z))
    box = box.cut(G.cyl_x(T.shaft_hole, X_MOT - 1, X_MOT + gt + 1))
    tl, tw, tt = T.tt_tab
    xm = X_MOT + gt / 2.0
    tab = G.box_span((xm - tt / 2.0, xm + tt / 2.0), (-tw / 2.0, tw / 2.0), (z0 - tl, z0 + 1))
    ml, mw, mt = T.tt_motor
    can = G.box_span((X_MOT, X_MOT + mt), (-mw / 2.0, mw / 2.0), (z0 + gl - 1, z0 + gl + ml))
    pd, ph, pz = T.tt_peg
    peg = G.cyl_x(pd, X_MOT - ph, X_MOT + 1, 0.0, pz)
    return G.fuse([box, tab, can, peg])


def bolt_set():
    """2 x M8 x 100 with a washer under the head and under the nut (bought parts): heads on the end wall side."""
    d, length = T.bolt
    wd, wt = T.washer
    hd, hh = T.bolt_head
    nd, nh = T.nut
    x_head = -X_OUT - wt
    x_nut = X_MOT + wt
    out = []
    for y, z in T.bolt_positions:
        out.append(G.fuse([G.cyl_x(hd, x_head - hh, x_head, y, z), G.cyl_x(d, x_head, x_head + length, y, z),
                           G.cyl_x(wd, x_head, -X_OUT, y, z), G.cyl_x(wd, X_MOT, x_nut, y, z),
                           G.cyl_x(nd, x_nut, x_nut + nh, y, z)]))
    return Part.makeCompound(out)


def motor_bolts():
    """2 x M3 x 25 socket head from the inside (head in the counterbore, flush with the inner face) and M3 nuts on
    the outer face of the gearbox (bought parts; drawn 0.1 smaller than their holes)."""
    _, cb, cbd = T.motor_bolt
    x_head = X_IN + cbd                 # underside of the head on the bottom of the counterbore
    x_nut = X_MOT + T.tt_gearbox[2]
    out = []
    for y, z in motor_holes():
        out.append(G.fuse([G.cyl_x(cb - 0.1, X_IN, x_head, y, z), G.cyl_x(2.9, x_head, x_head + 25.0, y, z),
                           G.cyl_x(6.2, x_nut, x_nut + 2.4, y, z)]))
    return Part.makeCompound(out)


def bolt_check():
    """Bolt length: thread beyond the nut (mm), must be >= 1 (one or two threads)."""
    d, length = T.bolt
    clamp = T.washer[1] + T.end_t + T.width + T.plate_t + T.washer[1]
    return {"clamped_mm": clamp, "with_nut_mm": clamp + T.nut[1], "thread_beyond_nut_mm": round(length - clamp - T.nut[1], 2)}


def tt_shaft():
    """The double-flat output shaft (own object: it turns with the roller)."""
    a, b = T.tt_shaft_out
    return double_d(T.tt_shaft[0], T.tt_shaft[1], X_MOT - a, X_MOT + T.tt_gearbox[2] + b)
