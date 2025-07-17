# -*- coding: utf-8 -*-
"""加权统计检验（小→中→大顺序+中英文标签）"""
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# ========================
# 0. 字体配置
# ========================
# 初始化字体路径
font_path = None

# 尝试使用系统字体
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Windows优先
    plt.rcParams['axes.unicode_minus'] = False
    print("已使用系统默认中文字体")
except:
    # 如果失败，尝试指定字体路径
    try:
        font_path = "C:/Windows/Fonts/msyh.ttc"  # 常见Windows字体路径
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        print(f"已手动加载字体: {font_path}")
    except Exception as e:
        print(f"字体加载失败: {str(e)}")
        # 如果所有尝试都失败，使用英文显示
        plt.rcParams['font.sans-serif'] = ['Arial']

# ========================
# 1. 数据准备
# ========================
df = pd.read_csv("H:/1_合并RQ3.8/teamsize/合并结果.csv")
# 修改为小→中→大顺序
df['项目规模'] = df['项目规模'].replace({
    '小规模项目': 'small',
    '中规模项目': 'middle',
    '大规模项目': 'big'
})

# ========================
# 2. 权重计算函数
# ========================
def calculate_weights(data, method="inverse"):
    group_counts = data['项目规模'].value_counts()

    if method == "inverse":
        weights = data['项目规模'].map({g: 1 / count for g, count in group_counts.items()})
    elif method == "equal":
        weights = data['项目规模'].map({g: 1 for g in group_counts.index})
    elif method == "sqrt":
        weights = data['项目规模'].map({g: 1 / np.sqrt(count) for g, count in group_counts.items()})

    return weights / weights.sum()

# ========================
# 3. 加权统计分析
# ========================
def weighted_analysis(data, weight_method="inverse"):
    weights = calculate_weights(data, method=weight_method)

    weighted_stats = []
    # 按小→中→大顺序处理
    for group in ['small', 'middle', 'big']:
        group_data = data[data['项目规模'] == group]['离开百分比']
        w_stats = DescrStatsW(group_data, weights=weights[data['项目规模'] == group])
        weighted_stats.append({
            '项目规模': group,
            '加权均值': w_stats.mean,
            '加权标准差': np.sqrt(w_stats.var),
            '原始样本量': len(group_data),
            '等效样本量': (weights[data['项目规模'] == group].sum()) ** 2 /
                     (weights[data['项目规模'] == group] ** 2).sum()
        })

    # 注意检验顺序与绘图顺序一致
    kw_stat, kw_p = stats.kruskal(
        data[data['项目规模'] == 'small']['离开百分比'],
        data[data['项目规模'] == 'middle']['离开百分比'],
        data[data['项目规模'] == 'big']['离开百分比']
    )

    return pd.DataFrame(weighted_stats), kw_stat, kw_p, weights

# ========================
# 4. 执行分析与可视化
# ========================
weighted_df, kw_stat, kw_p, weight_vector = weighted_analysis(df)

plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# 定义小→中→大顺序
order = ['small', 'middle', 'big']
# 颜色顺序调整为红→橙→蓝（小→中→大）
palette = ['#e15759', '#f28e2b', '#4e79a7']

ax = sns.boxplot(
    x='项目规模',
    y='离开百分比',
    data=df,
    order=order,  # 显式指定顺序
    palette=palette,  # 调整颜色顺序
    showmeans=True,
    meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "red"}
)

# 设置标题和标签
if font_path:
    # 使用中文字体
    font_prop = fm.FontProperties(fname=font_path)
    ax.set_title(f"项目规模对开发者离开率的影响\n(Kruskal-Wallis p={kw_p:.3f})",
                fontproperties=font_prop, size=14)
    ax.set_xlabel("项目规模", fontproperties=font_prop, size=12)
    ax.set_ylabel("离开百分比 (%)", fontproperties=font_prop, size=12)
    # 设置x轴中文标签
    ax.set_xticklabels(['小项目', '中项目', '大项目'], fontproperties=font_prop)
else:
    # 使用英文
    ax.set_title(f"Project Size vs Developer Departure Rate\n(Kruskal-Wallis p={kw_p:.3f})", size=14)
    ax.set_xlabel("Project Size", size=12)
    ax.set_ylabel("Departure Rate (%)", size=12)
    ax.set_xticklabels(['Small', 'Medium', 'Large'])

plt.tight_layout()
plt.savefig("H:/1_合并RQ3.8/teamsize/weighted_analysis_ordered.png",
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ========================
# 5. 结果输出
# ========================
print("=== 加权描述统计（小→中→大顺序） ===")
print(weighted_df)
print("\n=== 非参数检验 ===")
print(f"Kruskal-Wallis H统计量: {kw_stat:.2f}")
print(f"p值: {kw_p:.4f} ({'显著' if kw_p < 0.05 else '不显著'})")