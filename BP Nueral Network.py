# encoding: utf-8
import xlrd
import xlwt
import random
import math
import matplotlib.pyplot as plt


# 激活函数
def activate_func(hvalue):
    return 1.0 / (1.0 + math.exp(-1 * hvalue))


# 调整函数
def activate_derivative_func(ovalue):
    return ovalue * (1 - ovalue)


# 自动构造矩阵工具
def make_matrix(row_num, column_num, max=0.5, min=-0.5):
    matrix = []
    row = []
    for i in range(row_num):
        for j in range(column_num):
            row.append(random.uniform(min, max))
        matrix.append(row)
        row = []
    return matrix

class BP_Neural_Network:
    input_num = 0
    hidden_num = 0
    output_num = 0
    input_cells = []
    hidden_cells = []
    output_cells = []
    input_weight = []
    output_weight = []
    input_correlation = []
    output_correlation = []


    def initial(self, input_num, hidden_num, output_num):
        self.input_num = input_num
        self.hidden_num = hidden_num
        self.output_num = output_num
        # 初始化网络结点
        self.input_cells = [1.0] * (input_num + 1)
        self.hidden_cells = [1.0] * hidden_num
        self.output_cells = [1.0] * output_num
        # 初始化权重矩阵
        self.input_weight = make_matrix(input_num, hidden_num)
        self.output_weight = make_matrix(hidden_num, output_num)
        # 初始化矫正矩阵
        self.input_correlation = make_matrix(input_num, hidden_num, 0, 0)
        self.output_correlation = make_matrix(hidden_num, output_num, 0, 0)

    def feed_forward(self, input):
        # 输入输入层
        for i in range(0, self.input_num - 1):
            self.input_cells[i] = input[i]
        # 计算隐藏层
        for j in range(0, self.hidden_num):
            hidden_value = 0.0
            for i in range(0, self.input_num):
                hidden_value += self.input_cells[i] * self.input_weight[i][j]
            self.hidden_cells[j] = activate_func(hidden_value)
        # 计算输出层
        for k in range(0, self.output_num):
            output_value = 0.0
            for j in range(self.hidden_num):
                output_value += self.hidden_cells[j] * self.output_weight[j][k]
            self.output_cells[k] = activate_func(output_value)
        return self.output_cells

    def back_propagate(self, input_data, actual_output_data, learn_rate, correct_rate):
        # 计算feed forward
        self.feed_forward(input_data)
        # 计算输出层的误差
        output_delta = [0.0] * self.output_num
        for k in range(0, self.output_num):
            error = actual_output_data[k] - self.output_cells[k]
            output_delta[k] = activate_derivative_func(self.output_cells[k]) * error
        # 计算隐藏层误差
        hidden_delta = [0.0] * self.hidden_num
        for j in range(0, self.hidden_num):
            error = 0.0
            for k in range(0, self.output_num):
                error += output_delta[k] * self.output_weight[j][k]
            hidden_delta[j] = activate_derivative_func(self.hidden_cells[j]) * error
        # 调整输出权重
        for j in range(0, self.hidden_num):
            for k in range(0, self.output_num):
                change = output_delta[k] * self.hidden_cells[j]
                self.output_weight[j][k] += learn_rate * change + correct_rate * self.output_correlation[j][k]
                self.output_correlation[j][k] = change
        # 调整隐藏层权重
        for i in range(0, self.input_num):
            for j in range(0, self.hidden_num):
                change = hidden_delta[j] * self.input_cells[i]
                self.input_weight[i][j] += learn_rate * change + correct_rate * self.input_correlation[i][j]
                self.input_correlation[i][j] = change
        # 计算OLS
        error = 0.0
        for t in range(0, self.output_num):
            error += 0.5 * (actual_output_data[t] - self.output_cells[t]) ** 2
        return error

    def BP_Neural_Network_Train(self, input_datas, output_datas, limit=100, learn_rate=0.05, correct_rate=0.1):
        errors = []
        for i in range(limit):
            error = 0.0
            for i in range(len(input_datas)):
                input_data = input_datas[i]
                output_data = output_datas[i]
                error += self.back_propagate(input_data, output_data, learn_rate, correct_rate)
                print "隐藏层权重:"
                print self.input_weight
                print "输出层权重:"
                print self.output_weight
            errors.append(error)
        plt.plot(errors)
        plt.show()
        for i in range(len(input_datas)):
            input_data = input_datas[i]
            self.feed_forward(input_data)

    def BP_Neural_Network_Test(self):
        data = xlrd.open_workbook(u'data5.xlsx')
        re = xlwt.Workbook()
        sheet1 = re.add_sheet('result',cell_overwrite_ok=True)
        sheet = data.sheet_by_index(0)
        level = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row_values(row_num,1)
            result = self.feed_forward(row)
            for p in range(6):
                sheet1.write(row_num, 10+p, (str)(result[p]))
        re.save(u'data7.xlsx')


if __name__ == '__main__':
    class_type = [1, 2, 3, 4, 5, 6]
    bp = BP_Neural_Network()
    bp.initial(6,12,6)
    cases = []
    labels = []
    for x in range(100):
        ttype = random.randint(1, 6)
        if ttype == 1:
            cases.append(
                [random.uniform(7.5, 10), random.uniform(0.0, 0.15), random.uniform(0, 0.02), random.uniform(0, 0.2),
                 random.uniform(0, 2), random.uniform(0, 3)])
            labels.append([0, 0, 0, 0, 0, 1])

        if ttype == 2:
            cases.append(
                [random.uniform(6, 7.5), random.uniform(0.15, 0.5), random.uniform(0.02, 0.1), random.uniform(0.2, 0.5),
                 random.uniform(2, 4), random.uniform(0, 3)])
            labels.append([0, 0, 0, 0, 1, 0])
        if ttype == 3:
            cases.append(
                [random.uniform(5, 6), random.uniform(0.5, 1), random.uniform(0.1, 0.2), random.uniform(0.5, 1),
                 random.uniform(4, 6), random.uniform(3, 4)])
            labels.append([0, 0, 0, 1, 0, 0])
        if ttype == 4:
            cases.append(
                [random.uniform(3, 5), random.uniform(1, 1.5), random.uniform(0.2, 0.3), random.uniform(1, 1.5),
                 random.uniform(6, 10), random.uniform(4, 6)])
            labels.append([0, 0, 1, 0, 0, 0])
        if ttype == 5:
            cases.append(
                [random.uniform(2, 3), random.uniform(1.5, 2), random.uniform(0.3, 0.4), random.uniform(1.5, 2),
                 random.uniform(10, 15), random.uniform(6, 10)])
            labels.append([0, 1, 0, 0, 0, 0])
        if ttype == 6:
            cases.append(
                [random.uniform(0, 2), random.uniform(2, 5), random.uniform(0.4, 1), random.uniform(2, 5),
                 random.uniform(15, 20), random.uniform(10, 15)])
            labels.append([1, 0, 0, 0, 0, 0])
    bp.BP_Neural_Network_Train(cases, labels)
    bp.BP_Neural_Network_Test()




