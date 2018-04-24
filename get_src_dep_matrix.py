# prepare data especially the dictionary
import logging
import argparse
import numpy as np
import pdb

logger = logging.getLogger(__name__)

class GetMaskMatrix(object):

    def __init__(self, dep_file, out_name):
        self.dep_file = dep_file
        self.out_name = out_name
        self.get_mask_file()

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


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('dep_file', type=str)
    # parser.add_argument('out_name', type=str)
    # args = parser.parse_args()
    #GetMaskMatrix(dep_file=args.dep_file, out_name=args.out_name)
    GetMaskMatrix(dep_file='ch.txt.dep', out_name='ch.txt.dep.mask')

