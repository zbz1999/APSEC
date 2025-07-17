import pandas as pd

# 指定 CSV 文件路径
file_path = "H:/1_合并RQ3.2/1_max_year.csv"  # 请修改为你的实际文件路径

# 读取 CSV 文件
df = pd.read_csv(file_path, usecols=["Year of Max Developers"])

# 统计不同年份出现的次数
year_counts = df["Year of Max Developers"].value_counts()

# 输出结果
print(year_counts)
