import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy import stats

# 定义文件夹路径
folder_path = r'H:\1_合并RQ3.2\fenkaide_all_output_csvs'  # 替换为你的文件夹路径
output_csv = r'H:/1_合并RQ3.2/1_放大_论文_regression_results.csv'  # 输出CSV文件路径
output_images_folder = r'H:/1_合并RQ3.2/1_放大_论文_regression_images'  # 输出图像文件夹路径

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_images_folder):
    os.makedirs(output_images_folder)

# 初始化输出结果的DataFrame
regression_results = []

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 过滤掉数据行数小于等于5的文件
        if len(df) > 5:
            # 提取数据
            x = df['Year'].values.reshape(-1, 1)  # 需要转换为列向量
            y = df['Number of Developers'].values

            # 定义多个模型（线性回归、二次多项式回归和对数回归）
            models = {
                'Linear': (x, y),  # 线性回归
                'Polynomial 2nd Degree': (PolynomialFeatures(degree=2).fit_transform(x), y),  # 二次多项式回归
                'Logarithmic (ln(x))': (np.log(x), y)  # 对数回归（ln(x)）
            }

            # 存储最佳模型的结果
            best_model = None
            best_r_squared = -np.inf
            best_mse = np.inf
            best_eq = ""

            for model_name, (x_model, y_model) in models.items():
                if model_name == 'Linear':
                    # 线性回归
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x.flatten(), y)
                    y_pred = slope * x.flatten() + intercept
                    r_squared = r_value ** 2
                    mse = mean_squared_error(y, y_pred)
                    eq = f'y = {slope:.2f}x + {intercept:.2f}'
                elif model_name == 'Logarithmic (ln(x))':
                    # 对数回归：y = a * ln(x) + b
                    log_reg = LinearRegression()
                    log_reg.fit(x_model, y_model)
                    y_pred = log_reg.predict(x_model)
                    r_squared = log_reg.score(x_model, y_model)
                    mse = mean_squared_error(y, y_pred)
                    eq = f'y = {log_reg.intercept_:.2f} + {log_reg.coef_[0]:.2f}ln(x)'
                else:
                    # 二次多项式回归
                    poly_reg = LinearRegression()
                    poly_reg.fit(x_model, y_model)
                    y_pred = poly_reg.predict(x_model)
                    r_squared = poly_reg.score(x_model, y_model)
                    mse = mean_squared_error(y, y_pred)
                    eq = f'{model_name} Equation: {poly_reg.intercept_:.2f} + {poly_reg.coef_}'

                # 选择拟合度最好的模型
                if r_squared > best_r_squared or (r_squared == best_r_squared and mse < best_mse):
                    best_r_squared = r_squared
                    best_mse = mse
                    best_model = model_name
                    best_eq = eq

            # 修改文件名处理逻辑：仅去除_identities_filtered_years.csv后缀
            cleaned_filename = filename.replace('_identities_filtered_years.csv', '')

            # 绘制最佳回归图像（调整字号和图像质量）
            plt.figure(figsize=(8, 6))  # 调整图像大小
            plt.scatter(x, y, color='blue', label='Data Points')
            if best_model == 'Linear':
                plt.plot(x, slope * x.flatten() + intercept, color='red', 
                         label=f'Linear Fit: y = {slope:.2f}x + {intercept:.2f}')
            elif best_model == 'Polynomial 2nd Degree':
                y_poly = np.poly1d(np.polyfit(x.flatten(), y, 2))(x.flatten())
                plt.plot(x, y_poly, color='green', 
                         label=f'Poly 2nd: {np.polyfit(x.flatten(), y, 2)}')
            elif best_model == 'Logarithmic (ln(x))':
                plt.plot(x, log_reg.predict(np.log(x)), color='purple', 
                         label=f'Log Fit: y = {log_reg.intercept_:.2f} + {log_reg.coef_[0]:.2f}ln(x)')

            # 设置标题、坐标轴标签和图例的字号
            plt.title(f'Regression for {cleaned_filename}', fontsize=26, pad=16)  # 标题字号16，增加标题与图的间距
            plt.xlabel('Year', fontsize=20)  # X轴标签字号14
            plt.ylabel('Number of Developers', fontsize=20)  # Y轴标签字号14
            plt.legend(fontsize=14, loc='best')  # 图例字号12，自动选择最佳位置
            plt.xticks(fontsize=14)  # X轴刻度字号12
            plt.yticks(fontsize=14)  # Y轴刻度字号12

            # 保存高质量图像
            image_path = os.path.join(output_images_folder, f'{cleaned_filename}_best_regression.png')
            plt.savefig(image_path, dpi=300, bbox_inches='tight')  # 高DPI，防止裁剪
            plt.close()

            # 将最佳模型的回归方程和R²添加到结果中
            regression_results.append({
                'File': filename,
                'Best Model': best_model,
                'Equation': best_eq,
                'R²': best_r_squared
            })

# 将回归结果保存到CSV文件
regression_df = pd.DataFrame(regression_results)
regression_df.to_csv(output_csv, index=False)

print("回归分析完成，结果已保存。")