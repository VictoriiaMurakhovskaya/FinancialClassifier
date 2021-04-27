import pandas as pd
import numpy as np
from math import exp
from sklearn.preprocessing import normalize
import xgboost as xgb

norms = pd.read_excel('data.xlsx', sheet_name='normatives', index_col='Номер')
clf = xgb.XGBModel()
clf.load_model('xgb_class.json')


def to_float(x):
    try:
        x = x.replace(',', '.')
    except:
        pass
    return float(x)


for item in ['Зона опасности', 'Зона риска', 'Зона стабильности']:
    norms[item] = norms[item].apply(to_float)


def belong_f(x, param=1):
    """
    Функция, возвращающая кортеж значений функций принадлежности к каждому из состояний
    """
    # значения, разделяющие интервалы
    splitters = [norms.at[param, 'Зона риска'], norms.at[param, 'Зона опасности'], norms.at[param, 'Зона стабильности']]
    # расчет длины интервала
    interval = np.abs(splitters[1] - splitters[0])  # интервал между границами раздела (из таблицы нормативов)
    k = interval / (0.495 - 0.165)  # коэффициент масштабирования
    # экстремумы функций
    peaks = [splitters[i] - 0.166 * k for i in range(3)] + [splitters[2] + 0.166 * k]
    # расчет сигма для рассматриваемого случая
    sigma = 0.159 * k
    # функция Гаусса
    gauss = lambda x, c, sigma: exp((-1) * (x - c) * (x - c) / (2 * sigma * sigma))
    # значения функции принадлежности к каждой из категорий
    values = np.array([gauss(x, extr, sigma) for extr in peaks])
    # возврат np.array нормированных значений функций принадлежности
    if sum(values) < 1e-4:  # если сумма мала, значит x находится далеко с одного из "краев"
        if x > splitters[2]:
            return np.array([0, 0, 0, 1])
        else:
            return np.array([1, 0, 0, 0])
    else:  # если сумма больше отсечки, то возвращается нормализованный вектор значений
        return normalize(values.reshape(1, -1), norm='l1')[0]


def belong_total(p_set):
    v1, v2 = sum([i[0] for i in map(lambda x: belong_f(x, p_set.index(x) + 1), p_set)]),\
             sum([j[3] for j in map(lambda x: belong_f(x, p_set.index(x) + 1), p_set)])
    return v1, v2
