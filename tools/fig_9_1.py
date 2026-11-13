"""Draws content/figures/fig-9-1.svg: a simplified redraw of Figure 9.1 (facility map), manual p. 137."""
import math, pathlib
o = []
A = o.append
def circ(x, y, t, r=9, fs=10):
    A(f'<circle class="f-card s-ink" stroke-width="1.5" cx="{x}" cy="{y}" r="{r}"/>')
    A(f'<text class="f-ink" x="{x}" y="{y+3.5}" font-size="{fs}" font-weight="700" text-anchor="middle" font-family="var(--f-body)">{t}</text>')
def tri(x, y, s=8):
    A(f'<path class="s-ink" fill="none" stroke-width="1.5" d="M{x} {y-s} L{x+s} {y+s*.7} L{x-s} {y+s*.7} Z"/>')
def fence(x1, y1, x2, y2, step=12):
    n = max(1, int(math.hypot(x2-x1, y2-y1)//step))
    A(f'<path class="s-ink" stroke-width="1" d="M{x1} {y1} L{x2} {y2}"/>')
    for i in range(n+1):
        x = x1+(x2-x1)*i/n; y = y1+(y2-y1)*i/n
        A(f'<path class="s-ink" stroke-width="1.3" d="M{x-3:.1f} {y-3:.1f} l6 6 M{x-3:.1f} {y+3:.1f} l6 -6"/>')
def arrow(x1, y1, x2, y2):
    A(f'<path class="s-muted" stroke-width="1.5" fill="none" marker-end="url(#ah-9-1)" d="M{x1} {y1} L{x2} {y2}"/>')
def label(x, y, t, fs=11, w=700, cls="f-ink", anchor="middle", rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ''
    A(f'<text class="{cls}" x="{x}" y="{y}" font-size="{fs}" font-weight="{w}" text-anchor="{anchor}" font-family="var(--f-body)"{tr}>{t}</text>')
def bins(x, y, w, h, n, vertical=False):
    A(f'<rect class="f-line s-ink" fill-opacity=".35" stroke-width="1.5" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    for i in range(1, n):
        if vertical: A(f'<path class="s-ink" stroke-width="1" d="M{x} {y+h*i/n:.1f} h{w}"/>')
        else: A(f'<path class="s-ink" stroke-width="1" d="M{x+w*i/n:.1f} {y} v{h}"/>')

A('<svg viewBox="0 0 900 520" role="img" aria-label="Figure 9.1, simplified redraw: a facility map showing bulk bins, bag house, warehouse with chemical storage, offices, showroom, loading dock, parking, straw shed, dikes, tanks, drains, a well, fences, vehicle access, and a stream along the bottom edge, with a key to facilities">')
A('<defs><marker id="ah-9-1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path class="f-muted" d="M0 0 L10 5 L0 10 Z"/></marker></defs>')
# property outline
A('<path class="s-ink" stroke-width="1.5" fill="none" d="M30 25 V455 M30 25 C40 75 90 85 600 150 V455"/>')
# stream band
A('<path class="f-field" fill-opacity=".18" d="M25 462 H612 V492 H25 Z"/>')
A('<path class="s-field" stroke-width="1.5" stroke-dasharray="6 5" fill="none" d="M25 477 H612"/>')
for x in range(55, 600, 75): circ(x, 477, "S")
# fences
fence(40, 110, 300, 118); fence(40, 110, 40, 230)
fence(200, 455, 450, 455); fence(495, 455, 600, 455); fence(600, 380, 600, 455)
# vehicle access gap
A('<path class="s-ink" stroke-width="1.5" d="M466 420 V500 M474 420 V500"/>')
label(470, 515, "vehicle access", fs=10, w=400, cls="f-muted")
# west side
A('<rect class="f-line" fill-opacity=".35" x="35" y="232" width="20" height="200"/>')
circ(45, 258, "A")
bins(60, 165, 140, 45, 6); label(130, 159, "BULK BINS")
bins(55, 335, 140, 55, 7); circ(110, 362, "O"); label(115, 328, "BULK BINS")
bins(200, 345, 24, 60, 4, vertical=True); label(212, 418, "BULK BINS", fs=8)
A('<rect class="f-line s-ink" fill-opacity=".35" stroke-width="1.5" x="155" y="238" width="50" height="20"/>')
label(118, 247, "Blender", fs=10, w=400); label(118, 259, "Shed", fs=10, w=400)
tri(140, 282); circ(158, 282, "T", r=8); label(105, 290, "Propane", fs=10, w=400)
A('<rect class="f-line s-ink" fill-opacity=".35" stroke-width="1.5" x="178" y="262" width="72" height="56"/>'); label(214, 294, "Bag House", fs=10)
A('<rect class="f-line s-ink" fill-opacity=".5" stroke-width="1.5" x="183" y="318" width="72" height="14"/>'); label(219, 329, "Scales", fs=9)
for x in range(80, 190, 28): arrow(x, 225, x+18, 225)
# dikes
A('<path class="s-ink" stroke-width="4" fill="none" d="M250 262 L287 214 M255 330 L287 368"/>')
label(258, 230, "Dike", fs=10, rot=-52)
label(262, 442, "Diked FL Runoff", fs=9)
A('<path class="s-muted" stroke-width="1" d="M262 432 L280 368"/>')
# warehouse
A('<rect class="f-card s-ink" stroke-width="2" x="287" y="205" width="308" height="135"/>')
A('<rect class="f-line s-ink" fill-opacity=".35" stroke-width="1.5" x="292" y="212" width="26" height="118"/>')
label(309, 318, "Chemical Storage", fs=9, rot=-90, anchor="start")
label(400, 238, "WAREHOUSE", fs=13); label(400, 285, "Chemical", fs=11, w=400); label(400, 299, "Storage", fs=11, w=400)
A('<path class="s-ink" stroke-width="1.2" d="M540 205 V340 M540 255 H595 M560 205 V255 M578 205 V255"/>')
label(510, 228, "OFFICES", fs=10); label(505, 300, "SHOWROOM", fs=10)
for x in range(300, 440, 30): arrow(x+18, 196, x, 196)
for x in range(450, 590, 30): arrow(x, 196, x+18, 196)
circ(270, 290, "T", r=8)
# loading dock
A('<rect class="f-line s-ink" fill-opacity=".5" stroke-width="1.5" x="287" y="340" width="308" height="18"/>')
label(450, 353, "LOADING DOCK", fs=10)
circ(301, 349, "BT", r=8, fs=7); circ(319, 349, "BT", r=8, fs=7); circ(301, 372, "D", r=8)
label(345, 382, "Bulk", fs=10, w=400); label(345, 394, "Loading Pad", fs=10, w=400)
label(470, 400, "PARKING", fs=12)
for x, y in ((395, 372), (380, 400), (365, 428), (545, 372), (565, 400)): arrow(x, y, x-10 if x < 470 else x+10, y+16)
A('<rect class="f-line s-ink" fill-opacity=".35" stroke-width="1.5" x="305" y="408" width="42" height="40"/>')
label(326, 425, "Straw", fs=9, w=400); label(326, 437, "Shed", fs=9, w=400)
circ(290, 455, "YD", r=9, fs=7); circ(585, 437, "YD", r=9, fs=7)
circ(585, 368, "T", r=8); label(600, 372, "Propane", fs=10, w=400, anchor="start")
circ(570, 392, "W", r=8); tri(588, 398, 6)
# key
A('<rect class="f-card s-muted" stroke-width="1.5" x="660" y="20" width="225" height="320" rx="6"/>')
label(675, 46, "KEY TO FACILITIES", fs=13, anchor="start")
rows = [("S", "Stream"), ("O", "Oxidizer"), ("T", "Tank"), ("BT", "Bulk Tank"), ("YD", "Yard Drain"), ("fence", "Wire Fence"),
        ("tri", "Flammable (FL)"), ("D", "Drain"), ("veh", "Vehicle Access"), ("A", "Absorbent Material"), ("W", "Well")]
y = 72
for sym, name in rows:
    if sym == "fence": fence(673, y, 701, y, step=14)
    elif sym == "tri": tri(687, y)
    elif sym == "veh": A(f'<path class="s-ink" stroke-width="1.5" d="M673 {y-3} h28 M673 {y+3} h28"/>')
    else: circ(687, y, sym, r=10, fs=8 if len(sym) > 1 else 10)
    label(712, y+4, name, fs=13, w=400, anchor="start")
    y += 25
A('</svg>')
pathlib.Path(__file__).resolve().parent.parent.joinpath("content/figures/fig-9-1.svg").write_text("\n".join(o) + "\n")
