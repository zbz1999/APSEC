import subprocess
import pandas as pd
from collections import defaultdict
import os
from fuzzywuzzy import fuzz
from datetime import datetime

# 配置路径
input_root_folder = 'H:/matched_folders_final_469'
output_folder = 'H:/1_合并RQ3.5/all_operation'

# 全局存储已知开发者身份
developer_identity_map = {}


# 获取Git仓库路径
def get_git_repos(root_folder):
    return [os.path.join(root_folder, d) for d in os.listdir(root_folder)
            if os.path.isdir(os.path.join(root_folder, d))]


# 检测机器人账户
def is_robot_account(author):
    robot_keywords = ["-bot", "[bot]", "github-actions", "automation"]
    return any(kw in author.lower() for kw in robot_keywords)


# 检测通用邮箱
def is_generic_email(email):
    generic_domains = [
        'users.noreply.github.com',
        'example.com',
        'gmail.com',
        'hotmail.com'
    ]
    return any(email.endswith(f'@{d}') for d in generic_domains)


# 基于姓名相似度聚类
def cluster_names(entries, threshold=80):
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


# 合并开发者身份（使用您之前提供的逻辑）
def merge_identities(entries):
    # 第一阶段：按邮箱精确分组
    email_groups = defaultdict(list)
    for entry in entries:
        email = entry['author_email'].lower().strip()
        email_groups[email].append(entry)

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
        canonical = max(group, key=lambda x: x['timestamp'])
        for entry in group:
            identity_map[entry['original_author']] = canonical['author_name']

    return identity_map


# 解析Git日志并提取身份信息
def extract_author_info(log_output):
    entries = []
    for line in log_output.splitlines():
        if not line.strip():
            continue

        # 解析提交信息行（格式：哈希 作者 <邮箱>）
        if ' ' in line and '<' in line and '>' in line:
            parts = line.split(' ', 1)
            author_part = parts[1]
            name, email = author_part.split('<')[0].strip(), author_part.split('<')[1].split('>')[0].strip()

            entries.append({
                'original_author': author_part,
                'author_name': name,
                'author_email': email.lower(),
                'timestamp': 0  # 此处简化，实际应解析时间戳
            })

    return merge_identities(entries)


# 获取Git日志
def get_git_log(repo_path):
    cmd = ['git', 'log', '--name-status', '--pretty=format:%H %an <%ae>']
    result = subprocess.run(cmd, cwd=repo_path,
                            capture_output=True, text=True, encoding='utf-8')
    return result.stdout if result.returncode == 0 else ""


# 解析提交日志并统计操作
def parse_commit_operations(log_output, identity_map):
    operations = defaultdict(lambda: [0, 0, 0, 0, 0, 0])  # A, M, D, R, V, C
    current_author = None

    for line in log_output.splitlines():
        if not line:
            continue

        if ' ' in line:  # 作者行
            author_info = line.split(' ', 1)[1]
            current_author = identity_map.get(author_info, author_info)
            if is_robot_account(current_author):
                current_author = None
        else:  # 文件操作行
            operation = line[0]
            if current_author is not None:
                if operation == 'A':
                    operations[current_author][0] += 1
                elif operation == 'M':
                    operations[current_author][1] += 1
                elif operation == 'D':
                    operations[current_author][2] += 1
                elif operation == 'R':
                    operations[current_author][3] += 1
                elif operation == 'V':
                    operations[current_author][4] += 1
                elif operation == 'C':
                    operations[current_author][5] += 1

    return operations


# 处理单个仓库
def process_repo(repo_path, output_folder):
    print(f"处理仓库: {repo_path}")
    log_output = get_git_log(repo_path)
    if not log_output:
        print(f"仓库 {repo_path} 没有提交日志，跳过")
        return

    # 构建开发者身份映射
    identity_map = extract_author_info(log_output)

    # 统计操作
    operations = parse_commit_operations(log_output, identity_map)

    # 保存结果
    repo_name = os.path.basename(repo_path)
    df = pd.DataFrame([
        {'Developer': dev, 'Additions': ops[0], 'Modifications': ops[1],
         'Deletions': ops[2], 'Renames': ops[3], 'Replaces': ops[4], 'Copies': ops[5]}
        for dev, ops in operations.items()
    ])
    output_path = os.path.join(output_folder, f"{repo_name}_operations.csv")
    df.to_csv(output_path, index=False)
    print(f"结果已保存到 {output_path}")


# 主流程
def main():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for repo in get_git_repos(input_root_folder):
        process_repo(repo, output_folder)


if __name__ == "__main__":
    main()