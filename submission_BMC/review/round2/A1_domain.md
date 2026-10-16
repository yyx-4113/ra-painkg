# Round 2 独立领域评审 — 疼痛生物学 / 类风湿关节炎 / 神经免疫学

**评审对象：** manuscript_BMC.md（修订稿）
**评审依据：** 仅 manuscRIPT + 原始数据（track_assignments.csv, gene_centrality.csv, pain_signaling_pathways.md, RA_PainKG_summary.json）。未参考任何 prior-round 评审文件。
**评审者角色：** 独立领域专家（声音生物学 / RA / 神经免疫学），针对 BMC Bioinformatics（SCIE，声音完整性编辑政策）做证据性复审。

---

## 1. 逐条问题

### 问题 A — “20 个功能类别”与“9 条通路”的内部不一致（任务 1）

【Problem】
稿件在两个层面存在自相矛盾：(i) 声称“20 个功能类别”，但 Stage 1 实际枚举的列表只有 17 项；(ii) Stage 1 枚举的“9 条通路”与真正用于覆盖率映射的 9 条通路（pain_signaling_pathways.md）并非同一组九条，读者无法对应。

【Evidence】
- L13（摘要）、L29（引言）、L37（方法）、L69（结果）均称 “20 functional categories”。
- L37 的枚举文本按逗号拆分仅得 17 项：nociceptor transduction channels, voltage-gated sodium and calcium channels, neuropeptide signaling, neurotrophin signaling, opioid system, inflammatory cytokines and receptors, MAPK, JAK–STAT, NF-κB pathways, prostaglandin pathway, complement cascade, GABA/glycine and serotonin receptors, endocannabinoid system, kinase signaling, transcription factors, RA-specific genes, anesthetic targets。即便把“GABA/glycine 与 serotonin”拆分、把“MAPK/JAK–STAT/NF-κB”拆分，最多约 18 项，仍达不到 20。
- L37 枚举的 9 条通路为：(1) 伤害感受转导，(2) 突触传递，(3) 阿片系统，(4) 炎性细胞因子信号（细胞因子+受体+JAK–STAT+NF-κB+MAPK），(5) 前列腺素，(6) 补体，(7) 抑制性调制，(8) 激酶信号，(9) RA 特异+麻醉靶点。
- pain_signaling_pathways.md 实际映射覆盖率的是另一组 9 条：TRPV1-CGRP 轴、Nav1.7 轴、TNFa-NGF 轴、阿片轴、JAK-STAT 轴、MAPK 轴、补体神经免疫轴、GABA 能轴、前列腺素轴。其中 TNFa-NGF 轴与 MAPK 轴在 L37 的 (4) 内被合并；L37 的 (8) 激酶信号与 (4) 内的 MAPK/JAK–STAT 重叠；(9) 把“RA 特异基因”与“麻醉靶点”混为一条“通路”，而麻醉靶点（GABA/阿片）已在 (3)(7) 覆盖，构成重叠/概念不清。

【Why it matters】
对一家以“可重复性”为核心的期刊，声称的 20 类与枚举的 17 项不一致，且“九条通路”在方法与结果两处所指不同，会削弱方法可重复性，并让读者无法判断“57–100% 覆盖”到底映射的是哪九条。

【Specific fix】
1) 将 L37 的功能类别要么补全到 20 项（明确列出缺失的 3 类），要么把全文“20”改为真实的枚举数（并注明完整 20 类见 S1）；
2) 统一“九条通路”的定义：使 Stage 1 枚举的 9 条与 pain_signaling_pathways.md 中覆盖率映射的 9 条一一对应（建议直接引用后者为权威 9 条，并把 L37 的 9 条重新对齐，或明确说明两者是“主题分组”与“具体轴”的对应关系）；
3) 拆分/归并重叠项：把 MAPK、JAK–STAT 从“炎性细胞因子信号”中独立出来以匹配覆盖率表，或将 (9) 限定为单一明确类别。

---

### 问题 B — DRD2/COMT 遗漏声明与数据矛盾（任务 2）

【Problem】
L112 声称初始 192 基因集遗漏了 DRD2 与 COMT 两个“经典疼痛/镇痛基因”，应“在未来版本纳入”。但 COMT 实际已作为双轨 `pain_gene` 存在于资源中，构成事实性矛盾。

【Evidence】
- track_assignments.csv 第 26 行：`COMT,True,True`（双轨注释）。
- gene_centrality.csv 第 452 行：`COMT,pain_gene,...,True,True,True`（类别为 pain_gene，双轨，有组织学标注）。
- 因此 COMT 已在 165 基因注释集中（很可能属于 120 个“人工策展核心”而非 45 个扩展基因，因其为双轨）。
- DRD2：track_assignments.csv 中不存在；gene_centrality.csv 第 2401 行 `DRD2,other,...,False,False,True`——即存在于全图中但未进入 165 注释集、未赋轨。DRD2 的“遗漏”声明与数据一致，仅 COMT 部分错误。

