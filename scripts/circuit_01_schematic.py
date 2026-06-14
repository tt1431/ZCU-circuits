"""
电路 01 — UBD1 电源检测电路 原理图
ZCU 项目 | 经纬恒润
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import save_schemdraw, setup_chinese_font
import schemdraw
import schemdraw.elements as elm

setup_chinese_font()

# ═══════════════════════════════════════════
# 图1: UBD1 电源检测电路总图
# ═══════════════════════════════════════════
d = schemdraw.Drawing(fontsize=11)

# ── UBD1 电源输入 ──
d += elm.Dot(open=True).label("UBD1", loc="left")

# ── 上支路：ADC 电压采样 ──
d.push()
d += elm.Line().up().length(0.6)
d += elm.ResistorIEC().right().label("R3005\n24.3K 1%", fontsize=8).length(2.5)
d += elm.Dot().label("TP3016", loc="top", fontsize=7)

# C3001 + R3010 并联到地
d.push()
d += elm.ResistorIEC().down().label("R3010\n4.7K 1%", fontsize=8)
d += elm.Ground()
d.pop()
d.push()
d += elm.Capacitor().down().label("C3001\n10nF", fontsize=7).length(1.5)
d += elm.Ground()
d.pop()

# ADC 输出
d += elm.Line().right().length(1)
d += elm.Dot(open=True).label("UBD1_POWER_AN01 [9]", loc="right", fontsize=8)
d += elm.Label("→ MCU ADC", loc="right", fontsize=7, color="blue")
d.pop()

# ── 下支路：三极管数字检测 ──
d += elm.Line().down().length(0.6)
d += elm.ResistorIEC().right().label("R3000\n10K", fontsize=8).length(2.5)
d += elm.Label("(基极限流)", loc="top", fontsize=7, color="gray")
d += elm.BjtNpn().label("Q3001\nNSVMUN5", fontsize=8)
d += elm.Line().down().length(0.5)
d += elm.Ground()

# 集电极上拉到 3.3V
d += elm.Line().up().length(0.6).at(d.here)
d += elm.ResistorIEC().right().label("R3806\n4.7K 5%", fontsize=8, loc="bottom")
d += elm.Line().right().length(0.3)
d += elm.Vdd().label("3.3V", fontsize=9)

# GPIO 输出
d += elm.Line().right().length(0.5)
d += elm.Dot(open=True).label("→ MCU GPIO", loc="right", fontsize=8, color="blue")

d.draw()
save_schemdraw(d, "circuit_01_ubd1_schematic.png")
print("✅ 图1 完成")


# ═══════════════════════════════════════════
# 图2: 电阻分压网络详解
# ═══════════════════════════════════════════
d2 = schemdraw.Drawing(fontsize=12)
d2 += elm.Dot(open=True).label("UBD1 (Vin)", loc="left")
d2 += elm.Line().right().length(0.3)
d2 += elm.ResistorIEC().right().label("R3005\n24.3KΩ", fontsize=10).length(3)
d2 += elm.Dot()
d2 += elm.Line().right().length(1.2)
d2 += elm.Dot(open=True).label("Vout = Vin×0.162", loc="right", fontsize=9, color="red")

d2.push()
d2 += elm.ResistorIEC().down().label("R3010\n4.7KΩ", fontsize=10)
d2 += elm.Ground()
d2.pop()

d2.draw()
save_schemdraw(d2, "circuit_01_divider.png")
print("✅ 图2 完成")


# ═══════════════════════════════════════════
# 图3: 系统框图
# ═══════════════════════════════════════════
from common import set_mpl_style, IMAGES_DIR, savefig, get_font
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

set_mpl_style()
font = get_font(size=11)
font_bold = get_font(size=11)
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("UBD1 电源检测电路 — 系统框图", fontsize=16, fontweight="bold", pad=20, fontproperties=get_font(size=16))

def box(ax, x, y, w, h, text, color="#E8F4FD", fontsize=10, bold=False):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                     facecolor=color, edgecolor="#333", linewidth=1.5)
    ax.add_patch(rect)
    kw = {"fontsize": fontsize, "ha": "center", "va": "center", "fontproperties": get_font(size=fontsize)}
    ax.text(x + w/2, y + h/2, text, **kw)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#555"))

# Boxes
box(ax, 0.5, 3.5, 2.5, 1, "UBD1 电源\n(被监测电源)", "#FFF3CD", 10)
box(ax, 4, 4.5, 2.5, 1, "路径A：电阻分压\nR3005 + R3010\n降压比 = 0.162", "#E8F4FD", 9)
box(ax, 4, 2, 2.5, 1, "路径B：三极管开关\nQ3001 + R3000\n晶体管 ON/OFF", "#E8F4FD", 9)
box(ax, 7.5, 4.5, 3.5, 1, "MCU ADC 输入\nUBD1_POWER_AN01\n测量模拟电压值", "#D4EDDA", 9)
box(ax, 7.5, 2, 3.5, 1, "MCU GPIO 输入\n数字高/低电平\n判断电源有无", "#D4EDDA", 9)

# Arrows
arrow(ax, 3, 4, 4, 5)
arrow(ax, 3, 3.5, 4, 2.5)
arrow(ax, 6.5, 5, 7.5, 5)
arrow(ax, 6.5, 2.5, 7.5, 2.5)

# Annotation
ax.text(6, 1.2, "• 路径A：电阻分压 → ADC监测电压（精确测量，可用于欠压/过压告警）\n• 路径B：三极管开关 → GPIO检测通断（快速判断，用于时序控制、故障检测）",
        fontsize=9, ha="center", color="#666", va="top", fontproperties=get_font(size=9))

savefig(fig, "circuit_01_block.png")
print("✅ 图3 完成")
print("\n🎉 全部电路图绘制完毕")
