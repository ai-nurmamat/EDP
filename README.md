# EDP — 期望域感知方法（Expectation Domain Perception Method）

> **多源情报融合与概率态势感知框架**

> *A Multi-Source Intelligence Fusion and Probabilistic Situation Awareness Framework*

---

## 1. 概述 Overview

**期望域感知方法（Expectation Domain Perception Method, EDP）** 是一套用于**概率分析与统计研究**的学术计算框架。它整合了四个协同工作的分析层，从原始市场报价出发，经贝叶斯推断与时间序列动量分析，最终输出多源情报融合后的态势评估与资源分配方案。

本框架的设计遵循以下核心原则：

1. **概率公理化基础** —— 所有计算严格服从 Kolmogorov 概率公理；
2. **贝叶斯证据累积** —— 按序处理来自独立来源的情报，以共轭先验实现解析后验更新；
3. **时间序列动量分析** —— 基于 Moskowitz 等人的动量范式（2012），检测概率质量在结果空间的流动；
4. **多源情报融合** —— 融合加权线性意见池、对数优比池与 DeGroot 共识动力学；
5. **信息级联检测** —— 识别潜在的羊群效应与证据冗余；
6. **最优资本分配** —— 结合 Kelly 准则与 Markowitz 组合理论，实现带约束的资源分配。

⚠️ **本框架仅供学术研究与教育用途。历史概率模式不保证未来结果。本框架不构成任何投资建议或决策建议。**

---

