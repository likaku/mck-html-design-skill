"""主动健康 × AI 全景情报综合周报 — 基于11份监控报告的金字塔结构化分析
Generated with MckHtmlEngine (McKinsey HTML Presentation Framework)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=20)

# ══════════════════════════════════════════
# Slide 1: Cover
# ══════════════════════════════════════════
eng.cover(
    title='主动健康 × AI\n全景情报综合周报',
    subtitle='基于11份监控报告的金字塔结构化分析 | 2026年3月第3周',
    author='主动健康项目 · 情报研究组',
    date='2026年3月19日'
)

# ══════════════════════════════════════════
# Slide 2: TOC
# ══════════════════════════════════════════
eng.toc(
    title='报告目录',
    items=[
        ('1', '核心结论', 'AI与生命科学的历史性"双向融合"'),
        ('2', '三大支撑论点', 'MECE分解：壁垒打破 × 算力竞赛 × 资本重定价'),
        ('3', '四大关键发现', '技术路径、新靶点、基因编辑、Agentic AI'),
        ('4', '趋势研判矩阵', '确定性 × 时间窗口 × 影响等级'),
        ('5', '行动建议与数据来源', '战略启示与监控全览'),
    ],
    source='Source: 主动健康项目知识库，11份监控报告，超3,000条信息源'
)

# ══════════════════════════════════════════
# Slide 3: Executive Summary — 核心结论
# ══════════════════════════════════════════
eng.executive_summary(
    title='AI与生命科学正在完成历史性的"双向融合"，2026年Q1是从概念走向产业爆发的临界点',
    headline='AI同时从两个方向改写生命科学：向下渗透——将生物研发门槛从专业机构降至个人开发者；向上升维——将制药基础设施从"经验试错"升级为"AI驱动的自动化闭环"',
    items=[
        ('1', 'AI打破专业壁垒', 'Paul Conyngham用ChatGPT+AlphaFold花$3,000为爱犬设计mRNA疫苗，肿瘤缩小75%'),
        ('2', '算力军备竞赛', 'AlphaFold数据库加入蛋白互作，罗氏/礼来部署数千颗GPU，英矽智能18个月完成新药进临床'),
        ('3', '资本重新定价', 'Biotech标的涨幅超1000%，AI巨头IPO潮，"十五五"将生物医药列为新兴支柱产业'),
    ],
    source='Source: 综合11份监控报告 | 覆盖Twitter/Reddit/YouTube/微博/B站'
)

# ══════════════════════════════════════════
# Slide 4: Section Divider — 三大支撑论点
# ══════════════════════════════════════════
eng.section_divider(
    section_label='第一部分',
    title='三大支撑论点',
    subtitle='MECE分解：专业壁垒打破 × 算力基础设施竞赛 × 资本市场重定价'
)

# ══════════════════════════════════════════
# Slide 5: 论点一 — Paul Conyngham案例 (Case Study)
# ══════════════════════════════════════════
eng.case_study(
    title='论点一：AI彻底打破生物医药专业壁垒——"一人药厂"时代萌芽，Paul Conyngham案例震动全球',
    sections=[
        ('S', '背景', '澳洲ML工程师Paul Conyngham，零生物学背景，爱犬Rosie确诊癌症'),
        ('A', '方法', 'ChatGPT（逻辑/翻译）+ AlphaFold（蛋白结构）+ Grok（疫苗设计），DNA测序仅$3,000'),
        ('R', '成果', '肿瘤缩小75%，Rosie恢复活力。马斯克点赞、DeepMind CEO称"仅是开始"'),
    ],
    result_box=('深层意义', '当知识获取成本趋近零，创新主体不再只是机构——"一人药厂"从概念变为现实'),
    source='Source: Twitter/Reddit 数万次互动 | 马斯克、哈萨比斯、Brockman、Bryan Johnson多方认证'
)

# ══════════════════════════════════════════
# Slide 6: 论点一并行信号 — Table+Insight
# ══════════════════════════════════════════
eng.table_insight(
    title='AI辅助生物研发的"平民化"不止于个案——GPT-5云端实验室和CRISPR-GPT同步突破',
    headers=['领域', '突破', '影响'],
    rows=[
        ['GPT-5 × 云实验室', '3.6万次自动化实验', '蛋白合成成本↓40%，试剂成本↓57%'],
        ['CRISPR-GPT', 'Nature BME发表', '首个AI基因编辑智能体，全流程自动化'],
        ['LLM × 基因编辑', '斯坦福+DeepMind合作', '大语言模型首次用于基因编辑实验设计'],
        ['Paul Conyngham', 'mRNA疫苗设计', '零背景个人完成传统数十亿美元流程'],
    ],
    insights=[
        '生物研发门槛从机构级降至个人级',
        'AI+自动化实验闭环正在形成',
        '"公民科学家"驱动的分布式创新将爆发',
    ],
    insight_title='趋势研判：',
    source='Source: Nature BME, GTC 2026, Twitter'
)

# ══════════════════════════════════════════
# Slide 7: 论点二 — AlphaFold升级 (Big Number)
# ══════════════════════════════════════════
eng.big_number(
    title='论点二：AI制药基础设施进入"算力竞赛"——AlphaFold数据库首次加入蛋白质互作信息',
    number='170万',
    unit='个同源二聚体结构',
    description='覆盖人类、小鼠、酵母及结核分枝杆菌等20个关键物种，Nature评价"再上新台阶"',
    detail_items=[
        '英伟达GTC 2026宣布与DeepMind、EMBL-EBI合作完成此次升级',
        '蛋白质结构预测只是第一步，理解蛋白质如何相互作用才是药物设计核心',
        '从"看图纸"到"读说明书"，AlphaFold进入PPI（蛋白互作）时代',
    ],
    source='Source: 英伟达GTC 2026, Nature, DeepMind'
)

# ══════════════════════════════════════════
# Slide 8: 论点二 — 算力军备竞赛 (Data Table)
# ══════════════════════════════════════════
eng.data_table(
    title='制药巨头正在以前所未有的规模部署AI算力——"AI药厂"从概念走向现实',
    headers=['企业', '动作', '规模', '意义'],
    rows=[
        ['罗氏', '部署英伟达Blackwell GPU', '2,176颗', '制药行业最大规模'],
        ['礼来', '启用AI制药工厂"LillyPod"', '1,016颗Blackwell Ultra GPU', '9,000 PFlops'],
        ['英伟达', '发布BioNeMo + Protein-Complexa', '蛋白结合剂设计模型', '生态平台'],
        ['英矽智能', '18个月/260万美元完成新药进临床', '颠覆双十定律', '10亿/10年→260万/18月'],
    ],
    source='Source: GTC 2026, 企业公告, 行业分析'
)

# ══════════════════════════════════════════
# Slide 9: 论点二 — 算力生态重构 (Three Stat)
# ══════════════════════════════════════════
eng.three_stat(
    title='算力基础设施生态正在经历全面重构——从芯片到模型到工作站，全链条革新',
    stats=[
        ('$4,500亿', 'AI基础设施支出(2026E)', True),
        ('>70%', '推理算力占比首超', False),
        ('$600亿+', '英伟达两月投资额', True),
    ],
    detail_items=[
        '英伟达从"卖铲人"全面转向"生态架构师"，开年两月投资9家AI头部企业',
        'SEMI预测推理算力占比首次超过70%，标志着AI从训练走向大规模部署',
        'Tenstorrent发布TT-QuietBox 2：首款RISC-V桌面级AI工作站($9,999)，可本地运行1200亿参数模型',
    ],
    source='Source: SEMI报告, 英伟达公告, Tenstorrent'
)

# ══════════════════════════════════════════
# Slide 10: 论点三 — 资本重定价 (Grouped Bar)
# ══════════════════════════════════════════
eng.grouped_bar(
    title='论点三：资本市场正在为"AI×生命科学"重新定价——Biotech估值逻辑发生根本转变',
    categories=['Biotech标的涨幅', '段永平NVDA仓位', 'MiniMax港股', 'Isomorphic Labs'],
    series=[('估值增幅/规模', NAVY), ('参照基准', ACCENT_BLUE)],
    data=[
        [1000, 100],   # Biotech标的涨幅超1000%
        [772, 100],    # 段永平仓位占比7.72%→暴增11倍
        [3800, 500],   # MiniMax市值3800亿港元
        [600, 100],    # Isomorphic Labs 6亿美元融资
    ],
    max_val=4500,
    summary=('核心趋势', '估值逻辑从"管线进度"转向"数据与算法壁垒"，AI成为Biotech估值修复的关键引擎'),
    source='Source: 杰富瑞研报, 段永平持仓披露, 港交所'
)

# ══════════════════════════════════════════
# Slide 11: 论点三 — IPO潮与政策 (Vertical Steps)
# ══════════════════════════════════════════
eng.vertical_steps(
    title='AI巨头IPO潮涌动，中国政策加速推进生命科学商业化——双轮驱动产业爆发',
    steps=[
        ('1', 'AI巨头IPO潮', 'MiniMax港股上市60天市值飙升3,800亿 | OpenAI筹备年底IPO | Isomorphic Labs单轮6亿美元'),
        ('2', '"十五五"规划', '明确生物医药为六大新兴支柱产业之一，同时列入生物制造为未来产业'),
        ('3', '北京2026措施', '直接点名商业航天、人形机器人、合成生物三大未来产业'),
        ('4', '资本逻辑转变', 'Biotech估值从"管线进度"转向"数据与算法壁垒"，段永平重仓NVDA+Tempus AI'),
    ],
    source='Source: 港交所, 国务院文件, 北京市政府, 持仓披露'
)

# ══════════════════════════════════════════
# Slide 12: Section Divider — 四大关键发现
# ══════════════════════════════════════════
eng.section_divider(
    section_label='第二部分',
    title='四大关键发现',
    subtitle='合成生物平民化 × 代谢新靶点 × 基因编辑深水区 × Agentic AI范式转移'
)

# ══════════════════════════════════════════
# Slide 13: 发现1 — Paul Conyngham技术路径 (Process Chevron)
# ══════════════════════════════════════════
eng.process_chevron(
    title='发现1：Paul Conyngham案例的完整技术路径——从肿瘤DNA测序到"肿瘤缩小75%"仅花$3,000',
    steps=[
        ('1', '肿瘤DNA测序', '采集Rosie肿瘤样本进行全基因组测序'),
        ('2', 'AI解析基因', 'ChatGPT解释基因含义并翻译论文'),
        ('3', '蛋白质预测', 'AlphaFold预测蛋白质3D结构，锁定突变靶点'),
        ('4', '疫苗设计', 'Grok辅助设计mRNA序列，UNSW实验室合成'),
        ('5', '注射见效', '100页伦理审批→注射→肿瘤缩小75%'),
    ],
    bottom_bar=('关键指标', '成本: $3,000（测序）| 传统流程: 数十亿美元+十年周期 | Paul原话: "我只是想救我的狗"'),
    source='Source: Twitter/Reddit 原始帖文, 学术伦理审批文件'
)

# ══════════════════════════════════════════
# Slide 14: 发现2 — STRA6-RN7SL1 新靶点 (Key Takeaway)
# ══════════════════════════════════════════
eng.key_takeaway(
    title='发现2：STRA6-RN7SL1信号轴——颠覆性的代谢疾病干预全新靶点',
    left_text=[
        '• STRA6基因不仅是维生素A转运受体，更是新型细胞因子受体',
        '',
        '• 信号通路：招募RN7SL1非编码RNA → 激活PKA → 磷酸化STAT5 → 诱导SOCS3 → 直接导致胰岛素抵抗',
        '',
        '• 颠覆性认知：维生素A从"营养素"重新定义为"激素"',
        '',
        '• 合成生物学干预潜力：非编码RNA支架成为全新药物靶点类别',
    ],
    takeaways=[
        '非编码RNA支架是全新的药物靶点类别',
        '维生素A→激素的认知转变意义重大',
        '代谢疾病干预可能迎来范式转移',
    ],
    source='Source: 学术论文, 合成生物学前沿监控报告'
)

# ══════════════════════════════════════════
# Slide 15: 发现3 — 基因编辑深水区 (Data Table)
# ══════════════════════════════════════════
eng.data_table(
    title='发现3：基因编辑技术加速向"深水区"渗透——从线粒体到大片段DNA到个性化治疗',
    headers=['方向', '进展', '团队/期刊', '意义'],
    rows=[
        ['线粒体基因编辑', 'mtDNA编辑工具开发', '浙大团队', '异质性突变高效纠正'],
        ['大片段DNA重排', '桥接重组酶突破', 'Science双发', '人类细胞中兆碱基级DNA重排'],
        ['个性化基因治疗', '定制CRISPR治疗婴儿KJ Muldoon', '临床试验', '全球首例，新试验启动'],
        ['脑内CRISPR', 'RNA编辑疗法临床数据', '辉大基因', '全球首个脑内CRISPR数据'],
        ['心血管CRISPR', '单次注射降低坏胆固醇50%', 'NEJM', '心血管病防治新路径'],
    ],
    source='Source: Science, NEJM, 辉大基因公告, 临床试验注册数据',
    bottom_bar=('趋势判断', '基因编辑正从单基因→多基因、体外→体内、遗传病→慢性病全面扩展')
)

# ══════════════════════════════════════════
# Slide 16: 发现4 — Agentic AI (Before/After)
# ══════════════════════════════════════════
eng.before_after(
    title='发现4：Agentic AI范式转移正在重塑整个产业链——从"回答问题"到"直接执行任务"',
    before_title='传统AI模式',
    before_points=[
        '问答式交互，输入→输出',
        '人类决策，AI辅助',
        '单一模型，单一场景',
        '需要专业提示工程',
    ],
    after_title='Agentic AI模式',
    after_points=[
        'OpenClaw爆红：直接执行复杂任务',
        '腾讯整合进微信生态，市值+$350亿',
        '阿里"悟空"平台操控钉钉千项能力',
        '催生OPC（一人公司）全新模式',
    ],
    source='Source: OpenClaw社区, 腾讯/阿里公告 | ⚠️ 约3万台OpenClaw实例暴露公网，80%无强身份认证'
)

# ══════════════════════════════════════════
# Slide 17: Section Divider — 趋势与行动
# ══════════════════════════════════════════
eng.section_divider(
    section_label='第三部分',
    title='趋势研判与行动建议',
    subtitle='确定性-时间窗口-影响等级矩阵 & 五大战略行动建议'
)

# ══════════════════════════════════════════
# Slide 18: 趋势研判矩阵 (Horizontal Bar)
# ══════════════════════════════════════════
eng.horizontal_bar(
    title='趋势研判矩阵——8大趋势按影响等级排序，4项已进入"极高确定性"或"已发生"阶段',
    items=[
        ('AI辅助个人化精准医疗爆发 [1-2年]', 95, NAVY),
        ('AlphaFold数据库进入PPI时代 [已发生]', 92, NAVY),
        ('AI制药研发周期缩至18月级 [2-3年]', 90, ACCENT_BLUE),
        ('制药巨头AI算力军备竞赛 [进行中]', 88, ACCENT_BLUE),
        ('合成生物学绿色材料爆发 [2-4年]', 82, ACCENT_GREEN),
        ('AI Agent安全监管体系建立 [1-2年]', 80, ACCENT_GREEN),
        ('Biotech估值→算法壁垒 [进行中]', 78, ACCENT_ORANGE),
        ('非编码RNA靶点成新药物类别 [3-5年]', 60, ACCENT_ORANGE),
    ],
    summary=('关键洞见', '前4项趋势已进入不可逆阶段，建议立即启动相关战略布局'),
    source='Source: 基于11份监控报告多源交叉验证的综合研判'
)

# ══════════════════════════════════════════
# Slide 19: 行动建议 (Action Items)
# ══════════════════════════════════════════
eng.action_items(
    title='对主动健康项目的五大战略行动建议——覆盖工具、数据、靶点、安全、生态五个维度',
    actions=[
        ('构建AI辅助科研工具评估框架',
         'Q2 2026',
         '关注能将复杂生物数据转化为AI可理解指令的中间层平台',
         '研究组'),
        ('优先接入AlphaFold PPI数据',
         'Q2 2026',
         '利用BioNeMo平台进行蛋白质配体筛选，抢占PPI数据红利',
         '技术组'),
        ('跟踪STRA6-RN7SL1等新靶点',
         '持续',
         '非编码RNA支架为合成生物学干预提供全新可能',
         '研究组'),
        ('监控"合成安全"赛道',
         'Q2 2026',
         '为DNA合成序列建立AI审计流程，参考OpenAI Codex Security模式',
         '安全组'),
        ('跟踪Longevity领域KOL动态',
         '持续',
         'Bryan Johnson/Sinclair/Attia等对AI医疗民主化的关注预示长寿科技加速',
         '市场组'),
    ],
    source='Source: 战略规划组综合建议'
)

# ══════════════════════════════════════════
# Slide 20: 数据来源全览 + Closing
# ══════════════════════════════════════════
eng.data_table(
    title='数据来源全览——6大监控任务、11份报告、超3,000条信息源的全覆盖体系',
    headers=['监控任务', '报告数', '关键平台'],
    rows=[
        ['合成生物学前沿追踪', '2', 'Twitter, Reddit, 微博, B站'],
        ['AlphaFold & AI for Science', '2', 'Twitter, Reddit, 微博, B站, YouTube'],
        ['生命科学商业化与资本市场', '2', 'Twitter, Reddit, 微博, B站'],
        ['主动健康 & Longevity', '1', '多平台综合'],
        ['Sinclair/Johnson/Attia 动态', '3', 'Twitter 为主'],
        ['Longevity & Synbio 学术机构', '1', '多平台综合'],
    ],
    source='Source: 主动健康项目知识库 | 基于麦肯锡金字塔原则的结构化输出',
    bottom_bar=('方法论', '结论先行 · 以上统下 · 归类分组 · 逻辑递进')
)

# ══════════════════════════════════════════
# Save
# ══════════════════════════════════════════
outpath = os.path.join(os.path.dirname(__file__), '..', 'output', 'longevity_weekly.html')
eng.save(outpath)
print(f'✅ Done! {eng._page} slides generated → {outpath}')
