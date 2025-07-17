import pandas as pd
import os

# 设置文件夹路径
folder1_path = 'H:/1_合并RQ3.1/all_leave'  # 第一个文件夹路径（包含开发者名单）
folder2_path = 'H:/1_合并RQ3.6/all_work_type'  # 第二个文件夹路径（待处理文件）
output_folder = 'H:/1_合并RQ3.6/工作类型与离开结果的合并'  # 输出文件夹

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 获取两个文件夹中的所有CSV文件
file1_list = [f for f in os.listdir(folder1_path) if f.endswith('_identities_filtered.csv')]
file2_list = [f for f in os.listdir(folder2_path) if f.endswith('_identities.csv')]

# 遍历文件夹中的文件进行匹配和处理
for file1_name in file1_list:
    # 构造第一个文件的路径
    file1_path = os.path.join(folder1_path, file1_name)

    # 从第一个文件名中提取基础名称（去掉_identities_filtered.csv后缀）
    base_name = file1_name.replace('_identities_filtered.csv', '')

    # 构造对应的第二个文件名
    file2_name = f"matched_{base_name}_identities.csv"

    # 如果第二个文件存在则进行处理
    if file2_name in file2_list:
        file2_path = os.path.join(folder2_path, file2_name)

        try:
            # 读取第一个文件中的Author列
            df1 = pd.read_csv(file1_path)
            if 'Author' not in df1.columns:
                print(f"文件 {file1_name} 缺少Author列，跳过")
                continue

            # 读取第二个文件
            df2 = pd.read_csv(file2_path)
            if 'Developer' not in df2.columns:
                print(f"文件 {file2_name} 缺少Developer列，跳过")
                continue

            # 获取第一个文件中的开发者集合
            authors = set(df1['Author'].unique())

            # 为第二个文件添加leave列
            df2['leave'] = df2['Developer'].apply(lambda x: 1 if x in authors else 0)

            # 设置输出文件名和路径
            output_file_name = f"{base_name}_with_leave.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # 保存处理后的文件
            df2.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            print(f"已完成: {file1_name} -> {output_file_name}")

        except Exception as e:
            print(f"处理 {file1_name} 时出错: {str(e)}")
    else:
        print(f"未找到匹配文件: {file2_name}")

print("\n所有文件处理完成！")