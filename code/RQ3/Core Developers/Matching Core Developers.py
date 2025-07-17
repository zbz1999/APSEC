import pandas as pd
import os

# 设置输入文件夹路径
folder1_path = 'H:/1_合并RQ3.1/all_leave'  # 包含 Jax_last_commit_times_filtered.csv 格式文件的文件夹
folder2_path = 'H:/1_合并RQ3.4/all_morethan_5%'  # 包含 budibase_git_log_summary_filtered_百分之5.csv 格式文件的文件夹
output_folder = 'H:/1_合并RQ3.4/all_match_results'  # 输出文件夹

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历第一个文件夹中的所有CSV文件
for file1_name in os.listdir(folder1_path):
    if file1_name.endswith('_identities_filtered.csv'):
        # 获取文件的基础名（去掉后缀）
        base_name = file1_name.replace('_identities_filtered.csv', '')

        # 匹配第二个文件夹中的对应文件
        file2_name = f"{base_name}_identities_filtered_百分之5.csv"
        file1_path = os.path.join(folder1_path, file1_name)
        file2_path = os.path.join(folder2_path, file2_name)

        # 检查文件是否存在于第二个文件夹中
        if os.path.exists(file2_path):
            # 读取两个CSV文件
            df1 = pd.read_csv(file1_path)
            df2 = pd.read_csv(file2_path)

            # 确保两个文件包含所需列
            if 'Author' in df1.columns and 'developer' in df2.columns:
                # 提取两个文件中的开发者集合
                authors = set(df1['Author'].unique())
                developers = set(df2['developer'].unique())

                # 计算匹配成功和不成功的开发者数量
                matching_authors = authors.intersection(developers)
                non_matching_authors = authors.difference(developers)

                match_count = len(matching_authors)
                non_match_count = len(non_matching_authors)

                # 创建结果数据框
                result = pd.DataFrame({
                    'core-developer': [match_count],         # 核心开发者数量
                    'non-core-developer': [non_match_count]  # 非核心开发者数量
                })

                # 设置输出文件名和路径
                output_file_name = f"{base_name}_match_counts.csv"
                output_file_path = os.path.join(output_folder, output_file_name)

                # 保存结果到新的CSV文件
                result.to_csv(output_file_path, index=False, encoding='utf-8-sig')
                print(f"匹配结果已保存至: {output_file_path}")
            else:
                print(f"文件缺少所需列：{file1_name} 或 {file2_name}")
        else:
            print(f"未找到匹配文件：{file2_name}")
