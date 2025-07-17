import pandas as pd
import os

# 定义文件路径
input_file = r"H:\1_合并RQ2\10_20_matched_projects.csv"  # 请将 "your_file.csv" 替换为你的文件名
output_dir = r"H:\1_合并RQ2"
output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_percentage_distribution.csv")

# 读取CSV文件
df = pd.read_csv(input_file)

# 过滤出 'Median Change Percentage' 列，并将百分比字符串转换为浮点数
df['Median Change Percentage'] = df['Median Change Percentage'].str.rstrip('%').astype(float)

# 创建每10%的区间，统计每个区间的数量
bins = range(0, 101, 10)
labels = [f"{i}-{i+10}%" for i in bins[:-1]]
df['Percentage Range'] = pd.cut(df['Median Change Percentage'], bins=bins, labels=labels, right=False)

# 统计每个区间的数量
range_counts = df['Percentage Range'].value_counts().sort_index()

# 将结果保存到新的CSV文件
range_counts.to_csv(output_file, header=['Count'])

print(f"统计结果已保存到 {output_file}")
