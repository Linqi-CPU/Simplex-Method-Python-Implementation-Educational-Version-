# Simplex-Method-Python-Implementation-Educational-Version

由于spicy 1.15.2版本不支持单纯形法，所以我通过AI来展示详细内容。spicy（Python库）更新后，单纯形法不能用了，但其他的优化问题基本上都使用内点法来计算。然而，有些教学要求（如作业）需要展示单纯形法的过程，这个实现可以帮助你们输出单纯形法解决线性规划问题的过程和答案。

## 操作要求：

1. 首先转换成表格形式
   下面我将给出一个例子。

### 题目：

最小化 z = -x2 + 2x3

约束条件：
- x1 - 2x2 + x3 = 2
- x2 - 3x3 + x4 = 1
- x2 - x3 + x5 = 2

且 x1, x2, x3, x4, x5 >= 0

### 转换成表格形式：
注意z的系数要乘-1

| z    | -1 | 2 | 0 | 0 | 0 |
|------|----|---|---|---|---|
| x1   | 1  | -2| 1 | 0 | 0 |  2 |
| x2   | 0  | 1 | -3| 1 | 0 |  1 |
| x3   | 0  | 1 | -1| 0 | 1 |  2 |

其中，代码中约束条件的数量就是等式的个数，如例子中有3个。

请注意，上述表格中的"z"行代表目标函数的系数，而下面的行代表每个约束条件的系数，等号右边的数字是约束条件的右侧值。
下面是该例子的实操图

![新建 BMP 图像](https://github.com/user-attachments/assets/3a32e23c-b6e3-4694-b0e5-54a1bacf69d7)

