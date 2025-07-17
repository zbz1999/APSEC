import pandas as pd
import os

# 设置输入文件夹路径，包含所有需要处理的CSV文件
input_folder = 'H:/1_合并RQ3.5/all_primary_action_type'  # 请替换为实际文件夹路径

# 设置输出文件夹路径，保存统计结果
output_folder = 'H:/1_合并RQ3.5/all_Primary_Action_Type_counts'  # 请替换为实际输出文件夹路径

# 确保输出文件夹存在，如果不存在则创建
os.makedirs(output_folder, exist_ok=True)

# 获取输入文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 遍历所有CSV文件进行统计
for csv_file in csv_files:
    # 构建文件的完整路径
    file_path = os.path.join(input_folder, csv_file)

    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 检查文件是否包含 'Primary_Action_Type' 列
        if 'Primary_Action_Type' in df.columns:
            # 统计 Primary_Action_Type 列中每个不同值出现的次数
            action_type_counts = df['Primary_Action_Type'].value_counts()

            # 生成输出文件路径，以原文件名命名
            output_file_path = os.path.join(output_folder, f'{os.path.splitext(csv_file)[0]}_action_type_counts.csv')

            # 将统计结果保存到新的CSV文件
            action_type_counts.to_csv(output_file_path, header=['Count'], index_label='Primary_Action_Type')

            print(f"文件 {csv_file} 统计完成，结果已保存到 {output_file_path}")
        else:
            print(f"文件 {csv_file} 缺少 'Primary_Action_Type' 列，跳过此文件。")

    except Exception as e:
        print(f"处理文件 {csv_file} 时发生错误: {e}")

print("所有文件处理完成。")
