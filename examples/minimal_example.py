#!/usr/bin/env python3
"""Minimal example — generate a McKinsey-style HTML presentation.

Run:
    cd mck_html_design_skill
    python examples/minimal_example.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=10)

# ── Structure ──
eng.cover(
    title='Q1 2026 战略回顾',
    subtitle='董事会汇报材料',
    author='战略规划部',
    date='2026年3月'
)

eng.toc(items=[
    ('1', '市场概览', '当前竞争格局分析'),
    ('2', '财务表现', '收入与增长数据'),
    ('3', '战略规划', '下一阶段重点'),
])

eng.section_divider('第一章', '市场概览', '当前竞争格局分析')

# ── Data ──
eng.big_number(
    title='年度收入增长显著',
    number='¥2.8B',
    unit='年度总收入',
    description='同比增长23%，超出市场预期，主要受益于产品创新和市场扩张。',
    source='财务部 2026Q1 报告'
)

eng.donut(
    title='收入构成分析',
    segments=[
        (0.45, NAVY, '产品销售'),
        (0.30, ACCENT_BLUE, '服务收入'),
        (0.25, ACCENT_GREEN, '订阅收入'),
    ],
    center_label='100%',
    center_sub='总收入',
    source='内部财务数据'
)

# ── Framework ──
eng.matrix_2x2(
    title='战略优先级矩阵',
    quadrants=[
        ('高优先级', LIGHT_BLUE, '立即执行的关键项目，预期ROI > 20%'),
        ('战略储备', LIGHT_GREEN, '长期价值投资方向，培育期12-18月'),
        ('优化空间', LIGHT_ORANGE, '效率提升潜力区域，降本增效'),
        ('监控区域', LIGHT_RED, '需要持续关注的风险，设置预警'),
    ],
    axis_labels=['紧迫性 →', '影响力 ↑'],
    source='战略规划部分析'
)

# ── Timeline ──
eng.timeline(
    title='2026年关键里程碑',
    milestones=[
        ('Q1', '完成战略评估\n确定优先级'),
        ('Q2', '启动核心项目\n组建专项团队'),
        ('Q3', '阶段性成果验证\n中期复盘'),
        ('Q4', '全年目标冲刺\n年度总结'),
    ],
    source='项目管理办公室'
)

# ── Charts ──
eng.grouped_bar(
    title='季度收入对比（单位：万元）',
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[('2025', ACCENT_BLUE), ('2026E', NAVY)],
    data=[[650, 700], [720, 780], [800, 850], [850, 920]],
    summary=('增长趋势', '预计2026年全年增长15%，各季度保持稳健增势'),
    source='财务预测模型'
)

# ── Closing ──
eng.closing(
    title='谢谢',
    message='以上内容仅供内部讨论使用\n如有疑问请联系战略规划部'
)

# ── Save ──
outpath = eng.save('output/strategy_review.html')
print(f"\n🎯 Open in browser: file://{os.path.abspath(outpath)}")
