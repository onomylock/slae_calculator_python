class ListExtensions:
    @staticmethod
    def swap(lst, i, j):
        lst[i], lst[j] = lst[j], lst[i]

    @staticmethod
    def get_min_index(lst):
        tmp = [abs(x) for x in lst]
        min_index = min((item, index) for index, item in enumerate(tmp) if item != 0)[1]
        return min_index

    @staticmethod
    def get_last_non_zero_element_index(lst, ind):
        return lst.index(next(x for x in reversed(lst) if x != 0 and lst.index(x) != ind))

    @staticmethod
    def last_index_of_non_zero_element(lst):
        return lst.index(next(x for x in reversed(lst) if x != 0))

    @staticmethod
    def get_mask_elements(lst):
        return [x != 0 for x in lst]


class SolverSLAE:
    def __init__(self):
        self.A = []
        self.C = []
        self.B = []
        self.count_no_zero_elements = []
        self.N = 0
        self.M = 0

    def read_input(self):
        print("Set N, M")
        parameters = list(map(int, input().strip().split()))
        self.M = parameters[0]
        self.N = parameters[1]
        print("set elements")
        for _ in range(self.M):
            param = list(map(int, input().strip().split()))
            if len(param) != self.N + 1:
                raise Exception("Not valid parameters count")
            self.A.append(param[:-1])
            self.C.append(-param[-1])

    def generate_matrix_b(self):
        self.B = self.A.copy()
        for line in self.B:
            line.append(self.C[self.B.index(line)])
        for i in range(self.N):
            line = [0] * (self.N + 1)
            line[i] = 1
            self.B.append(line)

    def solve(self):
        K = 0
        res = []
        for k in range(self.M):
            self.count_no_zero_elements.append(sum(1 for x in self.B[k][:-1] if x != 0))
        for i in range(self.M):
            while self.count_no_zero_elements[i] > i + 1:
                min_index = ListExtensions.get_min_index(self.B[i])
                val_index = ListExtensions.get_last_non_zero_element_index(self.B[i][:-1], min_index)
                if min_index < 0:
                    raise Exception("NO SOLUTION")
                self.operation_sub(i, val_index, min_index)
            self.column_swapper(i)
        for i in range(self.M):
            min_index = ListExtensions.get_min_index(self.B[i][:-1])
            self.operation_sub(i, len(self.B[i]) - 1, min_index)
            if self.B[i][-1] != 0:
                raise Exception("NO SOLUTION")
        for i in range(self.M):
            # ind = self.B[i].index(ListExtensions.get_last_non_zero_element_index(self.B[i], len(self.B[i])))
            ind = ListExtensions.get_last_non_zero_element_index(self.B[i], len(self.B[i]))
            if ind > K:
                K = ind
        K = self.N - K - 1
        for i in range(self.N):
            res.append([])
            for j in range(self.N - K, len(self.B[i])):
                res[i].append(self.B[self.M + i][j])
        return K, res

    def line_swapper(self):
        for i in range(1, len(self.count_no_zero_elements)):
            for j in range(len(self.count_no_zero_elements) - i):
                if self.count_no_zero_elements[j] > self.count_no_zero_elements[j + 1]:
                    ListExtensions.swap(self.count_no_zero_elements, i, j)
                    ListExtensions.swap(self.B, i, j)

    def operation_sub(self, line_index, val_index, min_index):
        if val_index != -1 and min_index != -1:
            r = self.B[line_index][val_index] % self.B[line_index][min_index]
            q = (self.B[line_index][val_index] - r) // self.B[line_index][min_index]
            for j in range(len(self.B)):
                if self.B[j][val_index] == 0 and q * self.B[j][min_index] != 0 and j < self.M:
                    self.count_no_zero_elements[j] += 1
                elif self.B[j][val_index] != 0 and self.B[j][val_index] - q * self.B[j][min_index] == 0 and val_index != len(self.B[j]) - 1:
                    self.count_no_zero_elements[j] -= 1
                self.B[j][val_index] -= q * self.B[j][min_index]

    def column_swapper(self, index):
        flags = ListExtensions.get_mask_elements(self.B[index][:self.N])
        for i in range(len(flags)):
            if flags[i] and False in flags[:i] and i != index:
                swap_index = flags.index(False)
                ListExtensions.swap(flags, i, swap_index)
                for j in range(len(self.B)):
                    ListExtensions.swap(self.B[j], i, swap_index)


