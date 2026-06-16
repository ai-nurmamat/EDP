# 🎯 SPAF - Sports Analytics Framework

> **全域感知型体育竞彩分析框架**
>
> **Domain-Aware, Situational-Awareness-Driven, Probability-Flow-Based Sports Analytics Optimization System**

![Version](https://img.shields.io/badge/Version-4.1-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-blue)

---

## ⚠️ 风险声明

> **本框架仅供学术研究与教育用途。**
>
> - 竞彩分析涉及**真实金融风险**。历史概率模式**不保证**未来结果。
> - 所有竞彩活动因设计原因具有**负期望值**（博彩公司边际）。任何系统都无法在数学上克服这一事实。
> - **永远不要投入您无法承受损失的资金。** 竞彩应被视为娱乐，而非投资。
> - 作者对框架产生的任何分析准确性、完整性或盈利能力**不作任何保证**。
> - 用户对自身决策承担全部责任，必须遵守**当地法律法规**。

---

## 目录

- [架构总览](#架构总览)
- [设计哲学](#设计哲学-ooda-循环--循环工程--有向图执行)
- [数据获取层](#数据获取层)
- [概率分析引擎](#概率分析引擎)
- [概率流向倍增效应](#概率流向倍增效应)
- [全域感知系统](#全域感知系统)
- [方案设计引擎](#方案设计引擎)
- [规则合规层](#规则合规层)
- [输出生成](#输出生成)
- [学术基础](#学术基础)
- [快速开始](#快速开始)
- [API文档](#api文档)
- [MCP集成](#mcp集成)
- [Skill集成](#skill集成)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    输出生成层 (Output Generation)            │
│  方案摘要 → 叙事生成 → 质量检查清单                          │
├─────────────────────────────────────────────────────────────┤
│                    方案设计引擎 (Scheme Design Engine)       │
│  风险分层 → 串关构建 → 预算分配                              │
├─────────────────────────────────────────────────────────────┤
│                    流向倍增引擎 (Flow Amplification Engine)   │
│  基础流向 → 方向一致性 → 梯度位置                            │
├─────────────────────────────────────────────────────────────┤
│                    全域感知系统 (Domain Awareness System)     │
│  比赛情报 ← 概率流向 ← 市场共识                              │
├─────────────────────────────────────────────────────────────┤
│                    概率分析引擎 (Probability Analysis Engine)│
│  真实概率 → 条件概率 → 流向分析                              │
├─────────────────────────────────────────────────────────────┤
│                    数据获取层 (Data Acquisition Layer)       │
│  可视化提取 ← 网页抓取 ← API集成                            │
└─────────────────────────────────────────────────────────────┘
```

系统采用**有向无环图 (DAG) 流水线架构**，每层产生结构化数据供下游消费。核心设计原则源自三种方法论：

1. **OODA循环** (Boyd, 1987) — 观察-定向-决策-执行，每层嵌入迭代精炼
2. **循环工程** — 通过反馈回路持续校准信号质量
3. **DAG执行** — 类似LangGraph的有状态图执行模型，节点间标准化协议

### 设计原则（不可妥协）

| 原则 | 描述 |
|------|------|
| **数据无关** | 输入源通过统一接口抽象；流水线可连接任何概率数据源 |
| **实现无关** | 概率提取可使用任何视觉识别、OCR引擎或手动输入 |
| **规则感知** | 所有输出方案必须在呈现前通过规则验证 |
| **领域优先** | 态势感知引导但绝不覆盖概率信号 |

---

## 设计哲学：OODA循环 × 循环工程 × 有向图执行

### 竞彩分析中的OODA循环映射

OODA循环由美国空军上校John Boyd开发（Boys, 1987, "A Discourse on Winning and Losing"），最初用于军事决策。其核心是**快速感知-定向-决策-行动**闭环。

```
┌──────────────────────────────────────────────────────────┐
│  Observe（观察）                                           │
│  ├─ 概率快照（初始 vs 最新）                              │
│  ├─ 比赛情报（排名、状态、伤停、战术）                     │
│  └─ 市场信号（成交量分布、专家共识）                       │
│                                                          │
│  Orient（定向）                                            │
│  ├─ 真实概率计算（边际移除）                              │
│  ├─ 概率流向计算（初始→最新变化量）                        │
│  ├─ 倍增评分（方向一致性 × 梯度位置）                      │
│  └─ 交叉验证（概率 vs 情报 vs 市场共识）                   │
│                                                          │
│  Decide（决策）                                            │
│  ├─ 三原则验证（每个选项必须通过）                        │
│  ├─ 方案构建（分层 + 串关 + 预算分配）                     │
│  └─ 混合串关合规检查                                      │
│                                                          │
│  Act（执行）                                               │
│  ├─ 生成叙事                                              │
│  ├─ 质量清单验证                                          │
│  └─ 收集反馈 → 进入下一个OODA循环                        │
└──────────────────────────────────────────────────────────┘
```

**终止条件**：
- 所有可用数据处理完毕 → 输出最终方案
- 用户预算完全分配 → 输出最终方案
- 死循环检测（相同数据迭代无新信号） → 强制停止并报告

---

## 数据获取层

### 可视化信息提取

平台截图包含结构化表格数据（概率历史、比分矩阵、盘口线）。提取流水线遵循**三阶段策略**：

1. **类型分类** — 确定图像内容类型（概率表、比分矩阵、盘口历史等）
2. **结构化提取** — 提取数值数据同时保留时间上下文（初始 vs 最新）
3. **验证** — 交叉检查提取数据一致性（如概率单调性、字段完整性）

> **框架说明**：提取后端可插拔。任何多模态识别方案、OCR引擎或手动输入系统都可作为实现。

### 统一数据模式

所有数据源产生符合统一模式的数据制品：

| 字段 | 类型 | 描述 |
|------|------|------|
| match_id | string | 唯一比赛标识符 |
| teams | object | { home, away } 球队名称 |
| timestamp | datetime | 数据采集时间戳 |
| markets.1X2 | time series | 胜/平/负真实概率（初始→最新） |
| markets.handicap | time series | 盘口概率（如 -1, -2, +2） |
| markets.total_goals | time series | 总进球数概率（0, 1, 2, ..., 7+） |
| markets.correct_score | time series | 比分概率（所有比分组合） |

---

## 概率分析引擎

### 真实概率

平台概率嵌入了博彩公司边际（overround）。要提取**真实概率**，需要进行标准化：

```python
P_true(outcome_i) = (1 / odds_i) / Σ(1 / odds_j) × 100%
```

**数学基础**：如果市场为结果 `i` 提供概率 `o_i`，隐含概率为 `1/o_i`。由于 `Σ(1/o_j) > 1`（即边际），除以总和得到归一化概率分布，所有结果总和为100%。

**学术支持**：此标准化等价于简化版**Shin方法** (Shin, 1992)。

### 条件概率

对于比分市场，计算**方向条件概率**：

```python
P(score | direction) = P_true(score) / Σ P_true(scores_in_direction)
```

**解决的问题**："假设主队获胜，每个具体比分的概率是多少？"

### 概率流向

概率流向是本框架的核心概念。它衡量市场真实概率分布随**时间的变化**：

```python
Flow(outcome) = P_true_latest(outcome) - P_true_initial(outcome)
```

| 流向 | 含义 |
|------|------|
| **正（流入）** | 市场越来越倾向于此结果 |
| **负（流出）** | 市场正在远离此结果 |
| **零（稳定）** | 无显著信息变化 |

**核心洞察**：正向流向表明知情资金（或信息）正在积累向此结果。幅度（百分点，pp）反映信心强度。

---

## 概率流向倍增效应

> ⚠️ **本章节描述了框架最强大的分析工具，也最危险。倍增效应是概率分析放大器——它可以放大正确信号，也可以放大错误信号。必须与全域感知系统结合使用。**

### 倍增效应定义

当概率流向显示资金从结果A流向结果B时，通常意味着同一方向梯度上的相邻结果**也在向同一方向流动**。这就是**倍增效应**。

### 倍增评分公式

```python
Amplification_Score(outcome) =
    Base_Flow(outcome) × Directional_Consistency × Gradient_Position
```

| 变量 | 含义 |
|------|------|
| `Base_Flow` | 此结果的基础概率流向（pp） |
| `Directional_Consistency` | 方向一致的相邻结果中正向流向的比例（0~1） |
| `Gradient_Position` | 概率梯度中的位置（概率越高 = 倍增潜力越大） |

### 倍增效应安全保障

**保障1：全域感知验证**

倍增效应必须与比赛情报进行交叉验证：

| 情报评估 | 流向方向 | 倍增判定 |
|----------|----------|----------|
| 强队 + 高进攻效率 | 正向大胜 | **确认** ✅ |
| 强队 + 保守风格 | 正向大胜 | **存疑** ⚠️ |
| 弱队 + 防守漏洞 | 正向大胜 | **增强** ✅✅ |
| 无明确情报 | 正向大胜 | **可能** ✅（降权） |

**保障2：基础流向阈值**

仅当基础流向（Base_Flow）≥ 阈值（建议2pp）时启用倍增效应。

**保障3：凯利准则变体**

凯利的核心思想——**根据信号强度调整投资比例**——被借用到方案设计中。

---

## 全域感知系统

### 态势感知定义

**全域感知** = 所有可用信息源的完整覆盖。

**态势感知** = 对当前比赛背景的实时理解。

### 比赛情报整合

| 情报维度 | 数据点 | 权重 |
|----------|--------|------|
| **实力指标** | FIFA排名、阵容价值、近期状态 | 高 |
| **战术背景** | 攻守风格、场均进球、零封场次 | 高 |
| **动机因素** | 出线形势、压力、阵容轮换 | 中 |
| **市场共识** | 成交量分布、专家预测一致性 | 中 |

### 信号验证矩阵

每个概率流向信号必须与比赛情报进行交叉验证：

```python
Confidence = Flow_Strength × Intelligence_Support × Market_Consensus
```

| 置信度 | 条件 | 操作 |
|--------|------|------|
| **高** | 三维一致 | 全权重纳入方案 |
| **中** | 两维一致 | 降权纳入 |
| **低** | 一维支持 | 仅纳入高概率小额组合 |
| **负** | 维度冲突 | 排除或作为逆向信号 |

---

## 方案设计引擎

### 三原则（不可妥协）

所有方案**必须**满足以下三个原则。违反任何原则的方案**不得输出**：

| # | 原则 | 实现规则 |
|---|------|----------|
| 1 | **尊重概率流向** | 每张彩票的每个选项必须有正向概率流向。零流向选项仅在无正向替代时方可接受。**负流向选项严格禁止。** |
| 2 | **尊重非对称收益** | 每张彩票必须提供有意义的回报潜力。最低目标：3倍回报。保守"安全票"预算不超过总预算的20%。 |
| 3 | **尊重规则** | 同一比赛不同玩法不可串关。比分最高4串。单票最高99倍。单票最高¥20,000。 |

**三原则优先级**：原则1 > 原则3 > 原则2。

### 混合串关完整规则

#### 基本规则

| 规则 | 描述 |
|------|------|
| **不同比赛可混合** | 不同比赛的不同玩法**可以**串关 |
| **同一比赛不可混合** | 同一比赛的不同玩法**不可**串关 |
| **最低投注** | 每个组合最低¥2 |
| **单票倍数上限** | 单票最高99倍 |
| **单票金额上限** | 单票最高¥20,000 |

#### 串关深度限制

| 包含比分/半场 | 最大串关深度 |
|---------------|--------------|
| 无 | 最高8串 |
| 包含比分 | 最高4串 |
| 包含半场 | 最高4串 |
| 包含总进球 | 最高6串 |

---

## 规则合规层

### 验证流水线

每个生成的彩票必须通过以下验证流水线：

```
对于每个彩票：
  ✓ 1. 无来自同一比赛不同玩法的选项
  ✓ 2. 包含比分/半场 → 总串关深度 ≤ 4
  ✓ 3. 每注 × 组合数 ≤ ¥50（单张实体彩票限制）
  ✓ 4. 每注 ≥ ¥2
  ✓ 5. 倍数 ≤ 99
  ✓ 6. 所有选项有正向概率流向
  ✓ 7. 彩票提供有意义的上涨空间（非锚定彩票 ≥ 3倍）
```

---

## 输出生成

### 多层输出

| 层级 | 受众 | 内容 |
|------|------|------|
| **分析报告** | 分析师 | 完整概率流向表、信号强度、情报交叉验证 |
| **方案摘要** | 用户 | 彩票列表、成本、预期回报、覆盖图 |
| **叙事** | 运营者 | 简洁的文字说明 |

### 质量检查清单

呈现给用户前，所有方案必须通过每项检查：

- [ ] 所有选项有正向概率流向
- [ ] 所有选项有比赛情报支持（或明确标记为"纯流向"信号）
- [ ] 无规则违规
- [ ] 总成本与用户预算一致
- [ ] 每张彩票成本计算已验证
- [ ] 玩法多样性覆盖
- [ ] 比赛覆盖达标
- [ ] 无重复彩票组合
- [ ] 叙事明确无歧义

---

## 学术基础

### 核心理论基础

| 理论 | 文献 | 应用 |
|------|------|------|
| Shin赔率分解 | Shin (1992) | 真实概率提取 |
| 贝叶斯更新 | Gelman et al. (2013) | 概率流向解读 |
| 凯利准则 | Kelly (1956) | 资金分配启发式 |
| 时间序列动量 | Moskowitz et al. (2012) | 倍增效应基础 |
| 信息级联 | Banerjee (1992) | 从众行为建模 |
| 前景理论 | Kahneman & Tversky (1979) | 偏差缓解 |
| 现代投资组合理论 | Markowitz (1952) | 多元化策略 |
| 预测市场定价 | Wolfers & Zitzewitz (2006) | 概率解读基础 |
| OODA循环 | Boyd (1987) | 运营架构 |

完整文献列表请参见 [docs/theory/references.md](docs/theory/references.md)

---

## 快速开始

### 安装

```bash
# Python
pip install spaf-framework

# JavaScript/TypeScript
npm install spaf-framework
```

### Python 示例

```python
from spaf import (
    ProbabilityEngine,
    FlowAmplificationEngine,
    DomainAwarenessSystem,
)

# 初始化引擎
engine = ProbabilityEngine()
amplifier = FlowAmplificationEngine()
awareness = DomainAwarenessSystem()

# 计算真实概率
result = engine.calculate_true_probability({'home': 1.5, 'draw': 4.0, 'away': 6.0})

# 分析概率流向
flow_report = engine.analyze_flow(initial_snapshot, latest_snapshot)

# 计算倍增效应
amp_report = amplifier.calculate_amplification(flow_report, outcome_probs)

# 全域感知分析
domain_report = awareness.analyze_match(match_intel, flow_confidences)
```

### TypeScript 示例

```typescript
import { ProbabilityEngine, FlowAnalyzer, SchemeDesigner } from 'spaf-framework';

const engine = new ProbabilityEngine();
const analyzer = new FlowAnalyzer();
const designer = new SchemeDesigner();

const trueProbs = engine.calculateTrueProbability({ home: 1.5, draw: 4.0, away: 6.0 });
const flowReport = analyzer.analyzeFlow(initialProbs, latestProbs);
const schemes = designer.generateSchemes(flowReport, { budget: 100 });
```

更多示例请参见 [examples/](examples/) 目录。

---

## API文档

完整API文档请参见 [docs/api/](docs/api/)。

---

## MCP集成

本框架提供MCP（Model Context Protocol）服务器，使AI助手能够直接调用分析能力。

### 配置

```json
{
  "mcpServers": {
    "spaf": {
      "command": "spaf-mcp-server",
      "args": []
    }
  }
}
```

### 可用工具

- `calculate_true_probability` - 计算真实概率
- `analyze_flow` - 分析概率流向
- `calculate_amplification` - 计算倍增效应
- `validate_scheme` - 验证方案合规性
- `generate_schemes` - 生成优化方案

详细文档请参见 [mcp/README.md](mcp/README.md)。

---

## Skill集成

本框架可用作AI Agent Skill，支持快速集成到各种AI助手中。

详细文档请参见 [skill/README.md](skill/README.md)。

---

## 贡献指南

我们欢迎社区贡献！请参见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-org/spaf-framework.git
cd spaf-framework

# Python 开发
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# JavaScript 开发
npm install
npm run build
```

### 运行测试

```bash
# Python 测试
pytest tests/python/

# JavaScript 测试
npm test
```

---

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

---

## 免责声明

**本框架仅供学术研究与教育用途。**

- 本框架不构成任何投资建议或博彩建议。
- 使用本框架做出的任何决策由用户自行承担责任。
- 作者不对使用本框架造成的任何损失负责。
- 请遵守您所在地区的法律法规。

---

*通过结构化分析、严格概率论和全域认知提供边际优势——同时承认在竞彩分析中，概率本身永远有最终发言权。*

*© 2026 — 仅供学术研究与教育用途。*