【Why it matters】
局限性一节中的“遗漏”声明若为假，属于数据完整性问题；读者会误以为 COMT 不在图谱内，进而质疑其他“已恢复/遗漏”声明的可靠性（尤其本文核心卖点正是“透明恢复与缺口文档”）。

【Specific fix】
- 修正 L112：明确指出仅 DRD2 真正缺失于策展集；COMT 实际已通过注释/扩展纳入（若属 2-hop 扩展所得，应说明“COMT 经扩展恢复并纳入注释集”，而非“应在未来版本纳入”）。
- 若 COMT 确属 192 策展集，则直接删除 COMT，仅保留 DRD2。必须在 revision note 中说明改动并重新核对“192 策展集”清单的一致性。

补充（任务 2 第二部分）：稿件并未用“comprehensive/systematic”描述自身策展（“systematic”仅见于 L47、L95 的“恢复分析/缺口文档”，属合理用法），故不存在与遗漏相冲突的“全面性”措辞冲突。重点在于修正 COMT 事实错误，而非弱化语气。

---

### 问题 C — Track 解耦声明：单一轨基因可枚举（好），但 PPI 稀疏性统计不可复现（任务 3）

【Problem】
“10 个炎症单一轨 + 26 个伤害感受单一轨”基因可从 track_assignments.csv 完整枚举（已验证），这一部分是扎实的。但支撑“解耦标记干预点”的配套统计——“Track B 50% vs Track A 20% 在 PPI 子图中零边”（L75）——中 Track B 的 50% 无法从提供的数据复现。

【Evidence】
- 由 track_assignments.csv 计算：total=165, both=96, A-only=10, B-only=26, neither=33（96+10+26+33=165，自洽）。
- 可枚举的单一轨基因：
  - 炎症单一轨（10）：BDNF, CNR2, CTLA4, IFNG, IL10, MMP1, MMP9, PADI4, TNF, TRPA1。
  - 伤害感受单一轨（26）：ASIC2, ASIC4, CACNA1B, CACNA1H, GABRA2, GRIA2, GRIN1, KCNA1, KCNQ2, MAOB, NGFR, NTRK2, P2RY1, P2RY12, PIEZO2, PRKCG, PTGER1, RAMP3, SCN1A, SCN2A, SCN3A, SYT1, TAC1, TACR1, TACR2, TRPM3。
- PPI 零边复算（基于 RA_PainKG_edges.csv 的 28,972 条 protein_protein 边）：
  - 注释基因互作子图（两端均属 165 注释集）：共 780 条 PPI 边；Track A 106 个中 19 个零边 = 17.9%（≈20%，与 L75 吻合）；Track B（实际可映射 121 个）29 个零边 = 24.0%，**远非 50%**。
  - 全图 PPI 网络下：Track A 与 Track B 零边率均为 0%（每条注释基因在全 PPI 中均 ≥1 边）。
  - 两种合理解释均无法得到“Track B 50%”。L75 的 50% 在提供数据中不可复现。
- 另发现数据完整性瑕疵：track_assignments.csv 中的 CALCB、P2RX3、PIEZO2 三个注释基因在 gene_centrality.csv 中无对应记录（按名映射缺失），导致 Track B 由 122 降为可计 121；这 3 个基因缺中心性条目，需核实是否真正入图计算。

【Why it matters】
“解耦标记干预点”本身是作为“假设生成的概念透镜”（L69）提出的，措辞可接受；但支撑它的 50% vs 20% 不对称是具体数字主张，若为笔误或子图定义不清，会削弱“伤害感受先验知识更直接连接更稀疏”这一核心结论，且与本文“透明/诚实”的定位相悖。

【Specific fix】
1) 保留并显式列出上述 10+26 单一轨基因（建议在 S1 或正文补充），这能夯实“可枚举干预点”的论点；
2) 明确 L75 “PPI 子图”的精确定义（是 165 注释集互作子图？还是 benchmark 的 2400 边 PPI 变体？），并给出每条基因的 PPI 度（建议增补补充表）；
3) 重算并更正 50%/20% 这一对数字；若重算后 Track B 确为约 24%，则相应下调“伤害感受连接更稀疏”的量化表述（从 50% 改为实测值）；
4) 核实 CALCB、P2RX3、PIEZO2 是否真正进入图谱与中心性计算，补齐或说明。

---

### 问题 D — “组织情境化(tissue-contextualized)” 与 “未用 GTEx 过滤边” 的夸大风险（任务 4）

【Problem】
标题（L1）与摘要（L13, L17, L29）称“tissue-contextualized knowledge graph”，关键词含“tissue-specific”（L19）；但 L41 明确“GTEx … were not used to filter edges in the current release”，即组织表达仅作为节点属性，未用于构建组织特异的边或子图。

【Evidence】
- L1 标题：“a tissue-contextualized knowledge graph”；L19 关键词：“tissue-specific”。
- L41：“These annotations are node attributes … but were not used to filter edges in the current release, because removing edges on bulk tissue expression risks discarding valid low-expression interactions”。
- L107 局限性亦承认 GTEx v8 缺 DRG 与滑膜，且为 bulk TPM（细胞类型分辨率缺失）。

