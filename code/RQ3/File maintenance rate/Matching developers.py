import os
import pandas as pd

# 路径定义
folder1 = 'H:/1_合并RQ3.1'  # identities.csv 所在文件夹
folder2 = 'H:/1_合并RQ3.7/all_output'  # contributions_summary.csv 所在文件夹
output_folder = 'H:/1_合并RQ3.7/all_clearfile'  # 输出文件夹

# 如果输出文件夹不存在就创建
os.makedirs(output_folder, exist_ok=True)

# 获取文件名（去后缀的部分）
identities_files = [f for f in os.listdir(folder1) if f.endswith('_identities.csv')]
summary_files = [f for f in os.listdir(folder2) if f.endswith('_contributions_summary.csv')]

# 构建匹配字典
identities_map = {f.replace('_identities.csv', ''): f for f in identities_files}
summary_map = {f.replace('_contributions_summary.csv', ''): f for f in summary_files}

# 找出交集项目
common_projects = set(identities_map.keys()) & set(summary_map.keys())

# 遍历每个匹配项目
for project in common_projects:
    try:
        # 文件路径
        id_path = os.path.join(folder1, identities_map[project])
        summary_path = os.path.join(folder2, summary_map[project])

        # 读取 identities.csv 获取开发者
        df_id = pd.read_csv(id_path)
        authors = set(df_id['Author'].dropna().astype(str).str.strip())

        # 读取 contributions_summary.csv 并筛选
        df_summary = pd.read_csv(summary_path)
        df_filtered = df_summary[df_summary['Developer'].astype(str).str.strip().isin(authors)]

        # 保存筛选结果
        output_path = os.path.join(output_folder, f'{project}_filtered.csv')
        df_filtered.to_csv(output_path, index=False)

        print(f"✅ 输出完成：{project}_filtered.csv")
    except Exception as e:
        print(f"❌ 处理失败：{project}，错误：{e}")
