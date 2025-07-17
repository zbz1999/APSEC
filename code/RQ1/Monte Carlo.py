import numpy as np
from scipy.stats import chi2_contingency

# 原始数据表
observed = np.array([
    [2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [3, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [17, 6, 3, 1, 4, 0, 1, 1, 0, 2],
    [13, 18, 5, 8, 4, 2, 6, 2, 2, 5],
    [16, 29, 15, 20, 7, 8, 4, 8, 1, 3],
    [12, 38, 33, 24, 12, 9, 7, 5, 3, 6],
    [7, 2, 6, 2, 3, 2, 0, 0, 0, 2]
])

# 计算原始卡方统计量和期望频数
chi2, p_value, dof, expected = chi2_contingency(observed)

# 自定义计算卡方统计量
def calculate_chi2(observed, expected):
    # 仅保留期望值大于 0 的单元格
    mask = expected > 0
    return np.sum((observed[mask] - expected[mask]) ** 2 / expected[mask])

# 蒙特卡罗模拟
n_simulations = 10000
simulated_chi2 = []

for _ in range(n_simulations):
    # 按期望频数生成模拟表
    simulated = np.random.multinomial(observed.sum(), expected.flatten() / expected.sum()).reshape(expected.shape)

    # 计算模拟卡方统计量（跳过零期望频数单元格）
    sim_chi2 = calculate_chi2(simulated, expected)
    simulated_chi2.append(sim_chi2)

# 计算蒙特卡罗 P 值
simulated_chi2 = np.array(simulated_chi2)
p_value_simulated = np.mean(simulated_chi2 >= chi2)

# 计算Cramer's V系数
n = observed.sum()  # 样本总数
cramers_v = np.sqrt(chi2 / (n * min(observed.shape) - 1))

# 输出结果
R, C = observed.shape  # 获取行数和列数
print(f"原始卡方统计量: {chi2}")
print(f"自由度 (Degrees of Freedom): {dof}")
print(f"期望频数 (Expected Frequencies): \n{expected}")
print(f"蒙特卡罗 P 值: {p_value_simulated}")
print(f"Cramer's V 系数: {cramers_v}")
print(f"总样本数 (n): {n}")
print(f"列联表的行数 (R): {R}")
print(f"列联表的列数 (C): {C}")
