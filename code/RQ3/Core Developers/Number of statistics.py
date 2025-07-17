import pandas as pd
import os

# 输入文件夹路径
input_folder = 'H:/1_合并RQ3.4/all_baifenbi_result'  # 请替换为实际路径

# 初始化统计变量
equal_count = 0  # core-developer = non-core-developer
greater_count = 0  # core-developer > non-core-developer
less_count = 0  # core-developer < non-core-developer
core_zero_count = 0  # core-developer = 0
non_core_zero_count = 0  # non-core-developer = 0

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # 只处理CSV文件
        file_path = os.path.join(input_folder, filename)

        # 读取CSV文件
        try:
            df = pd.read_csv(file_path)

            # 获取core-developer和non-core-developer的第一行数值
            core_developer_value = df['core-developer'].iloc[0]  # 获取core-developer列第一行值
            non_core_developer_value = df['non-core-developer'].iloc[0]  # 获取non-core-developer列第一行值

            # 进行比较
            if core_developer_value == non_core_developer_value:
                equal_count += 1
            elif core_developer_value > non_core_developer_value:
                greater_count += 1
            elif core_developer_value < non_core_developer_value:
                less_count += 1

            # 统计core-developer和non-core-developer列第一行为0的情况
            if core_developer_value == 0:
                core_zero_count += 1
            if non_core_developer_value == 0:
                non_core_zero_count += 1

        except Exception as e:
            print(f"无法处理文件 {filename}: {e}")
            continue

# 输出统计结果
print(f"core-developer等于non-core-developer的文件数: {equal_count}")
print(f"core-developer大于non-core-developer的文件数: {greater_count}")
print(f"core-developer小于non-core-developer的文件数: {less_count}")
print(f"core-developer等于0的文件数: {core_zero_count}")
print(f"non-core-developer等于0的文件数: {non_core_zero_count}")
