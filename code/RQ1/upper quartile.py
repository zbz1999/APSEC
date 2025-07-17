import os
import pandas as pd


def calculate_median_change_percentage(csv_file_path):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)
    # 去掉百分号并转换为浮点数，忽略空值
    df['Change Percentage'] = pd.to_numeric(df['Change Percentage'].str.replace('%', ''), errors='coerce')
    # 计算中位数，忽略空值
    median_value = df['Change Percentage'].median()
    return median_value


def process_files(input_folder, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    results = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(input_folder, filename)
            median_value = calculate_median_change_percentage(csv_file_path)
            # 加上百分号
            median_value_str = f"{median_value:.2f}%"
            results.append((filename, median_value_str))

    # 保存结果到新的CSV文件
    results_df = pd.DataFrame(results, columns=['Filename', 'Median Change Percentage'])
    output_file = os.path.join(output_folder, 'median_results.csv')
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"中位数结果已保存到 {output_file}")


if __name__ == "__main__":
    input_folder = "H:/1_合并后469个按照6个月为阶段的离开文件"  # 替换为你的输入文件夹路径
    output_folder = "H:/1_合并后469个中位数"  # 替换为你的输出文件夹路径
    process_files(input_folder, output_folder)
