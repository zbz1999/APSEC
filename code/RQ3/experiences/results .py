import pandas as pd
import matplotlib.pyplot as plt
import os

def process_csv_files(input_folder, output_folder):
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(input_folder):
        # 只处理 CSV 文件
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)

            try:
                # 读取CSV文件
                data = pd.read_csv(file_path)

                # 确保CSV文件包含 'Year' 和 'Number of Developers' 列
                if 'Year' in data.columns and 'Number of Developers' in data.columns:
                    # 处理缺失值：如果有缺失的年份或开发者数量数据，先填充或者丢弃
                    data = data.dropna(subset=['Year', 'Number of Developers'])

                    # 确保 'Year' 和 'Number of Developers' 列为数值类型
                    data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
                    data['Number of Developers'] = pd.to_numeric(data['Number of Developers'], errors='coerce')

                    # 去除无效的年份和开发者数量数据（例如无法转换为数字的行）
                    data = data.dropna(subset=['Year', 'Number of Developers'])

                    # 绘制柱状图
                    plt.figure(figsize=(12, 8))
                    ax = data.plot(kind='bar', x='Year', y='Number of Developers', color='skyblue', legend=False)
                    plt.xlabel('Year')
                    plt.ylabel('Number of Developers')
                    plt.title(f'Developers per Year - {file_name}')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()

                    # 在每个柱上显示数量
                    for i, v in enumerate(data['Number of Developers']):
                        ax.text(i, v + 0.3, str(v), ha='center', va='bottom', fontweight='bold')

                    # 设置输出图像路径，基于输入文件名
                    output_image_path = os.path.join(output_folder,
                                                     os.path.splitext(file_name)[0] + '_developers_per_year.png')

                    # 保存图像
                    plt.savefig(output_image_path)
                    plt.close()  # 关闭图像，释放内存

                    print(f"处理完毕，柱状图已保存至: {output_image_path}")
                else:
                    print(f"文件 {file_name} 缺少 'Year' 或 'Number of Developers' 列，跳过该文件。")

            except Exception as e:
                print(f"处理文件 {file_name} 时出错: {e}")


# 设置输入文件夹路径（包含CSV文件）和输出文件夹路径（保存图像的文件夹）
input_folder = 'H:/1_合并RQ3.2/fenkaide_all_output_csvs'  # 请根据实际情况修改
output_folder = 'H:/1_合并RQ3.2/all_output_images'  # 输出文件夹，保存图像

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理文件夹中的所有CSV文件
process_csv_files(input_folder, output_folder)
