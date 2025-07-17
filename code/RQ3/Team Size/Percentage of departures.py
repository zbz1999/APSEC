import os
import csv

# 设置文件夹路径
folder1_path = 'H:/1_合并RQ3.1'  # 包含_first_commit_times.csv文件的文件夹
folder2_path = 'H:/1_合并RQ3.1/all_leave'  # 包含_identities_filtered.csv文件的文件夹
output_file = 'H:/1_合并RQ3.8/teamsize/leave.csv'  # 输出文件路径


def get_project_name(filename, suffix):
    """从文件名中去除指定后缀"""
    if filename.endswith(suffix):
        return filename[:-len(suffix)]
    return filename


# 收集第一个文件夹中的文件信息
folder1_files = {}
for filename in os.listdir(folder1_path):
    if filename.endswith('_identities.csv'):
        filepath = os.path.join(folder1_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                row_count = sum(1 for row in reader) - 1  # 减去标题行
                project_name = get_project_name(filename, '_identities.csv')
                folder1_files[project_name] = row_count
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")

# 收集第二个文件夹中的文件信息并计算百分比
results = []
for filename in os.listdir(folder2_path):
    if filename.endswith('_identities_filtered.csv'):
        filepath = os.path.join(folder2_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                row_count = sum(1 for row in reader) - 1  # 减去标题行
                project_name = get_project_name(filename, '_identities_filtered.csv')

                # 查找匹配的第一个文件夹中的文件
                if project_name in folder1_files:
                    percentage = (row_count / folder1_files[project_name]) * 100
                    results.append({
                        '项目名称': project_name,
                        '离开百分比': round(percentage, 2)  # 保留两位小数
                    })
                else:
                    print(f"警告: 未找到 {project_name} 的匹配文件")
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")

# 将结果写入新的csv文件
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['项目名称', '离开百分比']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print(f"结果已成功保存到 {output_file}")
except Exception as e:
    print(f"写入输出文件时出错: {e}")