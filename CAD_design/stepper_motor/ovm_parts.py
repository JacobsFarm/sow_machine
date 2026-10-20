"""Parts of the mini drop seeder (3D print). One function per part, returns a Part shape in the local frame of
ovm_params (x = along the roller, y = forward, z = up, origin = roller axis).

The hopper is drawn as a y-z profile extruded along x: printed standing on its left end wall, every wall is then
vertical and no support is needed.
"""
import math

import Part
from FreeCAD import Vector as V

import ovm_params as P

R = P.roller_d / 2.0
X_IN = P.width / 2.0                    # inner faces of the end walls at x = -X_IN (wall) and +X_IN (motor plate)
X_OUT = X_IN + P.end_t                  # outer face of the left end wall at -X_OUT
X_MOT = X_IN + P.motor_plate_t          # outer face of the motor plate (motor flange)
COS_B = math.cos(math.atan(P.TAN_BACK))
COS_F = math.cos(math.atan(P.TAN_FRONT))


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def prism(points, x0, x1):
    """Closed y-z polygon extruded along x from x0 to x1."""
    pts = [V(x0, y, z) for y, z in points]
    face = Part.Face(Part.makePolygon(pts + [pts[0]]))
    return face.extrude(V(x1 - x0, 0, 0))


def rect(y0, y1, z0, z1):
    return [(y0, z0), (y1, z0), (y1, z1), (y0, z1)]


def box_span(xs, ys, zs):
    return Part.makeBox(xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0], V(xs[0], ys[0], zs[0]))


def cyl_x(d, x0, x1, y=0.0, z=0.0):
    return Part.makeCylinder(d / 2.0, x1 - x0, V(x0, y, z), V(1, 0, 0))


