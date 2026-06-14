"""
ZCU 电路笔记 — 通用绘图配置
支持 schemdraw (电路原理图) + matplotlib (时序/框图)
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# ── 路径 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "..", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# ── 中文字体 ──
_CJK_FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Noto Sans CJK JP", "DejaVu Sans"],
    "axes.unicode_minus": False,
})

matplotlib.font_manager._load_fontmanager(try_read_cache=False)


def get_font(size=10):
    return FontProperties(fname=_CJK_FONT_PATH, size=size)


def savefig(fig, name, dpi=200):
    path = os.path.join(IMAGES_DIR, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.3, dpi=dpi)
    plt.close(fig)
    print(f"✅ {path}")
    return path


def save_schemdraw(drawing, name, dpi=200):
    path = os.path.join(IMAGES_DIR, name)
    drawing.save(path, dpi=dpi)
    print(f"✅ {path}")
    return path