【Why it matters】
对以声音完整性为政策的期刊，“contextualized/specific”暗示图谱结构具备组织维度，而实际仅节点级标注。若审稿人或读者按“组织特异网络”理解，构成夸大（overstatement）。L41 已诚实说明未过滤边，但标题/摘要/关键词未与之对齐。

【Specific fix】
- 将标题与摘要中“tissue-contextualized”改为“tissue-annotated”（或加限定“node-level tissue-annotated”），并在 L41 附近一句点明“context 仅存于节点属性，边未做组织过滤”；
- 将关键词“tissue-specific”改为“GTEx-annotated / tissue-annotated”，避免暗示组织特异边；
- 此举纯属措辞对齐，不削弱资源价值。

---

### 问题 E — “58.2% 双轨重叠”的生物学合理性（任务 5）

【Problem】
L69 称 96/165=58.2% 基因同属双轨，并给出理由：被炎性细胞因子激活的转录因子（FOS/JUN/STAT3）也驱动伤害感受敏化、MAPK 转导双重信号、前列腺素（COX-2/PTGS2）桥接免疫激活与伤害感受器敏化。

【Evidence】
- 该解释与神经免疫敏化文献一致（如 Basbaum 2009、Ji 2018 述评：炎症介质与伤害感受共享 TFs、激酶、前列腺素等汇聚节点）。
- 数据中双轨枢纽确实为 EGR1/FOS/STAT3/AKT1/SRC，与“汇聚节点”叙事自洽。

【Why it matters】
（属支持项，详见 §Stands up；此处仅记录其合理性已核实，不作为缺陷。）

【Specific fix】
无需修改。若增强，可在 L69 补 1–2 条具体文献支撑“桥接基因”论述；属可选。

---

## 2. §Stands up（已验证正确、不应改动）

- **双轨计数自洽**：track_assignments.csv 严格得到 165 = 96(双)+10(A-only)+26(B-only)+33(无轨)，与摘要/结果中的 106/122/96/33 完全吻合。
- **单一轨基因可枚举**（任务 3 核心）：10 个炎症单一轨与 26 个伤害感受单一轨基因均可从提供数据完整列出（见问题 C 证据），“解耦标记干预点”作为假设生成框架有数据支撑，未过度主张。
- **58.2% 双轨重叠的生物学解释合理**（任务 5）：炎症—疼痛共享 TFs/MAPK/前列腺素汇聚，符合领域共识，叙事可信。
- **透明恢复分析框架**：L73 对 ACPA（自身抗体而非基因）、NAPE-PLD→NAPEPLD、RANKL→TNFSF11、ADRA2B 的标识符/构造缺口分类清晰，是本文真实贡献点，处理得当。
- **K562 基准的诚实边界条件**：L99–L101 明确 K562 与本疾病生物学不匹配、并报告“结构随机/度保持零模型不劣于 RA-PainKG”，该自省对声音完整性期刊是加分项，应保留。
- **节点/边规模与来源一致**：RA_PainKG_summary.json 与正文 18,069 节点 / 127,226 边 / 24 关系类型 / 4,760 药靶边一致；PPI 28,972 边与 edges 文件统计吻合。
- **顶枢纽（EGR1/FOS/STAT3/AKT1/SRC）** 在 gene_centrality.csv 与摘要/图 1 一致。

---

## 3. §Residual risk / open questions（需作者决策的开放项）

1. **L75 的 50% 数字如何得来？** 在提供数据中 Track B 零 PPI 约为 24%（注释互作子图）或 0%（全图）。作者需给出精确子图定义并复算；若确为笔误，则是单一数字更正（Minor）；若涉及不同子图定义且无法合理解释 50%，则构成数据完整性疑虑，需上升处理。建议作者增补“每条注释基因的 PPI 度”补充表以消除歧义。
2. **COMT 究竟属于 192 策展集还是扩展集？** 决定 L112 是“删除 COMT 仅留 DRD2”还是“改写 COMT 已纳入”。需要作者核对策展清单与 S1。
3. **CALCB / P2RX3 / PIEZO2 为何不在 gene_centrality.csv？** 需确认它们是否真正参与网络计算；若仅注释表有而中心性表无，应补齐或说明。
4. **“20 类 / 9 通路”最终口径**：作者须决定补全 20 类枚举、或统一为真实枚举数，并使 Stage 1 的 9 与覆盖率映射的 9 对齐（问题 A）。
5. **DRD2 缺失是否应在正文更突出？** 作为经典多巴胺能镇痛/下行抑制基因，其仅以“other”入图未注释，是否在局限性中单列说明其生物学意义，可由作者定夺。

---

## 4. Verdict

**Minor revision（小修）**

**一句话理由：** 所有问题均可通过文本/数字更正与一次 PPI 统计复算解决，无需新实验；但须修正 L112 的 COMT 事实矛盾、L75 不可复现的“50%”数字、以及“20 类/9 通路”与“tissue-contextualized”的口径对齐——这些属于声音完整性层面的硬性更正，必须在修回稿中逐条落实。若 L75 的 50% 在复算后仍无法合理解释，则升级为 Major revision（数据完整性）。
