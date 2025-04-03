# Simplex-Method-Python-Implementation-Educational-Version-
due to the spicy 1.14.1 can't support the simplex way so i got this by ai to show the detalis 
md spicy（python库） 更新了 simplex不能用了但其他的都基本用内点法来计算但有些教学要求上（作业）会有单纯形法的过程要求，这个可以帮你们实现输出单纯形法的lp问题的过程和答案


操作要求：
1先转换成表格形式
（算了我给你们搞个例子）
题目：
min z = -x2+2x3
#s.t. x1-2x2+x3 = 2
      x2-3x3+x4 = 1
      x2-x3+x5  =2
x12345 >= 0 
#所以我们可以化为
z：
0 ，-1，2，0，0 
第一行：
1，-2，1，0，0
系数是2（等式又段的）
第二行：
0，1，-3，1，0
系数是1
第3行：
0，1，-1，0，1
系数是2
代码中约束条件的数量就是等式的个数
就如例子是3个

