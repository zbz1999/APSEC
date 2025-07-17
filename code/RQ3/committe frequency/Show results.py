import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 适配中文字体
rcParams['axes.unicode_minus'] = False   # 用于正常显示负号

# 设置背景为白色，去除背景线
sns.set(style="white")

# 加载数据
file_path = "H:/1_合并RQ3.3/1_combined_cleaned_data_1.csv"  # 替换为实际路径
data = pd.read_csv(file_path)

# 查看数据情况
print(data.head())
print(data.info())
print(data.isnull().sum())

# 如果存在缺失值，可以选择填补或删除
data = data.dropna()  # 这里删除含有缺失值的行，你也可以选择填补缺失值

# 描述提交频率的分布（每0.5为一组）
plt.figure(figsize=(10, 6))
bins = [i * 0.5 for i in range(int(data["Commit Frequency"].max() / 0.5) + 2)]  # 每0.5分组
ax = plt.hist(data["Commit Frequency"], bins=bins, color='skyblue', edgecolor='black')
plt.title("Commit frequency distribution (grouped by 0.5)")
plt.xlabel("Commit frequency ranges")
plt.ylabel("Number of developers")

# 显示数值并调整字体大小
for i in range(len(ax[0])):
    plt.text(ax[1][i] + 0.25, ax[0][i] + 1, str(int(ax[0][i])), ha='center', va='bottom', fontsize=10)

# 保存图片
plt.tight_layout()
plt.savefig("F:\研究生\MDPI-picture\p7.png",dpi=300)
print(f"提交频率分布图（每0.5为一组）已保存")
plt.show()
