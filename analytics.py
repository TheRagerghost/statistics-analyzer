import math
import random
from utils import SplitType, round_full, round_half, show_as_percentage

class Univariate:
    values: list[float] | list[int]
    n_sorted: list[float] | list[int]
    split_data: tuple

    def __init__(self, n: list[float] | list[int]):
        self.values = n
        self.n_sorted = sorted(n)
        self.split_data = self.split_by_intervals()

    def __str__(self) -> str:
        strings = []
        strings.append(f"Выборка: {self.values}")
        strings.append(f"Ранжированная: {self.n_sorted}")
        strings.append(f"\n")

        strings.append(f"Состоит из {self.i_count()} интервалов размером {self.i_size()}.")
        strings.append(f"Границы интервалов: {self.get_intervals()}")
        strings.append(f"Значения по интервалам: {self.split_data[0]}")
        strings.append(f"Частота: {self.split_data[2]}")
        strings.append(f"Накопленная частота: {self.split_data[3]}")
        strings.append(f"Частость: {self.split_data[4]}")
        strings.append(f"Накопленная частость: {self.split_data[5]}")
        strings.append(f"Средние значения: {self.split_data[6]}")
        strings.append(f"\n")

        strings.append(f"Среднее арифметическое: {self.mean()}")
        mode, mint = self.mode()
        strings.append(f"Мода ({mint} интервал): {mode}")
        strings.append(f"Медиана: {self.median()}")
        strings.append(f"Размах вариации: {self.range()}")
        strings.append(f"Дисперсия: {self.variance()}")
        strings.append(f"Среднее квадратичное отклонение: {self.stdev()}")
        cv, scv = self.cov()
        strings.append(f"Коэффициент вариации ({scv}): {show_as_percentage(cv)}")
        strings.append(f"Стандартная ошибка ср. арифм.: {self.sem()}")
        skew, ness = self.skewness()
        strings.append(f"Мера скошенности ({ness}): {skew}")
        kurt, osis = self.kurtosis()
        strings.append(f"Эксцесс ({osis}): {kurt}")
        output = "\n".join(strings)
        return f"===\n\n{output}\n"
    
    def i_count(self):
        return round_full(1 + 3.2*math.log10(len(self.values)))
    
    def i_size(self, toInt = True):
        size = (self.n_sorted[-1] - self.n_sorted[0]) / self.i_count()
        return round_full(size) if toInt else round_half(size)
    
    def get_intervals(self):
        i_size = self.i_size()
        breakpoints = [self.n_sorted[0]]
        bp = self.n_sorted[0]
        while bp < self.n_sorted[-1]:
            bp += i_size
            breakpoints.append(bp)
        return [(breakpoints[i], breakpoints[i+1]) for i in range(len(breakpoints) - 1)]
    
    def split_by_intervals(self, type = SplitType.inclusive):
        intervals = self.get_intervals()
        result = [[] for _ in intervals]
        distribution = []
        distribution_cumulative = []
        frequency = []
        frequency_cumulative = []
        mean = []
        for n in self.n_sorted:
            for i, val in enumerate(intervals):
                if n > val[1] or n < val[0]:
                    continue
                elif n == val[0] and type == SplitType.inclusive and i > 0:
                    continue
                elif n == val[1] and type == SplitType.exclusive and i < len(intervals) - 1:
                    continue
                else:
                    result[i].append(n)

        for i, r in enumerate(result):
            distribution.append(len(r))
            frequency.append(len(r)/10)
            m = 0 if len(r) == 0 else round_full(sum(r)/len(r), 2)
            mean.append(m)
            if i > 0:
                distribution_cumulative.append(len(r) + distribution_cumulative[i-1])
                frequency_cumulative.append((len(r) + distribution_cumulative[i-1])/10)
            else:
                distribution_cumulative.append(len(r))
                frequency_cumulative.append(len(r)/10)
        
        return (result, intervals, distribution, distribution_cumulative, frequency, frequency_cumulative, mean)
    
    def mean(self, digits = 4):
        return round_full(sum(self.values)/len(self.values), digits)
    
    def mode(self, digits = 4):
        '''
        Returns mode and modal interval
        '''
        distribution = self.split_data[2]
        mval = max(distribution)
        moin = random.choice([i for i, d in enumerate(distribution) if d == mval])
        interval = self.split_data[0][moin]
        ein = interval[0]
        hin = round_full(interval[-1] - interval[0])
        vin = distribution[moin]
        pin = 0 if moin == 0 else distribution[moin-1]
        nin = 0 if moin == len(distribution)-1 else distribution[moin+1]
        vpvn = vin - pin + vin - nin
        div = 0 if vpvn == 0 else (vin - pin)/vpvn
        return (round_full(ein + hin * div, digits), moin + 1)
    
    def median(self):
        count = len(self.n_sorted)
        if count % 2 == 1:
            return self.n_sorted[count//2]
        else:
            return self.mean()
    
    def range(self):
        return self.n_sorted[-1] - self.n_sorted[0]
    
    def variance(self, digits = 4):
        '''
        In statistics, variance is a measure of how spread out a set of data is. It is defined as the average of the squared deviations of each number from its mean.
        '''
        mean = self.mean()
        deviations = [(x - mean) ** 2 for x in self.values]
        return round_full(sum(deviations) / len(self.values), digits)
    
    def stdev(self, digits = 4):
        '''
        The square root of the variance is called the standard deviation, which is a widely used measure of the spread of a distribution.
        '''
        return round_full(self.variance() ** 0.5, digits)
    
    def cov(self, digits = 2):
        '''
        The coefficient of variation (CV) is a statistical measure of the relative variability of a data set. It is the ratio of the standard deviation to the mean, expressed as a percentage.
        '''
        cv = round_full(self.stdev()/self.mean()*100, digits)
        scv = ""
        if cv > 20.0:
            scv = "большой"
        elif cv > 10.0:
            scv = "средний"
        else:
            scv = "маленький"
        return cv, scv
    
    def sem(self, digits = 4):
        '''
        The standard error of the mean (SEM) is a measure of the variability of sample means from different samples of the same population. It is the standard deviation of the sample means, and it represents the precision of the sample mean as an estimate of the population mean.
        '''
        return round_full(self.stdev() / len(self.values) ** 0.5, digits)
    
    def skewness(self, digits = 4):
        '''
        Skewness is a measure of the asymmetry of a probability distribution. It is a measure of how much a distribution deviates from symmetry around its mean. A distribution that is symmetric has zero skewness, while a distribution that is skewed to the right (i.e., has a longer tail to the right) has positive skewness, and a distribution that is skewed to the left (i.e., has a longer tail to the left) has negative skewness.
        '''
        skew = (self.mean() - self.mode()[0]) / self.stdev()
        deviation = ""
        if skew == 0.0:
            deviation = "симметричная"
        elif skew < 0:
            deviation = "левосторонняя"
        else:
            deviation = "правосторонняя"
        return round_full(skew, digits), deviation
    
    def kurtosis(self, digits = 4):
        '''
        Kurtosis is a measure of the "peakedness" or "flatness" of a probability distribution, relative to a normal distribution. A normal distribution has a kurtosis value of 0, and distributions with higher kurtosis values have more extreme tails, indicating the presence of more outliers or extreme values.

        n = len(self.values): calculate the sample size of the data stored in the self.values attribute of an object.

        kurt = (sum((x - mean) ** 4 for x in self.values) / (n * self.stdev() ** 4)): calculate the numerator of the kurtosis formula by summing the fourth power of the difference between each data point and the sample mean, divided by the fourth power of the sample standard deviation.

        kurt = kurt - 3: subtract 3 from the numerator to adjust for the kurtosis of a normal distribution, which is 3.

        kurt = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * kurt: calculate the denominator of the kurtosis formula and multiply it with the adjusted numerator to obtain the final kurtosis value.
        '''
        n = len(self.values)
        mean = self.mean()
        kurt = (sum((x - mean) ** 4 for x in self.values) / (n * self.stdev() ** 4))
        kurt = kurt - 3
        kurt = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * kurt
        osis = ""
        if kurt == 0.0:
            osis = "нормальный"
        elif kurt < 0:
            osis = "плосковершинный"
        else:
            osis = "островершинный"
        return round_full(kurt, digits), osis


class Bivariate:
    values: tuple[list[float] | list[int], list[float] | list[int]]
    sums: tuple
    means: tuple
    data_a: tuple
    sums_a: tuple
    data_b: tuple
    sums_b: tuple

    def __init__(self, xn: list[float] | list[int], yn: list[float] | list[int]):
        self.values = (xn, yn)
        self.sums = (round_full(sum(xn), 1),round_full(sum(yn), 1))
        self.means = self.mean(2)
        self.data_a = self.get_data_a()
        self.sums_a = self.get_sums_a()
        self.data_b = self.get_data_b()
        self.sums_b = self.get_sums_b()
    
    def __str__(self):
        strings = []
        strings.append(f"Выборка X ({self.sums[0]} эл., {self.means[0]} ср.): {self.values[0]}")
        strings.append(f"Выборка Y ({self.sums[1]} эл., {self.means[1]} ср.): {self.values[1]}")
        strings.append(f"\n")

        strings.append(f"=== Первый метод: ===")
        strings.append(f"XMD (Xi - Xср): {self.data_a[0]}")
        strings.append(f"YMD (Yi - Yср): {self.data_a[1]}")
        strings.append(f"XMD*YMD ({self.sums_a[0]} эл.): {self.data_a[2]}")
        strings.append(f"XMD^2 ({self.sums_a[1]} эл.): {self.data_a[3]}")
        strings.append(f"YMD^2 ({self.sums_a[2]} эл.): {self.data_a[4]}")
        strings.append(f"\n")

        xssd, yssd = self.sample_standard_deviation()
        strings.append(f"Среднеквадратичное отклонение X: {xssd}, Y: {yssd}")
        strings.append(f"Коэффициент корреляции Пирсона: {self.pearson_correlation_coefficient()}")
        strings.append(f"Коэффициент детерминации: {show_as_percentage(self.determination_cofficient())}")
        strings.append(f"\n")

        strings.append(f"=== Второй метод: ===")
        strings.append(f"X^2 ({self.sums_b[0]} эл.): {self.data_b[0]}")
        strings.append(f"Y^2 ({self.sums_b[1]} эл.): {self.data_b[1]}")
        strings.append(f"X*Y ({self.sums_b[2]} эл.): {self.data_b[2]}")
        xdisp, ydisp = self.dispersion()
        strings.append(f"Дисперсия X:{xdisp} Y:{ydisp}")
        strings.append(f"Выборочный корреляционный момент: {self.sample_correlation_momentum()}")
        strings.append(f"Выборочный коэффициент корреляции: {self.sample_correlation_coefficient()}")
        strings.append(f"Прямая регрессии (x = 10..20): {self.line_of_regression([x for x in range(10, 21, 1)])}")
        output = "\n".join(strings)
        return f"===\n\n{output}\n"
    
    def mean(self, digits = 4):
        x_mean = round_full(sum(self.values[0])/len(self.values[0]), digits)
        y_mean = round_full(sum(self.values[1])/len(self.values[1]), digits)
        return x_mean, y_mean
    
    def get_data_a(self, digits = 2):
        x_mean, y_mean = self.means
        x_mdiff = [round_full(x - x_mean, digits) for x in self.values[0]]
        y_mdiff = [round_full(y - y_mean, digits) for y in self.values[1]]
        xy_dmull = [round_full(xmd * ymd, digits) for xmd, ymd in zip(x_mdiff, y_mdiff)]
        x_mdpow = [round_full(x ** 2, digits) for x in x_mdiff]
        y_mdpow = [round_full(y ** 2, digits) for y in y_mdiff]
        return x_mdiff, y_mdiff, xy_dmull, x_mdpow, y_mdpow

    def get_sums_a(self):
        return round_full(sum(self.data_a[2]), 1), round_full(sum(self.data_a[3]), 1), round_full(sum(self.data_a[4]), 1)
    
    def sample_standard_deviation(self, digits = 5):
        xssd = (self.sums_a[1] / (len(self.values[0]) - 1)) ** 0.5
        yssd = (self.sums_a[2] / (len(self.values[1]) - 1)) ** 0.5
        return round_full(xssd, digits), round_full(yssd, digits)
    
    def pearson_correlation_coefficient(self, digits = 4):
        xssd, yssd = self.sample_standard_deviation()
        return round_full(self.sums_a[0] / (len(self.values[0]) * xssd * yssd), digits)
    
    def determination_cofficient(self, digits = 2):
        return round_full(self.pearson_correlation_coefficient(6) ** 2 * 100, digits)
    
    def get_data_b(self, digits = 2):
        x_pow = [round_full(x ** 2, digits) for x in self.values[0]]
        y_pow = [round_full(y ** 2, digits) for y in self.values[1]]
        xy_mul = [round_full(x * y, digits) for x, y in zip(self.values[0], self.values[1])]
        return x_pow, y_pow, xy_mul
    
    def get_sums_b(self, digits = 1):
        return round_full(sum(self.data_b[0]), digits), round_full(sum(self.data_b[1]), digits), round_full(sum(self.data_b[2]), digits)
    
    def dispersion(self, digits = 2):
        xdisp = self.sums_b[0] / len(self.values[0]) - self.means[0] ** 2
        ydisp = self.sums_b[1] / len(self.values[1]) - self.means[1] ** 2
        return round_full(xdisp, digits), round_full(ydisp, digits)
    
    def sample_correlation_momentum(self, digits = 2):
        return round_full(self.sums_b[2] / len(self.values[0]) - self.means[0] * self.means[1], digits)
    
    def sample_correlation_coefficient(self, digits = 3):
        scm = self.sample_correlation_momentum()
        xssd, yssd = self.sample_standard_deviation()
        return round_full(scm / (xssd * yssd), digits)
    
    def line_of_regression(self, xlist: list[float], digits = 3):
        xdisp, ydisp = self.dispersion()
        a = round_full(self.sample_correlation_coefficient() / ((ydisp / xdisp) ** 0.5), digits)
        k = round_full(self.means[1] - a * self.means[0], digits)
        return [(round_full(x, digits), round_full(k + a * x, digits)) for x in xlist]


class CombinedDataset:
    value_block_one: list[float] | list[int] = []
    value_block_two: list = []
    uni: Univariate
    bi: Bivariate

    def __init__(self, xn: list[float] | list[int], yn: list[float] | list[int]):
        xns = sorted(xn)
        for i in range(0, len(xn)):
            self.value_block_one.append(i+1)
            self.value_block_one.append(xn[i])
            self.value_block_one.append(xns[i])
            self.value_block_one.append(yn[i])
#        self.value_block_one = [i for i in range(1,11)] + xn + sorted(xn) + yn
        self.uni = Univariate(xn)
        data_bt = self.uni.split_data[1:]
        for i in range(0, len(data_bt[0])):
            self.value_block_two.append(i+1)
            self.value_block_two.append(f"({data_bt[0][i][0]} - {data_bt[0][i][1]})")
            self.value_block_two.append(data_bt[1][i])
            self.value_block_two.append(data_bt[2][i])
            self.value_block_two.append(data_bt[3][i])
            self.value_block_two.append(data_bt[4][i])
            self.value_block_two.append(data_bt[5][i])

        self.bi = Bivariate(xn, yn)

    def __str__(self):
        return f"{self.uni}{self.bi}"