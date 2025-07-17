import os
import pandas as pd

# 设置输入文件夹和输出文件夹路径
input_folder = r"H:/1_合并RQ3.2/fenkaide_all_output_csvs"  # 请替换为你的输入文件夹路径
output_file = r"H:/1_合并RQ3.2/1_max_year.csv"  # 输出文件路径

# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 存储结果的列表
results = []
empty_files = []  # 用于存储空文件的文件名

# 遍历每个CSV文件
for file in csv_files:
    file_path = os.path.join(input_folder, file)  # 获取当前文件路径

    # 检查文件是否为空
    if os.path.getsize(file_path) == 0:
        empty_files.append(file)  # 如果文件为空，记录文件名
        continue  # 跳过该文件

    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 如果文件为空（即没有数据），跳过
    if df.empty:
        empty_files.append(file)  # 记录空文件名
        continue

    # 获取最大值对应的年份
    max_developer_row = df.loc[df['Number of Developers'].idxmax()]  # 获取最大值所在行
    max_developer_year = max_developer_row['Year']  # 获取对应的年份

    # 将结果添加到列表中
    results.append({
        "File Name": file,
        "Year of Max Developers": max_developer_year
    })

# 将结果保存到新的CSV文件
results_df = pd.DataFrame(results)
results_df.to_csv(output_file, index=False)

print(f"结果已保存到 {output_file}")

# 输出空文件名
if empty_files:
    print(f"空文件名: {', '.join(empty_files)}")
else:
    print("没有空文件。")
