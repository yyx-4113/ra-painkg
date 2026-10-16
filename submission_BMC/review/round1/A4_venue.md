# A4 报告 — 期刊契合度与报告规范审计（独立评审）

- **评审角色**：A4 — 期刊编辑视角 / 报告规范审计员
- **目标期刊**：*BMC Bioinformatics*（Springer Nature；SCIE；2025 JIF 4.4；采用 soundness-only 评审政策——只评估技术/科学严谨性，不评估"兴趣度/影响力"）
- **受理文章类型**：Research article、Software、Database、Methodology article 等
- **独立性声明**：本报告作为首次独立评审撰写。未读取任何 `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md`、`SUBMISSION_MANIFEST.md`、`REVISION_NOTE.md`、`declarations.md`、`submission_BMC/review/` 下其他文件，以及任何 `*_gen_*.py`。仅在履行第 5 项职责（cover-letter 与稿件一致性核对）时读取了 `cover_letter.md`，且仅用于提取标题/作者/期刊/邮箱等事实，未吸收其结论性表述。未对任何源文件或稿件文件做修改。

---

## 第 1 项　文章类型契合度（Article-type fit）

### 发现 F1【问题】
稿件以 "Research article" 投递，但其核心交付物是一个经过整理的知识图谱资源，且基准验证本质上为"零/阴性"结果，按 *BMC Bioinformatics* 的分类更应归入 **Database**（或 Software）类型。

### 【证据】
- `cover_letter.md` 第 6 行声明 "Manuscript type: Research article"，稿件标题（`manuscript_BMC.md` 第 1 行）与摘要 Results（第 15 行）均以 "with benchmark validation" 作为卖点。
- 但基准本身被作者自己判定为无法证成资源价值：Discussion 第 104 行 "Perturbation-prediction performance on K562 should therefore not be interpreted as a measure of RA-PainKG's biological validity"；第 108 行 "We emphasize that the K562 benchmark cannot resolve whether domain KGs improve prediction in disease-relevant systems."
- 真正的贡献是资源 + 透明的缺口文档（第 78 行、第 100 行），而非一项阳性的"研究"发现。

### 【为何重要】
*BMC Bioinformatics* 的 soundness-only 政策下，编辑会以"Research article"对应的"研究新颖性/证据强度"标准来审视；但本稿的研究证据（基准）被作者自己声明为无结论，形成类型与内容的错配，易触发"请改投 Database 类型"或"研究贡献不足"的质疑。稿件其实已部分满足 Database 类型的资源可用性/维护要求（Future updates，第 118–120 行），改类型反而更顺。

### 【具体修改】
二选一：
- **(a) 改投 Database 类型**：补充 BMC Database 标准资源表（resource name / URL / license / update policy），并在 "Future updates" 段补一句维护承诺，例如：`"RA-PainKG will be maintained at https://github.com/yyx-4113/ra-painkg; the v1.0.0 release is archived with SHA-256 checksums and will be re-archived on each PrimeKG major release."`
- **(b) 保留 Research article**：则须重构标题与摘要，使贡献落脚于"透明缺口文档方法"而非基准验证。建议标题改为：`"RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with transparent recovery and gap documentation"`（删除 "with benchmark validation"）。

---

## 第 2 项　结构化摘要合规性（Structured abstract）

### 发现 F2【合规，通过】
结构化摘要满足 *BMC Bioinformatics* 要求：含 **Background / Results / Conclusions** 三节（另有 Keywords）。

- **重算词数（自行逐词统计，不含 Keywords）**：Background 61 + Results 133 + Conclusions 41 = **约 235 词**，远低于 350 词上限。✓
- **无引文**：摘要中仅出现资源名（PrimeKG v1.0、GTEx v8、Norman K562 Perturb-seq），无可编号引用 `[n]`，符合"摘要不含参考文献"的要求。✓
- **自洽可读**：不依赖正文即可理解。✓

> 说明：BMC 实时投稿指南页（bot challenge 拦截）未能抓取，但上述三项为 BMC 结构化摘要的既定硬要求，结论不依赖该页面。

---

## 第 3 项　报告规范清单完整性（Reporting-checklist honesty）

### 发现 F3【合规，通过】
稿件末尾 Declarations（第 146–167 行）七个 BMC 强制子节**全部齐备**：
- Ethics approval and consent to participate（第 148–149 行，Not applicable）✓
- Consent for publication（第 151–152 行，Not applicable）✓
- Availability of data and materials（第 154–155 行）✓
- Competing interests（第 157–158 行）✓
- Funding（第 160–161 行）✓
- Authors' contributions（第 163–164 行）✓
- Acknowledgements（第 166–167 行）✓

