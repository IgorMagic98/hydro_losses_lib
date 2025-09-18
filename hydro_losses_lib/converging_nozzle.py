import math

def friction_coefficient_transition(Re):
    if Re < 2300:
        return 64 / Re
    elif Re > 4000:
        return 0.3164 * Re ** -0.25
    else:
        # логарифмическая интерполяция между 2300 и 4000
        lambda_laminar = 64 / 2300
        lambda_turbulent = 0.3164 * 4000 ** -0.25
        log_lambda_laminar = math.log(lambda_laminar)
        log_lambda_turbulent = math.log(lambda_turbulent)
        log_Re = math.log(Re)
        log_Re_min = math.log(2300)
        log_Re_max = math.log(4000)
        log_lambda = (log_lambda_turbulent - log_lambda_laminar) * (log_Re - log_Re_min) / (log_Re_max - log_Re_min) + log_lambda_laminar
        return math.exp(log_lambda)

def pipe(Q, Q_unit, d, d_unit, L, L_unit, delta, delta_unit, nu, nu_unit, rho, rho_unit,
         output_units=None):
    """
    Рассчитывает потерю давления в трубе по формуле Дарси-Вейсбаха с приведением входных параметров к СИ.
    Параметры:
    Q, Q_unit - расход и единица расхода
    d, d_unit - диаметр и его единица
    L, L_unit - длина и ее единица
    delta, delta_unit - шероховатость и ее единица
    nu, nu_unit - вязкость и ее единица
    rho, rho_unit - плотность и ее единица
    output_units - словарь с необходимыми единицами для вывода:
       {
          'delta_p': 'Pa' или 'kPa' или 'mbar' (давление),
          'v': 'm/s' или 'cm/s' (скорость),
          'Re': 'unitless' (число Рейнольдса без единиц),
          'lam': 'unitless' (коэффициент трения),
       }
    Возвращает:
    tuple: (потеря давления, Re, скорость, коэффициент трения) — в запрошенных единицах
    """

    def convert_flow_to_m3s(value, unit):
        if unit == 'm3/s': 
            return value
        elif unit == 'l/s': 
            return value / 1000
        elif unit == 'm3/h': 
            return value / 3600
        elif unit == 'l/h': 
            return value / (1000*3600)
        else:
            raise ValueError(f"Unknown flow unit: {unit}")

    def convert_length_to_m(value, unit):
        if unit == 'm': 
            return value
        elif unit == 'cm': 
            return value / 100
        elif unit == 'mm': 
            return value / 1000
        else:
            raise ValueError(f"Unknown length unit: {unit}")

    def convert_viscosity_to_m2s(value, unit):
        if unit == 'm2/s': 
            return value
        elif unit == 'cSt': 
            return value * 1e-6
        else:
            raise ValueError(f"Unknown viscosity unit: {unit}")

    def convert_density_to_kgm3(value, unit):
        if unit == 'kg/m3': 
            return value
        else:
            raise ValueError(f"Unknown density unit: {unit}")

    def convert_pressure_from_pa(value, unit):
        if unit == 'Pa':
            return value
        elif unit == 'kPa':
            return value / 1000
        elif unit == 'bar':
            return value / 1e5
        elif unit == 'mbar':
            return value / 100
        else:
            raise ValueError(f"Unknown pressure output unit: {unit}")

    def convert_speed_from_mps(value, unit):
        if unit == 'm/s':
            return value
        elif unit == 'cm/s':
            return value * 100
        else:
            raise ValueError(f"Unknown speed output unit: {unit}")

    # Конвертация входных параметров в СИ
    Q_si = convert_flow_to_m3s(Q, Q_unit)
    d_si = convert_length_to_m(d, d_unit)
    L_si = convert_length_to_m(L, L_unit)
    delta_si = convert_length_to_m(delta, delta_unit)
    nu_si = convert_viscosity_to_m2s(nu, nu_unit)
    rho_si = convert_density_to_kgm3(rho, rho_unit)

    # Расчёт скорости потока
    v = 4 * Q_si / (math.pi * d_si**2)

    # Число Рейнольдса
    Re = v * d_si / nu_si

    # Относительная шероховатость
    delta_e = delta_si / d_si

    # Определение коэффициента трения λ с использованием функции для переходного режима
    lam = friction_coefficient_transition(Re)

    # Потеря давления по формуле Дарси-Вейсбаха
    delta_p = lam * (L_si / d_si) * (rho_si * v**2) / 2

    # Приводим выходные данные к указанным единицам
    if output_units is None:
        output_units = {'delta_p': 'Pa', 'v': 'm/s', 'Re': 'unitless', 'lam': 'unitless'}

    dp_out = convert_pressure_from_pa(delta_p, output_units.get('delta_p', 'Pa'))
    v_out = convert_speed_from_mps(v, output_units.get('v', 'm/s'))
    Re_out = Re  # без единиц
    lam_out = lam  # без единиц

    return dp_out, Re_out, v_out, lam_out
