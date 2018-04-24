# prepare data especially the dictionary
import logging
import argparse
import numpy as np
import pdb
import sys

logger = logging.getLogger(__name__)

class GetMaskMatrix(object):

    def __init__(self, dep_file, out_name):
        self.dep_file = dep_file
        self.out_name = out_name
        self.get_n_mask_file()

    def matrix_to_string(self, matrix):
        str_ = ""
        length = matrix.shape[0]
        for step in range(length):
            for step_y in range(length):
                str_ += str(matrix[step][step_y]) + " "
        return str_

    def to_tuple(self, dep_split):
        tuple_list = []
        for step in range(len(dep_split)):
            tuple_step = dep_split[step].strip().split('-')
            child = int(tuple_step[0])
            parent = int(tuple_step[1])
            tuple_ = (child, parent)
            tuple_list.append(tuple_)
        return tuple_list

    def get_matrix(self, dep_line):
        dep_split = dep_line.strip().split()
        matrix = np.eye(len(dep_split)+1)
        dep_tuple = self.to_tuple(dep_split)
        for step in range(len(dep_split)):
            parent = dep_tuple[step][0] -1
            if parent !=-1:
                matrix[step][parent] = 1
            for step_child in range(len(dep_split)):
                par = dep_tuple[step_child][0]
                chi = dep_tuple[step_child][1]
                if par-1 == step:
                    matrix[step][chi-1] = 1
        matrix_str = self.matrix_to_string(matrix)
        return matrix_str

    def is_full(self, matrix):
        #判断matrix除对角线以外是否存在0,对称矩阵，判断上三角或者下三角矩阵是否有0 即可
        for i in range(matrix.shape[0]):
            for j in range(i+1, matrix.shape[1]):
                if matrix[i][j] == 0:
                    return False
        return True

    def fill_matrix(self, matrix):
        if self.is_full(matrix):
            return matrix
        else:
            for i in range(matrix.shape[0]) :
                for j in range(i+1, matrix.shape[1]):
                    if matrix[i][j] ==0 :
                        min_ij = float("inf")
                        for a in range(matrix.shape[0]):
                            # matrix[i][j] = matrix[j][a] + matrix[i][a]
                            # matrix[j][i] = matrix[j][a] + matrix[i][a]
                            # break
                            if matrix[j][a] != 0 and matrix[i][a] !=0 :
                                min_ij = matrix[i][a] + matrix[j][a]  if matrix[i][a] + matrix[j][a] < min_ij else min_ij
                        if min_ij < float("inf"):
                            matrix[i][j] = min_ij
                            matrix[j][i] = min_ij

            return self.fill_matrix(matrix)

    def get_n_matrix(self, dep_line):
        dep_split = dep_line.strip().split()
        matrix = np.zeros((len(dep_split), len(dep_split)))
        dep_tuple = self.to_tuple(dep_split)
        #矩阵初始化
        for step in range(len(dep_split)):
            parent = dep_tuple[step][0] -1
            child = dep_tuple[step][1] -1
            if parent ==-1:
                continue
            else:
                matrix[parent][child] = 1
                matrix[child][parent] = 1
        #填表
        matrix_str = self.matrix_to_string(self.fill_matrix(matrix))
        return matrix_str

    def get_mask_file(self):
        dep_stream = open(self.dep_file, "r")
        dep_lines = dep_stream.readlines()
        dep_stream.close()

        out_stream = open(self.out_name, "w")
        dep_len = len(dep_lines)
        for step in range(dep_len):
            dep_line = dep_lines[step]
            matrix_line = self.get_matrix(dep_line)
            print("parsed "+ str(step+1) + " lines")
            out_stream.write(matrix_line+ "\n")
        out_stream.close()

    def get_n_mask_file(self):
        dep_stream = open(self.dep_file, "r")
        dep_lines = dep_stream.readlines()
        dep_stream.close()

        out_stream = open(self.out_name, "w")
        dep_len = len(dep_lines)
        for step in range(dep_len):
            dep_line = dep_lines[step]
            matrix_line = self.get_n_matrix(dep_line)
            print("parsed "+ str(step+1) + " lines")
            out_stream.write(matrix_line+ "\n")
        out_stream.close()



if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('dep_file', type=str)
    # parser.add_argument('out_name', type=str)
    # args = parser.parse_args()
    # GetMaskMatrix(dep_file=args.dep_file, out_name=args.out_name)
    # GetMaskMatrix(dep_file=args.dep_file, out_name=args.out_name)
    GetMaskMatrix(dep_file='ch.txt.dep', out_name='ch.txt.dep.mask.txt')
    # GetMaskMatrix(dep_file='test.txt', out_name='test.mask.txt')
