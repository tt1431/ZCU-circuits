"""
Demo：用 schemdraw 画一个简单的分压/滤波电路
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from common import save_schemdraw, setup_chinese_font

import schemdraw
import schemdraw.elements as elm

setup_chinese_font()

d = schemdraw.Drawing()

# ── 画一个 RC 低通滤波电路 ──
d += elm.SourceSin().label("Vin").up()
d += elm.Resistor().right().label("R1")
d += elm.Capacitor().down().label("C1")
d += elm.Ground()
d += elm.Line().left()

d.draw()
path = save_schemdraw(d, "demo_rc_filter.png")
print(f"Demo 电路图已生成: {path}")
