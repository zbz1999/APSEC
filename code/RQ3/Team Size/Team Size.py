import os
import csv

# 设置文件夹路径和输出文件路径
folder_path = 'H:/1_合并RQ3.1'  # 替换为你的实际文件夹路径
output_file = 'H:/1_合并RQ3.8/teamsize/project_sizes.csv'  # 输出文件路径

# 确保输出目录存在
os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 自动创建目录（如果不存在）

# 定义规模分类函数
def classify_size(row_count):
    if row_count < 15:
        return "小规模项目"
    elif 15 <= row_count < 30:
        return "中规模项目"
    else:
        return "大规模项目"

# 准备结果列表
results = []

# 遍历文件夹中的所有csv文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                row_count = sum(1 for row in reader) - 1  # 减去标题行

                # 获取项目名称（去掉_identities.csv后缀）
                project_name = filename.replace('_identities.csv', '')

                # 分类项目规模
                project_size = classify_size(row_count)

                # 添加到结果列表
                results.append({
                    '项目名称': project_name,
                    '项目规模': project_size,
                    '项目行数': row_count
                })
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")

# 将结果写入新的csv文件
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['项目名称', '项目规模', '项目行数']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print(f"结果已成功保存到 {output_file}")
except Exception as e:
    print(f"写入输出文件时出错: {e}")