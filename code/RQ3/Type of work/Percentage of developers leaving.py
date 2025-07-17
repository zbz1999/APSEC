import os
import pandas as pd

# 文件夹路径
folder_1 = 'H:/1_合并RQ3.6/all_leave_work_Type_counts'  # 第一个文件夹路径
folder_2 = 'H:/1_合并RQ3.6/all_work_Type_counts'  # 第二个文件夹路径
output_folder = 'H:/1_合并RQ3.6/leave_percent_output_folder'  # 输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取第一个文件夹中的所有CSV文件（后缀为_matched_developers_work_type_counts.csv）
csv_files_1 = [f for f in os.listdir(folder_1) if f.endswith('_matched_developers_work_type_counts.csv')]

# 遍历第一个文件夹中的每个文件
for file_1 in csv_files_1:
    # 提取第一个文件的基础名称（去掉后缀）
    base_name = file_1.replace('_matched_developers_work_type_counts.csv', '')

    # 构建第二个文件的文件名：添加matched_前缀和_identities_work_type_counts.csv后缀
    file_2_name = f"matched_{base_name}_identities_work_type_counts.csv"
    file_2_path = os.path.join(folder_2, file_2_name)

    # 输出调试信息
    print(f"正在处理文件对: {file_1} 和 {file_2_name}")

    # 检查第二个文件是否存在
    if os.path.exists(file_2_path):
        try:
            # 读取两个CSV文件
            df_1 = pd.read_csv(os.path.join(folder_1, file_1))
            df_2 = pd.read_csv(file_2_path)

            # 检查文件是否包含 'Main Work Type' 和 'Count' 列
            required_columns = ['Main Work Type', 'Count']
            if all(col in df_1.columns for col in required_columns) and \
                    all(col in df_2.columns for col in required_columns):

                # 合并两个文件，按 'Main Work Type' 列进行匹配
                merged_df = pd.merge(
                    df_1,
                    df_2,
                    on='Main Work Type',
                    suffixes=('_matched', '_clear'),
                    how='outer'  # 使用outer join确保所有工作类型都包含
                ).fillna(0)  # 将NaN值替换为0

                # 计算百分比：matched_developers文件中的Count与clear文件中的Count之比
                merged_df['Percentage'] = (merged_df['Count_matched'] / merged_df['Count_clear'].replace(0, 1)) * 100
                # 避免除以0的情况，将0替换为1

                # 生成输出文件路径
                output_file_path = os.path.join(output_folder, f"{base_name}_work_type_percentage.csv")

                # 保存结果到新的CSV文件，按百分比降序排列
                merged_df.sort_values('Percentage', ascending=False).to_csv(
                    output_file_path,
                    index=False,
                    float_format='%.2f'  # 保留两位小数
                )

                print(f"处理完成: {output_file_path}")
            else:
                print(f"文件 {file_1} 或 {file_2_name} 缺少所需的列，跳过此文件。")
        except Exception as e:
            print(f"处理文件 {file_1} 时发生错误: {str(e)}")
    else:
        print(f"在第二个文件夹中找不到匹配文件: {file_2_name}")

print("所有文件处理完成。")