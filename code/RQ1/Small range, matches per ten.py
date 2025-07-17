import os
import pandas as pd

# 设置文件夹路径
first_folder = "H:/1_合并RQ2/10_20"  # 第一个文件夹路径，包含提交记录文件
second_file_path = "H:/1_合并RQ2/matched_files/combined_matched_data_0-99.csv"  # 匹配数据文件

# 根据第一个文件夹的名称生成输出文件名
folder_name = os.path.basename(first_folder)
output_file_path = f"H:/1_合并RQ2/{folder_name}_matched_projects.csv"

# 初始化一个空的DataFrame存储匹配结果
all_matched_data = pd.DataFrame()

# 读取匹配数据CSV文件
df = pd.read_csv(second_file_path)

# 遍历文件夹中的文件
for file_name in os.listdir(first_folder):
    # 处理文件名：移除前缀和后缀
    clean_name = file_name.replace("last_commit_", "").replace("_commits.csv", "")

    # 在匹配数据中查找对应项目
    matched_rows = df[df['Project'] == clean_name]

    if not matched_rows.empty:
        # 提取需要的列
        matched_data = matched_rows[['Project', 'Median Change Percentage']]

        # 添加到结果集
        all_matched_data = pd.concat([all_matched_data, matched_data], ignore_index=True)

        print(f"匹配成功：{clean_name}，已添加到输出文件")

# 输出匹配结果到CSV文件
if not all_matched_data.empty:
    all_matched_data.to_csv(output_file_path, index=False)
    print(f"匹配结果已保存至：{output_file_path}")
else:
    print("未找到任何匹配的项目。")