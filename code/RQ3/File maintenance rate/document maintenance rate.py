import pandas as pd
import os

# 输入文件夹路径（替换为实际路径）
input_folder_path = 'H:/1_合并RQ3.7/all_clearfile'
output_folder_path = 'H:/1_合并RQ3.7/all_developer_with_ratios'  # 输出文件夹路径

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 遍历输入文件夹中的所有CSV文件
for file_name in os.listdir(input_folder_path):
    # 检查文件是否是CSV文件
    if file_name.endswith('.csv'):
        input_file_path = os.path.join(input_folder_path, file_name)  # 构建输入文件路径

        try:
            # 读取 CSV 文件
            df = pd.read_csv(input_file_path)

            # 检查是否包含必要的列
            if 'Created Files Count' in df.columns and 'Total Files Count' in df.columns:
                # 计算比例：Created Files Count / Total Files Count，避免除以0
                df['Created Files Ratio'] = df.apply(
                    lambda row: row['Created Files Count'] / row['Total Files Count'] if row[
                                                                                             'Total Files Count'] > 0 else 0,
                    axis=1
                )

                # 构建输出文件路径
                output_file_path = os.path.join(output_folder_path, f"{os.path.splitext(file_name)[0]}_with_ratio.csv")

                # 保存结果到新的 CSV 文件
                df.to_csv(output_file_path, index=False)
                print(f"文件 {file_name} 处理完成，结果已保存到: {output_file_path}")
            else:
                print(f"文件 {file_name} 缺少必要的列，跳过处理。")

        except pd.errors.EmptyDataError:
            print(f"文件 {file_name} 为空，跳过处理。")
        except Exception as e:
            print(f"处理文件 {file_name} 时发生错误：{e}")

print("所有文件处理完成。")
