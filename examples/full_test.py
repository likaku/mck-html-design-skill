#!/usr/bin/env python3
"""Full test — call every MckHtmlEngine method to verify all 68 work.

Run:
    cd mck_html_design_skill
    python examples/full_test.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mck_html import MckHtmlEngine
from mck_html.constants import *

eng = MckHtmlEngine(total_slides=68)

# ═══ STRUCTURE (5) ═══
eng.cover(title='Full Method Test', subtitle='All 68 Methods', author='QA', date='2026-03-20')
eng.section_divider('Section 01', 'Structure Layouts')
eng.toc(items=[('1', 'Structure', '5 methods'), ('2', 'Data', '7 methods'), ('3', 'Framework', '4 methods')])
eng.closing(title='Thank You', message='All methods verified')
eng.appendix_title(title='Appendix', subtitle='Supplementary Data')

# ═══ DATA (7) ═══
eng.big_number(title='Big Number', number='42%', unit='Growth', description='Year-over-year increase', source='Test')
eng.two_stat(title='Two Stats', stats=[('85%', 'Completion', True), ('¥12M', 'Revenue', False)])
eng.three_stat(title='Three Stats', stats=[('95%', 'Quality', True), ('¥8M', 'Cost', False), ('120', 'Projects', False)])
eng.metric_cards(title='Metric Cards', cards=[('A', 'Revenue', 'Growing steadily'), ('B', 'Margin', 'Improving'), ('C', 'Retention', '95% rate')])
eng.data_table(title='Data Table', headers=['Name', 'Q1', 'Q2', 'Q3'], rows=[['Product A', '100', '120', '150'], ['Product B', '80', '90', '110']])
eng.table_insight(title='Table + Insight', headers=['Area', 'Score', 'Trend'], rows=[['Sales', '85', '↑'], ['Marketing', '72', '→']], insights=['Sales momentum strong', 'Marketing needs attention'])
eng.scorecard(title='Scorecard', items=[('AI/ML', '92/100', 0.92), ('Cloud', '78/100', 0.78), ('Security', '65/100', 0.65)])

# ═══ FRAMEWORK (4) ═══
eng.matrix_2x2(title='2×2 Matrix', quadrants=[('Q1', LIGHT_BLUE, 'High priority'), ('Q2', LIGHT_GREEN, 'Strategic'), ('Q3', LIGHT_ORANGE, 'Optimize'), ('Q4', LIGHT_RED, 'Monitor')])
eng.pyramid(title='Pyramid', levels=[('Vision', 'Long-term direction', 4), ('Strategy', 'Key initiatives', 6), ('Execution', 'Day-to-day operations', 9)])
eng.process_chevron(title='Process', steps=[('1', 'Plan', 'Define objectives'), ('2', 'Build', 'Develop solution'), ('3', 'Deploy', 'Launch to production')])
eng.temple(title='Temple', roof_text='Customer Value', pillar_names=['Innovation', 'Quality', 'Speed', 'Cost'], foundation_text='Operational Excellence')

# ═══ COMPARISON (3) ═══
eng.side_by_side(title='Side by Side', options=[('Option A', ['Lower cost', 'Faster delivery']), ('Option B', ['Higher quality', 'Better scalability'])])
eng.before_after(title='Before/After', before_title='Current State', before_points=['Manual processes', 'High error rate'], after_title='Future State', after_points=['Automated workflow', 'Near-zero errors'])
eng.swot(title='SWOT', quadrants=[('Strengths', ACCENT_GREEN, LIGHT_GREEN, ['Strong brand', 'Tech leadership']), ('Weaknesses', ACCENT_RED, LIGHT_RED, ['High costs']), ('Opportunities', ACCENT_BLUE, LIGHT_BLUE, ['New markets']), ('Threats', ACCENT_ORANGE, LIGHT_ORANGE, ['Competition'])])

# ═══ NARRATIVE (6) ═══
eng.executive_summary(title='Exec Summary', headline='Q1 results exceeded expectations across all metrics', items=[('1', 'Revenue', 'Up 23% YoY'), ('2', 'Margin', 'Improved by 5 points'), ('3', 'Growth', 'Market share gained')])
eng.key_takeaway(title='Key Takeaway', left_text=['Analysis shows strong momentum', 'Market position improving'], takeaways=['Continue investment in AI', 'Expand to new segments'])
eng.four_column(title='Four Columns', items=[('1', 'Plan', 'Strategy development'), ('2', 'Build', 'Product engineering'), ('3', 'Test', 'Quality assurance'), ('4', 'Ship', 'Market delivery')])
eng.quote(quote_text='The best way to predict the future is to create it.', attribution='— Peter Drucker')
eng.two_column_text(title='Two Columns', columns=[('A', 'Market Analysis', ['Strong growth in Asia', 'Europe stabilizing']), ('B', 'Competition', ['3 new entrants', 'Price pressure'])])
eng.pros_cons(title='Pros & Cons', pros_title='Advantages', pros=['Fast implementation', 'Low cost'], cons_title='Disadvantages', cons=['Limited scalability', 'Vendor lock-in'], conclusion=('Recommendation', 'Proceed with pilot phase'))

# ═══ TIMELINE (2) ═══
eng.timeline(title='Timeline', milestones=[('Jan', 'Kickoff'), ('Mar', 'MVP'), ('Jun', 'Beta'), ('Sep', 'Launch')])
eng.vertical_steps(title='Steps', steps=[('1', 'Discovery', 'Understand requirements'), ('2', 'Design', 'Create solution architecture'), ('3', 'Implement', 'Build and test'), ('4', 'Deploy', 'Go live')])

# ═══ TEAM & CASE (3) ═══
eng.meet_the_team(title='Team', members=[('Alice', 'CEO', 'Visionary leader'), ('Bob', 'CTO', 'Tech expert'), ('Carol', 'CFO', 'Financial strategist')])
eng.case_study(title='Case Study', sections=[('S', 'Situation', 'Company facing growth challenges'), ('A', 'Action', 'Implemented digital transformation'), ('R', 'Result', 'Revenue grew 40%')])
eng.action_items(title='Actions', actions=[('Phase 1', 'Q1 2026', 'Setup infrastructure', 'Team A'), ('Phase 2', 'Q2 2026', 'Launch beta', 'Team B')])

# ═══ CHARTS (11) ═══
eng.donut(title='Donut Chart', segments=[(0.4, NAVY, 'Product'), (0.35, ACCENT_BLUE, 'Service'), (0.25, ACCENT_GREEN, 'Other')], center_label='100%', source='Test')
eng.pie(title='Pie Chart', segments=[(0.5, NAVY, 'Domestic', 'Core market'), (0.3, ACCENT_BLUE, 'APAC', 'Growing'), (0.2, ACCENT_GREEN, 'Europe', 'Emerging')])
eng.grouped_bar(title='Grouped Bar', categories=['Q1', 'Q2', 'Q3'], series=[('2025', ACCENT_BLUE), ('2026', NAVY)], data=[[100, 120], [130, 150], [140, 170]])
eng.horizontal_bar(title='Horizontal Bar', items=[('AI/ML', 92, NAVY), ('Cloud', 78, ACCENT_BLUE), ('Data', 65, ACCENT_GREEN), ('Security', 55, ACCENT_ORANGE)])
eng.gauge(title='Gauge', score=78, benchmarks=[('Industry Avg', '65', ACCENT_ORANGE), ('Target', '85', ACCENT_GREEN)])
eng.stacked_bar(title='Stacked Bar', periods=['2022', '2023', '2024'], series=[('A', NAVY), ('B', ACCENT_BLUE), ('C', ACCENT_GREEN)], data=[[40, 35, 25], [35, 40, 25], [30, 40, 30]])
eng.waterfall(title='Waterfall', items=[('Base', 100, 'base'), ('Growth', 30, 'up'), ('New', 20, 'up'), ('Loss', -15, 'down'), ('Total', 135, 'base')], legend_items=[('Increase', ACCENT_GREEN), ('Decrease', ACCENT_RED)])
eng.line_chart(title='Line Chart', x_labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], y_labels=['0', '25', '50', '75', '100'], values=[0.2, 0.35, 0.5, 0.45, 0.7, 0.85], legend_label='Revenue')
eng.pareto(title='Pareto', items=[('A', 450), ('B', 300), ('C', 150), ('D', 80), ('E', 20)])
eng.stacked_area(title='Stacked Area', years=['2022', '2023', '2024', '2025'], series_data=[('Product', [100, 120, 150, 180], NAVY), ('Service', [50, 70, 90, 120], ACCENT_BLUE)])
eng.multi_bar_panel(title='Multi-Bar Panel', panels=[
    {'title': 'Revenue **growing**', 'unit': '¥M', 'legend': 'Annual', 'categories': ['2022', '2023', '2024'], 'values': [100, 130, 170], 'cagr': [{'rate': '+15% CAGR', 'start': 0, 'end': 2}]},
    {'title': 'Users **expanding**', 'unit': 'K', 'legend': 'Monthly', 'categories': ['2022', '2023', '2024'], 'values': [50, 80, 120], 'highlight_idx': [2]},
])

# ═══ IMAGES (7) ═══
eng.content_right_image(title='Content + Image', subtitle='Key Findings', bullets=['Point 1: Strong growth', 'Point 2: Expanding market'], image_label='Chart Image')
eng.full_width_image(title='Full Image', image_label='Hero Banner', overlay_text='Innovation Drives Growth')
eng.three_images(title='Three Images', items=[('Product A', 'Latest release', 'Product Photo'), ('Product B', 'In development', 'Prototype'), ('Product C', 'Concept', 'Mockup')])
eng.image_four_points(title='Image + 4 Points', image_label='Architecture Diagram', points=[('Speed', 'Sub-second response'), ('Scale', 'Millions of users'), ('Security', 'Enterprise-grade'), ('Simplicity', 'One-click deploy')])
eng.case_study_image(title='Case Study + Image', sections=[('Challenge', 'Legacy systems slowing growth', ACCENT_RED), ('Solution', 'Cloud-native migration', ACCENT_BLUE)], image_label='Architecture', kpis=[('40%', 'Cost Reduction'), ('3x', 'Speed Improvement')])
eng.quote_bg_image(image_label='Sunset', quote_text='Innovation distinguishes between a leader and a follower.', attribution='— Steve Jobs')
eng.goals_illustration(title='2026 Goals', goals=[('Growth', 'Achieve 30% revenue growth', ACCENT_BLUE), ('Quality', 'Maintain 99.9% uptime', ACCENT_GREEN), ('Team', 'Hire 50 engineers', ACCENT_ORANGE)], image_label='Team Photo')

# ═══ ADVANCED VIZ (7) ═══
eng.funnel(title='Funnel', stages=[('Visitors', '10,000', 1.0), ('Leads', '2,500', 0.6), ('Qualified', '800', 0.35), ('Customers', '200', 0.15)])
eng.cycle(title='Cycle', phases=[('Plan', 0.5, 1.5), ('Do', 3.5, 1.5), ('Check', 3.5, 4.0), ('Act', 0.5, 4.0)])
eng.venn(title='Venn', circles=[('Tech', ['AI', 'Cloud'], 1.0, 1.5, 4.0, 3.5), ('Business', ['Strategy', 'Growth'], 4.0, 1.5, 4.0, 3.5), ('Overlap', ['Digital Transformation'], 3.0, 2.5, 2.5, 2.0)])
eng.value_chain(title='Value Chain', stages=[('Inbound', 'Raw materials', ACCENT_BLUE), ('Operations', 'Manufacturing', ACCENT_GREEN), ('Outbound', 'Distribution', ACCENT_ORANGE), ('Sales', 'Revenue', NAVY)])
eng.checklist(title='Checklist', columns=['Project', 'Owner', 'Deadline', 'Status'], col_widths=[3.5, 2.5, 2.5, 2.5], rows=[['Cloud Migration', 'Alice', 'Q2 2026', 'active'], ['AI Platform', 'Bob', 'Q3 2026', 'risk'], ['Data Lake', 'Carol', 'Q4 2026', 'pending']])
eng.icon_grid(title='Icon Grid', items=[('AI Engine', 'Machine learning platform', ACCENT_BLUE), ('Cloud Infra', 'Scalable infrastructure', ACCENT_GREEN), ('Data Pipeline', 'Real-time processing', ACCENT_ORANGE), ('Security', 'Zero-trust framework', ACCENT_RED), ('Analytics', 'Business intelligence', NAVY), ('DevOps', 'CI/CD automation', ACCENT_BLUE)])
eng.rag_status(title='RAG Status', headers=['Project', 'Status', 'Progress', 'Budget', 'Notes'], rows=[['Alpha', ACCENT_GREEN, '85%', 'On budget', 'On track'], ['Beta', ACCENT_ORANGE, '60%', 'Over 10%', 'Needs attention'], ['Gamma', ACCENT_RED, '30%', 'Over 25%', 'At risk']])

# ═══ DASHBOARDS & SPECIAL (12) ═══
eng.kpi_tracker(title='KPI Tracker', kpis=[('Revenue Growth', 0.85, 'Target: 80%', 'on'), ('Customer NPS', 0.65, 'Target: 70%', 'risk'), ('Cost Reduction', 0.45, 'Target: 60%', 'off')], summary='Overall: 2 of 3 KPIs on track')
eng.bubble(title='Bubble Chart', bubbles=[(0.2, 0.8, 1.0, 'A', NAVY), (0.5, 0.5, 1.5, 'B', ACCENT_BLUE), (0.8, 0.3, 0.8, 'C', ACCENT_GREEN)], x_label='Market Size →', y_label='Growth Rate ↑')
eng.risk_matrix(title='Risk Matrix', grid_colors=[[ACCENT_RED, ACCENT_RED, ACCENT_ORANGE], [ACCENT_RED, ACCENT_ORANGE, ACCENT_GREEN], [ACCENT_ORANGE, ACCENT_GREEN, ACCENT_GREEN]], grid_lights=[[LIGHT_RED, LIGHT_RED, LIGHT_ORANGE], [LIGHT_RED, LIGHT_ORANGE, LIGHT_GREEN], [LIGHT_ORANGE, LIGHT_GREEN, LIGHT_GREEN]], risks=[(0, 2, 'Supply Chain'), (1, 1, 'Talent'), (2, 0, 'Compliance')])
eng.harvey_ball_table(title='Harvey Ball', criteria=['Cost', 'Speed', 'Quality', 'Risk'], options=['Option A', 'Option B', 'Option C'], scores=[[4, 2, 3], [3, 4, 2], [2, 3, 4], [1, 2, 3]])
eng.dashboard_kpi_chart(title='Dashboard KPI', kpi_cards=[('¥2.8B', 'Revenue', '+23% YoY', ACCENT_BLUE), ('85%', 'NPS Score', '+5pts', ACCENT_GREEN), ('92%', 'Retention', '+2pts', NAVY)])
eng.dashboard_table_chart(title='Dashboard Table', table_data={'headers': ['Region', 'Revenue', 'Growth'], 'col_widths': [2.0, 2.0, 2.0], 'rows': [['APAC', '¥1.2B', '+28%'], ['Europe', '¥0.8B', '+15%'], ['Americas', '¥0.8B', '+20%']]}, factoids=[('¥2.8B', 'Total Revenue', NAVY), ('+23%', 'YoY Growth', ACCENT_GREEN), ('85', 'NPS Score', ACCENT_BLUE)])
eng.stakeholder_map(title='Stakeholder Map', quadrants=[('紧密合作', 'Close Partner', LIGHT_BLUE, ['CEO', 'CTO']), ('持续关注', 'Keep Informed', LIGHT_GREEN, ['VP Sales']), ('重点管理', 'Key Manage', LIGHT_ORANGE, ['Board']), ('日常沟通', 'Regular Update', LIGHT_RED, ['Team Leads'])])
eng.decision_tree(title='Decision Tree', root=('Strategy',), branches=[('Growth', '+25%', ACCENT_BLUE, [('Organic', '+15%'), ('M&A', '+10%')]), ('Efficiency', '-20% cost', ACCENT_GREEN, [('Automation', '-12%'), ('Outsource', '-8%')])])
eng.metric_comparison(title='Metric Comparison', metrics=[('Response Time', '500ms', '120ms', '-76%'), ('Uptime', '99.5%', '99.99%', '+0.49%'), ('Cost/Request', '$0.05', '$0.02', '-60%')])
eng.agenda(title='Meeting Agenda', headers=[('时间', 1.5), ('议题', 4.0), ('负责人', 2.0), ('状态', 1.5)], items=[('09:00', 'Opening & Review', 'CEO', 'normal'), ('09:30', 'Strategy Update', 'CTO', 'key'), ('10:00', 'Break', '', 'break'), ('10:15', 'Financial Review', 'CFO', 'normal')])
eng.two_col_image_grid(title='Image Grid', items=[('Product Alpha', 'Next-gen platform', ACCENT_BLUE, 'Alpha Screenshot'), ('Product Beta', 'AI assistant', ACCENT_GREEN, 'Beta Screenshot'), ('Product Gamma', 'Analytics dashboard', ACCENT_ORANGE, 'Gamma Screenshot'), ('Product Delta', 'Mobile app', NAVY, 'Delta Screenshot')])
eng.numbered_list_panel(title='Strategic Priorities', items=[('Digital Transformation', 'Modernize all legacy systems'), ('AI Integration', 'Embed AI across products'), ('Global Expansion', 'Enter 5 new markets'), ('Talent Development', 'Hire and train 200+ engineers')], panel={'subtitle': 'Investment', 'big_number': '¥500M', 'big_label': 'Total Budget 2026', 'metrics': [('AI/ML', '¥200M'), ('Cloud', '¥150M'), ('Talent', '¥150M')]})

# ── Save ──
outpath = eng.save('output/full_test.html')
print(f"\n✅ All 68 methods called successfully!")
print(f"🎯 Open in browser: file://{os.path.abspath(outpath)}")
