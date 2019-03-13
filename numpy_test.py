import mysql.connector as db
import numpy as np
from openpyxl import Workbook
import sys
import re


# Базовый запрос к БД. Данная функция осущестляет подключение к БД
# и направляет запрос переданный в функцию в виде строки.
# Воозвращает результат запроса в виде кортежа

def zapros_base(query_str):
    db_user = 'soctraf'
    db_pass = 'traffic'
    db_IP = '10.245.41.196'
    db_db = 'traf'
    db_connection = db.connect(host=db_IP, user=db_user, password=db_pass, database=db_db)
    cursor = db_connection.cursor()
    cursor.execute(query_str)
    results = cursor.fetchall()
    db_connection.close()
    return results

def zapros_int(interface, provider, device, period):
    days = []
    maksimus = []
    totals = []
    z_year, z_month, z_start_day, z_stop_day = period
    zapros_str = """SELECT _av.peak,
                           _av.day 
                    FROM avtable_day _av 
                    WHERE 
                    _av.year = {year}
                    AND _av.month = {month} 
                    AND _av.day >= {start_day}
                    AND _av.day <= {stop_day} 
                    AND _av.traf = 'bps_in' 
                    AND _av.provider LIKE '{prov}' 
                    AND _av.device =  '{dev}'
                    AND _av.nameds LIKE '{iface}'
                    
                    ORDER BY
                    _av.day 
                    """.format(year=z_year, month=z_month, start_day=z_start_day, stop_day=z_stop_day,
                               prov=provider, dev=device, iface=interface)

    x_list = zapros_base(zapros_str)
    if len(x_list) != 0:
        for x in x_list:
            maksimus.append(x[0])
            days.append(x[1])
        totals.append(days)
        totals.append(maksimus)
    else:
        totals.append(0)

    return totals

def create_periods(year, month_start, month_stop, day_start, day_stop):
    period = []
    periods = []
    for i in range(month_stop - month_start + 1):
        period.append(year)
        period.append(month_start + i)
        if (i == 0):
            period.append(day_start)
        else:
            period.append(1)
        if (i == month_stop - month_start):
            period.append(day_stop)
        else:
            if month_start+i in [1, 3, 5, 7, 8, 10, 12]:
                period.append(31)
            if month_start+i in [4, 6, 9, 11]:
                period.append(30)
            if month_start+i in [2]:
                period.append(28)
        periods.append(period)
        period = []
    return periods

def create_zeros(period):
    days = []
    maksimus = []
    totals = []
    _, _, day_start, day_stop = period
    for i in range(day_stop-day_start+1):
        days.append(day_start+i)
        maksimus.append(0)
    totals.append(days)
    totals.append(maksimus)
    return totals

def sum_zeros_and_query(zeros, query):
    
    first_array = np.array(zeros).astype(float)
    second_array = np.array(query).astype(float)

# print(second_array)
    steps = len(second_array[0]) # Количество замен
    for step in range (steps):
    #print ('Шаг номер - {x}'.format(x =step))
    #print (second_array[:,step]) 
    
        x = second_array[0][step]
    
        t = np.where(first_array[0] == x)
        f_pos = t[0][0]
        
        # print(second_array[:,step])
        first_array[:,f_pos] = second_array[:,step]
        z = []
        z.append(first_array[0].astype(int).tolist())
        z.append(first_array[1].astype(float).tolist())
    
    return z



periods = create_periods(2019,2,3,25,3)
iface = '%xe-1/0/1%'
prov = 'MEGAFON'
dev = 'asta-gate-1'
sum_if_periods = []

for p in periods:
    z =[]
    q =[]
    z = create_zeros(p)
    q = zapros_int(iface, prov, dev, p)
    temp_list = sum_zeros_and_query(z, q)
    sum_if_periods = sum_if_periods + temp_list

print()
print(sum_if_periods)