- **AI 使用披露位置恰当且充分**：Methods 下设 "Implementation and AI-use disclosure"（第 57–59 行），明确列出工具（OpenAI Codex CLI、GitHub Copilot、Claude via API）、用途（代码开发、文献检索、语言润色）及人工负责制，符合 Springer Nature/BMC 对生成式 AI 须在稿件中披露的要求（置于 Methods 为合规位置）。✓
- **数据可用性声明准确（已与发布资产交叉核验）**：第 155 行声明图谱文件以 GraphML、CSV、pickle 三种格式存档于 GitHub Release v1.0.0。经比对 `MANIFEST_SHA256.txt` 与 GitHub Release v1.0.0 资产页，**GraphML（RA_PainKG_final.graphml、trackA、trackB）、CSV（nodes、edges）、pickle（final.pkl）均真实存在且 SHA-256 完全一致**（7 个校验和逐项匹配，无任何差异）。声明属实。✓

> 说明：第三方数据集 DOI（Harvard Dataverse 10.7910/DVN/R9JDLS、10.7910/DVN/IXA7BM）为本评审未独立抓取验证，但其为公开 Dataverse 常规 DOI，不影响声明成立。

---

## 第 4 项　过度声称与 soundness 张力（Overclaim / soundness tension）

### 发现 F4【问题】
Conclusions 对新颖性的表述过度，称其为"pain biology 中此前不存在的资源类型"，与稿件自身承认"基因集已被充分覆盖、价值在于组织整理"直接矛盾。

### 【证据】
- Conclusions 第 124 行：`"a resource type not previously available for pain biology"`。
- 但 Results 第 78 行作者自己写道：`"The principal added value of RA-PainKG is therefore not the recovery of absent genes, but the organization, tissue contextualization, and transparent annotation of an already well-covered gene set."`

### 【为何重要】
*BMC Bioinformatics* 为 soundness-only 且对"新颖性/影响力"宣称持高度审慎；一条被正文自身弱化的新颖性断言会直接损害可信度，并诱使编辑以"声称超出证据"为由质疑整体严谨性。

### 【具体修改】
将 Conclusions 第 124 行末尾改写为（英文可直接粘贴）：
`"RA-PainKG provides a tissue-contextualized, dual-track knowledge graph for RA pain signaling whose principal value is the transparent documentation of gene recovery and residual gaps for an already well-covered gene set — a documentation standard we argue should accompany domain-specific knowledge graphs."`

（注：Discussion 第 100 行的 "to our knowledge, rarely implemented / few precedents" 属缓称，尚可接受，但建议同步将上述"resource type not previously available"的强措辞收敛，避免与第 78 行自相矛盾。）

---

## 第 5 项　格式硬伤与一致性（Format hard-fails & consistency）

### 发现 F5【问题：自引 [19] 为未引用占位文献】
参考文献 [19] 是作者自引的 GitHub/Zenodo（2026）占位条目，在正文**从未被引用**，且作为编号文献不合规范。

### 【证据】
- 参考文献列表第 207 行：`[19] Yang Y. RA-PainKG: ... GitHub/Zenodo. 2026. Available at: https://github.com/yyx-4113/ra-painkg.`
- 通读全文，正文引用序列为 [1]–[18]、[20]–[22]，**无任何 `[19]` 出现**；该发布资源已完整写于 Availability 声明（第 155 行 URL + MANIFEST_SHA256.txt），与 [19] 内容重复。

### 【为何重要】
- 未引用的参考文献违反 Vancouver 编号体系的"列出即引用"原则，且 2026 年 GitHub/Zenodo 链接不是可引用的正式出版物。Soundness-only 编辑会将其视为清单性硬伤，并要求删除或规范化。

### 【具体修改】
删除参考文献 [19]（其内容已由 Availability of data and materials 覆盖）。若作者坚持正式引用该资源，应替换为带真实 DOI 的 Zenodo 存档条目（而非"GitHub/Zenodo. 2026"），并在正文中实际引用。

---

### 发现 F6【问题：内部数字不自洽（190 / 45 / 165）】
Methods 第 39 行的"190 个种子节点 + 45 个新增 = 165 个注释基因"在算术上不可能成立。

