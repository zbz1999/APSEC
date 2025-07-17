import pandas as pd
import os

# 设置输入文件夹路径（包含所有CSV文件）
input_folder = 'H:/1_合并RQ3.4/all_commit_ratio'  # 请将此路径替换为实际的文件夹路径
output_folder = 'H:/1_合并RQ3.4/80%'  # 输出文件夹路径

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有CSV文件
for file_name in os.listdir(input_folder):
    # 只处理CSV文件
    if file_name.endswith('.csv'):
        input_file_path = os.path.join(input_folder, file_name)  # 获取当前CSV文件的路径

        # 尝试读取CSV文件并处理异常
        try:
            data = pd.read_csv(input_file_path)
        except FileNotFoundError:
            print(f"错误：文件 {input_file_path} 未找到。")
            continue
        except pd.errors.EmptyDataError:
            print(f"错误：文件 {input_file_path} 为空。")
            continue

        # 确保CSV文件包含 'developer' 和 'commit_ratio' 列
        if 'developer' in data.columns and 'commit_ratio' in data.columns:
            # 按 commit_ratio 列从大到小排序
            sorted_data = data.sort_values(by='commit_ratio', ascending=False).reset_index(drop=True)

            # 计算累计提交比例，直到累计和大于或等于80%
            cumulative_sum = 0
            count = 0
            for index, row in sorted_data.iterrows():
                cumulative_sum += row['commit_ratio']  # 累加提交比例
                count += 1  # 计数开发者数量
                if cumulative_sum >= 80:  # 一旦累计和达到80%，停止
                    break

            # 获取符合条件的开发者数据
            filtered_data = sorted_data.iloc[:count][['developer', 'commit_ratio']]

            # 设置输出文件路径，基于输入文件名
            input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
            output_file_name = f"{input_file_name}_filtered.csv"  # 添加 _filtered 后缀
            output_file_path = os.path.join(output_folder, output_file_name)

            # 将结果保存到新的CSV文件，并确保文件编码为utf-8-sig（兼容Excel）
            filtered_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')

            print(f"文件 {file_name} 处理完成，结果已保存至: {output_file_path}")
        else:
            print(f"文件 {file_name} 缺少 'developer' 或 'commit_ratio' 列，跳过该文件。")

print("所有文件处理完成！")
