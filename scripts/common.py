"""
ZCU 电路笔记 — 通用绘图配置
"""

import matplotlib
matplotlib.use("Agg")  # 非交互后端，必须最先设置

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import os

# ── 路径 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "..", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# ── 中文字体 (全局配置) ──
_CJK_FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
_CJK_FONT = FontProperties(fname=_CJK_FONT_PATH)
_CJK_FONT_NAME = "Noto Sans CJK JP"

# 配置 matplotlibrc
matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [_CJK_FONT_NAME, "DejaVu Sans"],
    "axes.unicode_minus": False,
})

# 确保在 rcParams 已改后重建字体缓存
matplotlib.font_manager._load_fontmanager(try_read_cache=False)


def get_font(size=10):
    """返回中文字体 FontProperties 对象"""
    return FontProperties(fname=_CJK_FONT_PATH, size=size)


def setup_chinese_font():
    """兼容旧调用——已经在上方全局设置过了"""
    pass


# ── matplotlib 全局样式 ──
def set_mpl_style():
    """设置统一的 matplotlib 样式"""
    plt.rcParams.update({
        "figure.dpi": 150,
        "figure.figsize": (12, 6),
        "font.size": 12,
        "axes.linewidth": 1.2,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    })


# ── schemdraw 通用配置 ──
def setup_schemdraw():
    """返回基本的 schemdraw 配置"""
    import schemdraw
    schemdraw.use("svg")
    return schemdraw


def savefig(fig, name, dpi=150):
    """保存 matplotlib figure 到 images/ 目录"""
    path = os.path.join(IMAGES_DIR, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.2, dpi=dpi)
    plt.close(fig)
    print(f"✅ 已保存: {path}")
    return path


def save_schemdraw(drawing, name):
    """保存 schemdraw Drawing 到 images/ 目录"""
    path = os.path.join(IMAGES_DIR, name)
    drawing.save(path)
    print(f"✅ 已保存: {path}")
    return path
