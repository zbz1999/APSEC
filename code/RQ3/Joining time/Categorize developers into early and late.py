import os
import pandas as pd
from datetime import datetime


def process_csv_files(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有csv文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)

            try:
                # 读取CSV文件
                df = pd.read_csv(file_path)

                # 确保有需要的列
                if 'First Commit' not in df.columns:
                    print(f"文件 {filename} 缺少 'First Commit' 列，跳过处理")
                    continue

                # 转换日期格式
                df['First Commit'] = pd.to_datetime(df['First Commit'])

                # 计算中位数
                median_date = df['First Commit'].median()

                # 分类
                df['Date Comparison'] = df['First Commit'].apply(
                    lambda x: '早' if x <= median_date else '晚'
                )

                # 只保留需要的列
                result = df[['Author', 'First Commit', 'Date Comparison']]

                # 保存结果
                output_path = os.path.join(output_folder, filename)
                result.to_csv(output_path, index=False)

                print(f"已完成文件: {filename}")

            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")


# 使用示例
input_folder = 'H:/1_合并RQ3.1'  # 替换为你的实际路径
output_folder = 'H:/1_合并RQ3.1/分为早晚'  # 替换为你想要保存的路径

process_csv_files(input_folder, output_folder)