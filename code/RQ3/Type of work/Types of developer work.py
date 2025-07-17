import subprocess
import pandas as pd
from collections import defaultdict
import os
from datetime import datetime
from fuzzywuzzy import fuzz  # 用于名称相似度比较

# 配置路径
input_folder = 'H:/matched_folders_final_469'
output_folder = 'H:/1_合并RQ3.6/1_worktype_Results'


# 开发者身份统一识别相关函数
def is_robot_account(author):
    """检测是否为机器人账户"""
    robot_keywords = ["-bot", "[bot]", "github-actions", "automation"]
    return any(kw in author.lower() for kw in robot_keywords)


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


def merge_identities(entries):
    """合并开发者身份"""
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


def extract_author_info(log_output):
    """从日志中提取作者信息"""
    entries = []
    for line in log_output.splitlines():
        if not line.strip():
            continue

        # 解析提交信息行（格式：哈希 作者 <邮箱>）
        if ' ' in line and '<' in line and '>' in line:
            parts = line.split(' ', 1)
            author_part = parts[1]
            name = author_part.split('<')[0].strip()
            email = author_part.split('<')[1].split('>')[0].strip()

            entries.append({
                'original_author': author_part,
                'author_name': name,
                'author_email': email.lower(),
                'timestamp': 0  # 此处简化，实际应解析时间戳
            })

    return merge_identities(entries)


# 原有功能函数（稍作修改）
def get_git_log(repo_path):
    """获取Git日志（修改格式以包含邮箱）"""
    cmd = ['git', 'log', '--name-status', '--pretty=format:%H %an <%ae>']
    result = subprocess.run(cmd, cwd=repo_path,
                            capture_output=True, text=True, encoding='utf-8')
    return result.stdout if result.returncode == 0 else ""


def classify_file_type(file_name):
    """文件类型分类（保持不变）"""
    if file_name.endswith(('.py', '.js', '.java', '.c', '.cpp', '.h', '.html',
                           '.css', '.rb', '.go', '.php', '.ts', '.swift',
                           '.sh', '.sql', '.json', '.xml', '.pl', '.r',
                           '.vb', '.asm', '.rs', '.svelte', '.handlebars',
                           '.dockerfile', '.xsl', '.starlark', '.ipynb',
                           '.dart', '.scala', '.kotlin', '.groovy', '.lua', '.star', '.abtlr', '.xslt')):
        return 'Code'
    elif file_name.endswith(('.md', '.txt', '.pdf', '.docx', '.pptx', '.xls', '.xlsx',
                             '.rtf', '.odt', '.wps', '.html')):
        return 'Documentation'
    elif file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.tiff',
                             '.ico', '.webp')):
        return 'Image'
    elif file_name.endswith(('.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z',
                             '.whl', '.dmg', '.iso')):
        return 'Packaging'
    elif file_name.endswith(('.mp4', '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mov',
                             '.avi', '.mkv', '.wmv')):
        return 'Multimedia'
    elif file_name.startswith('i18n') or 'localization' in file_name:
        return 'Internationalization (i18n)'
    elif 'ui' in file_name or 'interface' in file_name:
        return 'User Interface (UI)'
    elif 'devel' in file_name:
        return 'Developer Documentation (devel-doc)'
    elif 'build' in file_name:
        return 'Build'
    else:
        return 'Other'


def parse_commit_operations(log_output, identity_map):
    """解析提交日志（整合身份识别）"""
    developer_file_types = defaultdict(lambda: defaultdict(int))
    current_author = None

    for line in log_output.splitlines():
        if not line:
            continue

        if ' ' in line and '<' in line and '>' in line:  # 作者行
            author_info = line.split(' ', 1)[1]
            current_author = identity_map.get(author_info, author_info)
            if is_robot_account(current_author):
                current_author = None
        elif line and line[0] in 'AMDRVC':  # 文件操作行
            parts = line.split()
            if len(parts) > 1 and current_author is not None:
                operation, file_name = parts[0], parts[1]
                file_type = classify_file_type(file_name)
                developer_file_types[current_author][file_type] += 1

    return developer_file_types


def process_repo(repo_path, output_folder):
    """处理单个仓库（整合新功能）"""
    print(f"处理仓库: {repo_path}")
    repo_name = os.path.basename(repo_path)
    log_output = get_git_log(repo_path)

    if not log_output:
        print(f"仓库 {repo_path} 没有提交日志，跳过")
        return

    # 构建开发者身份映射
    identity_map = extract_author_info(log_output)

    # 统计文件类型
    file_types_count = parse_commit_operations(log_output, identity_map)

    # 准备数据并保存
    data = [{'Developer': dev, **file_types} for dev, file_types in file_types_count.items()]
    file_type_columns = ['Code', 'Documentation', 'Image', 'Packaging', 'Multimedia',
                         'Internationalization (i18n)', 'User Interface (UI)',
                         'Developer Documentation (devel-doc)', 'Build', 'Other']

    df = pd.DataFrame(data).fillna(0)
    for column in file_type_columns:
        if column not in df.columns:
            df[column] = 0

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file_name = f"{repo_name}_file_types_summary_{timestamp}.csv"
    output_file_path = os.path.join(output_folder, output_file_name)
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

    print(f"完成统计仓库：{repo_name}，结果已保存到 {output_file_path}")


def process_all_repos_in_folder(folder_path, output_folder):
    """批量处理所有仓库"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for repo_name in os.listdir(folder_path):
        repo_path = os.path.join(folder_path, repo_name)
        if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
            process_repo(repo_path, output_folder)


# 主程序
if __name__ == "__main__":
    # 安装依赖：pip install pandas fuzzywuzzy python-Levenshtein
    process_all_repos_in_folder(input_folder, output_folder)
    print("所有仓库统计完成！结果已保存到指定文件夹。")