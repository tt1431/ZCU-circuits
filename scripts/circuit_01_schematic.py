"""
电路 01 — UBD1 双三极管电子开关（v5）
schemdraw 画电路原理图 + matplotlib 画时序图/框图

核心：PNP + NPN 级联 → 受控电子开关
DO_UBCTRL 控制 NPN → NPN 拉低 PNP 基极 → PNP 导通 → UBD1 电压输出
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import get_font, savefig, save_schemdraw

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties
import numpy as np

import schemdraw
import schemdraw.elements as elm


def _finish(d, name, title=None, w=None, h=None, dpi=250):
    """Draw + set size + title + save."""
    d.draw()
    if w and h:
        d.fig.fig.set_size_inches(w, h)
    if title:
        d.fig.fig.subplots_adjust(top=0.92)
        d.fig.fig.suptitle(title, fontsize=14, fontweight="bold")
    save_schemdraw(d, name, dpi=dpi)


# ═══════════════════════════════════════════════════════
# 图 1：完整原理图
# ═══════════════════════════════════════════════════════
print("图 1：完整原理图")

d1 = schemdraw.Drawing(fontsize=11, unit=1.8)

d1.push()
# 控制信号输入
d1 += (DIN := elm.Dot(open=True).label("DO_UBCTRL\n(P02.11)", loc="left", fontsize=9))

# R3806 下拉
d1 += elm.Line().down().at(DIN.start).length(0.7)
d1 += elm.Resistor().down().label("R3806\n4.7K", loc="right", fontsize=8)
d1 += elm.Ground()
d1 += elm.Line().up().length(0.7).at(DIN.start)

# → NPN base
d1 += elm.Line().right().at(DIN.start).length(0.7)
d1 += (QN := elm.BjtNpn().anchor("base").label("Q3001\n(NPN)", loc="top", fontsize=9))

# NPN emitter → GND
d1 += elm.Line().down().at(QN.emitter).length(0.5)
d1 += elm.Ground()

# NPN collector → up → right → R3000
d1 += elm.Line().up().at(QN.collector).length(0.5)
d1 += elm.Line().right().length(0.5)
d1 += elm.Resistor().right().label("R3000\n10K", loc="top", fontsize=9)
d1 += elm.Line().right().length(0.5)

# R3000 → PNP base (up)
d1 += elm.Line().up().length(0.7)
d1 += (QP := elm.BjtPnp().anchor("base").label("Q3001\n(PNP)", loc="top", fontsize=9))

# PNP emitter ← UBD1 (up)
d1 += elm.Line().up().at(QP.emitter).length(0.6)
d1 += elm.Dot(open=True).label("UBD1", loc="top", fontsize=10)

# TP3005
d1 += elm.Line().right(0.7).at(QP.emitter)
d1 += elm.Dot().label("TP3005", loc="right", fontsize=7)

# PNP collector → down → right
d1 += elm.Line().down().at(QP.collector).length(0.5)
d1 += elm.Line().right().length(1.0)

# R3005
d1 += elm.Resistor().right().label("R3005  24.3KΩ  1%", loc="top", fontsize=9)
d1 += elm.Line().right().length(0.5)

# TP3016
d1 += (TP := elm.Dot(open=True).label("TP3016", loc="top", fontsize=8))

# R3010 → GND
d1 += elm.Line().down().at(TP.start).length(0.5)
d1 += elm.Resistor().down().label("R3010\n4.7KΩ 1%", loc="right", fontsize=9)
d1 += elm.Ground()

# C3001 → GND
d1 += elm.Line().right(0.7).at(TP.start)
d1 += elm.Capacitor().down().label("C3001\n10nF", loc="right", fontsize=8)
d1 += elm.Ground()

# Output → MCU ADC
d1 += elm.Line().right().at(TP.start).length(1.2)
d1 += elm.Dot(open=True).label("MCU ADC\nUBD1_POWER_AN01[9]", loc="right", fontsize=9)

_finish(d1, "circuit_01_full_schematic.png", "UBD1 电源检测 — 双三极管电子开关", 14, 9)
print("✅ 图1 完成\n")


# ═══════════════════════════════════════════════════════
# 图 2：分压网络详解
# ═══════════════════════════════════════════════════════
print("图 2：分压网络详解")

d2 = schemdraw.Drawing(fontsize=11, unit=2.0)

d2 += elm.Dot(open=True).label("Vin\n(PNP集电极)", loc="left", fontsize=10)
d2 += elm.Line().right().length(0.5)
d2 += elm.Resistor().right().label("R3005\n24.3KΩ 1%", loc="top", fontsize=10)
d2 += elm.Line().right().length(0.5)
d2 += (MID := elm.Dot(open=True))

# R3010 → GND
d2 += elm.Line().down().at(MID.start).length(0.5)
d2 += elm.Resistor().down().label("R3010\n4.7KΩ 1%", loc="right", fontsize=10)
d2 += elm.Ground()

# C3001 → GND
d2 += elm.Line().right(0.8).at(MID.start)
d2 += elm.Capacitor().down().label("C3001\n10nF", loc="right", fontsize=9)
d2 += elm.Ground()

# Output
d2 += elm.Line().right().at(MID.start).length(1.2)
d2 += elm.Dot(open=True).label("Vout = Vin ×\nR3010/(R3005+R3010)\n≈ Vin × 0.162", loc="right", fontsize=10)

_finish(d2, "circuit_01_divider.png", "分压网络 + RC 低通滤波", 11, 5.5)
print("✅ 图2 完成\n")


# ═══════════════════════════════════════════════════════
# 图 3：电子开关核心 — matplotlib 手绘精简版
# ═══════════════════════════════════════════════════════
print("图 3：电子开关核心（matplotlib 精简）")

fig3, ax3 = plt.subplots(1, 1, figsize=(8, 6))
ax3.set_xlim(-1, 10)
ax3.set_ylim(-1, 8)
ax3.axis("off")

font9 = get_font(9)
font10 = get_font(10)

# ── NPN (bottom-left) ──
nx, ny = 2.5, 2.0
r = 0.5
# circle
ax3.add_patch(plt.Circle((nx, ny), r, fill=False, edgecolor="#222", lw=2))
# vertical bar
ax3.plot([nx, nx], [ny-r, ny+r], color="#222", lw=2)
# emitter arrow (bottom, outward)
ey = ny - r + r*0.5
ax3.plot([nx-r*0.3, nx], [ey, ey+r*0.25], color="#222", lw=2.5)
ax3.plot([nx+r*0.3, nx], [ey, ey+r*0.25], color="#222", lw=2.5)
# base line (left)
ax3.plot([nx-r, nx-r+r*0.5], [ny, ny], color="#222", lw=2)
# label
ax3.text(nx, ny-0.9, "Q3001\n(NPN)", fontsize=9, ha="center", va="top", fontproperties=font9)

# ── PNP (top-right) ──
px, py = 6.5, 5.5
ax3.add_patch(plt.Circle((px, py), r, fill=False, edgecolor="#222", lw=2))
ax3.plot([px, px], [py-r, py+r], color="#222", lw=2)
# emitter arrow (top, inward)
ey = py + r - r*0.5
ax3.plot([px-r*0.3, px], [ey, ey-r*0.25], color="#222", lw=2.5)
ax3.plot([px+r*0.3, px], [ey, ey-r*0.25], color="#222", lw=2.5)
# base line (left)
ax3.plot([px-r, px-r+r*0.5], [py, py], color="#222", lw=2)
# label
ax3.text(px, py-0.9, "Q3001\n(PNP)", fontsize=9, ha="center", va="top", fontproperties=font9)

# ── Connections ──
# NPN base ← DO_UBCTRL
ax3.plot([nx-r, 0.5], [ny, ny], color="#222", lw=1.8)
ax3.plot(0.5, ny, 'o', color="#222", markersize=5, zorder=5, markerfacecolor="#222")
ax3.text(0.3, ny, "DO_UBCTRL\n(P02.11)", fontsize=9, ha="right", va="center", fontproperties=font9, color="#1565C0")

# R3806: NPN base → down → GND
rx = nx - r*0.5
ax3.plot([rx, rx], [ny, ny-0.8], color="#222", lw=1.8)
# zigzag resistor
nz = 4; seg = 1.2/(2*nz+1); xs=[rx]; ys=[ny-0.8]
for i in range(nz):
    ys.append(ny-0.8 - seg*(2*i+1))
    xs.append(rx - 0.12 if i%2==0 else rx + 0.12)
    ys.append(ny-0.8 - seg*(2*i+2))
    xs.append(rx)
ax3.plot(xs, ys, color="#222", lw=1.8)
# ground
gy = ny-0.8-1.2
ax3.plot([rx, rx], [gy, gy-0.15], color="#222", lw=1.5)
for i, (ll, lr) in enumerate([(0.25,0.25),(0.15,0.15),(0.06,0.06)]):
    ax3.plot([rx-ll, rx+lr], [gy-0.15-i*0.13, gy-0.15-i*0.13], color="#222", lw=1.5)
ax3.text(rx+0.3, ny-0.8-0.6, "R3806\n4.7K", fontsize=8, ha="left", va="center", fontproperties=get_font(8))

# Link NPN base to R3806 top
ax3.plot([nx-r+0.1, rx], [ny, ny], color="#222", lw=1.2)

# NPN emitter → GND
ax3.plot([nx, nx], [ny-r, 0.5], color="#222", lw=1.8)
ax3.plot([nx-0.25, nx+0.25], [0.5, 0.5], color="#222", lw=1.5)
ax3.plot([nx-0.15, nx+0.15], [0.37, 0.37], color="#222", lw=1.5)
ax3.plot([nx-0.06, nx+0.06], [0.24, 0.24], color="#222", lw=1.5)

# NPN collector → up → right → R3000
top_y = ny + r + 0.6
ax3.plot([nx, nx], [ny+r, top_y], color="#222", lw=1.8)
ax3.plot([nx, nx+1.0], [top_y, top_y], color="#222", lw=1.8)
# R3000 zigzag
nz = 4; seg = 2.6/(2*nz+1); xs=[nx+1.0]; ys=[top_y]
for i in range(nz):
    xs.append(nx+1.0 + seg*(2*i+1))
    ys.append(top_y - 0.12 if i%2==0 else top_y + 0.12)
    xs.append(nx+1.0 + seg*(2*i+2))
    ys.append(top_y)
ax3.plot(xs, ys, color="#222", lw=1.8)
ax3.text(nx+1.0+1.3, top_y+0.25, "R3000 10K", fontsize=9, ha="center", fontproperties=font9)

# R3000 → PNP base
ax3.plot([nx+1.0+2.6, px-r], [top_y, top_y], color="#222", lw=1.8)
ax3.plot([px-r, top_y+0.3], [px-r, py], color="#222", lw=1.8)
ax3.plot(px-r, py, 'o', color="#222", markersize=5, zorder=5, markerfacecolor="#222")

# PNP emitter → UBD1
ax3.plot([px, px], [py+r, py+r+0.7], color="#222", lw=1.8)
ax3.plot(px, py+r+0.7, 'o', color="#222", markersize=5, zorder=5, markerfacecolor="#222")
ax3.text(px, py+r+0.9, "UBD1\n(电源输入)", fontsize=10, ha="center", va="bottom", fontproperties=font10)

# TP3005 stub
ax3.plot([px, px+1.0], [py+r+0.3, py+r+0.3], color="gray", lw=1.2, linestyle="--")
ax3.plot(px+1.0, py+r+0.3, 'o', color="gray", markersize=4, zorder=5, markerfacecolor="gray")
ax3.text(px+1.1, py+r+0.3, "TP3005", fontsize=7, va="center", fontproperties=get_font(7), color="gray")

# PNP collector → Vout
ax3.plot([px, px], [py-r, py-r-0.7], color="#222", lw=1.8)
ax3.plot(px, py-r-0.7, 'o', color="#222", markersize=5, zorder=5, markerfacecolor="#222")
ax3.text(px, py-r-0.9, "Vout\n→ 分压/ADC", fontsize=9, ha="center", va="top", fontproperties=font9, color="#E65100")

# ── Role labels ──
ax3.text(nx+0.8, ny+r+0.3, "驱动级", fontsize=9, ha="center", fontproperties=font9, color="#2E7D32")
ax3.text(px+0.8, py+r+0.3, "功率开关", fontsize=9, ha="center", fontproperties=font9, color="#C62828")

# ── Switch logic at bottom ──
ax3.text(4.5, 0.5,
         "开关逻辑：DO_UBCTRL=H → NPN导通 → PNP基极拉低 → PNP导通 → UBD1输出\n"
         "  DO_UBCTRL=L → NPN截止 → PNP基极浮高 → PNP截止 → 不耗电",
         fontsize=8.5, ha="center", fontproperties=font9,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#F8F8F8", edgecolor="#CCC", alpha=0.9))

fig3.suptitle("电子开关核心：双三极管（PNP+NPN）级联", fontsize=12, fontweight="bold", y=1.01)
fig3.tight_layout()
savefig(fig3, "circuit_01_switch_core.png")
print("✅ 图3 完成\n")


# ═══════════════════════════════════════════════════════
# 图 4：控制时序图（matplotlib）
# ═══════════════════════════════════════════════════════
print("图 4：控制时序图")

fig4, axes = plt.subplots(4, 1, figsize=(12, 7), sharex=True)
font = get_font(9)

t = np.linspace(0, 10, 2000)

# Signals
ctrl = np.where((t >= 2) & (t < 8), 3.3, 0.0)
npn_on = np.where(t >= 2.01, 1.0, 0.0)
npn_on[t >= 8.01] = 0.0
pnp_on = np.where(t >= 2.02, 1.0, 0.0)
pnp_on[t >= 8.02] = 0.0

tau = 0.00004
adc = np.zeros_like(t)
m = t >= 2.02
adc[m] = 1.94 * (1 - np.exp(-(t[m] - 2.02) / tau))
m2 = t >= 8.02
adc[m2] = 1.94 * np.exp(-(t[m2] - 8.02) / tau)

colors = ["#1565C0", "#2E7D32", "#E65100", "#C62828"]
labels = ["DO_UBCTRL\n(控制信号 P02.11)", "NPN 集电极\n(低 = 导通)", "PNP 集电极\n(高 = 导通)", "ADC 读数\n(UBD1_POWER_AN01)"]

axes[0].plot(t, ctrl, color=colors[0], lw=2.2)
axes[1].plot(t, npn_on * 3.3, color=colors[1], lw=2.2)
axes[2].plot(t, pnp_on * 12, color=colors[2], lw=2.2)
axes[3].plot(t, adc, color=colors[3], lw=2.2)

for i, (ax, label) in enumerate(zip(axes, labels)):
    ax.set_ylabel(label, fontsize=8.5, fontproperties=font)
    ax.grid(True, alpha=0.25)
    ax.tick_params(labelsize=8)

for ax in axes:
    ax.axvline(2, color="gray", ls=":", lw=1, alpha=0.5)
    ax.axvline(8, color="gray", ls=":", lw=1, alpha=0.5)

axes[3].annotate("开关闭合 → ADC 上升", xy=(2.5, 1.0), fontsize=8,
                  fontproperties=font, color="#555",
                  bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4", alpha=0.8))
axes[3].annotate("开关断开 → ADC 下降", xy=(8.5, 0.5), fontsize=8,
                  fontproperties=font, color="#555",
                  bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFECB3", alpha=0.8))

axes[-1].set_xlabel("时间", fontsize=10, fontproperties=font)
fig4.suptitle("双三极管电子开关 — 控制时序图", fontsize=13, fontweight="bold", y=1.02)
fig4.tight_layout()
savefig(fig4, "circuit_01_timing.png")
print("✅ 图4 完成\n")


# ═══════════════════════════════════════════════════════
# 图 5：系统框图（matplotlib）
# ═══════════════════════════════════════════════════════
print("图 5：系统框图")

fig5, ax5 = plt.subplots(1, 1, figsize=(14, 6.5))
ax5.set_xlim(0, 15)
ax5.set_ylim(0, 7)
ax5.axis("off")

font10 = get_font(10)
font9 = get_font(9)

def box(ax, x, y, w, h, text, color, fsize=10, edge="#444"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                       facecolor=color, edgecolor=edge, linewidth=2, alpha=0.9)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=fsize, ha="center", va="center",
            fontproperties=get_font(fsize))

def arrow(ax, x1, y1, x2, y2, c="#555", w=2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=c, lw=w))

# ── 主信号路径 ──
y1 = 4.8
box(ax5, 0.3, y1, 2.8, 1.2, "UBD1 电源\n(被监测轨)", "#FFF3CD", 10)
box(ax5, 3.8, y1, 3.0, 1.2, "电子开关\nPNP + NPN 级联\n(Q3001)", "#BBDEFB", 10)
box(ax5, 7.8, y1, 3.0, 1.2, "分压 + 滤波\nR3005/R3010\n+ C3001", "#E1BEE7", 10)
box(ax5, 11.5, y1, 2.8, 1.2, "MCU ADC\n12-bit 采样\n(AN01[9])", "#FFCDD2", 10)

arrow(ax5, 3.1, y1 + 0.6, 3.75, y1 + 0.6)
arrow(ax5, 6.8, y1 + 0.6, 7.75, y1 + 0.6)
arrow(ax5, 10.8, y1 + 0.6, 11.45, y1 + 0.6)

# ── 控制路径 ──
y2 = 2.0
box(ax5, 0.3, y2, 2.8, 1.0, "MCU GPIO\nDO_UBCTRL (P02.11)", "#C8E6C9", 10)
box(ax5, 3.8, y2, 3.0, 1.0, "NPN 驱动级\n(开关控制)", "#A5D6A7", 10)
arrow(ax5, 3.1, y2 + 0.5, 3.75, y2 + 0.5, "#388E3C")

# ── 下拉保护 ──
box(ax5, 7.8, y2, 2.8, 1.0, "R3806 基极下拉\n(防浮空误导通)", "#FFF9C4", 9)

# ── 控制 → 主路径 ──
ax5.annotate("", xy=(5.3, y1), xytext=(5.3, y2 + 1.0),
             arrowprops=dict(arrowstyle="->", color="#7B1FA2", lw=2.5))
ax5.text(5.8, 3.5, "R3000\n拉低基极", fontsize=9, ha="center", fontproperties=font9, color="#7B1FA2")

# ── 工作原理 ──
ax5.text(7.5, 0.5,
         "① DO_UBCTRL=H → ② NPN导通(集电极≈0V) → ③ R3000拉低PNP基极 →\n"
         "④ PNP导通(发射极=UBD1) → ⑤ 集电极输出 → ⑥ 分压(比0.162) → ⑦ C3001滤波 → ⑧ MCU ADC",
         fontsize=10, ha="center", fontproperties=font10, color="#333", va="top",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#F5F5F5", edgecolor="#CCC"))

fig5.suptitle("UBD1 电源检测 — 双三极管电子开关系统框图", fontsize=13, fontweight="bold", y=1.02)
fig5.tight_layout()
savefig(fig5, "circuit_01_block.png")
print("✅ 图5 完成\n")

print("=" * 50)
print("全部 5 张图生成完毕：")
print("  1. circuit_01_full_schematic.png  — 完整原理图")
print("  2. circuit_01_divider.png         — 分压网络详解")
print("  3. circuit_01_switch_core.png     — 电子开关核心")
print("  4. circuit_01_timing.png          — 控制时序图")
print("  5. circuit_01_block.png           — 系统框图")
print("=" * 50)
