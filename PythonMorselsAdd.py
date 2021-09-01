# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 16:04:17 2021

@author: catal
"""
import pdb

# def add(matrix1, matrix2):
#     """assumes matrix1 and matrix2 are lists of lists of numbers of the same lenghts
#     returns a list of lists of numbers of the same lenghts as the input, 
#     the sum of the respective elements of matrix1 and matrix2
#     """
#     #innitialize return matrix
#     matrix3 = [[0 for val in submatrix] for submatrix in matrix1]
#     #iterate over outer list
#     for i in range(len(matrix1)):
#         #iterate over inner list
#         for j in range(len(matrix1[i])):
#             matrix3[i][j] = matrix1[i][j] + matrix2[i][j]
#     return matrix3

def add(*args):
    """assumes matrix1 and matrix2 are lists of lists of numbers of the same lenghts
    returns a list of lists of numbers of the same lenghts as the input, 
    the sum of the respective elements of matrix1 and matrix2
    """
    #check that inputs are the same lenght
    for arg in args:
        #check if outer lists same lenght
        if len(arg) != len(args[0]):
            raise ValueError("Given matrices are not the same size.")
        #check if inner lists same lenght
        for i in range(len(arg)):
            if len(arg[0]) != len(arg[i]):
                raise ValueError("Given matrices are not the same size.")
    #innitialize return matrix
    add_matrix = [[0 for val in submatrix] for submatrix in args[0]]
    #iterate over outer list
    for i in range(len(args[0])):
        #iterate over inner list
        for j in range(len(args[0][i])):
            #take sum of args
            for arg in args:
                add_matrix[i][j] += arg[i][j]
    return add_matrix

# matrix1 = [[1, -2], [-3, 4]]
# matrix2 = [[2, -1], [0, -1]]
# print(add(matrix1, matrix2))
# print(add(matrix1, matrix2) == [[3, -3], [-3, 3]])

# matrix3 = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
# matrix4 = [[1, 1, 0], [1, -2, 3], [-2, 2, -2]]
# print(add(matrix3,matrix4))
# print(add(matrix3, matrix4) == [[2, -1, 3], [-3, 3, -3], [5, -6, 7]])

# matrix5 = [[1, 9], [7, 3]]
# matrix6 = [[5, -4], [3, 3]]
# matrix7 = [[2, 3], [-3, 1]]
# matrix8 = [[2, 3], [-3, 1], [-5,4]]
# print(add(matrix5, matrix6, matrix8) == [[8, 8], [7, 7]])

# m1 = [[6, 6], [3, 1]]
# m3 = [[6, 6], [3, 1, 2]]
# print(add(m1, m3))