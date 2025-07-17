import os
import pandas as pd
from datetime import datetime, timedelta

def generate_time_periods(first_commit_date, end_date_str="2024-06-16"):
    periods = []
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")  # 结束时间
    start_date = datetime.strptime(first_commit_date, "%Y-%m-%d")  # 开始时间

    current_date = end_date

    while current_date >= start_date:  # 倒序计算时间段
        if current_date - timedelta(days=180) < start_date:
            next_date = start_date  # 超出开始时间，结束时间设为开始时间
        else:
            next_date = current_date - timedelta(days=180)

        periods.append((next_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d")))
        current_date = next_date - timedelta(days=1)  # 下一阶段的结束日期是前一阶段的前一天

    return periods[::-1]  # 反转为正序返回

def is_bot_account(author_name):
    if isinstance(author_name, str):  # 确保 author_name 是字符串
        bot_indicators = ["-bot", "[bot]", "github-actions", "automation"]
        return any(indicator in author_name.lower() for indicator in bot_indicators)
    return False  # 如果不是字符串，返回 False

def process_commit_log(csv_file_path, output_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)

    # 检查和清理“Date”列中的无效日期
    invalid_dates = df[~df['Date'].apply(lambda x: isinstance(x, str) and x.strip() != "")]
    if not invalid_dates.empty:
        print(f"发现无效日期行:\n{invalid_dates}")  # 打印出包含无效日期的行

    # 确保日期列是 datetime 类型，并忽略错误
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # 将无法解析的日期转换为 NaT

    # 过滤掉无效日期
    df = df.dropna(subset=['Date'])

    # 过滤掉机器人账户
    df = df[~df['Author'].apply(is_bot_account)]

    if df.empty:
        print(f"处理文件 {csv_file_path} 时，没有有效的提交记录。")
        return

    first_commit_date = df['Date'].min().strftime("%Y-%m-%d")  # 获取最早提交日期
    last_commit_date = df['Date'].max().strftime("%Y-%m-%d")  # 获取最后提交日期

    # 生成时间段
    time_periods = generate_time_periods(first_commit_date, last_commit_date)

    data_to_save = []
    for start_date, end_date in time_periods:
        # 选择当前时间段的提交记录
        period_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        developers = {str(author) for author in period_df['Author'] if isinstance(author, (str, float))}  # 确保为字符串
        dev_count = len(developers)  # 当前阶段的开发者数量

        # 计算上一阶段有但是当前阶段没有的开发者
        if data_to_save:
            prev_developers = set(data_to_save[-1]["Developers"].split(", "))
            absent_in_next_period = prev_developers - developers
            absent_count = len(absent_in_next_period)
        else:
            absent_in_next_period = set()
            absent_count = 0

        # 保存当前阶段信息
        data_to_save.append({
            "Time Period": f"{start_date} to {end_date}",
            "Developers": ", ".join(developers),
            "Developer Count": dev_count,
            "Absent in Next Period": ", ".join(absent_in_next_period),
            "Absent Count": absent_count,
            "Change Percentage": ""  # 预留位置
        })

        # 计算当前阶段有但是下一个阶段没有的开发者数量
        if len(data_to_save) > 1:  # 如果是第二个阶段或后续阶段
            prev_developers = set(data_to_save[-2]["Developers"].split(", "))
            absent_in_next_period = prev_developers - developers
            absent_count = len(absent_in_next_period)
            change_percentage = (absent_count / len(prev_developers)) * 100 if prev_developers else 0
            data_to_save[-1]["Change Percentage"] = f"{change_percentage:.2f}%"

    # 保存到 CSV 文件
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    df_to_save = pd.DataFrame(data_to_save)
    df_to_save.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"开发者名单、数量和时间段已保存到 {output_file}")

def batch_process_commit_logs(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith("_commits.csv"):  # 确保文件是 CSV 格式
            csv_file_path = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{filename.replace('_commits.csv', '_处理后.csv')}")
            process_commit_log(csv_file_path, output_file)

if __name__ == "__main__":
    input_folder = "H:/1_469提交日志"  # 替换为你的文件夹路径
    output_folder = "H:/1_合并后469个按照6个月为阶段的离开文件"  # 替换为你想保存的输出文件夹路径
    batch_process_commit_logs(input_folder, output_folder)
