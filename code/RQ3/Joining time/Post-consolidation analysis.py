import os
import pandas as pd
from datetime import datetime

# 配置路径
input_folder = "H:/1_469_合并后的开发者"  # 原始 CSV 文件夹
output_folder = "H:/1_合并RQ3.1"  # 处理后的 CSV 文件夹
os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在

# 设定基准日期
base_date = datetime(2024, 6, 16)

# 机器人关键词（大小写不敏感）
bot_keywords = ["bot", "ci", "automation", "actions", "service", "build", "dependabot"]

# 遍历 CSV 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)

        # 读取 CSV 文件
        df = pd.read_csv(file_path, usecols=["Canonical Name", "Commit Count", "First Commit", "Last Commit"])

        # 重命名列
        df.rename(columns={"Canonical Name": "Author", "Commit Count": "Count"}, inplace=True)

        # 转换日期格式
        df["First Commit"] = pd.to_datetime(df["First Commit"], errors='coerce')
        df["Last Commit"] = pd.to_datetime(df["Last Commit"], errors='coerce')

        # 排除机器人账户
        df = df[~df["Author"].str.lower().str.contains('|'.join(bot_keywords), na=False)]

        # 过滤规则
        df = df[(df["Count"] >= 2) & ((df["Last Commit"] - df["First Commit"]).dt.days >= 2)]

        # 计算 `Last Commit` 到 `2024年6月16日` 的天数
        df["Days Since Last Commit"] = (base_date - df["Last Commit"]).dt.days

        # 保存文件
        output_path = os.path.join(output_folder, file_name)
        df.to_csv(output_path, index=False)

        # 输出处理完成的文件名
        print(f"处理完成: {file_name}")
