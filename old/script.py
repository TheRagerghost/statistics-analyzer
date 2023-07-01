import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from array import *
from fpdf import FPDF
from wand.image import Image
from wand.color import Color
from dotenv import load_dotenv

load_dotenv()

file_path = os.path.realpath(__file__)
tempdir = os.path.abspath(file_path + '/../../temp/')
output_file = os.path.abspath(file_path + '/../../output')

strs = os.getenv('INPUT').splitlines()
ceil_range = os.getenv('CEIL_RANGE')

# Утилити

def shorten(f : float, n = 4):
    x = pow(10, n)
    return math.floor(f * x) / x

def as_percent(f : float):
    return '{}%'.format(f*100)

# Переменные

a_cells = []
b_cells = []

# Данные

floats = [float(x) for x in strs]
r_floats = sorted(floats)

a_cells.insert(0, floats)
a_cells.insert(1, r_floats)

int_range = math.ceil((r_floats[9] - r_floats[0]) / 2) /2
if ceil_range: int_range = math.ceil(int_range)

breakpoints = [r_floats[0], r_floats[9]]
for i in range(3):
    breakpoints.insert(i+1, breakpoints[i] + int_range)

b_floats = [[r_floats[0]],[],[],[]]
b_points = []
b_lens = []
b_nis = []
b_avgs = []

ni=0
for i in range(4):
    for x in r_floats: 
        if x > breakpoints[i] and x <= breakpoints[i+1]: b_floats[i].append(x)
    b_points.append('{} - {}'.format(breakpoints[i],breakpoints[i+1]))
    b_lens.append(len(b_floats[i]))
    ni += b_lens[i]
    b_nis.append(ni)
    b_avgs.append(math.ceil(sum(b_floats[i]) / b_lens[i] * 100) / 100)
    b_cells.insert(i, [b_points[i], b_lens[i], b_nis[i], b_lens[i]/10, b_nis[i]/10, b_avgs[i]])

average = sum(floats)/len(floats)

def f_mode():

    r = 0
    x = 0
    
    for i in range(4):
        if b_lens[i] > r: 
            r = b_lens[i]
            x = i

    y = 0
    z = 0

    if x == 0:
        z = x + 1
    elif x == 3:
        y = x - 1
    else:
        y = x - 1
        z = x + 1

    if (b_lens[x] - b_lens[y] + b_lens[x] - b_lens[z]) == 0: print('x: {}, y: {}, z: {}'.format(b_lens[x], b_lens[y], b_lens[z]))
        
    return breakpoints[x] + 4 * (b_lens[x] - b_lens[y]) / (b_lens[x] - b_lens[y] + b_lens[x] - b_lens[z])

mode = f_mode()

def f_mediana():

    x = 0

    for i in range(4):
        if b_nis[i]/10 > 0.5: 
            x = i
            break

    y = max(x - 1, 0)

    #return math.floor((r_floats[5] + r_floats[6]) / 2)
    return math.floor(breakpoints[x] + 4 * (0.5 * len(floats) - b_nis[y]) / b_lens[x])

mediane = f_mediana()
spread = r_floats[9] - r_floats[0]

def f_variance():

    x = 0
    y = 0

    for i in range(10):
        x = x + pow(r_floats[i] - average, 2)

    for i in range(4):
        y = y + b_lens[i] * pow(b_avgs[i] - average, 2)

    #return shorten(y / (len(floats) - 1))
    return shorten(x / (len(floats) - 1))

variance = f_variance()
std_deviation = shorten(math.sqrt(variance))

def f_coeff_var():

    a = shorten(std_deviation/average)
    b = ''

    if a > 0.2:
        b = 'большой'
    elif a > 0.1:
        b = 'средний'
    else:
        b = 'небольшой'

    return (a, b)

coeff_var, str_coeff_var = f_coeff_var()

std_err = shorten(std_deviation / math.sqrt(len(floats)))

