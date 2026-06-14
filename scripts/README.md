# ZCU 绘图脚本

所有电路图用 Python 生成，保证可复现、可修改。

## 依赖

```bash
pip install matplotlib schemdraw numpy
```

## 脚本说明

| 脚本 | 输出 |
|:--|:--|
| `common.py` | 通用配置（字体、路径、保存函数） |
| `circuit_01_schematic.py` | 电路 01 全部 5 张图 |

## 生成方式

```bash
python3 circuit_01_schematic.py
```

输出在 `../images/` 目录。

## 工具选择

- **schemdraw** — 电路原理图（三极管、电阻、电容等标准符号）
- **matplotlib** — 时序图、框图、需要中文标注的复杂图
