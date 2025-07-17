import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


# 1. 数据加载与合并
def load_and_merge_data(folder_path):
    """加载并合并所有CSV文件"""
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = []

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        try:
            temp_df = pd.read_csv(file_path)
            # 确保列名一致
            temp_df.columns = ['Author', 'First Commit', 'Date Comparison', 'leave']
            df_list.append(temp_df)
        except Exception as e:
            print(f"处理文件 {file} 时出错: {e}")

    if not df_list:
        raise ValueError("未找到有效的CSV文件")

    return pd.concat(df_list, ignore_index=True)


# 2. 数据预处理 (修复版本)
def preprocess_data(df):
    """数据清洗和预处理"""
    # 处理缺失值
    print(f"原始数据量: {len(df)}")
    df = df.dropna()
    print(f"删除缺失值后数据量: {len(df)}")

    # 转换数据类型
    df['leave'] = df['leave'].astype(int)

    # 修复：将'Date Comparison'从字符串转换为数值
    print("转换Date Comparison为数值...")
    # 检查唯一值
    unique_values = df['Date Comparison'].unique()
    print(f"Date Comparison唯一值: {unique_values}")

    # 将'早'映射为0，'晚'映射为1
    df['Date Comparison'] = df['Date Comparison'].map({'早': 0, '晚': 1})

    # 检查转换后的分布
    print(f"转换后Date Comparison统计:\n{df['Date Comparison'].describe()}")
    print(f"转换后Date Comparison值分布:\n{df['Date Comparison'].value_counts()}")

    # 标准化Date Comparison (可选)
    scaler = StandardScaler()
    df['Date Comparison_std'] = scaler.fit_transform(df[['Date Comparison']])

    return df


# 3. 探索性分析 (更新标签)
def exploratory_analysis(df):
    """数据探索和可视化"""
    # 设置绘图风格
    sns.set(style="whitegrid")

    # 1. 加入时间分布
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.countplot(x='Date Comparison', data=df)
    plt.title('开发者加入时间分布')
    plt.xlabel('加入时间 (0=早, 1=晚)')
    plt.ylabel('人数')

    # 2. 离开比例
    plt.subplot(1, 2, 2)
    leave_counts = df['leave'].value_counts()
    plt.pie(leave_counts, labels=['留下', '离开'], autopct='%1.1f%%', startangle=90)
    plt.title('开发者离开比例')
    plt.tight_layout()
    plt.show()

    # 3. 加入时间与离开的关系
    plt.figure(figsize=(12, 10))

    # 3.1 分组条形图
    plt.subplot(2, 2, 1)
    # 直接使用0和1分组
    grouped = df.groupby('Date Comparison')['leave'].mean().reset_index()
    sns.barplot(x='Date Comparison', y='leave', data=grouped)
    plt.title('不同加入时间开发者的离开率')
    plt.xlabel('加入时间 (0=早, 1=晚)')
    plt.ylabel('离开率')
    plt.ylim(0, 1)

    # 3.2 逻辑回归趋势线
    plt.subplot(2, 2, 2)
    sns.regplot(x='Date Comparison', y='leave', data=df,
                logistic=True,
                scatter_kws={'alpha': 0.3, 's': 10},
                line_kws={'color': 'red', 'linewidth': 2})
    plt.title('加入时间与离开概率的关系')
    plt.xlabel('加入时间 (0=早, 1=晚)')
    plt.ylabel('离开概率')
    plt.yticks([0, 1], ['留下', '离开'])

    # 3.3 箱线图比较
    plt.subplot(2, 2, 3)
    sns.boxplot(x='leave', y='Date Comparison', data=df)
    plt.title('离开者与留下者的加入时间分布')
    plt.xlabel('是否离开 (0=留下, 1=离开)')
    plt.ylabel('加入时间 (0=早, 1=晚)')

    # 添加具体数值标签
    for i in [0, 1]:
        median = df[df['leave'] == i]['Date Comparison'].median()
        plt.text(i, median, f'{median:.2f}',
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 fontsize=10)

    # 3.4 交叉表热力图
    plt.subplot(2, 2, 4)
    cross_tab = pd.crosstab(df['Date Comparison'], df['leave'], normalize='index')
    sns.heatmap(cross_tab, annot=True, fmt='.2%', cmap='coolwarm')
    plt.title('加入时间与离开状态交叉分析')
    plt.xlabel('是否离开 (0=留下, 1=离开)')
    plt.ylabel('加入时间 (0=早, 1=晚)')
    plt.yticks([0.5, 1.5], ['早加入', '晚加入'], rotation=0)

    plt.tight_layout()
    plt.show()


# 4. 统计分析与建模
def statistical_analysis(df):
    """统计检验和建模"""
    # 4.1 基本统计
    stay_mean = df[df['leave'] == 0]['Date Comparison'].mean()
    leave_mean = df[df['leave'] == 1]['Date Comparison'].mean()
    print(f"留下组的平均加入时间: {stay_mean:.4f} (0=早, 1=晚)")
    print(f"离开组的平均加入时间: {leave_mean:.4f} (0=早, 1=晚)")
    print(f"差异: {abs(stay_mean - leave_mean):.4f}")

    # 4.2 T检验
    stay = df[df['leave'] == 0]['Date Comparison']
    leave = df[df['leave'] == 1]['Date Comparison']
    t_stat, p_value = stats.ttest_ind(stay, leave, equal_var=False)
    print(f"\nT检验结果: t = {t_stat:.4f}, p = {p_value:.4f}")

    if p_value < 0.05:
        print("结果显著：离开者与留下者的加入时间存在显著差异")
        if stay_mean > leave_mean:
            print("→ 留下组的加入时间晚于离开组")
        else:
            print("→ 留下组的加入时间早于离开组")
    else:
        print("结果不显著：加入时间与离开无显著关联")

    # 4.3 逻辑回归
    X = df[['Date Comparison']]
    y = df['leave']

    model = LogisticRegression()
    model.fit(X, y)

    coef = model.coef_[0][0]
    odds_ratio = np.exp(coef)
    print(f"\n逻辑回归系数: {coef:.4f}")
    print(f"加入时间每增加1单位，离开的几率变化: {odds_ratio:.4f}倍")

    if coef > 0:
        print("→ 加入时间越晚（数值越大），离开概率越高")
    else:
        print("→ 加入时间越早（数值越小），离开概率越高")

    # 4.4 预测概率可视化
    plt.figure(figsize=(10, 6))
    X_test = np.array([0, 1]).reshape(-1, 1)  # 只有两个值：0和1
    proba = model.predict_proba(X_test)[:, 1]

    sns.barplot(x=X_test.flatten(), y=proba, color='darkred')
    for i, p in enumerate(proba):
        plt.text(i, p, f'{p:.4f}', ha='center', va='bottom')

    plt.title('加入时间对离开概率的影响')
    plt.xlabel('加入时间 (0=早, 1=晚)')
    plt.ylabel('离开概率')
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return model


# 主函数
def main():
    # 替换为您的实际路径
    folder_path = "H:/1_合并RQ3.1/分为早晚_离开开发者/"

    # 执行分析流程
    try:
        df = load_and_merge_data(folder_path)
        df = preprocess_data(df)
        exploratory_analysis(df)
        model = statistical_analysis(df)

        # 保存处理后的数据
        output_path = "H:/1_合并RQ3.1/加入时间合并分析/combined_analysis.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"分析完成，结果已保存至: {output_path}")

    except Exception as e:
        print(f"分析过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()