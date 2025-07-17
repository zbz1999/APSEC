import subprocess
import pandas as pd
import os
from thefuzz import fuzz  # 用于姓名模糊匹配，安装：pip install thefuzz
from collections import defaultdict
from datetime import datetime


def extract_git_log(repo_dir):
    """提取Git仓库提交日志，包含增强字段"""
    try:
        result = subprocess.run(
            # 修改为只获取必要字段，确保时间戳是数字格式
            ['git', 'log', '--pretty=format:%H|%an|%ae|%at|%s'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            timeout=300  # 添加超时防止卡死
        )
        if result.returncode != 0:
            print(f'Error in {repo_dir}: {result.stderr}')
            return None
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f'Timeout in {repo_dir}, skipped')
        return None
    except Exception as e:
        print(f'Critical error in {repo_dir}: {str(e)}')
        return None


def merge_identities(log_entries):
    """开发者身份消歧核心逻辑"""
    # 第一阶段：邮箱精确分组
    email_groups = defaultdict(list)
    for entry in log_entries:
        email = entry['Author Email'].lower().strip()
        if not email:  # 跳过空邮箱
            continue
        email_groups[email].append(entry)

    # 第二阶段：匿名邮箱的姓名模糊匹配
    merged_entries = []
    for email, entries in email_groups.items():
        if is_generic_email(email):
            name_clusters = cluster_names(entries)
            merged_entries.extend(name_clusters)
        else:
            merged_entries.append(entries)

    return merged_entries


def is_generic_email(email):
    """检测是否为通用匿名邮箱"""
    generic_domains = [
        'users.noreply.github.com',
        'example.com',
        'gmail.com',
        'hotmail.com'
    ]
    return any(email.endswith(f'@{d}') for d in generic_domains)


def cluster_names(entries, similarity_threshold=80):
    """基于姓名相似度聚类"""
    clusters = []
    for entry in entries:
        matched = False
        current_name = entry['Author'].lower().strip()
        if not current_name:  # 跳过空名字
            continue

        for cluster in clusters:
            for e in cluster:
                if fuzz.ratio(current_name, e['Author'].lower().strip()) > similarity_threshold:
                    cluster.append(entry)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            clusters.append([entry])
    return clusters


def parse_git_log(log_output):
    """解析日志并执行身份合并"""
    raw_entries = []
    malformed_lines = 0

    for line in log_output.splitlines():
        parts = line.split('|', 4)  # 现在只有5个字段：%H|%an|%ae|%at|%s
        if len(parts) == 5:
            try:
                raw_entries.append({
                    'Commit Hash': parts[0].strip(),
                    'Author': parts[1].strip(),
                    'Author Email': parts[2].lower().strip(),
                    'Timestamp': int(parts[3]),  # 确保这是数字时间戳
                    'Message': parts[4].strip()
                })
            except (ValueError, IndexError) as e:
                print(f'Skipping malformed line: {line} ({str(e)})')
                malformed_lines += 1
        else:
            malformed_lines += 1

    if malformed_lines > 0:
        print(f'Warning: Skipped {malformed_lines} malformed lines')

    return merge_identities(raw_entries)


def save_identity_report(merged_data, output_path):
    """生成身份合并报告"""
    report = []
    for group in merged_data:
        if not group:  # 跳过空组
            continue

        canonical = max(group, key=lambda x: x['Timestamp'])
        first_date = datetime.fromtimestamp(min(e['Timestamp'] for e in group)).strftime('%Y-%m-%d')
        last_date = datetime.fromtimestamp(max(e['Timestamp'] for e in group)).strftime('%Y-%m-%d')

        report.append({
            'Canonical Name': canonical['Author'],
            'Canonical Email': canonical['Author Email'],
            'Aliases': '; '.join({e['Author'] for e in group if e['Author']}),
            'Commit Count': len(group),
            'First Commit': first_date,
            'Last Commit': last_date,
            'Unique Identities': len({e['Author'] for e in group})
        })

    pd.DataFrame(report).to_csv(output_path, index=False, encoding='utf-8-sig')


def process_repository(repo_path, output_dir):
    """处理单个仓库"""
    try:
        repo_name = os.path.basename(repo_path)
        print(f'Processing: {repo_name}')

        log_output = extract_git_log(repo_path)
        if not log_output:
            return False

        merged_data = parse_git_log(log_output)
        if not merged_data:
            print(f'No valid data in {repo_name}')
            return False

        # 保存原始数据（调试用）
        debug_path = os.path.join(output_dir, f'{repo_name}_raw.csv')
        all_entries = [e for group in merged_data for e in group]
        pd.DataFrame(all_entries).to_csv(debug_path, index=False, encoding='utf-8-sig')

        # 保存身份报告
        report_path = os.path.join(output_dir, f'{repo_name}_identities.csv')
        save_identity_report(merged_data, report_path)

        return True
    except Exception as e:
        print(f'Error processing {repo_path}: {str(e)}')
        return False


def batch_process(base_dir, output_dir):
    """批量处理目录下的所有仓库"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    success_count = 0
    total_repos = 0

    for item in sorted(os.listdir(base_dir)):
        repo_path = os.path.join(base_dir, item)
        if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
            total_repos += 1
            if process_repository(repo_path, output_dir):
                success_count += 1
            print(f'Progress: {success_count}/{total_repos}')

    print(f'\nProcess completed. Success: {success_count}/{total_repos} repositories')


if __name__ == '__main__':
    repositories_dir = 'H:/matched_folders_final_469'  # 仓库根目录
    output_directory = 'H:/1_change_Developer_Analysis'  # 输出目录

    # 添加UTF-8编码支持（Windows可能需要）
    import sys
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    batch_process(repositories_dir, output_directory)