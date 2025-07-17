# -*- coding: utf-8 -*-
"""PLoS ONE 项目规模与开发者离开率分析（完整版）"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal, mannwhitneyu
from scikit_posthocs import posthoc_dunn
import warnings
import os
import matplotlib

# ========================
# 中文显示配置（关键修改）
# ========================
# 方法1：使用系统字体（推荐）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 方法2：指定具体字体路径（如果系统字体不工作）
# font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑路径
# matplotlib.font_manager.fontManager.addfont(font_path)
# plt.rcParams['font.family'] = 'Microsoft YaHei'

warnings.filterwarnings('ignore')

# ========================
# 步骤0：设置输出目录
# ========================
output_dir = "H:/1_合并RQ3.8/teamsize/"
os.makedirs(output_dir, exist_ok=True)  # 确保目录存在

# ========================
# 步骤1：数据加载与清洗
# ========================
file_path = os.path.join(output_dir, "合并结果.csv")
try:
    df = pd.read_csv(file_path, encoding='utf-8')  # 尝试utf-8
except:
    df = pd.read_csv(file_path, encoding='gbk')  # 尝试gbk

# 检查必要列是否存在
assert '项目规模' in df.columns, "CSV中缺少'项目规模'列"
assert '离开百分比' in df.columns, "CSV中缺少'离开百分比'列"

# 统一规模分类名称
df['项目规模'] = df['项目规模'].replace({
    '大规模项目': '大项目',
    '中规模项目': '中项目',
    '小规模项目': '小项目'
})

# 删除缺失值
df = df.dropna(subset=['项目规模', '离开百分比']).copy()

print("=== 数据概览 ===")
print(f"总样本量: {len(df)}")
print(df['项目规模'].value_counts())

# ========================
# 步骤2：样本平衡与分组
# ========================
np.random.seed(42)

counts = df['项目规模'].value_counts()
n_medium = counts.get('中项目', 0)
n_small = counts.get('小项目', 0)

# 从大项目中随机抽取与中项目相同的数量
if n_medium > 0:
    large_sampled = df[df['项目规模'] == '大项目'].sample(n=min(n_medium, counts['大项目']))
else:
    large_sampled = pd.DataFrame()

df_balanced = pd.concat([
    large_sampled,
    df[df['项目规模'] == '中项目'],
    df[df['项目规模'] == '小项目']
])

print("\n=== 平衡后数据 ===")
print(df_balanced['项目规模'].value_counts())


# ========================
# 步骤3：统计检验
# ========================
def run_statistical_tests(data):
    results = {}
    groups = data.groupby('项目规模')['离开百分比'].apply(list)

    if len(groups) >= 2:
        if len(groups) == 2:
            stat, p = mannwhitneyu(groups[0], groups[1])
            test_name = "Mann-Whitney U"
        else:
            stat, p = kruskal(*groups)
            test_name = "Kruskal-Wallis"

        results['test'] = {'name': test_name, 'stat': stat, 'p': p}

        if test_name == "Kruskal-Wallis":
            results['effect_size'] = {'η²': stat / (len(data) - 1)}

        if p < 0.05 and len(groups) > 2:
            dunn_df = posthoc_dunn(data, val_col='离开百分比', group_col='项目规模', p_adjust='fdr_bh')
            results['posthoc'] = dunn_df
    return results


results = run_statistical_tests(df_balanced)

# ========================
# 步骤4：可视化（优化版）
# ========================
plt.figure(figsize=(10, 6), dpi=100)
sns.set_style("whitegrid", {
    'font.sans-serif': ['Microsoft YaHei', 'SimHei'],  # 中文字体设置
    'axes.unicode_minus': False
})

# 自定义颜色
palette = {"大项目": "#4e79a7", "中项目": "#f28e2b", "小项目": "#e15759"}

# 绘制小提琴图+箱线图
ax = sns.violinplot(
    x='项目规模',
    y='离开百分比',
    data=df_balanced,
    inner='quartile',
    palette=palette,
    cut=0,
    linewidth=1.5
)

# 添加统计标注
if 'test' in results:
    test = results['test']
    sig_symbol = '*' if test['p'] < 0.05 else 'n.s.'
    ax.set_title(
        f"{test['name']}检验: {sig_symbol} (p={test['p']:.3f})",
        fontsize=14,
        pad=20
    )

# 设置标签样式
ax.set_xlabel("项目规模", fontsize=12, labelpad=10)
ax.set_ylabel("开发者离开率 (%)", fontsize=12, labelpad=10)

# 调整坐标轴字体
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(11)

# 保存高清图
chart_path = os.path.join(output_dir, "leave_rate_analysis.png")
plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()  # 避免重复显示

# ========================
# 步骤5：结果输出与保存
# ========================
print("\n=== 统计分析结果 ===")
if 'test' in results:
    test = results['test']
    print(f"{test['name']}检验:")
    print(f"• 统计量: {test['stat']:.2f}")
    print(f"• p值: {test['p']:.4f} ({'显著' if test['p'] < 0.05 else '不显著'})")
    if 'effect_size' in results:
        print(f"• 效应量 η²: {results['effect_size']['η²']:.3f}")

if 'posthoc' in results:
    print("\n事后检验（Dunn检验，校正后p值）:")
    print(results['posthoc'])


# 保存结果（UTF-8 with BOM）
def save_csv_with_bom(df, path):
    df.to_csv(path, index=False, encoding='utf_8_sig')


save_csv_with_bom(df_balanced, os.path.join(output_dir, "balanced_data.csv"))
if 'posthoc' in results:
    save_csv_with_bom(results['posthoc'], os.path.join(output_dir, "posthoc_results.csv"))

print("\n分析结果已保存到:")
print(f"- 图表: {chart_path}")
print(f"- 平衡数据: {os.path.join(output_dir, 'balanced_data.csv')}")
if 'posthoc' in results:
    print(f"- 事后检验: {os.path.join(output_dir, 'posthoc_results.csv')}")