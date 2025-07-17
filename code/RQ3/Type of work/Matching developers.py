import pandas as pd
import os
import re

# 设置文件夹路径
identities_folder = 'H:/1_合并RQ3.1'  # 包含_identities.csv文件的文件夹
file_types_folder = 'H:/1_合并RQ3.6/1_worktype_Results'  # 包含_file_types_summary_时间戳.csv文件的文件夹
output_folder = 'H:/1_合并RQ3.6/筛选过后的开发者'  # 结果保存路径

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取两个文件夹中的文件列表
identities_files = [f for f in os.listdir(identities_folder) if f.endswith('_identities.csv')]
file_types_files = [f for f in os.listdir(file_types_folder) if '_file_types_summary_' in f and f.endswith('.csv')]

# 建立文件名映射关系
file_pairs = []
for id_file in identities_files:
    # 从identities文件名中提取基础名称（去掉_identities.csv）
    base_name = id_file.replace('_identities.csv', '')

    # 在file_types文件中寻找匹配的文件
    for ft_file in file_types_files:
        # 从file_types文件名中提取基础名称（去掉_file_types_summary_时间戳.csv）
        ft_base = re.sub(r'_file_types_summary_\d{8}_\d{6}\.csv$', '', ft_file)

        if ft_base == base_name:
            file_pairs.append((id_file, ft_file))
            break

print(f"找到 {len(file_pairs)} 对匹配文件")

# 处理每对匹配的文件
for id_file, ft_file in file_pairs:
    print(f"\n正在处理文件对: {id_file} 和 {ft_file}")

    # 读取identities文件获取Author列表
    id_path = os.path.join(identities_folder, id_file)
    try:
        id_df = pd.read_csv(id_path)
        if 'Author' not in id_df.columns:
            print(f"文件 {id_file} 缺少Author列，跳过")
            continue

        authors = set(id_df['Author'].dropna().unique())
        print(f"从 {id_file} 中找到 {len(authors)} 个唯一开发者")
    except Exception as e:
        print(f"读取文件 {id_file} 出错: {e}")
        continue

    # 读取file_types文件并筛选Developer
    ft_path = os.path.join(file_types_folder, ft_file)
    try:
        ft_df = pd.read_csv(ft_path)
        if 'Developer' not in ft_df.columns:
            print(f"文件 {ft_file} 缺少Developer列，跳过")
            continue

        # 筛选匹配的开发者
        filtered_df = ft_df[ft_df['Developer'].isin(authors)]
        print(f"在 {ft_file} 中找到 {len(filtered_df)} 条匹配记录")

        if len(filtered_df) == 0:
            print("没有匹配的记录，跳过保存")
            continue

        # 保存结果
        output_filename = f"matched_{os.path.splitext(id_file)[0]}.csv"
        output_path = os.path.join(output_folder, output_filename)
        filtered_df.to_csv(output_path, index=False)

        print(f"结果已保存到: {output_filename}")
    except Exception as e:
        print(f"处理文件 {ft_file} 出错: {e}")
        continue

print("\n所有文件处理完成！")