import os
import loader
import output as out
import utils
from analytics import Univariate, Bivariate, CombinedDataset
from vartests import RosenbaumQ, SignG, MannWhitneyU, WilcoxonU, FisherF










x_num, y_num = loader.load_default_xlsx()
x_num, y_num = loader.load_xlsx("default")

q = Bivariate(x_num, y_num)

print(q.sample_standard_deviation())






'''
ПРИМЕРЫ

numbers = utils.generate_random_ten() - создает ряд из 10 случайных элементов

numbers = [11, 24, 19, 25, 16, 18, 20, 21, 21, 14] - элементы, заданные вручную
y_numbers = [16, 45, 19, 20, 18, 21, 20, 20, 68, 46]

x_num, y_num = loader.load_default_xlsx() - загрузка элементов из базового файла
x_num, y_num = loader.load_xlsx("default") - загрузка элементов из xlsx файла c указанием названия

dataset = CombinedDataset(x_num, y_num) - полное решение 1 и 2 работы

out.save_dataset(dataset) - сохранение работы в формате txt
out.save_dataset_xlsx(dataset) - *не доделано* сохранение работы в формате xlsx

a_set = [137, 139, 129, 137, 140, 137, 136, 134, 137, 126, 132, 135, 141, 134, 141, 141]
b_set = [131, 132, 124, 137, 125, 124, 131, 125, 128, 125, 121, 128, 120]
qtest = RosenbaumQ(a_set, b_set) 
print(qtest)


xset = [85, 89, 88, 81, 83, 90, 95, 91, 85, 98, 87, 91]
yset = [93, 98, 95, 89, 89, 97, 95, 96, 90, 93, 91, 96]
gtest = SignG(xset, yset)
print(gtest)

xnums = [9.3, 9.0, 9.4, 8.9, 9.3, 9.5, 9.2, 9.0, 9.2, 9.3]
ynums = [9.0, 9.1, 8.7, 8.9, 9.0, 8.8, 9.2, 8.8, 9.0, 8.9]
utest = MannWhitneyU(xnums, ynums)
print(utest)

xlist = [240, 250, 270, 240, 260, 240, 220, 250, 250, 240, 260, 240]
ylist = [280, 270, 260, 280, 260, 290, 260, 250, 220, 270, 270, 260]
ttest = WilcoxonU(xlist, ylist)
print(ttest)

Не закончен
xvals = [8, 40]
yvals = [17, 27]
ftest = FisherF(xvals, yvals)
'''
