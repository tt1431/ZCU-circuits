"""
电路 01 — UBD1 电源检测电路（v4：matplotlib 手绘原理图，精确定位）
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import set_mpl_style, get_font, IMAGES_DIR, savefig
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc, Circle, Polygon, Rectangle
import numpy as np

set_mpl_style()

def draw_transistor(ax, typ, x, y, size=0.4, label="", fontsize=9, fontprop=None):
    """Draw NPN or PNP transistor symbol at (x,y)."""
    w, h = size * 1.2, size * 1.5
    # Draw circle
    circle = Circle((x, y), w/1.5, fill=False, edgecolor="#222", linewidth=1.8)
    ax.add_patch(circle)
    # Draw internal lines
    if typ == "npn":
        # Vertical line
        ax.plot([x, x], [y-h/2, y+h/2], color="#222", linewidth=1.8)
        # Emitter arrow (bottom, pointing out = down)
        ax.plot([x-size*0.15, x], [y-h/2+size*0.25, y-h/2], color="#222", linewidth=2)
        ax.plot([x+size*0.15, x], [y-h/2+size*0.25, y-h/2], color="#222", linewidth=2)
        emitter_y = y - h/2
        collector_y = y + h/2
        base_x = x - w/1.5
    else:  # pnp
        # Vertical line
        ax.plot([x, x], [y-h/2, y+h/2], color="#222", linewidth=1.8)
        # Emitter arrow (top, pointing in = up)
        ax.plot([x-size*0.15, x], [y+h/2-size*0.25, y+h/2], color="#222", linewidth=2)
        ax.plot([x+size*0.15, x], [y+h/2-size*0.25, y+h/2], color="#222", linewidth=2)
        emitter_y = y + h/2
        collector_y = y - h/2
        base_x = x - w/1.5
    # Base line (horizontal from left)
    ax.plot([base_x, x], [y, y], color="#222", linewidth=1.8)
    if label:
        ax.text(x + size*1.1, y, label, fontsize=fontsize, va="center", fontproperties=fontprop, color="#333")
    return {"x": x, "y": y, "emitter": (x, emitter_y), "collector": (x, collector_y), "base": (base_x, y)}


def draw_resistor(ax, x1, y1, x2, y2, label="", fontsize=9, fontprop=None, label_loc="top"):
    """Draw resistor as zigzag line between (x1,y1) and (x2,y2)."""
    if x2 != x1:  # horizontal
        length = x2 - x1
        n = 5
        seg = length / (2*n + 1)
        xs, ys = [x1], [y1]
        for i in range(n):
            xs.append(x1 + seg*(2*i+1))
            ys.append(y1 - 0.12 if i%2==0 else y1 + 0.12)
            xs.append(x1 + seg*(2*i+2))
            ys.append(y1)
        ax.plot(xs, ys, color="#222", linewidth=1.5)
    else:  # vertical
        length = y2 - y1
        n = 5
        seg = length / (2*n + 1)
        xs, ys = [x1], [y1]
        for i in range(n):
            ys.append(y1 + seg*(2*i+1))
            xs.append(x1 - 0.12 if i%2==0 else x1 + 0.12)
            ys.append(y1 + seg*(2*i+2))
            xs.append(x1)
        ax.plot(xs, ys, color="#222", linewidth=1.5)
    if label:
        midx, midy = (x1+x2)/2, (y1+y2)/2
        if label_loc == "top":
            ax.text(midx, midy+0.2, label, fontsize=fontsize, ha="center", va="bottom", fontproperties=fontprop)
        elif label_loc == "right":
            ax.text(midx+0.2, midy, label, fontsize=fontsize, ha="left", va="center", fontproperties=fontprop)
        elif label_loc == "bottom":
            ax.text(midx, midy-0.15, label, fontsize=fontsize, ha="center", va="top", fontproperties=fontprop)
        elif label_loc == "left":
            ax.text(midx-0.2, midy, label, fontsize=fontsize, ha="right", va="center", fontproperties=fontprop)


def draw_capacitor(ax, x, y1, y2, label="", fontsize=9, fontprop=None):
    """Draw capacitor as two parallel plates."""
    gap = 0.1
    ax.plot([x-0.15, x-0.15], [y1+gap, y2-gap], color="#222", linewidth=1.8)
    ax.plot([x+0.15, x+0.15], [y1+gap, y2-gap], color="#222", linewidth=1.8)
    if label:
        ax.text(x+0.3, (y1+y2)/2, label, fontsize=fontsize, va="center", fontproperties=fontprop)


def draw_ground(ax, x, y):
    """Draw ground symbol."""
    ax.plot([x, x], [y, y-0.15], color="#222", linewidth=1.5)
    ax.plot([x-0.25, x+0.25], [y-0.15, y-0.15], color="#222", linewidth=1.5)
    ax.plot([x-0.15, x+0.15], [y-0.28, y-0.28], color="#222", linewidth=1.5)
    ax.plot([x-0.06, x+0.06], [y-0.41, y-0.41], color="#222", linewidth=1.5)


def draw_dot(ax, x, y, label="", fontsize=9, fontprop=None, label_loc="right", color="blue"):
    """Draw a connection dot with optional label."""
    ax.plot(x, y, 'o', color="#222", markersize=5, zorder=5)
    if label:
        if label_loc == "right":
            ax.text(x+0.15, y, label, fontsize=fontsize, va="center", fontproperties=fontprop, color=color)
        elif label_loc == "left":
            ax.text(x-0.15, y, label, fontsize=fontsize, va="center", ha="right", fontproperties=fontprop, color=color)
        elif label_loc == "top":
            ax.text(x, y+0.15, label, fontsize=fontsize, ha="center", va="bottom", fontproperties=fontprop, color=color)
        elif label_loc == "bottom":
            ax.text(x, y-0.2, label, fontsize=fontsize, ha="center", va="top", fontproperties=fontprop, color=color)


def draw_line(ax, x1, y1, x2, y2, style="-"):
    ax.plot([x1, x2], [y1, y2], color="#222", linewidth=1.5, linestyle=style)


# ═══════════════════════════════════════════
# 图1: 完整电路原理图
# ═══════════════════════════════════════════
font = get_font(size=9)
font_sm = get_font(size=8)
font_lg = get_font(size=11)

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(-1, 13)
ax.set_ylim(-1, 8)
ax.axis("off")
ax.set_title("UBD1 电源检测电路", fontsize=16, fontweight="bold", pad=20, fontproperties=get_font(size=16))

# Key positions
pnp_x, pnp_y = 5.5, 5.5     # PNP transistor center
npn_x, npn_y = 2.0, 2.5     # NPN transistor center

# ── PNP transistor (top right) ──
pnp = draw_transistor(ax, "pnp", pnp_x, pnp_y, size=0.5, label="Q3001\n(PNP)\nNSVMUN5333", fontsize=9, fontprop=font)

# PNP emitter (top) → UBD1
em_x, em_y = pnp["emitter"]
draw_line(ax, em_x, em_y, em_x, em_y+0.8)
draw_line(ax, em_x, em_y+0.8, em_x-3.5, em_y+0.8)
draw_dot(ax, em_x-3.5, em_y+0.8, "UBD1", fontsize=10, fontprop=font_lg, label_loc="left", color="black")
# TP3005
draw_dot(ax, em_x, em_y+0.8, "TP3005", fontsize=8, fontprop=font_sm, label_loc="right", color="gray")

# PNP collector (bottom) → R3005
col_x, col_y = pnp["collector"]
draw_line(ax, col_x, col_y, col_x, col_y-0.5)

# R3005 horizontal
r3005_start = (col_x, col_y-0.5)
r3005_end = (col_x+3.5, col_y-0.5)
draw_resistor(ax, r3005_start[0], r3005_start[1], r3005_end[0], r3005_end[1],
              "R3005  24.3K  1%", fontsize=9, fontprop=font, label_loc="top")

# TP3016
draw_dot(ax, col_x+3.5, col_y-0.5, "TP3016", fontsize=8, fontprop=font_sm, label_loc="top", color="gray")

# R3010 vertical to GND
draw_resistor(ax, col_x+3.5, col_y-0.5, col_x+3.5, col_y-2.2,
              "R3010\n4.7K 1%", fontsize=9, fontprop=font, label_loc="right")
draw_ground(ax, col_x+3.5, col_y-2.2)

# C3001 vertical to GND (to the right of R3010)
draw_capacitor(ax, col_x+4.5, col_y-0.5, col_y-2.2,
               "C3001\n10nF", fontsize=8, fontprop=font_sm)

# Connect C3001 to TP3016 node
draw_line(ax, col_x+3.5, col_y-0.5, col_x+4.5, col_y-0.5)
# C3001 to GND
draw_line(ax, col_x+4.5, col_y-2.2, col_x+4.5, col_y-2.2)
draw_ground(ax, col_x+4.5, col_y-2.2)

# Output to MCU ADC
draw_line(ax, col_x+3.5, col_y-0.5, col_x+6.5, col_y-0.5)
draw_dot(ax, col_x+6.5, col_y-0.5, "MCU ADC\nUBD1_POWER_AN01[9]",
         fontsize=9, fontprop=font, label_loc="right", color="blue")

# ── NPN transistor (bottom left) ──
npn = draw_transistor(ax, "npn", npn_x, npn_y, size=0.5, label="Q3001\n(NPN)", fontsize=9, fontprop=font)

# NPN emitter (bottom) → GND
nem_x, nem_y = npn["emitter"]
draw_line(ax, nem_x, nem_y, nem_x, nem_y-0.5)
draw_ground(ax, nem_x, nem_y-0.5)

# NPN base (left) ← DO_UBCTRL + R3806
nbase_x, nbase_y = npn["base"]
draw_line(ax, nbase_x, nbase_y, nbase_x-1.5, nbase_y)
draw_dot(ax, nbase_x-1.5, nbase_y, "DO_UBCTRL\nP02.11", fontsize=9, fontprop=font, label_loc="left", color="green")

# R3806 pull-down from NPN base to GND
draw_resistor(ax, nbase_x+0.1, nbase_y-0.1, nbase_x+0.1, nbase_y-2.2,
              "R3806\n4.7K", fontsize=8, fontprop=font_sm, label_loc="right")
draw_ground(ax, nbase_x+0.1, nbase_y-2.2)
# Connect R3806 top to NPN base
draw_line(ax, nbase_x, nbase_y, nbase_x+0.1, nbase_y-0.1)

# NPN collector (top) → R3000 → PNP base
ncol_x, ncol_y = npn["collector"]
draw_line(ax, ncol_x, ncol_y, ncol_x, ncol_y+0.3)

# R3000 from NPN collector going up-right to PNP base
pbase_x, pbase_y = pnp["base"]
# Horizontal from NPN collector to right
draw_resistor(ax, ncol_x, ncol_y+0.3, pbase_x, ncol_y+0.3,
              "R3000  10K", fontsize=9, fontprop=font, label_loc="top")
# Vertical up to PNP base
draw_line(ax, pbase_x, ncol_y+0.3, pbase_x, pbase_y)

# ── Test point labels ──
# TP3000: UBD1 input area
draw_dot(ax, em_x-3.5, em_y+0.8, fontsize=8, fontprop=font_sm, label_loc="left")

# TP3007 at NPN base
draw_dot(ax, nbase_x-1.5, nbase_y, "TP3007", fontsize=8, fontprop=font_sm, label_loc="bottom", color="gray")

# Annotation
ax.text(7, 1.5, 
        "工作逻辑：\n"
        "① DO_UBCTRL=H → NPN导通\n"
        "② NPN集电极≈0V → 通过R3000\n"
        "   拉低PNP基极\n"
        "③ PNP导通(发射极=UBD1)\n"
        "④ PNP集电极输出电压\n"
        "⑤ R3005/R3010分压 → MCU ADC",
        fontsize=8.5, va="top", fontproperties=get_font(size=8.5),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F0F8FF", edgecolor="#888", alpha=0.8),
        linespacing=1.6)

savefig(fig, "circuit_01_ubd1_schematic.png")
print("✅ 图1 完成 (matplotlib 手绘版)")


# ═══════════════════════════════════════════
# 图2: ADC 分压网络
# ═══════════════════════════════════════════
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 5))
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 5)
ax2.axis("off")
ax2.set_title("ADC 分压网络", fontsize=14, fontweight="bold", pad=15, fontproperties=get_font(size=14))

# PNP collector input
draw_dot(ax2, 1, 3, "PNP集电极\n(导通后输出电压)", fontsize=10, fontprop=get_font(size=10), label_loc="left", color="black")
draw_line(ax2, 1, 3, 2.5, 3)

# R3005
draw_resistor(ax2, 2.5, 3, 5.5, 3, "R3005  24.3KΩ  1%", fontsize=10, fontprop=get_font(size=10), label_loc="top")

# TP3016 node
draw_dot(ax2, 5.5, 3, "TP3016", fontsize=9, fontprop=font, label_loc="top", color="gray")

# R3010 to GND
draw_resistor(ax2, 5.5, 3, 5.5, 1.2, "R3010\n4.7KΩ 1%", fontsize=10, fontprop=get_font(size=10), label_loc="right")
draw_ground(ax2, 5.5, 1.2)

# Output
draw_line(ax2, 5.5, 3, 8, 3)
draw_dot(ax2, 8, 3, "Vout = Vin × 0.162\n→ MCU ADC", fontsize=10, fontprop=get_font(size=10), label_loc="right", color="red")

# Formula
ax2.text(3, 4.2, "分压比 = R3010/(R3005+R3010) = 4.7/(24.3+4.7) ≈ 0.162",
         fontsize=9, ha="center", fontproperties=get_font(size=9), color="#555")

savefig(fig2, "circuit_01_divider.png")
print("✅ 图2 完成")


# ═══════════════════════════════════════════
# 图3: 系统框图
# ═══════════════════════════════════════════
fig3, ax3 = plt.subplots(1, 1, figsize=(14, 6.5))
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 6.5)
ax3.axis("off")
ax3.set_title("UBD1 电源检测电路 — 系统框图", fontsize=16, fontweight="bold", pad=20, fontproperties=get_font(size=16))

def box(ax, x, y, w, h, text, color="#E8F4FD", fontsize=10):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor="#333", linewidth=1.8)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, fontsize=fontsize, ha="center", va="center", fontproperties=get_font(size=fontsize))

def arrow(ax, x1, y1, x2, y2, color="#555"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", lw=2, color=color, mutation_scale=15))

# Row 1: Main signal path (top)
y_top = 4.2
box(ax3, 0.5, y_top, 2.2, 1.2, "UBD1 电源\n(被监测)", "#FFF3CD", 10)
box(ax3, 3.5, y_top, 2.5, 1.2, "Q3001 PNP 开关\n导通→集电极输出", "#D4E6F1", 9)
box(ax3, 7.0, y_top, 2.5, 1.2, "分压 + 滤波\nR3005/R3010 + C3001\n分压比 = 0.162", "#EBDEF0", 9)
box(ax3, 10.5, y_top, 2.5, 1.2, "MCU ADC\nUBD1_POWER_AN01[9]", "#FADBD8", 9)

# Row 2: Control path (bottom)
y_bot = 1.0
box(ax3, 0.5, y_bot, 2.5, 1.0, "控制信号\nDO_UBCTRL (P02.11)", "#D5F5E3", 9)
box(ax3, 3.5, y_bot, 2.5, 1.0, "Q3001 NPN 使能\n导通→拉低PNP基极", "#A9DFBF", 9)

# Arrows: main path
arrow(ax3, 2.7, y_top+0.6, 3.4, y_top+0.6)
arrow(ax3, 6.0, y_top+0.6, 6.9, y_top+0.6)
arrow(ax3, 9.5, y_top+0.6, 10.4, y_top+0.6)

# Arrow: control to NPN
arrow(ax3, 3.0, y_bot+0.5, 3.4, y_bot+0.5)

# Arrow: NPN to PNP (diagonal)
ax3.add_patch(FancyArrowPatch((3.5, y_bot+0.8), (4.75, y_top-0.5),
                               arrowstyle="->", lw=2, color="#8E44AD", mutation_scale=15,
                               connectionstyle="arc3,rad=0.3"))
ax3.text(3.8, 2.8, "R3000\n拉低基极", fontsize=9, fontproperties=get_font(size=9), ha="center", color="#8E44AD")

# Working principle
ax3.text(7.0, 0.3,
         "工作原理：DO_UBCTRL = H → NPN导通 → 集电极≈0V → R3000拉低PNP基极 →\n"
         "PNP导通(发射极=UBD1) → 集电极输出 → R3005/R3010分压(比0.162) → C3001滤波 → MCU ADC采集",
         fontsize=9, ha="center", color="#555", va="top", fontproperties=get_font(size=9))

savefig(fig3, "circuit_01_block.png")
print("✅ 图3 完成")
print("\n🎉 v4 matplotlib 手绘版完毕")
