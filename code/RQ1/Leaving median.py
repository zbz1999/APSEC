import os
import pandas as pd

# 配置路径
source_folder_path = "H:/1_合并RQ2/1100-1199"  # 包含 last_commit_*_commits.csv 的文件夹
target_file_path = "H:/1_合并后469个中位数/median_results.csv"
output_file_path = "H:/1_合并RQ2/matched_files/combined_matched_data_1100-1199.csv"

# 创建输出目录（如果不存在）
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# 读取目标文件并预处理项目名
target_df = pd.read_csv(target_file_path)
target_df['Project'] = target_df['Filename'].str.replace("_处理后.csv", "", regex=True)

# 初始化结果DataFrame
combined_data = pd.DataFrame()

# 遍历源文件夹
for root, dirs, files in os.walk(source_folder_path):
    for filename in files:
        # 匹配形如 last_commit_*_commits.csv 的文件
        if filename.startswith("last_commit_") and filename.endswith("_commits.csv"):
            # 提取项目名（移除前后缀）
            project_name = filename[12:-12]  # 移除"last_commit_"和"_commits.csv"

            # 在目标数据中查找匹配项
            matched_data = target_df[target_df['Project'] == project_name]

            if not matched_data.empty:
                combined_data = pd.concat([combined_data, matched_data], ignore_index=True)
                print(f"匹配成功：{project_name} (来自文件: {filename})")

# 保存结果
if not combined_data.empty:
    combined_data.to_csv(output_file_path, index=False)
    print(f"成功匹配 {len(combined_data)} 个项目，结果已保存到: {output_file_path}")
else:
    print("警告：未匹配到任何项目，请检查文件名格式和匹配逻辑")