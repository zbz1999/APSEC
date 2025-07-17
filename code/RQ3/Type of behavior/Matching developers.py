import os
import pandas as pd

# 配置路径
identities_folder = 'H:/1_合并RQ3.1'  # 包含_identities.csv文件的文件夹
operations_folder = 'H:/1_合并RQ3.5/all_operation'  # 包含_operations.csv文件的文件夹
output_folder = 'H:/1_合并RQ3.5/筛选过后的开发者'  # 结果保存路径

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取两个文件夹中的文件列表
identities_files = [f for f in os.listdir(identities_folder) if f.endswith('_identities.csv')]
operations_files = [f for f in os.listdir(operations_folder) if f.endswith('_operations.csv')]

# 建立文件名映射关系（去掉后缀后匹配）
file_pairs = []
for id_file in identities_files:
    base_name = id_file.replace('_identities.csv', '')
    for op_file in operations_files:
        if op_file.replace('_operations.csv', '') == base_name:
            file_pairs.append((id_file, op_file))
            break

# 处理每对匹配的文件
for id_file, op_file in file_pairs:
    print(f"正在处理文件对: {id_file} 和 {op_file}")

    # 读取identities文件获取Author列表
    id_path = os.path.join(identities_folder, id_file)
    id_df = pd.read_csv(id_path)
    authors = set(id_df['Author'].dropna().unique())

    # 读取operations文件并筛选Developer
    op_path = os.path.join(operations_folder, op_file)
    op_df = pd.read_csv(op_path)
    filtered_df = op_df[op_df['Developer'].isin(authors)]

    # 保存结果
    output_filename = f"filtered_{op_file}"
    output_path = os.path.join(output_folder, output_filename)
    filtered_df.to_csv(output_path, index=False)

    print(f"完成处理并保存: {output_filename}")

print("所有文件处理完成！")