## 2. 五层堆叠式分析架构 Five-Layer Analytical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  第 5 层 · 资源分配层  Resource Allocation                    │
│  Kelly Criterion · Markowitz Portfolio Theory · Three Principles  │
├──────────────────────────────────────────────────────────────┤
│  第 4 层 · 全域感知层  Domain Awareness                      │
│  Multi-Source Intelligence Fusion · Evidence Combination     │
│  Consensus Dynamics · Anomaly Detection · Cascade Detection  │
├──────────────────────────────────────────────────────────────┤
│  第 3 层 · 流向倍增层  Flow Amplification                    │
│  Base Flow → Directional Consistency → Gradient Position     │
│  Market Momentum → Amplification Score                       │
├──────────────────────────────────────────────────────────────┤
│  第 2 层 · 贝叶斯推断层  Bayesian Inference                  │
│  Beta-Binomial Conjugacy · Shin Marginal Decomposition       │
│  Glicko-2 Rating System · Credible Intervals                 │
├──────────────────────────────────────────────────────────────┤
│  第 1 层 · 概率分析层  Probability Analysis                  │
│  Market Quotes → Shin Normalization → True Probabilities     │
│  Conditional Probabilities → Flow Analysis                   │
├──────────────────────────────────────────────────────────────┤
│  第 0 层 · 数据获取层  Data Acquisition                      │
│  Snapshot Collection · Quality Validation · Standard Interface│
└──────────────────────────────────────────────────────────────┘
```

---

## 3. 数学基础 Mathematical Foundations

### 3.1 Shin 归一化方法 — 真实概率的提取

市场报价包含边际利润（"overround"），无法直接解释为概率。Shin（1992）提出的模型假设边际与"内幕交易者"的存在成比例，从而从报价中反解出"真实概率"。

**问题形式化**：给定 N 个结果的报价 *q₁, q₂, ..., qN*，其中 *qᵢ > 1* 为小数报价。

**隐含概率**：πᵢ = 1/qᵢ。市场边际 *overround* 为：

> Σᵢ₌₁ᴺ πᵢ - 1 > 0

**Shin 迭代法**求解真实概率 *p*：

> pᵢ^{(k+1)} = (πᵢ − zᵏ √pᵢᵏ) / (1 − zᵏ Σⱼ √pⱼᵏ)

其中 *z* 为内幕交易比例估计，迭代直至 |pᵢᵏ⁺¹ − pᵢᵏ| < ε。

**参考**：Shin, H.S. (1992). *Prices of State-Contingent Claims with Insider Traders*. Economic Journal, 102(411), 426-435.

### 3.2 Beta-Binomial 共轭贝叶斯推断

对于 Bernoulli 试验，采用 Beta 分布作为共轭先验：

- **先验**：Beta(α₀, β₀)
- **观察**：在 *n* 次试验中获得 *k* 次成功
- **后验**：Beta(α₀ + k, β₀ + n − k)

**后验均值**：

> E[p | evidence] = (α₀ + k) / (α₀ + β₀ + n)

**95% 可信区间**采用正态近似：

> CI₉₅ = p̂ ± 1.96 × √(p̂(1 − p̂)/(n_eff + 1))

**参考**：Gelman, A., Carlin, J.B., Stern, H.S., & Rubin, D.B. (2013). *Bayesian Data Analysis*, 3rd ed. Chapman & Hall/CRC.

### 3.3 Glicko-2 评级系统

对 Elo 系统的改进，引入评级偏差（RD）与波动率（σ），提供更稳健的动态实力建模。

**核心更新方程**（在 Glicko-2 尺度：μ, φ, σ）：

> E(μ, μⱼ, φⱼ) = 1 / (1 + exp(−g(φⱼ)(μ − μⱼ)))

> g(φ) = 1 / √(1 + 3φ²/π²)

> ν = [Σⱼ g(φⱼ)² E(1 − E)]⁻¹

> Δ = ν · Σⱼ g(φⱼ) (sⱼ − E)

其中 ν 为估计方差，Δ 为改进偏差。

**参考**：Glickman, M.E. (1999). *Parameter Estimation in Large Dynamic Paired Comparison Systems*. Applied Statistics, 48(3), 377-394.

### 3.4 概率流向分析

**定义**（在时间 Δt 内）：

> Flowᵢ = pᵢ(t + Δt) − pᵢ(t)

**时间序列动量评分**（Moskowitz et al., 2012）：

> momentum_score = Σ_t w_t · flow_t, 其中 Σ_t w_t = 1

**速度与加速度**：

> vᵢ = d(Flowᵢ) / dt,  aᵢ = d²(Flowᵢ) / dt²

**显著性阈值**：|flow| < 0.5% 稳定；0.5%–2% 低显著；2%–5% 中显著；≥5% 高显著。

### 3.5 流向倍增评分

对结果 *i* 的倍增评分综合四要素：

> AmpScoreᵢ = BaseFlowᵢ × DirConsistᵢ × (1 + GradientPosᵢ) × MarketMomentum

- **方向一致性** *DirConsistᵢ*：相邻结果流向与目标结果同向的比例
- **梯度位置** *GradientPosᵢ*：归一化概率水平——低概率结果具有更高倍增潜力
- **市场动量** *MarketMomentum*：全体结果的平均动量

### 3.6 多源情报融合

采用**混合融合策略**——线性池与对数优比池的加权组合：

**线性意见池**（Cooke, 1991）：

> p_linear = Σᵢ wᵢ · pᵢ, 其中 Σᵢ wᵢ = 1

**对数优比意见池**（Genest & Zidek, 1986）：

> logit(p_logodds) = Σᵢ wᵢ · logit(pᵢ)

**混合估计**：

> p_fused = α · p_linear + (1 − α) · p_logodds,  α ∈ [0, 1]

**源权重**由三维构成：

> wᵢ = reliabilityᵢ × confidenceᵢ × temporal_decayᵢ

> temporal_decayᵢ = 2^(−Δtᵢ / t½)

**共识评分**（基于源估计的离散度）：

> Consensus = 1 − min(σ_observed / σ_max, 1.0)

其中 σ_max = 0.5 为 Bernoulli(p=0.5) 的理论最大标准差。

### 3.7 Kelly 最优资本分配

Kelly 准则最大化对数财富的期望增长率：

> f* = (p · b − q) / b = (p(b + 1) − 1) / b

其中：*p* 为成功概率，*b* 为净赔率（小数报价 − 1），*q = 1 − p*。

**分数 Kelly**（本框架默认 quarter-Kelly, 即 1/4）：

> f = κ · f*,  κ ∈ (0, 1]

用于控制波动率，代价是降低期望增长速率。

**资本分配的三大原则**：
1. **信号对齐原则**：仅分配给具有正概率流向信号的结果
2. **非对称潜力原则**：要求赔率与概率乘积满足正期望条件
3. **风险分散原则**：分配集中度 cap ≤ 20%，并维持多样化比

---

## 4. 核心引擎 Core Engines

### 4.1 ProbabilityEngine — 概率分析引擎

| 功能模块 | 理论基础 | 输出 |
|---------|---------|------|
| 真实概率计算 | Shin 归一化 / 迭代法 | p_true, margin, CI |
| 条件概率推断 | 贝叶斯条件定义 | p(A \| B) |
| 贝叶斯更新 | Beta-Binomial 共轭模型 | posterior α, β, CI |
| 先验融合 | 对数池 / 线性池 | 组合后验 |
| Glicko-2 评级 | Glickman (1999) | μ, RD, σ |
| 流向分析 | 时间序列动量 | flow_velocity, acceleration |

### 4.2 FlowAnalyzer — 流向倍增引擎

| 功能模块 | 理论基础 | 输出 |
|---------|---------|------|
| 基础流向 | 差分时间序列 | Δp, v, a |
| 方向一致性 | 邻接结构评分 | 0 – 1 一致性系数 |
| 梯度位置 | 概率空间逆映射 | 0 – 1 倍增潜力 |
| 市场动量 | 加权聚合动量 | aggregate_momentum |
| 级联风险 | 信息级联理论 | 风险等级标记 |

### 4.3 DomainAwarenessEngine — 全域感知引擎

| 功能模块 | 理论基础 | 输出 |
|---------|---------|------|
| 情报预处理 | 源可靠性评级（STANAG 2511 改编） | w_i, 归一化权重 |
| 线性池融合 | Cooke (1991) 意见池 | p_linear |
| 对数优比融合 | Genest & Zidek (1986) | p_logodds |
| 贝叶斯累积 | Pearl (1988) 序贯更新 | 后验对数优比 |
| 共识分析 | 方差-离散度变换 | consensus_score |
| 异常检测 | Z-score 阈值法 | anomaly list |
| 级联检测 | 信息级联理论 Bikhchandani (1992) | potential_cascade 标记 |
| 态势评估 | 稳定性分类器 | aggregate_probability, confidence, status |

### 4.4 AllocationEngine — 资源分配引擎

| 功能模块 | 理论基础 | 输出 |
|---------|---------|------|
| 合法性检验 | 三大分配原则 | valid / warning / invalid |
| Kelly 分配 | Kelly (1956) 信息率准则 | fraction, amount |
| 风险分层 | 概率-赔率映射 | conservative / balanced / aggressive / extreme |
| Markowitz 再平衡 | 集中度约束 + 多样化比 | 优化后分配 |
| 组合统计 | 期望价值 / 风险贡献 | portfolio_EV, diversification_ratio |

---

## 5. 实现规范 Implementation Specifications

### 5.1 技术栈

| 层面 | 技术 |
|-----|------|
| 编程语言 | Python 3.10+, TypeScript 5.0+ |
| 类型安全 | 完整类型标注 (dataclass, Enum) |
| 数值精度 | IEEE 754 double-precision |
| 收敛准则 | ε = 1e-10 (Shin 迭代) |
| 收敛上限 | 100 次迭代 |

### 5.2 代码质量与验证

- **Linting**: 静态语法与风格检查
- **格式化**: 标准风格统一格式化
- **类型检查**: MyPy 静态类型验证
- **测试框架**: pytest (Python) / Jest (TypeScript)

---

## 6. 关键文献 Key References

| 理论 / 方法 | 文献 |
|-----------|------|
| Shin 归一化 | Shin, H.S. (1992). *Prices of State-Contingent Claims with Insider Traders*. Economic Journal, 102(411), 426-435. |
| 贝叶斯推断 | Gelman, A., Carlin, J.B., Stern, H.S., & Rubin, D.B. (2013). *Bayesian Data Analysis*, 3rd ed. Chapman & Hall/CRC. |
| 时间序列动量 | Moskowitz, T.J., Ooi, Y.H., & Pedersen, L.H. (2012). *Time Series Momentum*. Journal of Financial Economics, 104(2), 228-250. |
| Glicko-2 评级 | Glickman, M.E. (1999). *Parameter Estimation in Large Dynamic Paired Comparison Systems*. Applied Statistics, 48(3), 377-394. |
| Elo 评级系统 | Elo, A.E. (1978). *The Rating of Chessplayers, Past and Present*. Arco. |
| 信息级联 | Banerjee, A.V. (1992). *A Simple Model of Herd Behavior*. Quarterly Journal of Economics, 107(3), 797-817. |
| | Bikhchandani, S., Hirshleifer, D., & Welch, I. (1992). *A Theory of Fads, Fashion, Custom, and Cultural Change as Information Cascades*. JPE, 100(5), 992-1026. |
| 概率分布融合 | Genest, C., & Zidek, J.V. (1986). *Combining Probability Distributions: A Critique and an Annotated Bibliography*. Statistical Science, 1(1), 114-135. |
| 共识动力学 | DeGroot, M.H. (1974). *Reaching a Consensus*. JASA, 69(345), 118-121. |
| 专家不确定性 | Cooke, R.M. (1991). *Experts in Uncertainty*. Oxford University Press. |
| Kelly 准则 | Kelly, J.L. (1956). *A New Interpretation of Information Rate*. Bell System Technical Journal, 35(4), 917-926. |
| | MacLean, L.C., Thorp, E.O., & Ziemba, W.T. (2010). *The Kelly Capital Growth Investment Criterion*. World Scientific. |
| 组合理论 | Markowitz, H.M. (1952). *Portfolio Selection*. Journal of Finance, 7(1), 77-91. |
| 通用组合 | Cover, T.M. (1991). *Universal Portfolios*. Mathematical Finance, 1(1), 1-29. |
| 前景理论 | Kahneman, D., & Tversky, A. (1979). *Prospect Theory: An Analysis of Decision Under Risk*. Econometrica, 47(2), 263-291. |
| 贝叶斯网络 | Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann. |
| 信息论 | Cover, T.M., & Thomas, J.A. (2006). *Elements of Information Theory*, 2nd ed. Wiley. |

---

## 7. 使用范例 Usage Examples

### 7.1 Python 接口示例

```python
from edp import (
    ProbabilityEngine,
    FlowAnalyzer,
    DomainAwarenessEngine,
    AllocationEngine,
)

