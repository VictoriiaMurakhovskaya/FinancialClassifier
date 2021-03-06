import pandas as pd

def indicators(values):
    res = [{'key': 'Коэффициент текущей ликвидности',
            'value': values[1200] / (values[1510] + values[1520] + values[1550])},
           {'key': 'Коэффициент обеспеченности собственными средствами',
            'value': (values[1100] + values[1200]) /(values[1510] + values[1520] + values[1550])},
           {'key': 'Коэффициент соотношения чистых активов и уставного капитала',
            'value': values[1300] / values[1310]},
           {'key': 'Коэффициент рентабельности использования всего капитала',
            'value': values[2400] / (values[1300] + values[1400] + values[1530])},
           {'key': 'Коэффициент использования собственных средств',
            'value': values[2400] / values[1300]},
           {'key': 'Коэффициент рентабельности продаж по валовой прибыли',
            'value': values[2100] / values[2110]},
           {'key': 'Коэффициент рентабельности продаж по операционной прибыли',
            'value': (values[2300] + values[2330]) / values[2110]},
           {'key': 'Коэффициент рентабельности продаж по чистой прибыли',
            'value': values[2400] / values[2110]},
           {'key': 'Коэффициент рентабельности по текущим затратам',
            'value': values[2300] / values[2120]},
           {'key': 'Рентабельность оборотных средств',
            'value': values[2400] / values[1200]},
           {'key': 'Рентабельность активов',
            'value': values[2400] / values[1600]},
           {'key': 'Коэффициент независимости или автономности (концентрации собственного капитала)',
            'value': values[1300] / values[1700]},
           {'key': 'Коэффициент соотношения привлеченных и собственных средств',
            'value': (values[1410] + values[1510]) / values[1300]},
           {'key': 'Коэффициент дебиторской задолженности',
            'value': values[2110] / values[1230]},
           {'key': 'Коэффициент капитализации (плечо финансового рычага)'
                   ' (коэффициент соотношения заемных и собственных средств)',
            'value': (values[1400] + values[1500]) / values[1300]},
           {'key': 'Коэффициент обеспеченности запасов собственными источниками',
            'value': (values[1300] - values[1100]) /(values[1210] + values[1220])},
           {'key': 'Коэффициент финансирования',
            'value': values[1300] / (values[1400] + values[1500])},
           {'key': 'Коэффициент финансовой устойчивости',
            'value': values[1300] / (values[1400] + values[1700])},
           {'key': 'Коэффициент маневренности',
            'value': (values[1300] - values[1100]) / values[1300]},
           {'key': 'Коэффициент иммобилизации',
            'value': values[1100] / values[1200]},
           {'key': 'Коэффициент зависимости (концентрации заемного капитала) (мультипликартор собственного капитала)',
            'value': values[1700] / values[1300]},
           {'key': 'Коэффициент абсолютной ликвидности',
            'value': (values[1250] + values[1240]) / (values[1510] + values[1520] + values[1550])},
           {'key': 'Промежуточный коэффициент покрытия',
            'value': (values[1240] + values[1250] + values[1260]) / (values[1500] - values[1530] - values[1540])},
           {'key': 'Коэффициент обеспеченности запасами краткосрочных обязательств',
            'value': values[1500] / values[1210]},
           {'key': 'Коэффициент быстрой (срочной) ликвидности',
            'value': (values[1230] + values[1240] + values[1250]) / (values[1510] + values[1520] + values[1550])},
           {'key': 'Коэффициент маневремнности функционирующего капитала',
            'value': (values[1210] + values[1220] + values[1230]) / (values[1200] - (values[1510] + values[1520]
                                                                                     + values[1550]))},
           {'key': 'Доля оборотных средств в активах',
            'value': values[1200] / values[1600]},
           {'key': 'Коэффициент обеспеченности',
            'value': (values[1300] - values[1100]) / values[1200]},
           {'key': 'Общий коэффициент оборачиваемости',
            'value': values[2110] / values[1600]},
           {'key': 'Коэффициент оборачиваемости запасов',
            'value': values[2110] / (values[1210] + values[1220])},
           {'key': 'Коэффициент оборачиваемости собственных средств',
            'value': values[2110] / values[1300]}
           ]

    return pd.DataFrame(res)