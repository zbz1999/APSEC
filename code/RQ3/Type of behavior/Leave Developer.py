import pandas as pd
import os

# 设置文件夹路径
folder1_path = 'H:/1_合并RQ3.1/all_leave'  # 第一个文件夹路径
folder2_path = 'H:/1_合并RQ3.5/all_primary_action_type'  # 第二个文件夹路径
output_folder = 'H:/1_合并RQ3.5/all_leave_Matched_Results'  # 输出文件夹，用于保存匹配结果

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 获取两个文件夹中的所有CSV文件
file1_list = [f for f in os.listdir(folder1_path) if f.endswith('_identities_filtered.csv')]
file2_list = [f for f in os.listdir(folder2_path) if f.endswith('_operations_primary_action_type.csv')]

# 遍历文件夹中的文件进行匹配
for file1_name in file1_list:
    # 构造第一个文件的路径
    file1_path = os.path.join(folder1_path, file1_name)

    # 从第一个文件名中提取基础名称（去掉_identities_filtered.csv后缀）
    base_name = file1_name.replace('_identities_filtered.csv', '')

    # 构造对应的第二个文件名（添加filtered_前缀，去掉_operations_primary_action_type.csv后缀）
    file2_name = f"filtered_{base_name}_operations_primary_action_type.csv"

    # 如果第二个文件在文件夹中存在，则进行匹配
    if file2_name in file2_list:
        # 构造第二个文件的路径
        file2_path = os.path.join(folder2_path, file2_name)

        # 读取第一个文件中的 'Author' 列
        df1 = pd.read_csv(file1_path, usecols=['Author'])

        # 读取第二个文件中的 'Developer' 和 'Primary_Action_Type' 列
        df2 = pd.read_csv(file2_path, usecols=['Developer', 'Primary_Action_Type'])

        # 确保文件包含所需的列
        if 'Author' in df1.columns and 'Developer' in df2.columns and 'Primary_Action_Type' in df2.columns:
            # 获取第一个文件中的唯一开发者（Author列）
            authors = set(df1['Author'].unique())

            # 筛选出在第二个文件中与第一个文件匹配的开发者
            developers_df2 = df2[df2['Developer'].isin(authors)]

            # 只保留匹配成功的 'Developer' 和 'Primary_Action_Type' 列
            matching_developers = developers_df2[['Developer', 'Primary_Action_Type']]

            # 设置输出文件路径，基于第一个文件名
            output_file_name = f"{base_name}_matched_developers.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # 将结果保存到新的CSV文件
            matching_developers.to_csv(output_file_path, index=False, encoding='utf-8-sig')

            print(f"匹配结果已保存至: {output_file_path}")
        else:
            print(f"文件 {file1_name} 或 {file2_name} 缺少所需列，跳过该文件。")
    else:
        print(f"未找到与 {file1_name} 匹配的文件 {file2_name}，跳过该文件。")