# ── 初始化引擎 ──────────────────────────────────────
prob_engine = ProbabilityEngine()
flow_engine = FlowAnalyzer()
domain_engine = DomainAwarenessEngine()
alloc_engine = AllocationEngine()

# ── 1. 从市场报价计算真实概率 ──────────────────────
result = prob_engine.calculate_true_probability({
    "home": 1.50, "draw": 4.20, "away": 6.00
})

# 结果包含: true_probabilities, margin, confidence_interval, method

# ── 2. 概率流向分析（时间序列） ─────────────────────
flow_report = prob_engine.analyze_flow(
    initial_snapshot=snapshot_t0,
    latest_snapshot=snapshot_t1,
    historical_snapshots=history,
)

# 结果包含: flows (逐结果 flow / velocity / acceleration / significance),
#          aggregate_momentum, time_delta

# ── 3. 流向倍增评分 ─────────────────────────────────
amp_report = flow_engine.calculate_amplification(
    flow_report,
    gradient_map={"home": ["draw"], "away": ["draw"]},
    outcome_probs=result.true_probabilities,
)

# ── 4. 全域感知 · 多源情报融合 ──────────────────────
from edp import EvidenceSource, SourceReliability, EvidenceType

sources = [
    EvidenceSource(
        source_id="model_01",
        source_type=EvidenceType.ANALYTICAL,
        reliability=SourceReliability.B,  # usually reliable
        timestamp=datetime.now(),
        content={"probability": 0.62},
        confidence=0.80,
    ),
    EvidenceSource(
        source_id="market_quote",
        source_type=EvidenceType.OBSERVATIONAL,
        reliability=SourceReliability.A,  # completely reliable
        timestamp=datetime.now(),
        content={"probability": result.true_probabilities["home"]},
        confidence=0.95,
    ),
    # ... additional intelligence sources
]

