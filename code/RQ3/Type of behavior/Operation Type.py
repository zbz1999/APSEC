import pandas as pd
import os

# 输入文件夹路径：包含所有需要处理的CSV文件
input_folder = 'H:/1_合并RQ3.5/筛选过后的开发者'  # 请替换为实际文件夹路径

# 输出文件夹路径：保存结果的文件夹
output_folder = 'H:/1_合并RQ3.5/all_primary_action_type'  # 请替换为实际输出文件夹路径

# 确保输出文件夹存在，如果不存在则创建
os.makedirs(output_folder, exist_ok=True)

# 获取输入文件夹中所有CSV文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 操作列（不包括 Developer 列）
action_columns = ['Additions', 'Modifications', 'Deletions', 'Renames', 'Replaces', 'Copies']

# 遍历所有 CSV 文件
for csv_file in csv_files:
    # 构建文件的完整路径
    file_path = os.path.join(input_folder, csv_file)

    try:
        # 读取CSV文件
        data = pd.read_csv(file_path)

        # 检查文件中是否包含需要的六个操作列
        if not all(col in data.columns for col in action_columns):
            print(f"文件 {csv_file} 缺少某些操作列，跳过此文件。")
            continue  # 跳过此文件，处理下一个文件

        # 找出每行中数值最大的列（即主要操作类型）
        data['Primary_Action_Type'] = data[action_columns].idxmax(axis=1)

        # 动态生成输出文件名：根据输入文件名命名
        output_file_name = f'{os.path.splitext(csv_file)[0]}_primary_action_type.csv'
        output_file_path = os.path.join(output_folder, output_file_name)

        # 保存结果到新的CSV文件，只保留 Developer 和 Primary_Action_Type 列
        data[['Developer', 'Primary_Action_Type']].to_csv(output_file_path, index=False)

        print(f"文件 {csv_file} 处理完成，结果已保存到 {output_file_path}")

    except Exception as e:
        # 捕获并打印处理文件时的错误
        print(f"处理文件 {csv_file} 时发生错误: {e}")
