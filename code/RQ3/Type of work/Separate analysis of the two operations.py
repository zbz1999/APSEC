import pandas as pd

# 读取CSV文件（请替换为你的实际文件路径）
file_path = "H:/1_合并RQ3.6/工作类型与离开合并结果.csv"  # 修改为你的实际文件路径
df = pd.read_csv(file_path)

# 筛选出Main Work Type为Code或Documentation的数据
filtered_df = df[df['Main Work Type'].isin(['Code', 'Documentation'])]

# 按Main Work Type和leave分组计算计数
grouped = filtered_df.groupby(['Main Work Type', 'leave']).size().unstack(fill_value=0)

# 计算百分比
percentages = grouped.div(grouped.sum(axis=1), axis=0) * 100

# 重命名列以便更清晰
percentages.columns = ['Leave_0_Percentage', 'Leave_1_Percentage']

# 打印结果
print("百分比结果:")
print(percentages)
