# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:15:05 2020

@author: cm
"""



# 1. sigmoid
# 函数：f(z) = 1 / (1 + exp( − z))
# 导数：f(z)' = f(z)(1 − f(z))

# 2. tanh
# 函数：f(z) = tanh(z)
# 导数：f(z)' = 1 − (f(z))**2

# 3. multiply
# multiply:点乘

# 4. 目标优化函数求导 f(x) = 1/2*multiply(yp-y,yp-y)
# f'(x)= -(yp-y)*y' = -err*delta
  其中(yp-y) = err，y'= delta :y的梯度

