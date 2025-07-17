import os
import pandas as pd

# 设置源文件夹和输出文件夹
input_folder = "H:/1_合并RQ2/0-99"  # 请替换为实际文件夹路径
output_base_folder = "H:/1_合并RQ2"  # 请替换为实际输出文件夹路径


# 创建按行数区间输出文件夹
def create_output_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# 获取文件夹中的所有csv文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 遍历每个文件
for file_name in csv_files:
    file_path = os.path.join(input_folder, file_name)

    # 读取csv文件
    df = pd.read_csv(file_path)
    row_count = len(df)

    # 计算区间范围
    range_start = (row_count // 10) * 10
    range_end = range_start + 10
    range_folder_name = f"{range_start}_{range_end}"

    # 设置输出文件夹路径
    output_folder = os.path.join(output_base_folder, range_folder_name)
    create_output_folder(output_folder)

    # 保存文件到对应区间的文件夹
    output_path = os.path.join(output_folder, file_name)
    df.to_csv(output_path, index=False)

    print(f"文件 {file_name} 行数为 {row_count}，保存到文件夹 {range_folder_name}")
'''边界值示例：
如果文件的行数为 0 或者 1，则会被保存到 0_10 文件夹。
行数为 9 的文件，也会被保存到 0_10 文件夹。
行数为 10 的文件，会被保存到 10_20 文件夹。
行数为 19 的文件，会被保存到 10_20 文件夹。
行数为 20 的文件，会被保存到 20_30 文件夹。
如果行数为 99，则文件会被保存到 90_100 文件夹'''