assessment = domain_engine.assess_situation(
    sources,
    prior_probability=0.5,
    fusion_method="hybrid",
)

# 结果包含: aggregate_probability, confidence, consensus_score,
#          stability_status, anomalies, variance

# ── 5. 资源分配（Kelly + Markowitz） ─────────────────
from edp import AllocationLeg

candidates = [
    AllocationLeg(
        identifier="outcome_home",
        probability=assessment.aggregate_probability,
        odds=1.50,
        signal_score=flow_report.flows[0].momentum_score,
        confidence=assessment.confidence,
        flow_direction="upward",
    ),
    # ...
]

bundle = alloc_engine.generate_allocation(
    budget=1000.0,
    candidates=candidates,
)

bundle = alloc_engine.optimize_portfolio(
    bundle, target_diversification=0.6
)
```

### 7.2 TypeScript 接口示例

```typescript
import {
  ProbabilityEngine,
  FlowAnalyzer,
} from 'edp-framework';

const engine = new ProbabilityEngine();

const result = engine.calculateTrueProbability({
  home: 1.50, draw: 4.20, away: 6.00
});
```

---

## 8. 免责声明 Disclaimer

**本框架仅供学术研究与教育用途。**

- 本框架不构成任何投资建议或决策建议；
- 使用本框架进行的任何决策由用户自行承担责任；
- 作者不对使用本框架造成的任何损失负责；
- 请遵守所在地区的法律法规。

---

## 9. 许可证 License

MIT License — 详见仓库根目录 *LICENSE* 文件。

---

*以结构化分析、严格概率论与全域认知提供学术研究支持——仅供学术研究用途。*

*© 2026 — For Academic Research and Educational Purposes Only.*
