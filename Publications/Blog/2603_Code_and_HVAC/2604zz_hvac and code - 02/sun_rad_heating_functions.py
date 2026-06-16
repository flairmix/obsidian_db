import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

from typing import Literal

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

begin = {'01': 0, '02': 0, '03': 0,}
end = {'20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}

n_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 88, '05' : 103, '06' : 17, '07' : 15, '08' : 0, '09' : 0, '10' : 0, '11' : 0, '12' : 0, '13' : 0, '14' : 0, '15' : 0, '16' : 0, '17' : 15, '18' : 107, '19' : 112 , '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
ne_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 63, '05' : 272, '06' : 387, '07' : 404, '08' : 331, '09' : 146, '10' : 19, '11' : 0, '12' : 0, '13' : 0, '14' : 0, '15' : 0, '16' : 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, }
e_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 237, '05' : 433, '06' : 523, '07' : 547, '08' : 504, '09' : 378, '10' : 193, '11' : 37, '12' : 0, '13' : 0, '14' : 0, '15' : 0, '16' : 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
se_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 28, '05' : 140, '06' : 287, '07' : 424, '08' : 479, '09' : 479, '10' : 427, '11' : 330, '12' : 176, '13' : 21, '14' : 0, '15' : 0, '16' : 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
s_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 0, '05' : 0, '06' : 0, '07' : 22, '08' : 128, '09' : 245, '10' : 347, '11' : 398, '12' : 398, '13' : 347, '14' : 245, '15' : 128, '16' : 22, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
sw_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 0, '05' : 0, '06' : 0, '07' : 0, '08' : 0, '09' : 0, '10' : 21, '11' : 176, '12' : 330, '13' : 427, '14' : 479, '15' : 479, '16' : 424, '17' : 287, '18' : 140, '19' : 28, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
w_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 0, '05' : 0, '06' : 0, '07' : 0, '08' : 0, '09' : 0, '10' : 0, '11' : 0, '12' : 37, '13' : 193, '14' : 378, '15' : 504, '16' : 547, '17' : 523, '18' : 433, '19' : 237, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
nw_d_56 = {'01': 0, '02': 0, '03': 0, '04' : 0, '05' : 0, '06' : 0, '07' : 0, '08' : 0, '09' : 0, '10' : 0, '11' : 0, '12' : 0, '13' : 0, '14' : 26, '15' : 174, '16' : 339, '17' : 401, '18' : 344, '19' : 165, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
n_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 19, '05': 56, '06': 66, '07': 65, '08': 62, '09': 58, '10': 57, '11': 55, '12': 55, '13': 57, '14': 58, '15': 62, '16': 65, '17': 66, '18': 56, '19': 19, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
ne_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 32, '05': 74, '06': 93, '07': 98, '08': 87, '09': 71, '10': 62, '11': 59, '12': 53, '13': 58, '14': 57, '15': 56, '16': 53, '17': 44, '18': 30, '19': 13, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
e_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 27,'05': 74,'06': 115,'07': 122,'08': 114,'09': 91,'10': 76,'11': 67,'12': 63,'13': 58,'14': 56,'15': 55,'16': 48,'17': 43,'18': 30,'19': 13, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
se_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 20, '05': 57, '06': 90, '07': 105, '08': 108, '09': 102, '10': 92, '11': 79, '12': 76, '13': 72, '14': 67, '15': 64, '16': 53, '17': 42, '18': 28, '19': 13, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
s_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 12, '05': 35, '06': 58, '07': 74, '08': 85, '09': 88, '10': 91, '11': 92, '12': 92, '13': 91, '14': 88, '15': 85, '16': 74, '17': 58, '18': 35, '19': 12, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
sw_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 13, '05': 28, '06': 42, '07': 53, '08': 64, '09': 67, '10': 72, '11': 76, '12': 79, '13': 92, '14': 102, '15': 108, '16': 105, '17': 90, '18': 57, '19': 20, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
w_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 13, '05': 30, '06': 43, '07': 48, '08': 55, '09': 56, '10': 58, '11': 53, '12': 67, '13': 76, '14': 91, '15': 114, '16': 122, '17': 115, '18': 74, '19': 27, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}
nw_nd_56 = {'01': 0, '02': 0, '03': 0, '04': 13, '05': 30, '06': 44, '07': 53, '08': 56, '09': 57, '10': 58, '11': 53, '12': 59, '13': 62, '14': 71, '15': 87, '16': 98, '17': 96, '18': 74, '19': 32, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0,}


