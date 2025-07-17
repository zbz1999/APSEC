import os
import pandas as pd


def calculate_leave_percentage(input_folder, output_file):
    results = []

    # 遍历输入文件夹中的所有csv文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)

            try:
                # 读取CSV文件
                df = pd.read_csv(file_path)

                # 检查必要的列是否存在
                required_columns = ['Author', 'First Commit', 'Date Comparison', 'leave']
                if not all(col in df.columns for col in required_columns):
                    print(f"文件 {filename} 缺少必要的列，跳过处理")
                    continue

                # 获取项目名称（去掉文件扩展名）
                project_name = os.path.splitext(filename)[0]

                # 计算早开发者的离开百分比
                early_devs = df[df['Date Comparison'] == '早']
                early_leave_percentage = 0
                if len(early_devs) > 0:
                    early_leave_percentage = early_devs['leave'].mean() * 100

                # 计算晚开发者的离开百分比
                late_devs = df[df['Date Comparison'] == '晚']
                late_leave_percentage = 0
                if len(late_devs) > 0:
                    late_leave_percentage = late_devs['leave'].mean() * 100

                # 添加到结果列表
                results.append({
                    '项目': project_name,
                    '早的离开百分比': round(early_leave_percentage, 2),
                    '晚的离开百分比': round(late_leave_percentage, 2)
                })

                print(f"已处理文件: {filename}")

            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

    # 将结果保存到新的CSV文件
    if results:
        result_df = pd.DataFrame(results)
        result_df.to_csv(output_file, index=False)
        print(f"结果已保存到: {output_file}")
    else:
        print("没有找到可处理的有效文件")


# 使用示例
input_folder = 'H:/1_合并RQ3.1/分为早晚_离开开发者'  # 替换为你的实际路径
output_file = 'H:/1_合并RQ3.1/1_离开百分比统计.csv'  # 替换为你想要保存的路径

calculate_leave_percentage(input_folder, output_file)