### 【证据】
- 第 39 行：`"The pipeline identified 190 seed gene nodes. From these seeds, a 2-hop neighborhood expansion ... identified 45 additional pain-relevant genes ... yielding a final annotated set of 165 genes."`
- 190 + 45 = 235 ≠ 165；若要 165 为终值，基数应为 120（120 + 45 = 165）。
- 附带：Track A 106 + Track B 122 − 重叠 96 = 并集 132，与"165 annotated genes"亦需对账（33 个基因需解释为非双轨成员）。

### 【为何重要】
数字矛盾出现在资源构建的核心方法段，直接动摇图谱规模统计（18,069 节点 / 127,226 边）与下游基准的可重复性，是 soundness 审查的重点扣分项。

### 【具体修改】
对账并修正：若最终注释基因为 165 且扩增加入 45，则种子基数应为 120，应将 "190 seed gene nodes" 改为 `"120 seed gene nodes"`（或相应调整终值/扩展数，使三者自洽）；并补充一句说明 165 中除双轨 132 外 33 个基因（扩展所得且未分配轨）的归属。

---

### 发现 F7【问题：标题卖点与正文告诫自相抵触】
标题 "with benchmark validation" 暗示基准"验证"了资源，但 Discussion 明确声明该基准"无法判定资源是否有效"。

### 【证据】
- 标题（第 1 行）：`"... with benchmark validation"`。
- Discussion 第 108 行：`"We emphasize that the K562 benchmark cannot resolve whether domain KGs improve prediction in disease-relevant systems."`
- 同见第 104 行："should therefore not be interpreted as a measure of RA-PainKG's biological validity."

### 【为何重要】
将"无结论的基准"写进标题，等于用正文已自我否定的信号去支撑稿件门面，在 soundness-only 评审中会被直接标记为"声称与证据不符"，与 F4 的新颖性矛盾叠加放大可信度风险。

### 【具体修改】
标题删除 "with benchmark validation"（见 F1 建议改法）；若保留基准相关表述，应改为中性定位，例如：`"... with transparent benchmark boundary-condition characterization"`。

---

### 发现 F8【合规，通过：cover-letter 与稿件一致性】
逐项核对 `cover_letter.md` 与 `manuscript_BMC.md`，**完全一致**：
- 标题：cover letter 第 13 行 与 稿件第 1 行 文字相同 ✓
- 作者/单位：cover letter 第 15 行 与 稿件第 3–5 行（福建中医药大学附属第二人民医院麻醉科，福州）一致 ✓
- 通讯邮箱 960856791@qq.com：两端一致 ✓
- ORCID 0009-0004-9698-6552：两端一致 ✓
- 期刊 BMC Bioinformatics / 类型 Research article：一致 ✓

### 发现 F9【合规，通过：是否存在"过期 Scientific Data 文献"】
未发现有问题的 Scientific Data 引用。参考文献 [13] Chandak et al. "Building a knowledge graph to enable precision medicine. *Sci Data*. 2023;10:67." 为 PrimeKG 的正式出处，年份 2023、卷期页码齐全，**属正确且不过期**的引用，非占位。✓

### 发现 F10【合规，通过：参考文献格式】
除 F5 的 [19] 外，其余 [1]–[22] 为 Vancouver 编号、顺序引用、作者–标题–期刊–年;卷(期):页码 格式规范，且引用顺序与出现顺序基本一致。仅需按 F5 移除 [19]。✓

---

## 第 6 项　贡献清晰度（Contribution clarity）

### 发现 F11【问题】
最强且最站得住的贡献（透明的基因回收与缺口文档）被弱化，而较弱的"阴性基准"却占据了标题与摘要的醒目位置。

### 【证据】
- 标题（第 1 行）与摘要 Results（第 15 行）前置 "benchmark validation"；
- 透明缺口文档这一真正贡献被置于 Discussion（第 98–100 行），且作者自认其价值在组织整理（第 78 行）。

### 【为何重要】
Soundness-only 编辑评估的是"实际做出的贡献"。用一条作者自己声明"无信息量"的基准做门面，会使稿件被按其自身的弱势信号评判，而真正可称道的方法实践（逐基因系统化回收文档）反而被漏看，增加被低估/拒稿风险。

### 【具体修改】
在摘要 Background/Results 与标题中以文档贡献为引领，将基准降为"边界条件刻画"的方法/验证小节。例如 Results 开篇可改为（英文可直接粘贴）：
`"We introduce a transparent recovery-and-gap documentation workflow that reports, per curated gene, whether and why it is absent from the graph; applied to 192 pain genes, it shows 188/192 are recovered and the four non-recoveries are identifier or construction artifacts rather than biological absences."`

