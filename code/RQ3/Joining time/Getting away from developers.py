import pandas as pd
import os


def filter_csv_files(input_folder, output_folder, days_threshold=365):
    """
    筛选输入文件夹中的所有CSV文件，筛选出 'days_since_last_commit' 列中大于指定阈值的行，并保存到新的文件夹中。

    参数：
    input_folder: str - 输入CSV文件所在的文件夹路径。
    output_folder: str - 筛选结果保存的文件夹路径。
    days_threshold: int - 筛选天数阈值（默认值为180）。
    """
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有CSV文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):  # 只处理CSV文件
            input_file_path = os.path.join(input_folder, file_name)

            # 读取CSV文件为DataFrame
            df = pd.read_csv(input_file_path)

            # 筛选出 'days_since_last_commit' 大于指定阈值的行
            filtered_df = df[df['Days Since Last Commit'] > days_threshold]

            # 生成输出文件路径
            output_file_name = f"{os.path.splitext(file_name)[0]}_filtered.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # 将筛选后的数据保存到新的CSV文件中
            filtered_df.to_csv(output_file_path, index=False)

            print(f"文件 {file_name} 筛选完成，结果已保存为：{output_file_path}")


if __name__ == "__main__":
    # 输入文件夹路径（包含多个CSV文件）
    input_folder = r"H:\1_合并RQ3.1"  # 替换为实际的输入文件夹路径

    # 输出文件夹路径（保存筛选结果）
    output_folder = r"H:\1_合并RQ3.1\all_leave"  # 替换为实际的输出文件夹路径

    # 执行筛选操作，默认筛选超过365天未提交的记录
    filter_csv_files(input_folder, output_folder)

    print("所有文件处理完成！")
