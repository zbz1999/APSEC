import subprocess
import pandas as pd
from collections import defaultdict
import os
from fuzzywuzzy import fuzz  # 用于名称相似度比较


# 执行 Git 日志命令，获取提交信息（修改为包含邮箱）
def get_git_log(repo_path):
    try:
        # 修改命令格式以获取邮箱信息
        command = ['git', 'log', '--name-status', '--pretty=format:%H %an <%ae>']
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            raise RuntimeError(f"Git log 执行失败: {result.stderr}")

        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"获取 Git 日志时出错: {e}")
        return []


# 判断开发者是否为机器人（保持不变）
def is_bot(author):
    bot_keywords = ["-bot", "[bot]", "github-actions", "automation"]
    return any(keyword in author.lower() for keyword in bot_keywords)


# 开发者身份统一识别相关函数
def is_generic_email(email):
    """检测是否为通用/匿名邮箱"""
    generic_domains = [
        'users.noreply.github.com',
        'example.com',
        'gmail.com',
        'hotmail.com'
    ]
    return any(email.endswith(f'@{d}') for d in generic_domains)


def cluster_names(entries, threshold=80):
    """基于姓名相似度聚类"""
    clusters = []
    for entry in entries:
        current_name = entry['author_name'].lower().strip()
        if not current_name:
            continue

        matched = False
        for cluster in clusters:
            if any(fuzz.ratio(current_name, e['author_name'].lower().strip()) > threshold
                   for e in cluster):
                cluster.append(entry)
                matched = True
                break
        if not matched:
            clusters.append([entry])
    return clusters


def build_identity_map(log_output):
    """构建开发者身份映射表"""
    entries = []

    # 提取作者信息
    for line in log_output:
        if not line.strip():
            continue

        if ' ' in line and '<' in line and '>' in line:
            parts = line.split(' ', 1)
            author_part = parts[1]
            name = author_part.split('<')[0].strip()
            email = author_part.split('<')[1].split('>')[0].strip().lower()

            entries.append({
                'original_author': author_part,
                'author_name': name,
                'author_email': email
            })

    # 第一阶段：按邮箱精确分组
    email_groups = defaultdict(list)
    for entry in entries:
        email_groups[entry['author_email']].append(entry)

    # 第二阶段：处理匿名邮箱
    merged = []
    for email, group in email_groups.items():
        if not email or is_generic_email(email):
            merged.extend(cluster_names(group))
        else:
            merged.append(group)

    # 构建身份映射表
    identity_map = {}
    for group in merged:
        # 选择组内最长的名称作为规范名称
        canonical_name = max(group, key=lambda x: len(x['author_name']))['author_name']
        for entry in group:
            identity_map[entry['original_author']] = canonical_name

    return identity_map


# 解析提交日志（修改为使用身份映射）
def parse_commit_operations(commit_logs):
    # 先构建身份映射表
    identity_map = build_identity_map(commit_logs)

    developer_stats = defaultdict(lambda: {'created_count': 0, 'total_count': 0})
    current_author = None

    for log in commit_logs:
        if not log:
            continue
        if ' ' in log and '<' in log and '>' in log:  # 作者行
            author_info = log.split(' ', 1)[1]
            current_author = identity_map.get(author_info, author_info)
            if is_bot(current_author):
                current_author = None
        elif current_author and log[0] in 'AMDRVC':  # 文件操作行
            parts = log.split(maxsplit=1)
            if len(parts) == 2:
                operation, _ = parts
                developer_stats[current_author]['total_count'] += 1
                if operation == 'A':
                    developer_stats[current_author]['created_count'] += 1

    return developer_stats


# 主函数（保持不变）
def process_all_repos(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for repo_name in os.listdir(input_dir):
        repo_path = os.path.join(input_dir, repo_name)

        if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            print(f"正在处理仓库: {repo_name}")
            output_file_path = os.path.join(output_dir, f"{repo_name}_contributions_summary.csv")

            if os.path.exists(output_file_path):
                print(f"{output_file_path} 已存在，跳过此仓库。")
                continue

            commit_logs = get_git_log(repo_path)
            developer_stats = parse_commit_operations(commit_logs)

            data = [{'Developer': dev, 'Created Files Count': stats['created_count'],
                     'Total Files Count': stats['total_count']}
                    for dev, stats in developer_stats.items()]

            df = pd.DataFrame(data)
            df.to_csv(output_file_path, index=False)
            print(f"已保存统计结果到 {output_file_path}")


# 输入输出路径（保持不变）
input_dir = 'H:/matched_folders_final_469'
output_dir = 'H:/1_合并RQ3.7/all_output'

# 执行处理
process_all_repos(input_dir, output_dir)
print("所有仓库的统计已完成。")