theta_glass = {
    '15' : 1, 
    '16' : 0.97, 
    '17' : 0.87, 
    '18' : 0.71, 
    '19' : 0.5, 
    '20' : 0.26, 
    '21' : 0,   
    '22' : -0.26, 
    '23' : -0.5, 
    '24' : -0.71,
    '01' : -0.87, 
    '02' : -0.97,
    '03' : -1,
    '04' : -0.97,
    '05' : -0.87, 
    '06' : -0.71,
    '07' : -0.5,
    '08' : -0.26,
    '09' : 0,
    '10' : 0.26,
    '11' : 0.5, 
    '12' : 0.71,
    '13' : 0.87, 
    '14' : 0.97, 
}

data_combined = {
    'n_d': n_d_56 ,
    'ne_d': ne_d_56 ,
    'e_d': e_d_56 ,
    'se_d': se_d_56 ,
    's_d': s_d_56 ,
    'sw_d': sw_d_56 ,
    'w_d': w_d_56 ,
    'nw_d': nw_d_56,
    'n_nd': n_nd_56,
    'ne_nd': ne_nd_56 ,
    'e_nd': e_nd_56 ,
    'se_nd': se_nd_56 ,
    's_nd': s_nd_56 ,
    'sw_nd': sw_nd_56 ,
    'w_nd': w_nd_56 ,
    'nw_nd': nw_nd_56 
}

a_d_8 = {
'Z'    : 0.08,
'Z+1'  : 0.15,
'Z+2'  : 0.26,
'Z+3'  : 0.38,
'Z+4'  : 0.46,
'Z+5'  : 0.50,
'Z+6'  : 0.49,
'Z+7'  : 0.42,
'Z+8'  : 0.30,
'Z+9'  : 0.22,
'Z+10' : 0.19,
'Z+11' : 0.17,
'Z+12' : 0.15,
'Z+13' : 0.14,
'Z+14' : 0.13,
'Z+15' : 0.13,
'Z+16' : 0.11,
'Z+17' : 0.11,
'Z+18' : 0.10,
'Z+19' : 0.10,
'Z+20' : 0.10,
'Z+21' : 0.09,
'Z+22' : 0.09,
'Z+23' : 0.08,
}

a_d = {
'Z'    : 0.14,
'Z+1'  : 0.15,
'Z+2'  : 0.2,
'Z+3'  : 0.25,
'Z+4'  : 0.3,
'Z+5'  : 0.33,
'Z+6'  : 0.34,
'Z+7'  : 0.32,
'Z+8'  : 0.28,
'Z+9'  : 0.27,
'Z+10' : 0.22,
'Z+11' : 0.21,
'Z+12' : 0.2,
'Z+13' : 0.19,
'Z+14' : 0.18,
'Z+15' : 0.18,
'Z+16' : 0.17,
'Z+17' : 0.17,
'Z+18' : 0.16,
'Z+19' : 0.16,
'Z+20' : 0.16,
'Z+21' : 0.15,
'Z+22' : 0.15,
'Z+23' : 0.14,
}

orientations = ['n_d', 'ne_d', 'e_d', 'se_d', 's_d', 'sw_d', 'w_d', 'nw_d', 'n_nd','ne_nd', 'e_nd', 'se_nd', 's_nd', 'sw_nd', 'w_nd', 'nw_nd']


def create_hour_dict(hour_start_rad, original_dict=a_d_8):

    if not (1 <= hour_start_rad <= 24):
        raise ValueError("Час суток должен быть в диапазоне от 1 до 24")

    original_keys = list(original_dict.keys())
    num_keys = len(original_keys)
    new_dict = {}
    for i, original_key in enumerate(original_keys):
        new_hour = (hour_start_rad + i - 1) % 24 + 1
        if new_hour <= 9:
            new_hour = f'0{new_hour}'
        else:
            new_hour = str(new_hour)

        value = original_dict[original_key]

        # Добавляем в новый словарь: ключ — час, значение — данные из исходного словаря
        new_dict[new_hour] = value

    return new_dict


def calculate_Q_sun_i_orien(
    A_m2: float,     
    q_d: int,     
    q_nd: int,     
    K1: float = 0.9,     
    K2: float = 1,     
    K3: float = 0.4,     
    K4: float = 0.34,     
    ):
    return round( (q_d*K1 + q_nd*K2)*K3*K4*A_m2*1e-3, 3)
    



