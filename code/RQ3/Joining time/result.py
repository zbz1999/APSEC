import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置输入文件夹路径和输出文件夹路径
input_folder = 'H:/1_合并RQ3.1'  # 输入文件夹路径（包含多个CSV文件）
output_csv_folder = 'H:/1_合并RQ3.1/all_output_csv'  # 保存统计结果的文件夹
output_plot_folder = 'H:/1_合并RQ3.1/all_output_plots'  # 保存折线图的文件夹

# 创建输出文件夹（如果不存在）
os.makedirs(output_csv_folder, exist_ok=True)
os.makedirs(output_plot_folder, exist_ok=True)

# 获取输入文件夹中所有CSV文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 遍历所有CSV文件进行处理
for file_name in csv_files:
    # 构建文件路径
    file_path = os.path.join(input_folder, file_name)

    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 提取年份信息并统计开发者数量
    df['Year'] = pd.to_datetime(df['First Commit']).dt.year
    yearly_counts = df.groupby('Year')['Author'].nunique()

    # 保存统计结果到新的CSV文件
    output_csv_path = os.path.join(output_csv_folder, f"yearly_counts_{file_name}")
    yearly_counts.to_csv(output_csv_path, header=['Number of Developers'])  # 保存统计结果
    print(f"统计结果已保存到: {output_csv_path}")

    # 绘制折线图
    plt.figure(figsize=(10, 6))
    yearly_counts.plot(kind='line', marker='o', color='skyblue', linewidth=2, markersize=8, linestyle='-', markeredgecolor='black')
    plt.title('Number of Developers by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Developers')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 在折线图上添加数量标注
    for index, value in enumerate(yearly_counts):
        plt.text(index, value + 0.5, str(value), ha='center', va='bottom', fontsize=10)

    # 保存折线图到PNG文件
    output_plot_path = os.path.join(output_plot_folder, f"yearly_counts_plot_{os.path.splitext(file_name)[0]}.png")
    plt.savefig(output_plot_path)  # 保存图表为PNG文件
    plt.close()  # 关闭图表，释放内存
    print(f"折线图已保存到: {output_plot_path}")

print("所有文件处理完成！")
