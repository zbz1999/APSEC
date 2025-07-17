import os
import pandas as pd
from datetime import datetime

# 配置参数
INPUT_FOLDER = "H:/1_469提交日志"  # 替换为你的CSV文件夹路径
OUTPUT_FOLDER = "H:/1_developer_last_commit"  # 输出目录
TARGET_DATE = datetime(2024, 6, 16)  # 目标日期


def process_file(file_path):
    """处理单个CSV文件"""
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 确保有需要的列
        if not all(col in df.columns for col in ['Author', 'Date']):
            print(f"文件 {os.path.basename(file_path)} 缺少必要列")
            return None

        # 转换日期格式
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        # 按开发者分组，获取最后一次提交
        last_commits = df.sort_values('Date').groupby('Author').last()

        # 计算天数差
        last_commits['Days_to_Target'] = (TARGET_DATE - last_commits['Date']).dt.days

        # 重置索引并重命名列
        result = last_commits.reset_index()
        result = result.rename(columns={
            'Date': 'Last_Commit_Date',
            'Days_to_Target': 'Days_From_LastCommit_to_2024-06-16'
        })

        # 只保留需要的列
        result = result[['Author', 'Last_Commit_Date', 'Days_From_LastCommit_to_2024-06-16']]

        return result

    except Exception as e:
        print(f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}")
        return None


def process_all_files(input_folder, output_folder):
    """处理文件夹中的所有CSV文件"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_count = 0

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            result = process_file(file_path)

            if result is not None:
                # 保存结果
                output_path = os.path.join(
                    output_folder,
                    f"last_commit_{filename}"
                )
                result.to_csv(output_path, index=False)
                print(f"已处理: {filename} -> {output_path}")
                processed_count += 1

    print(f"\n处理完成! 共处理 {processed_count} 个文件")


if __name__ == "__main__":
    process_all_files(INPUT_FOLDER, OUTPUT_FOLDER)