def f_skewness():
    a = shorten((average - mode)/std_deviation)
    b = ''

    if a > 0:
        b = 'левосторонняя ассиметрия'
    elif a < 0:
        b = 'правосторонняя ассиметрия'
    else:
        b = 'симметрия'

    return (a, b)

skewness, str_skewness = f_skewness()

def f_excess():

    a = 0

    for i in range(4):
        a = a + b_lens[i] * pow(b_avgs[i] - average, 4)

    a = (a / (len(floats) * math.pow(variance, 2))) - 3
    b = ''

    if a > 0:
        b = 'тенденция к островершинности'
    elif a < 0:
        b = 'тенденция к плосковершинности'
    else:
        b = 'норма'

    return (shorten(a), b)

excess, str_excess = f_excess()

# Строки

title = 'Вишняков Андрей, 201-322'
str_att = 'Входные данные'
str_rw = 'Ширина интервала - ' + str(int_range)
str_aa = 'Аналитический анализ'

# Таблицы и графики

fig1, ax1 = plt.subplots()

a_row_labels = ['x', 'x ранж']
a_col_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

a_row_colors = plt.cm.Greens(np.full(len(a_row_labels), 0.2))
a_col_colors = plt.cm.Greens(np.full(len(a_col_labels), 0.2))

ax1.axis('off')
a_table = ax1.table(cellText=a_cells,
                  rowLabels=a_row_labels,
                  colLabels=a_col_labels,
                  rowColours=a_row_colors,
                  colColours=a_col_colors,
                  loc='center')

a_table.auto_set_font_size(False)
a_table.set_fontsize(4)


fig2, ax2 = plt.subplots()

b_row_labels = ['  1  ', '  2  ', '  3  ', '  4  ']
b_col_labels = ['Границы интервалов', 'Частота', 'Накопленная частота', 'Частость', 'Накопленная частость', 'Среднее значение']

b_row_colors = plt.cm.Greens(np.full(len(b_row_labels), 0.2))
b_col_colors = plt.cm.Greens(np.full(len(b_col_labels), 0.2))

ax2.axis('off')
b_table = ax2.table(cellText=b_cells,
                  cellLoc='center',
                  rowLabels=b_row_labels,
                  colLabels=b_col_labels,
                  rowColours=b_row_colors,
                  colColours=b_col_colors,
                  loc='center')

b_table.auto_set_font_size(False)
b_table.set_fontsize(4)


fig3, ax3 = plt.subplots()

a_chart = ax3.bar([1, 2, 3, 4],
            b_lens,
            tick_label = b_points,
            width = 0.8,
            color = 'blue')

ax3.set_title('Гистограмма частот')
ax3.set_ylabel('Частота')
ax3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

yticks = np.linspace(0, 5, 6)
ylabls = ['0', '1', '2', '3', '4', '']
ax3.set_yticks(yticks)
ax3.set_yticklabels(ylabls)


fig4, ax4 = plt.subplots()

b_chart = ax4.plot([1, 2, 3, 4], b_lens,'o-')

ax4.set_title('Полигон распределения частот')
ax4.set_ylabel('Частота')
ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax4.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

def x_labels_formatter(x, labels):
    x = sorted((1, math.floor(x), len(labels)))[1] - 1
    return labels[x]

ax4.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{}'.format(x_labels_formatter(x, b_avgs))))

ax4.set_yticks(yticks)
ax4.set_yticklabels(ylabls)


fig5, ax5 = plt.subplots()

c_row_labels = ['Среднее арифметическое', 
                'Мода', 
                'Медиана',
                'Размах вариации', 
                'Дисперсия', 
                'Среднее квадратичние отклонение', 
                'Коэффициент вариации ({})'.format(str_coeff_var), 
                'Стандартная ошибка среднего арифметического', 
                'Мера скошенности ({})'.format(str_skewness), 
                'Эксцесс ({})'.format(str_excess)]
c_col_labels = ['Значения']

c_row_colors = plt.cm.Greens(np.full(len(c_row_labels), 0.2))
c_col_colors = plt.cm.Greens(np.full(len(c_col_labels), 0.2))

