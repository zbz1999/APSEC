import pandas as pd
import os
import chardet

# 定义文件路径
input_file = r"H:\1_合并RQ2\8-99分段10人.csv"  # 替换为你的文件名


# 检测文件编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


try:
    # 尝试自动检测编码读取文件
    encoding = detect_encoding(input_file)
    df = pd.read_csv(input_file, index_col=0, encoding=encoding)

    # 创建一个空的 DataFrame 来存储百分比
    percentage_df = pd.DataFrame(index=df.index, columns=df.columns)

    # 计算每列中每行的百分比
    for col in df.columns:
        column_sum = df[col].sum()  # 计算当前列的总和
        if column_sum > 0:  # 防止除以零
            percentage_df[col] = (df[col] / column_sum * 100).round(2)  # 保留2位小数
        else:
            percentage_df[col] = 0.0  # 如果列的总和为0，百分比设为0

    # 输出结果文件路径
    output_dir = r"H:\1_合并RQ2"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}_percentage_output.csv")

    # 保存结果到新的CSV文件
    percentage_df.to_csv(output_file, encoding='utf-8-sig')  # 使用utf-8-sig确保中文正常

    print(f"百分比计算结果已保存到 {output_file}")
    print("\n前5行计算结果预览:")
    print(percentage_df.head())

except Exception as e:
    print(f"处理文件时出错: {e}")
    print("\n尝试使用备选编码...")

    # 尝试常见中文编码
    encodings_to_try = ['gbk', 'gb2312', 'utf-16', 'latin1']
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(input_file, index_col=0, encoding=enc)
            print(f"成功使用 {enc} 编码读取文件")
            # 这里可以加入上面的处理逻辑
            break
        except:
            continue