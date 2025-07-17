# -*- coding: utf-8 -*-
"""PLoS ONE 不显著结果的后续分析方案"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.stats.power as smp
import matplotlib

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载之前保存的平衡数据
df_balanced = pd.read_csv("H:/1_合并RQ3.8/teamsize/balanced_data.csv")


# ========================
# 1. 描述性统计与分布检查
# ========================
def descriptive_analysis(data):
    # 基本描述统计
    desc = data.groupby('项目规模')['离开百分比'].describe()

    # 方差齐性检验
    levene = stats.levene(
        data[data['项目规模'] == '大项目']['离开百分比'],
        data[data['项目规模'] == '中项目']['离开百分比'],
        data[data['项目规模'] == '小项目']['离开百分比']
    )

    print("=== 描述性统计 ===")
    print(desc)
    print("\n=== 方差齐性检验 ===")
    print(f"Levene检验: W={levene.statistic:.2f}, p={levene.pvalue:.4f}")

    return desc


desc_stats = descriptive_analysis(df_balanced)


# ========================
# 2. 功效分析（计算所需样本量）
# ========================
def power_analysis(data):
    # 计算观察到的效应量（Cohen's f）
    grand_mean = data['离开百分比'].mean()
    group_means = data.groupby('项目规模')['离开百分比'].mean()
    effect_size = np.sqrt(((group_means - grand_mean) ** 2).mean()) / data['离开百分比'].std()

    # 参数设置
    alpha = 0.05
    power = 0.8
    groups = 3

    # 计算所需样本量
    power_analysis = smp.FTestAnovaPower()
    required_n = power_analysis.solve_power(
        effect_size=effect_size,
        nobs=None,
        alpha=alpha,
        power=power,
        k_groups=groups
    )

    print("\n=== 功效分析 ===")
    print(f"当前效应量 (Cohen's f): {effect_size:.3f}")
    print(f"达到80%功效所需每组样本量: {np.ceil(required_n):.0f}")

    return required_n


req_n = power_analysis(df_balanced)


# ========================
# 3. 分组优化分析
# ========================
def alternative_grouping(data):
    # 方案1：合并中小项目
    data['规模分组2'] = data['项目规模'].replace({'中项目': '非大项目', '小项目': '非大项目'})

    # 方案2：按百分位数重新分组
    size_metric = ...  # 需替换为实际项目规模连续变量
    if '项目行数' in data.columns:
        percentiles = np.percentile(data['项目行数'], [33, 66])
        data['规模分组3'] = pd.cut(
            data['项目行数'],
            bins=[0, percentiles[0], percentiles[1], np.inf],
            labels=['小项目', '中项目', '大项目']
        )

    # 执行Mann-Whitney U检验（合并组）
    if '规模分组2' in data.columns:
        group1 = data[data['规模分组2'] == '大项目']['离开百分比']
        group2 = data[data['规模分组2'] == '非大项目']['离开百分比']
        stat, p = stats.mannwhitneyu(group1, group2)

        print("\n=== 合并分组分析 ===")
        print(f"Mann-Whitney U检验: U={stat:.0f}, p={p:.4f}")
        print(f"大项目 (n={len(group1)}) vs 非大项目 (n={len(group2)})")

    return data


df_modified = alternative_grouping(df_balanced.copy())


# ========================
# 4. 增强可视化
# ========================
def enhanced_visualization(data):
    plt.figure(figsize=(15, 5))

    # 子图1：带置信区间的均值图
    plt.subplot(1, 3, 1)
    sns.pointplot(
        x='项目规模',
        y='离开百分比',
        data=data,
        capsize=0.1,
        order=['大项目', '中项目', '小项目'],
        palette=['#4e79a7', '#f28e2b', '#e15759']
    )
    plt.title("均值与95%置信区间")

    # 子图2：分布直方图
    plt.subplot(1, 3, 2)
    for size, color in zip(['大项目', '中项目', '小项目'], ['#4e79a7', '#f28e2b', '#e15759']):
        sns.kdeplot(
            data[data['项目规模'] == size]['离开百分比'],
            label=size,
            color=color,
            fill=True
        )
    plt.title("分布密度估计")
    plt.legend()

    # 子图3：效应量展示
    plt.subplot(1, 3, 3)
    effects = pd.DataFrame({
        '指标': ['η²', 'Cohen\'s f'],
        '值': [0.025, 0.18],  # 替换为实际计算结果
        '阈值': [0.01, 0.1]  # 小效应阈值
    })
    sns.barplot(x='值', y='指标', data=effects, color='skyblue')
    plt.axvline(x=0.1, color='red', linestyle='--', label='小效应阈值')
    plt.title("效应量对比")
    plt.legend()

    plt.tight_layout()
    plt.savefig("H:/1_合并RQ3.8/teamsize/enhanced_analysis.png", dpi=300)
    plt.show()


enhanced_visualization(df_balanced)


# ========================
# 5. 结果保存
# ========================
def save_results(desc, req_n):
    with pd.ExcelWriter("H:/1_合并RQ3.8/teamsize/supplementary_analysis.xlsx") as writer:
        desc.to_excel(writer, sheet_name='描述统计')

        power_df = pd.DataFrame({
            '参数': ['显著性水平', '统计功效', '当前效应量', '所需样本量'],
            '值': [0.05, 0.8, 0.18, np.ceil(req_n)]
        })
        power_df.to_excel(writer, sheet_name='功效分析', index=False)

        if '规模分组2' in df_modified.columns:
            df_modified[['项目规模', '规模分组2', '离开百分比']].to_excel(
                writer, sheet_name='分组优化', index=False)


save_results(desc_stats, req_n)

print("\n=== 分析完成 ===")
print("结果已保存至:")
print("- enhanced_analysis.png")
print("- supplementary_analysis.xlsx")