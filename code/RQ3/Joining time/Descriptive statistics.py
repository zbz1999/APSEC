import pandas as pd

# 1. 读取数据
df = pd.read_csv("H:/1_合并RQ3.1/1_离开百分比统计.csv")  # 替换为您的实际文件路径

# 2. 基本数据检查
print("=== 数据前5行 ===")
print(df.head())

print("\n=== 数据基本信息 ===")
print(f"总项目数: {len(df)}")
print(f"缺失值检查:\n{df.isnull().sum()}")

# 3. 描述性统计
desc_stats = df[["早的离开百分比", "晚的离开百分比"]].describe().transpose()
desc_stats["IQR"] = desc_stats["75%"] - desc_stats["25%"]  # 添加四分位距

# 4. 计算两组差异
df["差异(晚-早)"] = df["晚的离开百分比"] - df["早的离开百分比"]
diff_stats = df["差异(晚-早)"].describe().to_frame().transpose()
diff_stats["IQR"] = diff_stats["75%"] - diff_stats["25%"]

# 5. 输出统计结果
print("\n=== 描述性统计 ===")
print(desc_stats[["count", "mean", "std", "min", "25%", "50%", "75%", "max", "IQR"]])

print("\n=== 晚-早差异统计 ===")
print(diff_stats[["count", "mean", "std", "min", "25%", "50%", "75%", "max", "IQR"]])

# 6. 保存统计结果到新CSV
output_stats = pd.concat([desc_stats, diff_stats])
output_stats.to_csv("H:/1_合并RQ3.1/1_描述性统计结果.csv", index_label="统计项")
print("\n统计结果已保存到: 描述性统计结果.csv")