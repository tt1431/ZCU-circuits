"""
ZCU 电路笔记 — 通用绘图配置
"""

import matplotlib.pyplot as plt
import matplotlib
import os

# ── 路径 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "..", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# ── 中文字体 ──
def setup_chinese_font():
    """配置中文字体（优先选用系统常见中文字体）"""
    candidates = [
        "WenQuanYi Micro Hei",
        "Noto Sans CJK SC",
        "Noto Sans SC",
        "SimHei",
        "Microsoft YaHei",
        "DejaVu Sans",  # fallback
    ]
    for name in candidates:
        try:
            matplotlib.font_manager.findfont(name, fallback_to_default=False)
            plt.rcParams["font.sans-serif"] = [name]
            break
        except Exception:
            continue
    plt.rcParams["axes.unicode_minus"] = False


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
    setup_chinese_font()


# ── schemdraw 通用配置 ──
def setup_schemdraw():
    """返回基本的 schemdraw 配置"""
    import schemdraw
    schemdraw.use("svg")  # 使用 SVG 后端保证清晰度
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
