import numpy as np
from fractions import Fraction


# 判断是否满足B所对应的z是否为零（是否满足第一张单纯形表）
def check_zb(row_zlist: list, b_ylist: list):
    """
    row_zlist: z行的值 就是最初始单纯形表的第零行的值 也是目标函数的系数*-1(或者是max类的目标函数的系数)
    b_ylist: 存储了初始的可行基B的列的值如单纯形表的第1行第零个就是z[1][0] 假设这个就是可行基那在B_list里存的就是[0]
    check_zblist:存储了对应情况(如果是对应的为0的话就记为true否则false) check_list=[True,False ...]
    zb = [0,3,4]
    print(czb([1,1,1,1,1,1,1],zb))
    [False, True, True, False, False, True, True]
    """
    cc = len(row_zlist)
    check_zblist = [True for i in range(cc)]
    # print(f'b_ylist{b_ylist}')
    for i in b_ylist:
        if row_zlist[i] != 0:
            check_zblist[i] = False
        else:
            check_zblist[i] = True
    return check_zblist


# 判断是否满足最优解条件or无解条件

def check_za(row_zlist: list, z: list) -> int:
    """
    :param row_zlist: 当前的第零行的值
    :param z: 当前的包含第零行的整个的系数矩阵z=[row_zlist,list1,list2]
    :return:  check_zanum (0 1 2 0:满足最优解，1不满足最优解，2无界)
    """
    c = 0
    tempc = []
    tempb = []
    ans = 0
    for i in row_zlist:
        if i > 0:
            tempc.append(c)
        c += 1
    if len(tempc) == 0:
        ans = 0
    else:
        for a in tempc:  # 确定哪一列
            for i in z:  # 取每一行
                if i[a] > 0:
                    tempb.append(i)  # 第几行是正的放在tempb里
            if len(tempb) == 1:
                ans = 2  # 存在一列全是小于等于0的
                break
            else:
                tempb = []  # 重置判断
        if ans != 2:  # 就是之前没出现过一列全为负的情况
            ans = 1
    return ans



# 找到互换的元的下标x下标从0开始
def seek_change(row_zlist: list, z: list):
    """
    :param row_zlist: 当前的第零行的值
    :param z: 当前的包含第零行的整个的系数矩阵z=[row_zlist,list1,list2]
    :return:  check_zclist = [a,b] xa是单纯形表左边的xa xb是要换上去的xb
    """
    check_zclist = [0, 0]
    # 先找到最大的正系数对应的列
    max_index = 0
    for i in range(len(row_zlist)):
        if row_zlist[i] > row_zlist[max_index]:
            max_index = i
    check_zclist[1] = max_index

    ratios = []
    for i in range(1, len(z)):  # 跳过第零行
        if z[i][max_index] > 0:
            ratios.append((z[i][-1] / z[i][max_index], i))

    if not ratios:
        # 处理无界情况
        raise ValueError("问题无界，找不到合适的换出变量")

    min_ratio_index = min(range(len(ratios)), key=lambda x: ratios[x][0])
    check_zclist[0] = ratios[min_ratio_index][1]

    return check_zclist


# 我要设置一个函数用来找到单位矩阵
def find_dan(z: list, c1=1):
    """


    :param z:   z=[[0,0,0],
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0]]
    :return:   ['X1', 'X5', 'X3', 'X4', 'X2']
    """
    nz = z[1::]  # 去掉第零行
    haha = np.array(nz)
    # print(haha)#矩阵转置前的结果
    haha1 = np.transpose(haha)
    # print(haha1)#矩阵转置后的结果
    # print(haha1[0])
    c = 0
    ans_list = []
    nun = 1
    e = 0
    d = [0 for i in range(len(nz))]  # 存储列的下标
    for a in haha1:
        # print(a)
        for i in range(len(a)):
            c += a[i]
            if a[i] != 0:
                e = i
                # print(f'e{e}')
        if c == max(a):
            # print(c)
            d[e] = nun  # d中第e个就是x（nun）
        nun += 1
        c = 0
    for i in range(len(d)):
        # print(d)
        if d[i] != 0:
            if c1 == 1:
                ans_list.append(f'X{d[i]}')
            else:
                ans_list.append(d[i] - 1)
    return ans_list



def hangchange(z, position, return_as_fractions=False):
    """
    :param z: 当前的包含第零行的整个的系数矩阵z[rowzlist,list1,list2]
    :param position: 要改变的位置按z[0][0]为起始点（包含基础的系数行）
    :param return_as_fractions: 如果为True，则返回分数形式的矩阵，否则返回浮点数形式的矩阵
    :return: newz [[],[],[],[]....]
    """
    # 将矩阵的每个元素转换为Fraction对象
    zn = np.array([[Fraction(x) for x in row] for row in z])
    dd = zn[position[0], position[1]]
    beishu = Fraction(1, dd)
    zn[position[0]] *= beishu  # 将指定行乘以倍数

    for i in range(len(zn)):
        if i != position[0]:
            beishu1 = zn[i, position[1]] / dd * (-1)
            zn[i] += beishu1 * zn[position[0]]  # 调整其他行

    if return_as_fractions:
        return zn
    else:
        # 将Fraction矩阵转换回浮点数形式
        newz = [[float(x) for x in row] for row in zn]
        return newz


# 示例矩阵和位置

# 调用函数


def start(z=[], dt=1,cc=False,CN = 1):#CN=0后面不在对是否使用分式计算提问
    if len(z) == 0 :
        lenz = int(input('请输入单纯形表一共有多少行：'))
        for i in range(lenz):
            zi = input(f'第{i}行数值；').split(',')
            int_zi = list(map(int, zi))
            z.append(int_zi)
    if cc != True or CN == 1:
        cc = input('是否开启分式计算？输入（y/n）')
        CN = input('是否保持上述提问？输入（y/n）')
        if cc == 'y':
            cc = True
        else:
            cc = False
        if CN == 'y':
            CN = 1
        else:
            CN = 0
    print(f'第{dt}次')
    x_list = find_dan(z)
    print(f"x-list{x_list}")
    zb = find_dan(z, c1=0)
    # print(f'zb{zb}')
    print(f'z{dt}')
    print(z)
    yn = check_zb(z[0], zb)
    for i in range(len(yn)):
        if not yn[i]:
            z = np.array(z, dtype=float)
            z[0] -= z[zb[i]]
            print("处理初始单纯形表条件后的行列式:")
            print(z)

    if isinstance(z, list):
        z = np.array(z)
    if check_za(z[0].tolist(), z.tolist()) == 0:
        print(f'最优值是{z[0][-1]}')
        print(f'最优解是：{x_list}')
        print(z[1:, -1])
        return 0
    elif check_za(z[0].tolist(), z.tolist()) == 2:
        print('无界')
        return 0
    else:
        change_xl = seek_change(z[0].tolist(), z.tolist())
        print(change_xl)
        a = change_xl[0] - 1
        if 0 <= a < len(x_list):
            x_list[a] = f'X{change_xl[1] + 1}'
        else:
            print(f"警告：索引 {a} 超出 x_list 范围，跳过基变量更新。")
        # print(f'x_list\n{x_list}')

        z = hangchange(z, change_xl,return_as_fractions=cc)
        print("行变换操作后的行列式:")
        print(z)
        dt += 1
        start(z, dt,cc,CN)


# 调用start函数
start(dt=1)