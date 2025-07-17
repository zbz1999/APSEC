import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# 读取CSV文件
file_path = 'H:/1_合并RQ2/percentage_distribution.csv'  # 替换为您的实际文件路径
data = pd.read_csv(file_path)

# 假设数据格式如您提供的：
# Percentage Range,0-99,100-199,200-299,300-399,400-499,500-599,600-699,700-799,800-899,900-999
# 0-10%,2,0,1,0,0,0,0,0,0,0
# 10-20%,0,0,1,0,0,0,0,0,0,0
# ...
# 90-100%,6,3,4,2,3,2,0,0,0,2

# 转换为列联表（这里假设您的数据列以逗号分隔）
contingency_table = data.iloc[:, 1:].values  # 取所有行，去掉第一列（Percentage Range）
# 将字符串索引转为实际列联表
percentage_ranges = data.iloc[:, 0].tolist()  # 获取第一列（百分比范围）
contingency_table = pd.DataFrame(contingency_table, index=percentage_ranges)

# 进行卡方检验
chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

# 计算样本量、行数和列数
n = contingency_table.sum().sum()  # 总样本量
k = contingency_table.shape[1]  # 列数
r = contingency_table.shape[0]  # 行数

# Cramer's V 计算
def cramers_v(chi2_stat, n, k, r):
    return np.sqrt(chi2_stat / (n * min(k - 1, r - 1)))

v = cramers_v(chi2_stat, n, k, r)

# 输出结果
print(f"Chi-Square Statistic: {chi2_stat}")
print(f"P-Value: {p_value}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected Frequencies: \n{expected}")
print(f"Cramer's V: {v}")
