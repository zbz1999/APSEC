import os
import pandas as pd

# 定义文件夹路径和输出文件
folder_path = "H:/1_合并RQ3.3/all_matched_results"  # 你的CSV文件所在文件夹
output_file = "H:/1_合并RQ3.3/1_combined_cleaned_data_1.csv"  # 合并后的CSV文件路径

# 创建一个空的 DataFrame 来存储合并结果
merged_df = pd.DataFrame(columns=["Author", "Commit Frequency"])

# 遍历文件夹中的所有CSV文件
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 确保包含需要的列
        if {"Author", "Commit Frequency"}.issubset(df.columns):
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        else:
            print(f"跳过 {file}，缺少必要列")

# 保存合并后的结果
merged_df.to_csv(output_file, index=False)

print(f"合并完成，结果保存至 {output_file}")
