import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV文件，假设文件路径和名称
input_file = r"H:\1_合并RQ2\8-99分段10人_percentage_output.csv"  # 替换为你的文件名
df = pd.read_csv(input_file)

# 将数据转换为数值类型，并将无法转换的数据设为 NaN
df = df.apply(pd.to_numeric, errors='coerce')

# 计算每列中每行的占比
df_percentage = df.div(df.sum(axis=0), axis=1) * 100

# 绘制热力图
plt.figure(figsize=(12, 8))
sns.heatmap(df_percentage, annot=True, cmap="YlGnBu", fmt=".2f", cbar_kws={'label': 'Percentage'})

# 设置图表标题和轴标签
plt.title("Distribution of Value Ranges by Percentage Ranges")
plt.xlabel("Percentage Range")
plt.ylabel("Value Range")
plt.xticks(rotation=45)
plt.tight_layout()

# 保存热力图
output_file = r"H:\1_合并RQ2\8-99_percentage_distribution_heatmap.png"  # 替换为保存路径和文件名
plt.savefig(output_file, dpi=300)  # dpi=300 提高分辨率

# 显示热力图
plt.show()

print(f"热力图已保存到 {output_file}")
