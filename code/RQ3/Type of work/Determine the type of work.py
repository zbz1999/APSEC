import os
import pandas as pd
from pathlib import Path

# 定义输入和输出文件夹路径
input_folder = Path("H:/1_合并RQ3.6/筛选过后的开发者")  # CSV文件所在的目录
output_folder = Path("H:/1_合并RQ3.6/all_work_type")  # 处理后CSV文件的目录

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 需要比较的工作类型列（排除Developer列）
work_type_columns = [
    "Code", "Other", "Documentation", "Image", "Packaging", "Multimedia",
    "Internationalization (i18n)", "User Interface (UI)",
    "Developer Documentation (devel-doc)", "Build"
]

# 遍历所有CSV文件
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        file_path = input_folder / file
        df = pd.read_csv(file_path)

        # 确保CSV文件包含所需列
        if "Developer" in df.columns and all(col in df.columns for col in work_type_columns):
            # 找到每位开发者的主要工作类型
            df["Main Work Type"] = df[work_type_columns].idxmax(axis=1)

            # 只保留 Developer 和 Main Work Type 两列
            df = df[["Developer", "Main Work Type"]]

            # 生成输出文件路径
            output_file_path = output_folder / file

            # 保存到新的CSV文件
            df.to_csv(output_file_path, index=False)
            print(f"处理完成：{file}，结果已保存到 {output_file_path}")
        else:
            print(f"文件 {file} 缺少必要的列，跳过处理。")
