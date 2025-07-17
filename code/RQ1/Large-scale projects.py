import os
import pandas as pd
import shutil

# 源文件夹路径
source_folder_path = "H:/1_developer_last_commit"
# 目标文件夹路径
destination_folder_path = "H:/1_合并RQ2"

# 如果目标文件夹不存在，则创建目标文件夹
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# 遍历源文件夹中的所有CSV文件
for filename in os.listdir(source_folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(source_folder_path, filename)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 假设开发者数据在名为 "Developer" 的列中，根据实际情况调整列名
        developer_count = df['Author'].nunique()

        # 计算分类区间（例如：每100人一个区间）
        category = (developer_count // 100) * 100
        category_folder = os.path.join(destination_folder_path, f"{category}-{category + 99}")

        # 创建分类文件夹（如果不存在）
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # 将文件保存到对应的分类文件夹
        shutil.copy(file_path, os.path.join(category_folder, filename))

print("文件分类并保存成功！")
