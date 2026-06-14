"""
电路 01 — UBD1 双三极管电子开关 — 辅助图生成
生成：分压网络 / 控制时序 / 系统框图
主原理图由天哥手绘，不在此脚本中生成
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import get_font, savefig, save_schemdraw

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

import schemdraw
import schemdraw.elements as elm

# ═══════════════════════════════════════════════════════
# 图 1：分压网络详解
# ═══════════════════════════════════════════════════════
print("图 1：分压网络详解")

d = schemdraw.Drawing(fontsize=11, unit=2.0)
d += elm.Dot(open=True).label("Vin\n(UBD1)", loc="left", fontsize=10)
d += elm.Line().right().length(0.5)
d += elm.Resistor().right().label("R3\n24.3K 1%", loc="top", fontsize=10)
d += elm.Line().right().length(0.5)
d += (MID := elm.Dot(open=True))
d += elm.Line().down().at(MID.start).length(0.5)
d += elm.Resistor().down().label("R4\n4.7K 1%", loc="right", fontsize=10)
d += elm.Ground()
d += elm.Line().right(0.8).at(MID.start)
d += elm.Capacitor().down().label("C1\n10nF", loc="right", fontsize=9)
d += elm.Ground()
d += elm.Line().right().at(MID.start).length(1.2)
d += elm.Dot(open=True).label("Vout = Vin ×\nR4/(R3+R4)\n≈ Vin × 0.162", loc="right", fontsize=10)
d.draw()
d.fig.fig.set_size_inches(11, 5)
d.fig.fig.subplots_adjust(top=0.90)
d.fig.fig.suptitle("分压网络 + RC 低通滤波", fontsize=13, fontweight="bold")
save_schemdraw(d, "circuit_01_divider.png", dpi=250)
print("✅ 分压网络 完成\n")

# ═══════════════════════════════════════════════════════
# 图 2：控制时序图
# ═══════════════════════════════════════════════════════
print("图 2：控制时序图")

fig, axes = plt.subplots(4, 1, figsize=(12, 7), sharex=True)
font = get_font(9)

t = np.linspace(0, 10, 2000)
ctrl = np.where((t >= 2) & (t < 8), 3.3, 0.0)
q1_on = np.where(t >= 2.01, 1.0, 0.0); q1_on[t >= 8.01] = 0.0
q2_on = np.where(t >= 2.02, 1.0, 0.0); q2_on[t >= 8.02] = 0.0

tau = 0.00004
adc = np.zeros_like(t)
m = t >= 2.02; adc[m] = 1.94 * (1 - np.exp(-(t[m] - 2.02) / tau))
m2 = t >= 8.02; adc[m2] = 1.94 * np.exp(-(t[m2] - 8.02) / tau)

colors = ["#1565C0", "#2E7D32", "#E65100", "#C62828"]
labels = ["控制信号", "Q1 状态", "Q2 状态", "ADC 读数"]

axes[0].plot(t, ctrl, color=colors[0], lw=2.2)
axes[1].plot(t, q1_on * 3.3, color=colors[1], lw=2.2)
axes[2].plot(t, q2_on * 12, color=colors[2], lw=2.2)
axes[3].plot(t, adc, color=colors[3], lw=2.2)

for i, (ax, label) in enumerate(zip(axes, labels)):
    ax.set_ylabel(label, fontsize=8.5, fontproperties=font)
    ax.grid(True, alpha=0.25)
    ax.tick_params(labelsize=8)
for ax in axes:
    ax.axvline(2, color="gray", ls=":", lw=1, alpha=0.5)
    ax.axvline(8, color="gray", ls=":", lw=1, alpha=0.5)

axes[-1].set_xlabel("时间", fontsize=10, fontproperties=font)
fig.suptitle("电子开关 — 控制时序图", fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout()
savefig(fig, "circuit_01_timing.png")
print("✅ 时序图 完成\n")

# ═══════════════════════════════════════════════════════
# 图 3：系统框图
# ═══════════════════════════════════════════════════════
print("图 3：系统框图")

fig, ax = plt.subplots(1, 1, figsize=(14, 5.5))
ax.set_xlim(0, 15); ax.set_ylim(0, 6); ax.axis("off")

font10 = get_font(10); font9 = get_font(9)

def box(ax, x, y, w, h, text, color, fsize=10):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                       facecolor=color, edgecolor="#444", linewidth=2, alpha=0.9)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, fontsize=fsize, ha="center", va="center",
            fontproperties=get_font(fsize))

def arrow(ax, x1, y1, x2, y2, c="#555"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=c, lw=2))

y = 4.0
box(ax, 0.3, y, 2.8, 1.2, "UBD1 电源", "#FFF3CD", 10)
box(ax, 3.8, y, 3.0, 1.2, "电子开关\nQ1 + Q2 级联", "#BBDEFB", 10)
box(ax, 7.8, y, 3.0, 1.2, "分压 + 滤波\nR3/R4 + C1", "#E1BEE7", 10)
box(ax, 11.5, y, 2.8, 1.2, "MCU ADC\n12-bit", "#FFCDD2", 10)
arrow(ax, 3.1, y+0.6, 3.75, y+0.6)
arrow(ax, 6.8, y+0.6, 7.75, y+0.6)
arrow(ax, 10.8, y+0.6, 11.45, y+0.6)

y2 = 1.6
box(ax, 0.3, y2, 2.8, 1.0, "MCU GPIO\n控制信号", "#C8E6C9", 10)
box(ax, 3.8, y2, 3.0, 1.0, "Q1 驱动级", "#A5D6A7", 10)
arrow(ax, 3.1, y2+0.5, 3.75, y2+0.5, "#388E3C")

ax.annotate("", xy=(5.3, y), xytext=(5.3, y2+1.0),
            arrowprops=dict(arrowstyle="->", color="#7B1FA2", lw=2.5))
ax.text(5.8, 2.8, "R2 驱动", fontsize=9, ha="center", fontproperties=font9, color="#7B1FA2")

fig.suptitle("UBD1 电源检测 — 系统框图", fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout()
savefig(fig, "circuit_01_block.png")
print("✅ 系统框图 完成\n")

print("=" * 50)
print("全部 3 张辅助图生成完毕")
