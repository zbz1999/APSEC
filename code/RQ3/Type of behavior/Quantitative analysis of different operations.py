import pandas as pd

# 文件路径
input_file = r'H:\1_合并RQ3.5\行为类型与离开合并结果.csv'  # 替换为实际文件路径
output_file = r'H:\1_合并RQ3.5\操作类型统计结果.csv'  # 统计结果保存路径

# 读取CSV文件
try:
    df = pd.read_csv(input_file, usecols=['Primary_Action_Type'])
except Exception as e:
    print(f"读取文件失败: {str(e)}")
    exit()

# 统计操作类型频次
action_counts = df['Primary_Action_Type'].value_counts().reset_index()
action_counts.columns = ['操作类型', '出现次数']

# 计算百分比
total = action_counts['出现次数'].sum()
action_counts['百分比(%)'] = round((action_counts['出现次数'] / total) * 100, 2)

# 按出现次数降序排序
action_counts = action_counts.sort_values('出现次数', ascending=False)

# 保存结果
action_counts.to_csv(output_file, index=False, encoding='utf-8-sig')

# 打印结果
print("操作类型统计结果：")
print(action_counts)
print(f"\n结果已保存到: {output_file}")