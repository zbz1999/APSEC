import pandas as pd
import os

# 设置文件夹路径
input_folder = r'H:\1_合并RQ3.5\行为类型与离开结果的合并'  # 包含多个CSV文件的文件夹
output_file = r'H:\1_合并RQ3.5\行为类型与离开合并结果.csv'  # 合并后的输出文件路径

# 创建一个空列表来存储所有DataFrame
all_data = []

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        try:
            # 读取CSV文件，确保只读取需要的三列
            df = pd.read_csv(file_path, usecols=['Developer', 'Primary_Action_Type', 'leave'])
            all_data.append(df)
            print(f"已加载: {filename}")
        except Exception as e:
            print(f"加载文件 {filename} 时出错: {str(e)}")

# 检查是否有数据可以合并
if not all_data:
    print("没有找到可合并的CSV文件")
else:
    # 合并所有DataFrame
    merged_df = pd.concat(all_data, ignore_index=True)

    # 保存合并后的结果
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n合并完成！结果已保存到: {output_file}")
    print(f"总行数: {len(merged_df)}")