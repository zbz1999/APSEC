import os
import pandas as pd


def process_matching_files(folder1, folder2, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取第一个文件夹中的文件基名映射
    folder1_files = {}
    for filename in os.listdir(folder1):
        if filename.endswith('_identities_filtered.csv'):
            base_name = filename.replace('_identities_filtered.csv', '')
            folder1_files[base_name] = os.path.join(folder1, filename)

    # 获取第二个文件夹中的文件基名映射
    folder2_files = {}
    for filename in os.listdir(folder2):
        if filename.endswith('_identities.csv'):
            base_name = filename.replace('_identities.csv', '')
            folder2_files[base_name] = os.path.join(folder2, filename)

    # 找出两个文件夹中都存在的基名
    common_base_names = set(folder1_files.keys()) & set(folder2_files.keys())

    if not common_base_names:
        print("没有找到匹配的文件对")
        return

    # 处理每个匹配的文件对
    for base_name in common_base_names:
        try:
            # 读取第一个文件夹中的文件（过滤条件）
            df_filter = pd.read_csv(folder1_files[base_name])
            filter_authors = set(df_filter['Author'].unique())

            # 读取第二个文件夹中的文件（待处理文件）
            df_main = pd.read_csv(folder2_files[base_name])

            # 添加leave列
            df_main['leave'] = df_main['Author'].apply(
                lambda x: 1 if x in filter_authors else 0
            )

            # 保存结果
            output_filename = f"{base_name}_with_leave.csv"
            output_path = os.path.join(output_folder, output_filename)
            df_main.to_csv(output_path, index=False)

            print(f"已完成文件对: {base_name}")

        except Exception as e:
            print(f"处理文件对 {base_name} 时出错: {str(e)}")


# 使用示例
folder1 = 'H:/1_合并RQ3.1/all_leave'  # 包含 _identities_filtered.csv 文件的文件夹
folder2 = 'H:/1_合并RQ3.1/分为早晚'  # 包含 _identities.csv 文件的文件夹
output_folder = 'H:/1_合并RQ3.1/分为早晚_离开开发者'  # 保存结果的文件夹

process_matching_files(folder1, folder2, output_folder)