import pandas as pd
import os

# 定义文件路径
input_file = r"H:\1_合并RQ2\percentage_distribution.csv"  # 替换为你的文件名

# 读取CSV文件
df = pd.read_csv(input_file, index_col=0)

# 创建一个空的 DataFrame 来存储百分比
percentage_df = pd.DataFrame(index=df.index, columns=df.columns)

# 计算每列中每行的百分比
for col in df.columns:
    column_sum = df[col].sum()  # 计算当前列的总和
    if column_sum > 0:  # 防止除以零
        percentage_df[col] = (df[col] / column_sum) * 100
    else:
        percentage_df[col] = 0  # 如果列的总和为0，百分比设为0

# 输出结果文件路径
output_file = os.path.join(r"H:\1_合并RQ2", f"{os.path.splitext(os.path.basename(input_file))[0]}_percentage_output.csv")

# 保存结果到新的CSV文件
percentage_df.to_csv(output_file)

print(f"百分比计算结果已保存到 {output_file}")