def calculate_sun_rad_heat(
        result_sun_base: pd.DataFrame,
        A_m2: float, 
        orient = Literal[orientations], 
        K1 = 0.9,     
        K2 = 1,     
        K3 = 0.4,     
        K4 = 0.34/0.87, 
):
    result = result_sun_base.copy()
    
    col_d = f'{orient}_d'
    col_nd = f'{orient}_nd'
    new_col = f'{orient}_Q_kW'
    
    result[new_col] = calculate_Q_sun_i_orien( 
        A_m2=A_m2,
        q_d = result[col_d],
        q_nd = result[col_nd],
        K1=K1,
        K2=K2,
        K3=K3,
        K4=K4,
        )

    Q_i_sum = sum(result[new_col])

    if orient in ('n', 'ne', 'e', 'se'):
        hour_start_rad = 4
    elif orient in ('s'):
        hour_start_rad = 7
    elif orient in ('sw'):
        hour_start_rad = 10
    elif orient in ('w'):
        hour_start_rad = 12
    elif orient in ('nw'):
        hour_start_rad = 14

    # hour_start_rad = int(result[new_col].idxmax())

    # Расставляем коэфициент поглащения по часам 
    shifted_dict = create_hour_dict(
        hour_start_rad, 
        original_dict=a_d_8
        )
    result[f'{orient}_a_d'] = shifted_dict
    
    # Определяем теплопоступления через максимальное удельное значение интенсивности излучения
    # result[f'{orient}_Q_sun_kW'] = round(Q_i_sum * result[f'{orient}_a_d'], 3)
    result[f'{orient}_Q_sun_kW'] = round(result[new_col] * result[f'{orient}_a_d'], 3)

    drop_list = [ i for i in result.columns if i not in (f'{orient}_Q_W', f'{orient}_a_d', f'{orient}_Q_sun_kW')]

    result.drop(drop_list, axis=1, inplace=True)

    return result 
    


