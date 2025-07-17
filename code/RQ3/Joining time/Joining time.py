import subprocess
import pandas as pd
from datetime import datetime
import os
from collections import defaultdict


def get_first_commit_times(repo_path):
    """
    获取指定 Git 仓库中每个开发者的首次提交时间（基于邮箱统一识别开发者）。
    返回格式：{'统一作者名': 最早提交日期}
    """
    # 执行 git log 命令，获取作者、邮箱和提交时间
    log_output = subprocess.check_output(
        ['git', 'log', '--pretty=format:%an|%ae|%ad', '--date=iso', '--reverse'],
        cwd=repo_path,
        text=True,
        encoding='utf-8'
    )

    # 排除机器人账户的关键词
    bot_keywords = ["-bot", "[bot]", "github-actions", "automation"]

    # 用邮箱作为唯一标识
    email_to_info = {}  # 格式：{email: {'primary_name': str, 'first_date': date}}

    for line in log_output.splitlines():
        parts = line.split('|', 2)
        if len(parts) != 3:
            continue

        author, email, date_str = parts[0].strip(), parts[1].strip().lower(), parts[2].strip()

        # 跳过机器人账户
        if any(bot in author.lower() for bot in bot_keywords) or any(bot in email for bot in bot_keywords):
            continue

        try:
            commit_date = datetime.fromisoformat(date_str).date()
        except ValueError:
            continue

        # 如果是新邮箱，记录信息
        if email not in email_to_info:
            email_to_info[email] = {
                'primary_name': author,  # 第一次出现的用户名作为主名称
                'first_date': commit_date
            }
        else:
            # 更新最早日期
            if commit_date < email_to_info[email]['first_date']:
                email_to_info[email]['first_date'] = commit_date
                # 可以选择更新主名称（这里保持第一次出现的名称）

    # 转换为最终格式：{'主作者名': 最早提交日期}
    return {info['primary_name']: info['first_date'] for email, info in email_to_info.items()}


def save_to_csv(file_path, first_commit_times):
    """
    将结果保存为两列CSV：Author 和 First Commit Date
    """
    df = pd.DataFrame(list(first_commit_times.items()), columns=['Author', 'First Commit Date'])
    df['First Commit Date'] = pd.to_datetime(df['First Commit Date']).dt.strftime('%Y-%m-%d')
    df.to_csv(file_path, index=False)


def process_all_repos(base_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for repo_name in os.listdir(base_folder):
        repo_path = os.path.join(base_folder, repo_name)

        if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
            print(f"正在处理仓库：{repo_name}")

            try:
                first_commit_times = get_first_commit_times(repo_path)
                output_file = os.path.join(output_folder, f"{repo_name}_first_commit_times.csv")
                save_to_csv(output_file, first_commit_times)
                print(f"结果已保存到：{output_file}")
            except Exception as e:
                print(f"处理 {repo_name} 时出错：{str(e)}")


if __name__ == "__main__":
    base_folder = "H:/matched_folders_final_469"
    output_folder = "H:/1_合并RQ3.1/all_jointime"
    process_all_repos(base_folder, output_folder)
    print("所有仓库处理完成！")