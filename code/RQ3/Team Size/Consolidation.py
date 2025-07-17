import pandas as pd

# 设置文件路径
file1_path = 'H:/1_合并RQ3.8/teamsize/project_sizes.csv'  # 主文件路径
file2_path = 'H:/1_合并RQ3.8/teamsize/leave.csv'  # 包含离开百分比的文件路径
output_path = 'H:/1_合并RQ3.8/teamsize/合并结果.csv'  # 输出文件路径

try:
    # 读取两个CSV文件
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # 根据项目名称列合并两个数据框
    merged_df = pd.merge(df1, df2[['项目名称', '离开百分比']],
                         on='项目名称',
                         how='left')

    # 保存合并后的结果
    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"文件合并成功，已保存到: {output_path}")

except Exception as e:
    print(f"处理过程中出错: {e}")