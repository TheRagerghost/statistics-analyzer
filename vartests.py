from scipy.stats import rankdata, fisher_exact

class RosenbaumQ:
    name = "rosenbaum"
    f_seq: list[float] | list[int]
    s_seq: list[float] | list[int]

    def __init__(self, first: list[float] | list[int], second: list[float] | list[int]) -> None:
        self.f_seq = first
        self.s_seq = second

    def __str__(self) -> str:
        return f"=== Q Критерий Розенбаума ===\n\n{self.f_seq}\n{self.s_seq}\n\n{self.solve()}\n"

    def solve(self) -> str:

        if len(self.f_seq) < 11 or len(self.s_seq) < 11:
            return "В выборках не хватает значений."

        a_ranged = sorted(self.f_seq)
        b_ranged = sorted(self.s_seq)

        a_min = a_ranged.pop(0)
        b_max = b_ranged.pop()

        s1 = len([a for a in a_ranged if a > b_max])
        s2 = len([b for b in b_ranged if b < a_min])

        a_len = len(a_ranged)
        b_len = len(b_ranged)

        if (s1 + s2) >= self.getTableNumber(a_len, b_len):
            return f"Так как Qэмп {s1 + s2} ≥ Qкр {self.getTableNumber(a_len, b_len)} -> H1: Результаты первой группы превосходят результаты второй группы по уровню измеренного признака"
        else:
            return f"Так как {s1 + s2} < {self.getTableNumber(a_len, b_len)} -> H0: Результаты первой группы НЕ превосходят результаты второй группы по уровню измеренного признака"
    
    'p = 0.05'
    def getTableNumber(self, a: int, b: int) -> int:

        if a > 26 or b > 26: return 8

        table = [[6],
                 [6, 6],
                 [6, 6, 6],
                 [7, 7, 6, 6],
                 [7, 7, 6, 6, 6],
                 [8, 7, 7, 7, 6, 6],
                 [7, 7, 7, 7, 7, 7, 7],
                 [7, 7, 7, 7, 7, 7, 7, 7],
                 [7, 7, 7, 7, 7, 7, 7, 7, 7],
                 [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                 [8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                 [8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                 [8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7]]
        
        aa = a - 11 if a >= b else b - 11
        bb = b - 11 if a >= b else a - 11

        return table[aa][bb]

class SignG:
    x_seq: list[float] | list[int]
    y_seq: list[float] | list[int]

    def __init__(self, first: list[float] | list[int], second: list[float] | list[int]) -> None:
        self.x_seq = first
        self.y_seq = second

    def __str__(self) -> str:
        return f"=== G Критерий знаков ===\n\nX: {self.x_seq}\nY: {self.y_seq}\n\n{self.solve()}\n"
    
    def solve(self) -> str:
        if len(self.x_seq) < 5 or len(self.y_seq) < 5:
            return "В выборках не хватает значений."
        
        signlist = [("+" if y > x else "-") for x,y in zip(self.x_seq, self.y_seq) if x != y]
        #print(f"Символы: {signlist}")

        plus = signlist.count("+")
        minus = signlist.count("-")

        g = self.getTableNumber(len(signlist))

        if min(plus, minus) <= g:
            return f"Так как Gэмп ({min(plus, minus)}) ≤ Gкр ({g}) -> H1: Сдвиг в типичную сторону может считаться достоверным."
        else:
            return f"Так как Gэмп ({min(plus, minus)}) > Gкр ({g}) -> H0: Сдвиг в типичную сторону НЕ может считаться достоверным."
    
    'p = 0.05'
    def getTableNumber(self, a: int) -> int:

        if a > 100: return 45

        table = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 16, 17, 17, 18, 18, 19, 20, 21, 22, 23, 24, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 33, 34, 35, 36, 37, 38, 39, 40, 41]

        return table[a - 5]
    
class MannWhitneyU:
    x_seq: list[float] | list[int]
    y_seq: list[float] | list[int]

    def __init__(self, first: list[float] | list[int], second: list[float] | list[int]) -> None:
        self.x_seq = first
        self.y_seq = second

    def __str__(self) -> str:
        return f"=== U Критерий Манна-Уитни ===\n\nX: {self.x_seq}\nY: {self.y_seq}\n\n{self.solve()}\n"
    
    def solve(self) -> str:
        if len(self.x_seq) < 4 or len(self.y_seq) < 4:
            return "В выборках не хватает значений."
        elif len(self.x_seq) > 20 or len(self.y_seq) > 20:
            return "Количество значений в одной из выборок превосходит 20. Сократите ее."
        
        marked_list = [(x, "x") for x in self.x_seq] + [(y, "y") for y in self.y_seq]
        marked_list.sort()
        ranked_list = [(x, y[1]) for x,y in zip(rankdata([x[0] for x in marked_list], axis=0), marked_list)]

        xranks = [x[0] for x in ranked_list if x[1] == "x"]
        yranks = [y[0] for y in ranked_list if y[1] == "y"]

        xrsum = sum(xranks)
        yrsum = sum(yranks)
        #print (f"\nX: {xranks} = {xrsum}\nY: {yranks} = {yrsum}")

        u = len(self.x_seq) * len(self.y_seq) + len(self.x_seq) * (len(self.x_seq) + 1) / 2 - xrsum if xrsum >= yrsum else len(self.x_seq) * len(self.y_seq) + len(self.y_seq) * (len(self.y_seq) + 1) / 2 - yrsum

        #print(f"\n{u}")
        u2 = self.getTableNumber(len(self.x_seq), len(self.y_seq))

        if u < u2:
            return f"Так как Uэмп ({u}) < Uкр ({u2}) -> H1: Результат отражает эффективность."
        else:
            return f"Так как Uэмп ({u}) ≥ Uкр ({u2}) -> H0: Результат отражает НЕэффективность."
        
    'p = 0.05'
    def getTableNumber(self, a: int, b: int) -> int:

        table = [[ 0,  1,  2,  3,  4,  4,  5,  6,  7,  8,  9, 10, 11,  11,  12,  13,  14],
                 [ 1,  2,  3,  5,  6,  7,  8,  9, 11, 12, 13, 14, 15,  17,  18,  19,  20],
                 [ 2,  3,  5,  6,  8, 10, 11, 13, 14, 16, 17, 19, 21,  22,  24,  25,  27],
                 [ 3,  5,  6,  8, 10, 12, 14, 16, 18, 20, 22, 24, 26,  28,  30,  32,  34],
                 [ 4,  6,  8, 10, 13, 15, 17, 19, 22, 24, 26, 29, 31,  34,  36,  38,  41],
                 [ 4,  7, 10, 12, 15, 17, 20, 23, 26, 28, 31, 34, 37,  39,  42,  45,  48],
                 [ 5,  8, 11, 14, 17, 20, 23, 26, 29, 33, 36, 39, 42,  45,  48,  52,  55],
                 [ 6,  9, 13, 16, 19, 23, 26, 30, 33, 37, 40, 44, 47,  51,  55,  58,  62],
                 [ 7, 11, 14, 18, 22, 26, 29, 33, 37, 41, 45, 49, 53,  57,  61,  65,  69],
                 [ 8, 12, 16, 20, 24, 28, 33, 37, 41, 45, 50, 54, 59,  63,  67,  72,  76],
                 [ 9, 13, 17, 22, 26, 31, 36, 40, 45, 50, 55, 59, 64,  69,  74,  78,  83],
                 [10, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 70,  75,  80,  85,  90],
                 [11, 15, 21, 26, 31, 37, 42, 47, 53, 59, 64, 70, 75,  81,  86,  92,  98],
                 [11, 17, 22, 28, 34, 39, 45, 51, 57, 63, 69, 75, 81,  87,  93,  99, 105],
                 [12, 18, 24, 30, 36, 42, 48, 55, 61, 67, 74, 80, 86,  93,  99, 106, 112],
                 [13, 19, 25, 32, 38, 45, 52, 58, 65, 72, 78, 85, 92,  99, 106, 113, 119],
                 [14, 20, 27, 34, 41, 48, 55, 62, 69, 76, 83, 90, 98, 105, 112, 119, 127]]

        return table[a - 4][b - 4]
    
class WilcoxonU:
    x_seq: list[float] | list[int]
    y_seq: list[float] | list[int]
    xydiffs: list[float] | list[int]
    xydranks: list[float]

    def __init__(self, first: list[float] | list[int], second: list[float] | list[int]) -> None:
        self.x_seq = first
        self.y_seq = second
        self.xydiffs = []
        self.xydranks = []

    def __str__(self) -> str:
        out = self.solve()
        return f"=== T Критерий Вилкоксона ===\n\nX: {self.x_seq}\nY: {self.y_seq}\nY-X: {self.xydiffs}\nRi: {self.xydranks}\n\n{out}\n"
    
    def solve(self) -> str:
        if len(self.x_seq) < 6 or len(self.y_seq) < 6:
            return "В выборках не хватает значений."
        elif len(self.x_seq) > 50 or len(self.y_seq) > 50:
            return "Количество значений в одной из выборок превосходит 20. Сократите ее."
        
        self.xydiffs = [y - x for x,y in zip(self.x_seq, self.y_seq) if x != y]
        xydiffs = sorted(self.xydiffs, key=abs)
        xydtemp = [abs(x) for x in xydiffs]
        self.xydranks = rankdata([abs(x) for x in self.xydiffs])
        xydranks = rankdata(xydtemp)

        idxplus = [i for i in range(len(xydiffs)) if xydiffs[i] >= 0]
        idxminus = [i for i in range(len(xydiffs)) if xydiffs[i] < 0]
        smalleridx = idxplus if len(idxplus) < len(idxminus) else idxminus

        t = sum([xydranks[i] for i in smalleridx])
        t2 = self.getTableNumber(len(xydiffs))
        
        if t < t2:
            return f"Так как Tэмп ({t}) < Tкр ({t2}) -> H1: Интенсивность положительного сдвига результатов тестирования превышает интенсивность отрицательного сдвига. Результаты улучшились."
        else:
            return f"Так как Tэмп ({t}) ≥ Tкр ({t2}) -> H0: Интенсивность положительного сдвига результатов тестирования НЕ превышает интенсивность отрицательного сдвига."
        
    'p = 0.05'
    def getTableNumber(self, a: int) -> int:

        table = [0, 2, 3, 5, 8, 10, 13, 17, 21, 25, 29, 34, 40, 46, 52, 58, 65, 73, 81, 89, 98, 107, 116, 126, 137, 147, 159, 170, 182, 195, 208, 221, 235, 249, 264, 279, 294, 310, 327, 343, 361, 378, 396, 415, 434]

        return table[a - 6]
    
# НЕ ДОДЕЛАНО
class FisherF:
    x_seq: list[float] | list[int]
    y_seq: list[float] | list[int]

    def __init__(self, first: list[float] | list[int], second: list[float] | list[int]) -> None:
        self.x_seq = first
        self.y_seq = second

    def __str__(self) -> str:
        return f"\n=== Ф Критерий Фишера ===\nX: {self.x_seq}\nY: {self.y_seq}\n{self.solve()}\n"
    
    def solve(self) -> str:
        if len(self.x_seq) != 2 or len(self.y_seq) != 2:
            return "Нужен блок 2х2 данных."
        
        res = fisher_exact([self.x_seq, self.y_seq], alternative="less")
        print(res.statistic)
        print(res.pvalue)
        
    