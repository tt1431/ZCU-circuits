# 绘图脚本

每个电路对应一个脚本，统一输出到上级 `images/` 目录。

## 环境

```bash
pip install schemdraw matplotlib numpy
```

## 脚本命名

- `circuit_01_schematic.py` — 原理图
- `circuit_01_waveform.py` — 波形图
- `circuit_01_block.py` — 框图/流程图

## 通用配置

所有脚本使用统一主题：

- 中文字体：`WenQuanYi Micro Hei` 或 `Noto Sans CJK SC`
- 尺寸：图幅宽度 1920px，DPI 150
- 配色：深色标注 + 明亮的信号线
