"""Generate content/figures/fig-1-4.svg (Figure 1.4 Pesticide resistance)."""
import math, random, pathlib
random.seed(14)
W = 204
panels = [
    {"x": 6,   "spray": True,  "lines": ["Some individuals", "survive the spray"], "resistant": {10}},
    {"x": 218, "spray": True,  "lines": ["Offspring inherit", "the resistance"], "resistant": {1, 4, 8, 10, 12, 15, 19}},
    {"x": 430, "spray": False, "lines": ["After frequent sprays:", "mostly resistant"], "resistant": set(range(21)) - {12}},
]
out = ['<svg viewBox="0 0 640 336" role="img" aria-label="Figure 1.4: pesticide resistance builds over repeated sprays until the population is mostly resistant individuals">']
for n, p in enumerate(panels, 1):
    x0 = p["x"]
    out.append(f'<rect class="f-card" x="{x0}" y="6" width="{W}" height="290" rx="8"/>')
    out.append(f'<text class="f-field" x="{x0+14}" y="38" font-family="var(--f-display)" font-weight="800" font-size="26">{n}</text>')
    for i, line in enumerate(p["lines"]):
        out.append(f'<text class="f-ink" x="{x0+38}" y="{31+i*19}" font-family="var(--f-body)" font-size="14" font-weight="700">{line}</text>')
    cx = x0 + W / 2
    if p["spray"]:
        for k in range(9):
            tx = x0 + 14 + k * (W - 28) / 8
            out.append(f'<path class="s-muted" stroke-width="1.5" stroke-dasharray="5 5" fill="none" d="M{cx:.0f} 74 L{tx:.0f} 182"/>')
        out.append(f'<rect class="f-ink" x="{cx-9:.0f}" y="62" width="18" height="12" rx="2"/>')
    k = 0
    for row in range(3):
        for col in range(7):
            bx = x0 + 22 + col * 26.5 + (13 if row % 2 else 0) * (1 if col < 6 else 0) + random.uniform(-3, 3)
            by = 206 + row * 30 + random.uniform(-4, 4)
            ang = random.uniform(-40, 40)
            res = k in p["resistant"]
            body = 'class="f-ink"' if res else 'class="f-field s-field" fill-opacity=".35" stroke-width="1.5"'
            out.append(f'<g transform="rotate({ang:.0f} {bx:.0f} {by:.0f})"><ellipse {body} cx="{bx:.0f}" cy="{by:.0f}" rx="10" ry="6.5"/><circle {body} cx="{bx+11:.0f}" cy="{by:.0f}" r="3.5"/></g>')
            if n == 1 and res:
                out.append(f'<path class="s-ink" stroke-width="1.5" fill="none" d="M{bx:.0f} {by-9:.0f} L{cx:.0f} 132"/>')
                out.append(f'<text class="f-ink" x="{cx:.0f}" y="126" text-anchor="middle" font-family="var(--f-body)" font-size="13" font-weight="700">resistant individual</text>')
            if n == 3 and not res:
                out.append(f'<path class="s-ink" stroke-width="1.5" fill="none" d="M{bx:.0f} {by-9:.0f} L{cx:.0f} 132"/>')
                out.append(f'<text class="f-ink" x="{cx:.0f}" y="126" text-anchor="middle" font-family="var(--f-body)" font-size="13" font-weight="700">susceptible individual</text>')
            k += 1
out.append('<g font-family="var(--f-body)" font-size="14">')
out.append('<ellipse class="f-ink" cx="200" cy="318" rx="10" ry="6.5"/><circle class="f-ink" cx="211" cy="318" r="3.5"/><text class="f-ink" x="222" y="323">Resistant</text>')
out.append('<ellipse class="f-field s-field" fill-opacity=".35" stroke-width="1.5" cx="340" cy="318" rx="10" ry="6.5"/><circle class="f-field s-field" fill-opacity=".35" stroke-width="1.5" cx="351" cy="318" r="3.5"/><text class="f-ink" x="362" y="323">Susceptible</text>')
out.append('</g></svg>')
pathlib.Path(__file__).resolve().parent.parent.joinpath('content/figures/fig-1-4.svg').write_text('\n'.join(out) + '\n')
print('ok')