c_cells = [[shorten(average)],
           [shorten(mode)],
           [shorten(mediane)],
           [shorten(spread)],
           [shorten(variance)],
           [shorten(std_deviation)],
           [as_percent(round(shorten(coeff_var), 4))],
           [shorten(std_err)],
           [shorten(skewness)],
           [shorten(excess)]]

ax5.axis('off')
c_table = ax5.table(cellText=c_cells,
                  cellLoc='center',
                  rowLabels=c_row_labels,
                  colLabels=c_col_labels,
                  rowColours=c_row_colors,
                  colColours=c_col_colors,
                  loc='center')

c_table.auto_set_font_size(False)
c_table.set_fontsize(4)
c_table.scale(0.25, 1)


fig1.canvas.draw()
fig2.canvas.draw()
fig3.canvas.draw()
fig4.canvas.draw()
fig5.canvas.draw()

fig1.savefig(tempdir + '/a_table.pdf', bbox_inches='tight', format='pdf')
fig2.savefig(tempdir + '/b_table.pdf', bbox_inches='tight', format='pdf')
fig3.savefig(tempdir + '/a_chart.pdf', bbox_inches='tight', format='pdf')
fig4.savefig(tempdir + '/b_chart.pdf', bbox_inches='tight', format='pdf')
fig5.savefig(tempdir + '/c_table.pdf', bbox_inches='tight', format='pdf')

#plt.show()

# Конвертация PDF в png

def pdf_to_png(path, crop=(0, 0, 0, 0), res=300):
    with Image(filename=path + '.pdf', resolution=res) as pdf:
        page = pdf.sequence[0]

        with Image(page) as image:
            image.background_color = Color('white')
            image.alpha_channel = 'remove'
        
            w = image.width
            h = image.height

            image.crop(left=crop[0], top=crop[1], right=w-crop[2], bottom=h-crop[3])

            image.save(filename=path + '.png')

            return image.size


# Создание PDF

pdf = FPDF()

FONT_REGULAR = os.path.join(os.path.dirname(__file__), "fonts", "consola.ttf")
pdf.add_font('Consolas', '', FONT_REGULAR, uni=True)
pdf.set_font('Consolas', '', 12)

content_w = 0.8
offset_x = pdf.w * (1.0 - content_w) / 2
spacing_y = pdf.font_size + 4

def offset_y(offset):
    y = pdf.get_y()
    y = y + offset
    pdf.set_y(y)

def place_img(path, crop=(0, 0, 0, 0), scale=content_w, align='center', skip_offset=False):

    match align:
        case 'center':
            alignment = pdf.w * (1.0 - scale) / 2
        case 'left':
            alignment = offset_x
        case 'right':
            alignment = pdf.w * (1.0 - scale) - offset_x

    size = pdf_to_png(path, crop)
    pdf.image(path+'.png', x = alignment, y = pdf.y+spacing_y, w = pdf.w*scale)
    if not skip_offset: offset_y(size[1]*scale/10 + spacing_y)

pdf.add_page()
pdf.cell(content_w, spacing_y, title)
pdf.ln(spacing_y)
pdf.set_font('Consolas', '', 8)
pdf.cell(content_w, spacing_y, str_att)

place_img(tempdir + r'\a_table', (10, 490, 10, 490))

offset_y(8)
pdf.cell(content_w, spacing_y, str_rw)

place_img(tempdir + r'\b_table', (10, 440, 10, 440))
pdf.ln(spacing_y)

place_img(tempdir + r'\a_chart', scale=0.4, align='left', skip_offset=True)
place_img(tempdir + r'\b_chart', scale=0.4, align='right')
pdf.ln(spacing_y)

offset_y(8)
pdf.cell(content_w, spacing_y, str_aa)

place_img(tempdir + r'\c_table', crop=(50, 300, 575, 300), scale=0.6, align='left')

pdf.output(output_file + '.pdf', 'F')

pdf_to_png(output_file)