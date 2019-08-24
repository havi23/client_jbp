def get_sale(currency, is_first, spec_count, plan):
    # is_first - параметр первой покупки
    if is_first:
        single_cost = 39
    else:
        single_cost = 10
    # Цена за один скрипт
    if currency == 'EUR':
        pass
    elif currency == 'USD':
        eur_to_usd = 1.11  # Курс
        single_cost = single_cost * eur_to_usd
    elif currency == 'RUB':
        eur_to_rub = 72.74  # Курс
        russian_soul_coefficient = 0.5  # Коэффициент щедрой русской души (поправка на жадность и нищету в рашке)
        single_cost = single_cost * eur_to_rub * russian_soul_coefficient
    else:
        raise KeyError # Для ошибки
    # Цена без скидки
    clear_cost = plan * spec_count * single_cost

    if plan>1 or spec_count>1: # Расчет скидки (В ПРОЦЕНТАХ)
        plan_value_corrector = plan*(2.8-spec_count)
        subscribe_value = plan*(spec_count*0.5)
        # Влияние этого параметра должно быть гораздо ниже при расчете цены за подписку
        if is_first:
            first_buy_value = (spec_count*10)
        else:
            first_buy_value = (spec_count*3)
        sale = plan_value_corrector*2 + subscribe_value + first_buy_value * 2
    else:
        sale = 0

    # Итоговая цена
    total_cost = clear_cost - (clear_cost/100*sale)
    return total_cost, sale
currency = 'RUB'
row = list()
print(f'   1    3    6    12')
for spec_count in (1,2,3):
    for plan in (1, 3, 6, 12):
        row.append(round(get_sale(currency, True, spec_count, plan)[0]))
    print(f'{spec_count} {row}')
    row.clear()

