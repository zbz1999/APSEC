import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# GitHub访问令牌
token = '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'

# 并行处理的线程数
max_workers = 10

# 请求头部信息，包含认证信息
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 常见的软件开发相关目录和文件
software_dev_indicators = [
    'src/', 'lib/', 'include/', 'bin/', 'main.c', 'main.cpp', 'main.py',
    'Makefile', 'CMakeLists.txt', 'build.gradle', 'pom.xml', 'package.json',
    'setup.py', 'requirements.txt', 'Dockerfile'
]

# 从GitHub获取仓库的内容列表，并判断是否包含常见的软件开发相关目录或文件
def is_software_dev_repo(repo_name):
    contents_url = f'https://api.github.com/repos/{repo_name}/contents'
    response = requests.get(contents_url, headers=headers)
    if response.status_code == 200:
        repo_contents = response.json()
        for item in repo_contents:
            if any(indicator in item['path'] for indicator in software_dev_indicators):
                return True  # 找到软件开发相关的目录或文件
    return False

# 处理单个URL
def process_url(url):
    repo_name = url.strip().replace("https://github.com/", "")
    is_dev_repo = is_software_dev_repo(repo_name)
    return url, is_dev_repo

# 主函数
def main():
    # 输入和输出文件路径
    input_file = 'H:/filtered_projects_contributors.xlsx'
    output_file_filtered = 'H://filtered_projects_dev_related.xlsx'
    output_file_removed = 'H://removed_projects_dev_related.xlsx'

    # 读取Excel文件中的URL列表
    df = pd.read_excel(input_file)
    urls = df['Filtered Projects'].tolist()

    filtered_urls = []
    removed_urls = []

    # 使用ThreadPoolExecutor进行并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url, is_dev_repo = future.result()
            if is_dev_repo:
                filtered_urls.append(url)
            else:
                removed_urls.append(url)

    # 将筛选后保留和移除的项目分别保存到Excel
    pd.DataFrame(filtered_urls, columns=["Filtered Projects"]).to_excel(output_file_filtered, index=False)
    pd.DataFrame(removed_urls, columns=["Removed Projects"]).to_excel(output_file_removed, index=False)

    # 输出筛选信息
    print(f"最终剩余的项目数量: {len(filtered_urls)}")
    print(f"筛选掉的项目数量: {len(removed_urls)}")

if __name__ == "__main__":
    main()
