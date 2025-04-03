import numpy as np

def print_tableau(tableau):
    print("Current Simplex Tableau:")
    print(np.array_str(tableau, precision=3, suppress_small=True))
    print()

def pivot_on(tableau, pivot_row, pivot_col):
    # Make the pivot element to 1
    tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]

    # Make other elements in pivot column to 0
    for i in range(tableau.shape[0]):
        if i != pivot_row:
            tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

def simplex_method(objective_coeffs, constraint_coeffs, constraint_constants):
    num_vars = len(objective_coeffs)
    num_constraints = len(constraint_constants)

    # Construct the initial tableau
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:-1, :num_vars] = constraint_coeffs
    tableau[:-1, -1] = constraint_constants
    tableau[-1, :num_vars] = objective_coeffs
    tableau[-1, -1] = 0

    print_tableau(tableau)
    c = 1

    while True:
        # Check for optimality
        if np.all(tableau[-1, :-1] >= 0):
            break

        # Choose pivot column (most negative coefficient in objective row)
        pivot_col = np.argmin(tableau[-1, :-1])

        # Check for unboundedness
        if np.all(tableau[:-1, pivot_col] <= 0):
            print("警告：该线性规划问题无界，无法找到最优解。")
            return None, None

        # Choose pivot row (minimum ratio test)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        ratios[ratios <= 0] = np.inf
        pivot_row = np.argmin(ratios)

        # Perform pivot operation
        pivot_on(tableau, pivot_row, pivot_col)

        # Print the updated tableau
        print(f'第{c}次:')
        print_tableau(tableau)
        c += 1

    # Extract solution and optimal value
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        basic_vars = np.where(tableau[:-1, i] == 1)[0]
        if len(basic_vars) == 1:
            solution[i] = tableau[basic_vars[0], -1]

    optimal_value = tableau[-1, -1]

    return solution, optimal_value

def get_juzheng():
    print('请输入以下信息：')
    while True:
        try:
            z = input('输入目标函数系数z值(英文逗号间隔)：')
            list_z = list(map(int, z.split(',')))
            break
        except ValueError:
            print("输入无效，请输入以英文逗号分隔的整数。")
    while True:
        try:
            r_len = int(input('输入约束条件的数量：'))
            break
        except ValueError:
            print("输入无效，请输入一个整数。")
    total_z = [list_z]
    num_vars = len(list_z)
    for i in range(r_len):
        while True:
            try:
                A = input(f'输入第{i+1}个约束条件的系数(英文逗号间隔)：')
                b = input(f'输入第{i+1}个约束条件的常数项：')
                list_A = list(map(int, A.split(',')))
                # 检查约束条件系数数量是否与目标函数系数数量一致
                if len(list_A) != num_vars:
                    print(f"输入无效，第{i+1}个约束条件的系数数量必须为 {num_vars} 个。")
                    continue
                total_z.append(list_A + [int(b)])
                break
            except ValueError:
                print("输入无效，请输入以英文逗号分隔的整数。")
    return total_z

def max_juzheng(total_z):
    total_z[0] = [-1 * i for i in total_z[0]]  # 将目标函数系数乘以 -1
    return total_z[0], np.array(total_z[1:])[:, :-1], np.array(total_z[1:])[:, -1]  # 返回目标函数系数、系数矩阵和常数项
# def min_juzheng(total_z):
#     total_z[0] = [1 * i for i in total_z[0]]
#     return total_z[0], np.array(total_z[1:])[:, :-1], np.array(total_z[1:])[:, -1]  # 返回目标函数系数、系数矩阵和常数项
# 示例使用
#很奇怪用min_juzheng会出现无解的情况ax
coefficients = get_juzheng()
c, A_eq, b_eq = max_juzheng(coefficients)
solution, optimal_value = simplex_method(c, A_eq, b_eq)
if solution is not None and optimal_value is not None:
    print("Solution:", solution)
    print("Optimal value:", optimal_value)
else:
    # 修正字符串和括号问题
    print("未找到有效解。")
# 保留输入提示，使程序可以等待用户输入
input('输入任意键结束：')