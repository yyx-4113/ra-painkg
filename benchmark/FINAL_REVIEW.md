# JBI 全方位终审报告 — RA-PainKG Benchmark (Final Pre-submission Review)
## 逐段、逐数字、逐逻辑链审查

---

## 🔴 严重错误 (必须修复，否则 Desk Reject)

### F1. 疼痛基因表达数据严重虚报 (38.6% vs 59.1%)

**论文声称:** "K562 cells express pain genes at low levels (38.6% below mean expression 0.01, vs genome-wide mean 0.107)"
**实际数据 (k562_pain_expr.csv):** 44个疼痛基因中有26个低于0.01，即59.1%，而非38.6%。
**差异:** 20.5个百分点！论文将表达问题**低估了一半以上**。

另外，疼痛基因均值论文声称"mean 0.032"，实际均值0.117，甚至**高于**全基因组均值0.107。

**影响:** 这直接改变了K562细胞是否适合测试疼痛KG的解释。论文说38.6%低表达（暗示大部分尚可表达），但实际近60%低表达（表明该系统对疼痛生物学极为不适合）。

### F2. CI [-0.085, +0.007] 与实际数据不符

**论文声称:** RA-PainKG vs GO: delta = -0.039, 95% CI [-0.085, +0.007]
**实际数据验证:** RA-PainKG vs GO (r_pain): diff=-0.0390, 95% CI = [-0.0785, +0.0004]
**差异:** CI半宽从0.046缩小到~0.039。论文的CI被人为加宽了。

可能的来源：使用了Pooled SE而非Paired SE，或计算了错误的自由度。

### F3. KG数量声称矛盾

**论文声称:** "10 KG variants"
**实际列表:** GO + RA-PainKG + 5个Random + RA-PainKG-degPreserved + GO-painCentric + Identity + STRING = **11个**
需修正为11或重新定义计数方式。

---

## 🟡 中等错误 (显著问题，需修正)

### M1. Delta +0.077 应为 +0.078

Random_R1 vs GO (r_all): diff=0.0775，标准四舍五入应为0.078，论文写0.077。

### M2. 5,045基因 vs metadata的2,000基因

benchmark_metadata.json记录n_genes=2,000，但gene_sets.json的norman_all有5,045个基因。需确认哪个数字正确并在全文中保持一致。如果实际使用了5,045基因，metadata应更新。

### M3. 165 pain genes vs 44 in benchmark

论文中多处提到165个疼痛基因，但基准测试中仅44个与Norman数据集重叠（norman_all∩pain_all=44）。Abstract/Results中应明确此重叠情况。

### M4. k范围不一致

Abstract: "k = 32–256"；但sensitivity数据含k=512。应统一为32–256或扩展至512。

### M5. 训练样本数不一致

Methods某处提到"227 conditions"但另处和metadata提到n_train="227"是条件数而非样本数。应统一术语。

---

## 🟢 轻微问题 (建议修正)

### m1. Reference [9] Adamson 2016 年份
[9] 引用标注2016，但Adamson et al.的Perturb-seq论文确实是2016年Cell论文。✅ 正确。

### m2. 摘要字数395词
JBI结构化摘要通常≤250词。当前395词偏长，建议再压缩。

### m3. "Precision"应为"Recall"或其他
"68.3% of Norman-measured genes are isolated in RA-PainKG" — "isolated"指无邻接边。这是precision相关但非标准术语。

### m4. Keywords中的"clinical informatics" — 无临床验证情况下不妥

---

## 📊 逻辑链审查

### ✅ 已通过的逻辑链:
1. GEARS使用GO提升预测 → 引出KG先验重要性
2. 构建RA-PainKG → 测试domain specificity
3. 多分割+ablation → 分离density vs specificity
4. Random > GO > RA-PainKG → 密度驱动结论
5. degPreserved匹配RA-PainKG → 因果证据

### ⚠️ 脆弱的逻辑链:
1. MLP单分割 → "非线性模型减弱KG区分" → 声明过于宽泛
2. 两点外推60,000边 → 已加警示但本质上仍是n=2外推
3. K562 → "保守测试" → 但疼痛基因近60%不表达使系统可能根本无效

---

## 📋 逐项修改清单

| # | 严重度 | 位置 | 问题 | 修正 |
|---|--------|------|------|------|
| 1 | 🔴 | Abstract+L243 | 38.6%→59.1% | 基于k562_pain_expr.csv重新计算 |
| 2 | 🔴 | Abstract+L243 | mean 0.032→0.117 | 重新计算 |
| 3 | 🔴 | Abstract+Results | CI [-0.085,+0.007]→[-0.078,+0.000] | 基于paired t-test重新计算 |
| 4 | 🔴 | Abstract+Methods | "10 KG variants"→"11 KG variants" | 重新计数 |
| 5 | 🟡 | Abstract | delta +0.077→+0.078 | 标准四舍五入 |
| 6 | 🟡 | Methods | 确认5,045 vs 2,000基因 | 澄清实际使用量 |
| 7 | 🟡 | Abstract | 明确44个重叠疼痛基因 | 加入overlap说明 |
| 8 | 🟡 | Abstract | k=32-256→32-512 | 与数据一致 |