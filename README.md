# ZCU 电路笔记

ZCU（区域控制单元）电路分析笔记 —— 从原理到面试，一份搞定。

## 📂 目录

| 编号 | 名称 | 核心架构 |
|:--|:--|:--|
| 01 | [UBD1 双三极管电子开关](circuits/circuit_01_ubd1_power_detection.md) | PNP+NPN 级联 |

## 📐 图例

所有原理图/时序图/框图均由 Python 生成（schemdraw + matplotlib），源码在 `scripts/` 目录。

### 电路 01 — 配图清单

| 图 | 内容 | 工具 |
|:--|:--|:--|
| `circuit_01_full_schematic.png` | 完整电路原理图 | schemdraw |
| `circuit_01_switch_core.png` | 电子开关核心（PNP+NPN级联） | matplotlib |
| `circuit_01_divider.png` | 分压网络 + RC滤波 | schemdraw |
| `circuit_01_timing.png` | 控制信号时序图 | matplotlib |
| `circuit_01_block.png` | 系统框图 | matplotlib |

## 🛠 使用方式

```bash
# 生成全部电路图
cd scripts
python3 circuit_01_schematic.py
```

## 📝 模板

新电路笔记请用 [TEMPLATE.md](TEMPLATE.md)。

---

> 📅 2026-06 | 经纬恒润 ZCU 项目
