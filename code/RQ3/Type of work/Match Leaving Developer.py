import pandas as pd
import os

# 设置文件夹路径
folder1_path = 'H:/1_合并RQ3.1/all_leave'  # 第一个文件夹路径
folder2_path = 'H:/1_合并RQ3.6/all_work_type'  # 第二个文件夹路径
output_folder = 'H:/1_合并RQ3.6/all_leave_Matched_Results'  # 输出文件夹

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 获取第一个文件夹中的所有CSV文件（以_identities_filtered.csv结尾）
file1_list = [f for f in os.listdir(folder1_path) if f.endswith('_identities_filtered.csv')]

# 获取第二个文件夹中的所有文件，并创建映射字典（去掉"matched_"前缀和"_identities.csv"后缀）
file2_dict = {}
for f in os.listdir(folder2_path):
    if f.startswith('matched_') and f.endswith('_identities.csv'):
        base_name = f.replace('matched_', '').replace('_identities.csv', '')
        file2_dict[base_name] = f

# 遍历第一个文件夹中的文件进行匹配
for file1_name in file1_list:
    # 构造第一个文件的完整路径
    file1_path = os.path.join(folder1_path, file1_name)

    # 获取文件名前缀（去掉 '_identities_filtered.csv'）
    base_name = file1_name.replace('_identities_filtered.csv', '')

    # 检查是否有匹配的文件在第二个文件夹中
    if base_name in file2_dict:
        # 构造第二个文件的完整路径
        file2_name = file2_dict[base_name]
        file2_path = os.path.join(folder2_path, file2_name)

        # 读取第一个文件中的 'Author' 列
        df1 = pd.read_csv(file1_path, usecols=['Author'])

        # 读取第二个文件中的 'Developer' 和 'Main Work Type' 列
        df2 = pd.read_csv(file2_path, usecols=['Developer', 'Main Work Type'])

        # 确保文件包含所需的列
        if 'Author' in df1.columns and 'Developer' in df2.columns and 'Main Work Type' in df2.columns:
            # 获取第一个文件中的唯一开发者（Author列）
            authors = set(df1['Author'].unique())

            # 筛选出在第二个文件中与第一个文件匹配的开发者
            developers_df2 = df2[df2['Developer'].isin(authors)]

            # 只保留匹配成功的 'Developer' 和 'Main Work Type' 列
            matching_developers = developers_df2[['Developer', 'Main Work Type']]

            # 设置输出文件路径
            output_file_name = f"{base_name}_matched_developers.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # 将结果保存到新的CSV文件
            matching_developers.to_csv(output_file_path, index=False, encoding='utf-8-sig')

            print(f"匹配结果已保存至: {output_file_path}")
        else:
            print(f"文件 {file1_name} 或 {file2_name} 缺少所需列，跳过该文件。")
    else:
        print(f"未找到与 {file1_name} 匹配的文件（基础名: {base_name}），跳过该文件。")