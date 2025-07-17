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

# 从GitHub获取仓库的Pull Request数量
def get_pull_requests_count(repo_name):
    pulls_url = f'https://api.github.com/repos/{repo_name}/pulls?state=all'
    response = requests.get(pulls_url, headers=headers)
    if response.status_code == 200:
        return len(response.json())  # 返回Pull Requests的数量
    else:
        return 0

# 处理单个URL
def process_url(url):
    repo_name = url.strip().replace("https://github.com/", "")
    pull_requests_count = get_pull_requests_count(repo_name)
    return url, pull_requests_count > 0

# 主函数
def main():
    # 输入和输出文件路径
    input_file = 'H:/top_github_repositories.xlsx'
    output_file_filtered = 'H://filtered_projects_pull_request.xlsx'
    output_file_removed = 'H://removed_projects_pull_request.xlsx'

    # 读取Excel文件中的URL列表
    df = pd.read_excel(input_file)
    urls = df['URL'].tolist()

    filtered_urls = []
    removed_urls = []

    # 使用ThreadPoolExecutor进行并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url, has_pull_request = future.result()
            if has_pull_request:
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
