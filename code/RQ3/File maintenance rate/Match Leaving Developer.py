import pandas as pd
import os

# 输入文件夹路径
input_folder_1 = 'H:/1_合并RQ3.1/all_leave'  # 第一个文件夹路径，包含文件名格式：*_identities_filtered.csv
input_folder_2 = 'H:/1_合并RQ3.7/all_developer_with_ratios'  # 第二个文件夹路径，包含文件名格式：*_filtered_with_ratio.csv

# 输出文件夹路径（确保文件夹存在）
output_folder = 'H:/1_合并RQ3.7/all_leave_Matched_Results/'
os.makedirs(output_folder, exist_ok=True)  # 如果输出文件夹不存在，创建它

# 获取第一个文件夹中的所有csv文件（以_identities_filtered.csv结尾）
file_list_1 = [f for f in os.listdir(input_folder_1) if f.endswith('_identities_filtered.csv')]

# 遍历第一个文件夹中的文件
for file_1 in file_list_1:
    try:
        # 构建文件1的完整路径
        input_file_path_1 = os.path.join(input_folder_1, file_1)

        # 获取基础文件名（去掉_identities_filtered.csv后缀）
        file_name_base = file_1.replace('_identities_filtered.csv', '')

        # 构建第二个文件的完整路径（添加_filtered_with_ratio.csv后缀）
        input_file_path_2 = os.path.join(input_folder_2, file_name_base + '_filtered_with_ratio.csv')

        # 检查第二个文件是否存在
        if os.path.exists(input_file_path_2):
            # 读取第一个文件（开发者信息）
            df1 = pd.read_csv(input_file_path_1)
            df1.columns = df1.columns.str.strip()  # 去除列名的前后空格

            # 检查是否包含Author列
            if 'Author' not in df1.columns:
                print(f"文件 {file_1} 缺少Author列，跳过")
                continue

            authors = df1['Author'].unique()  # 获取唯一的开发者列表

            # 读取第二个文件（开发者及创建文件比率信息）
            df2 = pd.read_csv(input_file_path_2)
            df2.columns = df2.columns.str.strip()  # 去除列名的前后空格

            # 检查是否包含Developer和Created Files Ratio列
            if 'Developer' not in df2.columns or 'Created Files Ratio' not in df2.columns:
                print(f"文件 {input_file_path_2} 缺少必要列，跳过")
                continue

            # 过滤出匹配的开发者
            matched_developers = df2[df2['Developer'].isin(authors)]

            # 如果有匹配的开发者，则保存结果
            if not matched_developers.empty:
                output_data = matched_developers[['Developer', 'Created Files Ratio']]

                # 构建输出文件路径
                output_file_name = os.path.join(output_folder, f"{file_name_base}_leave_developer_ratio.csv")

                # 保存结果到新的 CSV 文件
                output_data.to_csv(output_file_name, index=False)
                print(f"匹配完成，结果已保存到: {output_file_name}")
            else:
                print(f"没有匹配的开发者：{file_name_base}")
        else:
            print(f"未找到匹配的文件：{input_file_path_2}")
    except Exception as e:
        print(f"处理文件 {file_1} 时发生错误: {str(e)}")

print("所有文件处理完成。")