def plot_df(df):

    sns.set_style('whitegrid')

    # Создаём фигуру с подзаграфиками
    fig, ax = plt.subplots(figsize=(18, 8))

    # Строим линии для разных показателей
    sns.lineplot(data=df, x=df.index, y='w_Q_sun_kW', linestyle='--', label='Запад радиация, кВт', linewidth=1, ax=ax)
    sns.lineplot(data=df, x=df.index, y='e_Q_sun_kW', linestyle='--', label='Восток радиация, кВт', linewidth=1, ax=ax)
    sns.lineplot(data=df, x=df.index, y='n_Q_sun_kW', linestyle='--', label='Север радиация, кВт', linewidth=1, ax=ax)
    sns.lineplot(data=df, x=df.index, y='s_Q_sun_kW', linestyle='--', label='Юг радиация, кВт', linewidth=1, ax=ax)

    sns.lineplot(data=df, x=df.index, y='Q_people_kW', linestyle='dashdot', label='От людей, кВт', linewidth=1, ax=ax)
    sns.lineplot(data=df, x=df.index, y='Q_appliances_kW', linestyle='dashdot', label='От техники, кВт', linewidth=1, ax=ax)

    sns.lineplot(data=df, x=df.index, y='Q_heating_air_kW', linestyle='-', label='От приточного воздуха, кВт', linewidth=3, ax=ax)
    sns.lineplot(data=df, x=df.index, y='Rad_kW', linestyle='-', label='Суммарный радиация, кВт', linewidth=3, ax=ax)
    sns.lineplot(data=df, x=df.index, y='Q_conduction_kW', linestyle='-', label='Теплопроводность, кВт', linewidth=3, ax=ax)

    sns.lineplot(data=df, x=df.index, y='Q_sum', label='Общий тепловой баланс, кВт', linewidth=4, ax=ax)

    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1.5)

    # Находим максимумы и их позиции
    max_Rad_kW = df['Rad_kW'].max()
    max_Q_conduction = df['Q_conduction_kW'].max()
    max_Q_sum = df['Q_sum'].max()
    max_Q_heating_air_kW = df['Q_heating_air_kW'].max()

    idx_Sum_kW = df['Rad_kW'].idxmax()
    idx_Q_conduction = df['Q_conduction_kW'].idxmax()
    idx_Q_sum = df['Q_sum'].idxmax()
    idx_Q_heating_air_kW = df['Q_heating_air_kW'].idxmax()

    # Добавляем текстовые аннотации
    ax.annotate(f'Радиация: {max_Rad_kW:.1f} кВт',
                xy=(idx_Sum_kW, max_Rad_kW),
                xytext=(10, 10),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                fontsize=7,
                fontweight='bold')

    ax.annotate(f'Теплопередача: {max_Q_conduction:.1f} кВт',
                xy=(idx_Q_conduction, max_Q_conduction),
                xytext=(10, -20),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                fontsize=7,
                fontweight='bold')

    ax.annotate(f'Нагрев воздуха: {max_Q_heating_air_kW:.1f} кВт',
                xy=(idx_Q_heating_air_kW, max_Q_heating_air_kW),
                xytext=(-60, 20),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                fontsize=7,
                fontweight='bold')
    
    ax.annotate(f'Баланс: {max_Q_sum:.1f} кВт',
                xy=(idx_Q_sum, max_Q_sum),
                xytext=(-60, 20),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                fontsize=10,
                fontweight='bold')
    

    # Улучшаем разметку оси Y
    y_min = min(df['Rad_kW'].min(), df['Q_conduction_kW'].min(), df['Q_sum'].min(), df['Q_heating_air_kW'].min())
    y_max = max(max_Rad_kW, max_Q_conduction, max_Q_sum)
    ax.set_ylim(y_min * 0.95, y_max * 1.05)  # небольшой запас по краям

    # Устанавливаем больше делений на оси Y
    y_ticks =  np.linspace(y_min, y_max, 20)  
    
    # y_ticks = np.append(y_ticks_max, y_ticks_min)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{y:.1f}' for y in y_ticks])

    # Настраиваем оформление
    ax.set_title('Динамика тепловых потоков в течение суток', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Час суток', fontsize=12)
    ax.set_ylabel('Мощность, кВт', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def calculation_Qi_conduction_kW(
        A_air_day,
        theta,
        F_m2,
        R_m2K_W,
        t_out_day_mid = 23,
        t_in = 22,
    ):
    return round((t_out_day_mid + 0.5*A_air_day*theta - t_in)*(F_m2/R_m2K_W)*1e-3, 3)


def calculatating_Qsum_conduction_kW(
        df,
        A_air_day,
        A_full, 
        R, 
        t_out_day_mid,
        ):

    df['Q_conduction_kW'] = df.apply(
        lambda row: calculation_Qi_conduction_kW(
            A_air_day=A_air_day,
            theta=row['theta_glass'],  
            F_m2=A_full,
            R_m2K_W=R,
            t_out_day_mid=t_out_day_mid,  
            t_in=24
        ),
        axis=1
    )


    return df 

def calculation_sun_kW(
        df_sun_base,
        A_m2_w,
        A_m2_e,
        A_m2_n,
        A_m2_s,
        Q_people_kW,
        Q_appliances_kW,
        L_m3_h = 0,
        t_out_day_mid = 19,
        t_in_air = 22,
        A_air_day = 24,
        R = 1.45,
        K1 = 0.9,     
        K2 = 1,     
        K3 = 0.4,     
        K4 = 0.34/0.87,
    ):

        A_full = A_m2_w + A_m2_e + A_m2_n + A_m2_s

        result_w = calculate_sun_rad_heat(
            result_sun_base = df_sun_base, 
            A_m2= A_m2_w,
            orient = 'w',
            K1=K1,
            K2=K2,
            K3=K3,
            K4=K4,
        )

        result_e = calculate_sun_rad_heat(
            result_sun_base = df_sun_base, 
            A_m2= A_m2_e,
            orient = 'e',
            K1=K1,
            K2=K2,
            K3=K3,
            K4=K4,
        )

        result_n = calculate_sun_rad_heat(
            result_sun_base = df_sun_base, 
            A_m2= A_m2_n,
            orient = 'n',
            K1=K1,
            K2=K2,
            K3=K3,
            K4=K4,
        )

        result_s = calculate_sun_rad_heat(
            result_sun_base = df_sun_base, 
            A_m2= A_m2_s,
            orient = 's',
            K1=K1,
            K2=K2,
            K3=K3,
            K4=K4,
        )

        result = result_w.join([result_e, result_n, result_s])
        result['Q_people_kW'] = Q_people_kW
        result['Q_appliances_kW'] = Q_appliances_kW

        result['Rad_kW'] = result['e_Q_sun_kW'] + result['n_Q_sun_kW'] + result['w_Q_sun_kW'] + result['s_Q_sun_kW']
        result['theta_glass'] = theta_glass

        df = calculatating_Qsum_conduction_kW(
            result,
            A_air_day,
            A_full, 
            R, 
            t_out_day_mid)
            
        df['t_air_out'] = (t_out_day_mid + 0.5 * A_air_day * result['theta_glass'])
        df['delta_t_air_in_out'] = df['t_air_out'] - t_in_air
        df['Q_heating_air_kW'] = round(df['delta_t_air_in_out'] * 1.2 * L_m3_h / 3600, 0)

        df['Q_sum'] = df['Q_conduction_kW']  + df['Rad_kW'] + df['Q_people_kW'] + df['Q_appliances_kW'] + df['Q_heating_air_kW']
        

        
        return df