def cyl_z(d, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(d / 2.0, z1 - z0, V(x, y, z0), V(0, 0, 1))


def fuse(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.removeSplitter()


def convex_hull(points):
    pts = sorted(set((round(y, 4), round(z, 4)) for y, z in points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def d_shape(d, flat, x0, x1):
    """D shaft (or socket) along x: circle d with one flat, 'flat' from the round side (flat on top, normal +z)."""
    c = cyl_x(d, x0, x1)
    return c.common(box_span((x0 - 1, x1 + 1), (-d, d), (-d / 2.0, flat - d / 2.0)))


# ---------------------------------------------------------------------
# Hopper geometry (profile)
# ---------------------------------------------------------------------
def back_outer(z):
    """y of the outer face of the back wall at height z (sloping part)."""
    return P.y_back - (z - P.z_throat) * P.TAN_BACK - P.wall / COS_B


def front_outer(z):
    return P.y_front + (z - P.z_throat) * P.TAN_FRONT + P.wall / COS_F


def boss_positions():
    """(y, z) of the 4 screw columns for the motor plate, each just outside a wall."""
    off = P.boss_d / 2.0 - 0.5
    return [(P.y_back - P.wall - off, P.boss_z_low[0]),
            (P.y_front + P.wall + off, P.boss_z_low[1]),
            (back_outer(P.boss_z_high) - off, P.boss_z_high),
            (front_outer(P.boss_z_high) + off, P.boss_z_high)]


def end_profile():
    """Outline of the left end wall and the motor plate: convex hull of the walls and the screw columns."""
    lb, lh = P.rim_block
    pts =[(P.y_back - P.wall, P.plate_bottom), (P.y_back - P.wall, P.z_throat),
           (back_outer(P.z_top), P.z_top), (front_outer(P.z_top), P.z_top),
           (P.y_front + P.wall, P.z_throat), (P.y_front + lb, lh / 2.0), (P.y_front + lb, -lh / 2.0),
           (P.y_front + P.wall, P.plate_bottom)]
    r = P.boss_d / 2.0
    for y, z in (boss_positions() if P.screw_columns else []):
        pts += [(y + r * math.cos(a * math.pi / 12), z + r * math.sin(a * math.pi / 12)) for a in range(24)]
    return convex_hull(pts)


def wall_profiles():
    t = P.wall
    yb, yf, zt, zb = P.y_back, P.y_front, P.z_throat, P.z_bottom
    lb, lh = P.rim_block
    out = [rect(yb - t, yb, zb, zt),
           rect(yf, yf + t, zb, zt),
           rect(yf, yf + lb, -lh / 2.0, lh / 2.0),
           [(yb, zt), (P.top_back, P.z_top), (back_outer(P.z_top), P.z_top), (yb - t / COS_B, zt)],
           [(yf, zt), (yf + t / COS_F, zt), (front_outer(P.z_top), P.z_top), (P.top_front, P.z_top)]]
    if P.flange:
        out.append(rect(P.flange_y[0], P.flange_y[1], P.flange_z[0], P.flange_z[1]))
    return out


# ---------------------------------------------------------------------
# Printed parts
# ---------------------------------------------------------------------
def body():
    """Hopper with housing, left end wall, rim slot, screw columns and mounting flange (PETG, one print)."""
    x0 = -X_OUT
    solids = [prism(p, x0, X_IN) for p in wall_profiles()]
    columns = boss_positions() if P.screw_columns else []
    solids += [cyl_x(P.boss_d, x0, X_IN, y, z) for y, z in columns]
    solids.append(prism(end_profile(), x0, -X_IN))
    s = fuse(solids)
    cuts = [cyl_x(P.journal[0] + 2 * P.clear, x0 - 1, -X_IN + 1)]
    sw, sd = P.rim_slot
    cuts.append(box_span((-X_IN, X_IN + 1), (P.y_front - 1, P.y_front + sd), (-sw / 2.0, sw / 2.0)))
    d, depth = P.boss_pilot
    cuts += [cyl_x(d, X_IN - depth, X_IN + 1, y, z) for y, z in columns]
    if P.flange:
        cuts += [cyl_z(P.flange_hole_d, P.flange_z[0] - 1, P.flange_z[1] + 1, x, P.flange_hole_y)
                 for x in P.flange_holes_x]
    for c in cuts:
        s = s.cut(c)
    return s.removeSplitter()


def stepper_holes():
    """(y, z) of the 4 motor screws (31 mm square); the button heads sit in counterbores on the inner face."""
    r = P.stepper_holes[0] / math.sqrt(2.0)
    return [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]


def motor_plate():
    """Right end wall: closes the hopper, carries the stepper (PETG, printed flat)."""
    s = prism(end_profile(), X_IN, X_MOT)
    cuts = [cyl_x(P.screw_hole, X_IN - 1, X_MOT + 1, y, z) for y, z in boss_positions()] if P.screw_columns else []
    cuts.append(cyl_x(P.stepper_boss[0] + 2 * P.clear, X_IN - 1, X_MOT + 1))
    cd, ch = P.counterbore
    for y, z in stepper_holes():
        cuts.append(cyl_x(P.stepper_holes[1], X_IN - 1, X_MOT + 1, y, z))
        cuts.append(cyl_x(cd, X_IN - 1, X_IN + ch, y, z))
    for c in cuts:
        s = s.cut(c)
    return s.removeSplitter()


def roller(variant=P.ROLLER_DEFAULT):
    """Metering roller, variant from P.ROLLERS (A = straight flutes, B/C = helical round-bottom flutes, D to H =
    cam rollers),
    with the journal on the left and the D socket for the stepper on the right (PETG, printed standing on the
    motor end)."""
    v = P.ROLLERS[variant]
    x0, x1 = P.roller_x
    if v["kind"] == "studs":
        s = studded_core(v)
    else:
        s = cyl_x(P.roller_d, x0, x1)
        for g in (straight_flutes(v) if v["kind"] == "straight" else helical_flutes(v)):
            s = s.cut(g)
    s = s.fuse(cyl_x(P.journal[0], x0 - P.journal[1], x0 + 1))
    d, flat, depth = P.d_socket
    s = s.cut(d_shape(d + 2 * P.clear, flat + 2 * P.clear, x1 - depth, x1 + 1))
    return s.removeSplitter()


def straight_flutes(v):
    """Cutting tools of the rectangular flutes (variant A)."""
    x0, x1 = P.roller_x
    fw, fd = v["flute"]
    out = []
    for i in range(v["flutes"]):
        g = box_span((x0 + P.flute_end, x1 - P.flute_end), (-fw / 2.0, fw / 2.0), (R - fd, R + 1))
        g.rotate(V(0, 0, 0), V(1, 0, 0), 360.0 * i / v["flutes"])
        out.append(g)
    return out


def helical_flutes(v):
    """Cutting tools of the helical flutes: a circle of radius r, normal to the flute, swept (Frenet) along a helix
    of radius R at 'lead' degrees to the axis, then cut off square at flute_end from the roller ends. Printed with
    the axis vertical the flute walls lean at most 'lead' from vertical; the top end bridges 2 r."""
    x0, x1 = P.roller_x
    r, n = v["radius"], v["flutes"]
    pitch = 2.0 * math.pi * R / math.tan(math.radians(v["lead"]))
    extra = r + 1.0
    length = x1 - x0 - 2 * P.flute_end + 2 * extra
    helix = Part.makeHelix(pitch, length, R)        # along z, starts at (R, 0, 0)
    tangent = V(0, 2.0 * math.pi * R, pitch)
    tangent.normalize()
    circle = Part.Wire(Part.makeCircle(r, V(R, 0, 0), tangent))
    tool = Part.Wire(helix).makePipeShell([circle], True, True)
    tool.rotate(V(0, 0, 0), V(0, 1, 0), 90.0)       # z -> x
    tool.translate(V(x0 + P.flute_end - extra, 0, 0))
    slab = box_span((x0 + P.flute_end, x1 - P.flute_end), (-R - 2, R + 2), (-R - 2, R + 2))
    tool = tool.common(slab)
    out = []
    for i in range(n):
        g = tool.copy()
        g.rotate(V(0, 0, 0), V(1, 0, 0), 360.0 * i / n)
        out.append(g)
    return out


def revolve_x(points):
    """Closed (x, r) profile revolved 360 deg about the x axis."""
    pts = [V(x, 0, r) for x, r in points]
    face = Part.Face(Part.makePolygon(pts + [pts[0]]))
    return face.revolve(V(0, 0, 0), V(1, 0, 0), 360.0)


def studded_core(v):
    """Cam rollers D to H: Ø40 end rims with a core of Ø40 - 2 h between them and rings of cams h high. The -x rim
    (the top when printed) steps down to the core at 45 deg; each cam is a ring with a 45 deg chamfer on its +x
    side (the down side when printed: tip 'length' long, base length + h), cut to its width around. One cam is
    made per ring and copied around, then everything is fused in one go (H has 400 cams)."""
    x0, x1 = P.roller_x
    length, width, h = v["stud"]
    rc = R - h
    a, b = P.studded_span()
    core = revolve_x([(x0, 0), (x0, R), (a, R), (a + h, rc), (b, rc), (b, R), (x1, R), (x1, 0)])
    studs = []
    for xs, off in P.stud_rows(v):
        ring = revolve_x([(xs, rc - 0.5), (xs, R), (xs + length, R), (xs + length + h + 0.5, rc - 0.5)])
        cam = ring.common(box_span((xs - 1, xs + length + h + 1), (-width / 2.0, width / 2.0), (0, R + 1)))
        for i in range(v["around"]):
            c = cam.copy()
            c.rotate(V(0, 0, 0), V(1, 0, 0), off + 360.0 * i / v["around"])
            studs.append(c)
    return core.fuse(studs).removeSplitter()


def rim():
    """Cut-off rim (PETG, printed flat): a flat strip in the slot of the front housing wall, its tip rim_gap from
    the roller. Square edges: the sharp top edge cuts the seed layer off cleanly (in steel: a sawn flat bar)."""
    return box_span(P.rim_x, (R + P.rim_gap, P.y_front + P.rim_slot[1]), (-P.rim_t / 2.0, P.rim_t / 2.0))


def lid():
    """Lid with a locating rim (PETG, printed upside down)."""
    s = box_span((-X_OUT, X_MOT), (back_outer(P.z_top), front_outer(P.z_top)), (P.z_top, P.z_top + P.lid_t))
    w, depth, inset = P.lid_rim
    ox, y0, y1 = X_IN - inset, P.top_back + inset, P.top_front - inset
    zs = (P.z_top - depth, P.z_top + 0.5)
    rim = box_span((-ox, ox), (y0, y1), zs).cut(box_span((-ox + w, ox - w), (y0 + w, y1 - w), (zs[0] - 1, zs[1] + 1)))
    return s.fuse(rim).removeSplitter()


def tray():
    """Catch tray for the calibration (PETG, open top)."""
    t = P.tray_t
    s = box_span(P.tray_x, P.tray_y, P.tray_z)
    inner = box_span((P.tray_x[0] + t, P.tray_x[1] - t), (P.tray_y[0] + t, P.tray_y[1] - t),
                     (P.tray_z[0] + t, P.tray_z[1] + 1))
    return s.cut(inner)


# ---------------------------------------------------------------------
# Bought parts (for the check and the images)
# ---------------------------------------------------------------------
def stepper():
    """NEMA 17 on the outside of the motor plate, shaft on the roller axis, connector down."""
    a, length = P.stepper_body
    body_ = box_span((X_MOT, X_MOT + length), (-a / 2.0, a / 2.0), (-a / 2.0, a / 2.0))
    for y, z in stepper_holes():
        body_ = body_.cut(cyl_x(3.0, X_MOT - 1, X_MOT + 4.5, y, z))
    bd, bh = P.stepper_boss
    boss = cyl_x(bd, X_MOT - bh, X_MOT)
    cw, ch, cl = P.stepper_connector
    conn = box_span((X_MOT + length - cl, X_MOT + length), (-cw / 2.0, cw / 2.0), (-a / 2.0 - ch, -a / 2.0 + 1.0))
    return fuse([body_, boss, conn])


def stepper_shaft():
    """Shaft of the stepper (own object: it turns with the roller)."""
    sd, sf, sl = P.stepper_shaft
    return d_shape(sd, sf, X_MOT - sl, X_MOT - P.stepper_boss[1])
