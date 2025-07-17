import os
import pandas as pd

# 定义文件夹路径和输出文件
folder_path = "H:/1_合并RQ3.1"  # 替换为你的实际路径
output_folder = "H:/1_合并RQ3.4/all_commit_ratio"  # 结果保存路径
os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在

# 遍历文件夹中的所有CSV文件
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        output_path = os.path.join(output_folder, file)  # 结果存储路径

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 确保包含所需的列
        if {"Author", "Count"}.issubset(df.columns):
            # 计算总提交数量
            total_commits = df["Count"].sum()

            # 计算提交比例
            df["commit_ratio"] = (df["Count"] / total_commits) * 100

            # 重命名列
            df = df.rename(columns={"Author": "developer", "Count": "commit_count"})

            # 选择需要的列
            df_result = df[["developer", "commit_count", "commit_ratio"]]

            # 保存结果
            df_result.to_csv(output_path, index=False)

            print(f"处理完成: {file}, 结果已保存至 {output_path}")
        else:
            print(f"跳过 {file}，缺少必要列")