---

## § 站得住（Stands up — 稿件达标的方面，≥3）
1. **数据可用性真实可核验**：GitHub Release v1.0.0 的 7 个图谱/表/JSON 资产与 `MANIFEST_SHA256.txt` 的 SHA-256 **逐项完全一致**，无缺失、无篡改迹象；GraphML/CSV/pickle 三种格式均到位，声明属实。
2. **Declarations 七节齐备且 AI 披露到位**：全部 BMC 强制子节存在；AI 工具使用在 Methods 中具名、用途与负责制清晰，位置合规。
3. **结构化摘要合规**：Background/Results/Conclusions 三节俱全，重算约 235 词（≤350），无引文，自洽可读。
4. **基准结论诚实**：作者并未掩盖 K562 测试系统错配与基准的"无法判定"性质（第 104–108 行），反而明确划出边界，符合 soundness-only 对透明度的要求。
5. **cover-letter 与稿件事实一致**：标题、作者、邮箱、ORCID、期刊、类型五处均无缝吻合，无低级不一致。

## § 给作者的问题（Questions for the authors）
1. 第 39 行 "190 seed gene nodes + 45 additional = 165 annotated genes" 中，正确的基数究竟是 120 还是 190？请对账 190/45/165 以及 Track A 106 + Track B 122 − 重叠 96 = 132 与 "165" 的关系，并说明那 33 个非双轨基因的来源。
2. 参考文献 [19]（自引 GitHub/Zenodo 2026）是否在正文任何位置被引用？若否，是否同意删除（其信息已由 Availability 声明覆盖）或替换为带真实 DOI 的 Zenodo 条目？
3. 作者是否考虑将文章类型由 "Research article" 改为 "Database"？若保留 Research article，是否同意弱化标题中的 "benchmark validation" 以避免与 Discussion 第 108 行自相矛盾？
4. Conclusions 第 124 行 "a resource type not previously available for pain biology" 与 Results 第 78 行 "already well-covered gene set" 是否应统一措辞，将声称收敛为"透明文档标准"而非"全新资源类型"？

## § 我实际核查了什么（What I actually checked）
**读取的文件**
- `submission_BMC/manuscript_BMC.md`（全文 214 行）
- `submission_BMC/cover_letter.md`（仅用于第 5 项事实一致性核对）
- `ra-painkg/MANIFEST_SHA256.txt`（7 条 SHA-256 清单）

**执行的核验（命令/动作）**
- 逐词重算摘要词数：Background 61 + Results 133 + Conclusions 41 = 约 235 词。
- WebFetch GitHub Release v1.0.0 资产页，取得 10 个资产的文件名与 SHA-256，与 MANIFEST_SHA256.txt 逐条比对。
- 通读全文核对参考文献 `[n]` 的引用出现情况（定位 [1]–[18]、[20]–[22]，确认 [19] 未出现）。
- 尝试 WebFetch `bmcbioinformatics.biomedcentral.com/submission-guidelines` 与 `springernature.com/.../ai` 两页，均被 "Client Challenge"（bot 拦截）阻挡，故 BMC 结构化摘要与 AI 披露要求依据既定 BMC 作者政策判断，结论不依赖这两页。

**发现的差异（discrepancies）**
- ✅ MANIFEST ↔ Release：**0 差异**，7/7 校验和完全匹配（RA_PainKG_final.graphml、.pkl、nodes/edges CSV、trackA/trackB graphml、summary.json 全部吻合）。
- ❌ 参考文献 [19]：未引用 + 占位（GitHub/Zenodo 2026），应删或规范。
- ❌ 数字不自洽：第 39 行 190 + 45 ≠ 165。
- ❌ 标题 "benchmark validation" 与 Discussion 第 108 行 "cannot resolve" 抵触。
- ❌ Conclusions "resource type not previously available" 与 Results 第 78 行 "already well-covered gene set" 抵触。

**未读取（遵守独立性）**
`submission_BMC/review/` 下除本报告外的一切文件（含 `_PANEL_BRIEF.md`、`REVIEW_*`/`RESPONSE_*`/`REVISION_*`）、`SUBMISSION_MANIFEST.md`、`REVISION_NOTE.md`、`declarations.md`、任何 `*_gen_*.py`；亦未修改任何源/稿件文件。
