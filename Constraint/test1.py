from z3 import *

# 创建一个解析器
s = Solver()

# 声明变量
x = Int('x')
y = Int('y')

# 添加约束
s.add(x > 0, y > 0, x * y > 100)

# 查找模型
print(s.check())

s.minimize(x + y)  # 最小化 x + y

# 获取模型
m = s.model()
print(m[x], m[y])