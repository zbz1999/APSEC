import pandas as pd
import os

# 定义文件路径
match_counts_folder = 'H:/1_合并RQ3.4/all_match_results'   # 包含 '12306_match_counts.csv' 文件的文件夹
summary_folder = 'H:/1_合并RQ3.4/all_morethan_5%'  # 包含 '12306_git_log_summary_filtered_百分之5.csv' 文件的文件夹
last_commit_folder = 'H:/1_合并RQ3.1/all_leave'  # 包含 '12306_last_commit_times_filtered.csv' 文件的文件夹
first_commit_folder = 'H:/1_合并RQ3.1'  # 包含 '12306_first_commit_times.csv' 文件的文件夹
output_folder = 'H:/1_合并RQ3.4/all_baifenbi_result'  # 输出文件夹路径

# 获取文件夹中的所有文件
match_counts_files = [f for f in os.listdir(match_counts_folder) if f.endswith('.csv')]
summary_files = [f for f in os.listdir(summary_folder) if f.endswith('.csv')]
last_commit_files = [f for f in os.listdir(last_commit_folder) if f.endswith('.csv')]
first_commit_files = [f for f in os.listdir(first_commit_folder) if f.endswith('.csv')]

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有文件
for match_file, summary_file, last_commit_file, first_commit_file in zip(match_counts_files, summary_files, last_commit_files, first_commit_files):
    # 构建完整的文件路径
    match_counts_path = os.path.join(match_counts_folder, match_file)
    summary_path = os.path.join(summary_folder, summary_file)
    last_commit_path = os.path.join(last_commit_folder, last_commit_file)
    first_commit_path = os.path.join(first_commit_folder, first_commit_file)

    # 读取CSV文件
    match_counts_df = pd.read_csv(match_counts_path)
    summary_df = pd.read_csv(summary_path)
    last_commit_df = pd.read_csv(last_commit_path)
    first_commit_df = pd.read_csv(first_commit_path)

    # 获取核心开发者和非核心开发者的数量
    core_developer_count = match_counts_df['core-developer'].iloc[0]
    non_core_developer_count = match_counts_df['non-core-developer'].iloc[0]

    # 获取开发者数量（unique的developer）
    developer_count = len(summary_df['developer'].unique())

    # 获取所有提交者（即作者）数量
    author_count = len(last_commit_df['Author'].unique())

    # 获取所有首次提交的作者数量
    first_commit_author_count = len(first_commit_df['Author'].unique())

    # 计算core-developer的百分比
    if developer_count > 0:
        core_developer_ratio = (core_developer_count / developer_count) * 100
    else:
        core_developer_ratio = 0  # 防止除以0的错误

    # 计算non-core-developer的百分比
    # 计算non-core-developer时需要考虑（first_commit_author_count的数量 - developer_count的数量）
    if (first_commit_author_count - developer_count) > 0:
        non_core_developer_ratio = (non_core_developer_count / (first_commit_author_count - developer_count)) * 100
    else:
        non_core_developer_ratio = 0  # 防止除以0的错误

    # 创建输出数据框，包含两列：core-developer 和 non-core-developer
    result_df = pd.DataFrame({
        'core-developer': [core_developer_ratio],
        'non-core-developer': [non_core_developer_ratio]
    })

    # 设置输出文件路径
    output_file_name = f"result_{match_file.replace('.csv', '')}.csv"
    output_file_path = os.path.join(output_folder, output_file_name)

    # 保存结果到CSV文件
    result_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

    print(f"处理完成：{output_file_name} 已保存至: {output_file_path}")

