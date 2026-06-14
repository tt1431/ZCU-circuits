# ZCU 绘图脚本

## 生成方式

```bash
python3 circuit_01_schematic.py
```

输出 `../images/` 中的辅助图：
- `circuit_01_divider.png` — 分压网络（schemdraw）
- `circuit_01_timing.png` — 控制时序图（matplotlib）
- `circuit_01_block.png` — 系统框图（matplotlib）

主原理图由天哥手绘，不在脚本中生成。

## 依赖

```bash
pip install matplotlib schemdraw numpy
```
