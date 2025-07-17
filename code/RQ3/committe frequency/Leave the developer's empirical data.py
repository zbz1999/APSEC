import os
import pandas as pd

# 定义文件夹路径
folder_path = "H:/1_合并RQ3.1/all_leave"  # 替换为你的实际路径
output_folder = "H:/1_合并RQ3.3/all_matched_results"  # 结果保存路径
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有CSV文件
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        output_path = os.path.join(output_folder, file)  # 结果存储路径

        # 读取数据，让 pandas 自动检测分隔符
        df = pd.read_csv(file_path)

        # 确保列存在
        required_cols = {"Author", "Count", "First Commit", "Last Commit"}
        if not required_cols.issubset(df.columns):
            print(f"跳过 {file}，缺少必要列")
            continue

        # 处理时间列
        df["First Commit"] = pd.to_datetime(df["First Commit"], errors='coerce')
        df["Last Commit"] = pd.to_datetime(df["Last Commit"], errors='coerce')

        # 计算间隔天数
        df["Days Active"] = (df["Last Commit"] - df["First Commit"]).dt.days

        # 过滤 First Commit 和 Last Commit 间隔小于 30 天的开发者
        df_filtered = df[df["Days Active"] >= 30].copy()

        # 计算提交频率
        df_filtered["Commit Frequency"] = df_filtered["Count"] / df_filtered["Days Active"]

        # 选择所需列
        df_result = df_filtered[["Author", "Commit Frequency"]]

        # 保存结果
        df_result.to_csv(output_path, index=False)

        print(f"处理完成: {file}, 结果已保存至 {output_path}")
