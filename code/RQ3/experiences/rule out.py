import os
import pandas as pd

# 配置路径
input_folder = "H:/1_合并RQ3.1/all_leave"  # 修改为你的实际路径
output_folder = "H:/1_合并RQ3.2/all_output_csvs"  # 结果输出目录
output_file = os.path.join(output_folder, "all_output_csvs.csv")  # 结果输出文件

# 确保输出目录存在
os.makedirs(output_folder, exist_ok=True)

# 统计字典
year_counts = {}

# 遍历 CSV 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)

        # 读取 CSV 文件
        df = pd.read_csv(file_path, usecols=["First Commit", "Last Commit"])

        # 转换日期格式（增加异常处理）
        df["First Commit"] = pd.to_datetime(df["First Commit"], errors='coerce')
        df["Last Commit"] = pd.to_datetime(df["Last Commit"], errors='coerce')

        # 移除无效日期数据
        df = df.dropna(subset=["First Commit", "Last Commit"])

        # 计算时间差（单位：天）
        df["Active Days"] = (df["Last Commit"] - df["First Commit"]).dt.days

        # 过滤活跃时间少于 365 天的开发者
        df = df[df["Active Days"] >= 365]

        # 计算活跃年数（四舍五入）
        df["Active Years"] = (df["Active Days"] / 365).round().astype(int)

        # 统计每种活跃年数的开发者数量
        year_count = df["Active Years"].value_counts().to_dict()

        # 合并统计结果
        for year, count in year_count.items():
            year_counts[year] = year_counts.get(year, 0) + count

# 转换为 DataFrame 并保存
result_df = pd.DataFrame(sorted(year_counts.items()), columns=["Year", "Number of Developers"])
result_df.to_csv(output_file, index=False)

print(f"统计完成，结果保存在: {output_file}")
