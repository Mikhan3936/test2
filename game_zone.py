#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:04:45 2021

@author: Поздняков Михаил
"""
'''
 Расчитыаются зоны безопасности для каждой точки
 для ИИ и для игрока. Устанавливается правило
 постановки знака ИИ там где своя безопасная зона 
 и опасная зона игрока, можно по случайности.
 
'''

import tkinter as tk

def init_1():
    # начальные значения для игрока и ИИ
    # нумерация зон по числам, [ряд, столбец, безопасность, кто в точке]
    # 0 - безопасно, 1 - рядом 1 точка 5 - проигрыш
    # 0 - никого, 1 - ИИ, 2 - игрок
    zone = {}
    for i in range(100):
        x = i % 10
        y = i // 10
        zone[i]= [x,y,0,0]
    return zone

def proigrysh_ii():
    # Процедура проигрыша
    #label.config(text='Проиграл ИИ')
    global text1
    text1 = 'Проиграл ИИ'

    print('Проиграл ИИ')
    pass
def proigrysh_man():
    global text1
    text1 = 'Проиграл человек'
    print('Проиграл человек')
    pass

def analize_zone(a):
    sum_ii = 0
    sum_man = 0
    podryad = 0
    podryad_prev = 0
    podryad_man = 0
    podryad_prev_man = 0
    for i in range(len(a)):
        if podryad >= podryad_prev:
            # Вычисляем наибольший ряд совпадений для ии
            podryad_prev = podryad
        if podryad_man >= podryad_prev_man:
            # Вычисляем наибольший ряд совпадений для человека
            podryad_prev_man = podryad_man
        if a[i][3] == 1:
            sum_ii += 1
            podryad += 1
        else:
            podryad = 0
            
        if a[i][3] == 2:
            sum_man += 1
            podryad_man += 1
        else:
            podryad_man = 0

    for i in range(len(a)):
        # Заполняем значениями
        #TODO как будет формироваться итоговая оценка по сумме или нет
        if podryad_prev >= 1 and a[i][2]<podryad_prev:
            a[i][2] = podryad_prev
        if podryad_prev >= 3:
            # если перед проигрышем то максимальный статус безопасности
            a[i][2] = 9
        if podryad_prev > 4:
            # проигрыш ии
            proigrysh_ii()
            
            
       
        if podryad_prev_man >= 1 and a[i][2]<podryad_prev_man:
            a[i][2] = podryad_prev_man
        if podryad_prev_man >= 3:
            # если перед проигрышем то максимальный статус безопасности
            a[i][2] = 9
        if podryad_prev_man > 4:
            proigrysh_man()

    '''
    @Расчет безопасности
    Если Сумма какого либо параметра >= 5 то проигрыш
    соответственно (вызов процедуры)
    Если менее 5 то поиск подряд идущих, после чего
    необходимо проставить в незанятые ячейки безопасность,
    соответственно числу максимально занятых (не важно кем)
    в сами ячейки выставить максимальный ключ безопасности 9
    в случае если подряд идет 4 + 4 одного игрока ставить 
    максимальный тэг безопасности
    '''
    
    return a
    
    
def search_around(zone):
    # поиск окружающих точек
    # установка знака безопасности
    #TODO Добавить проверку по горизонтали и вертикали
    # После основной проверки 
    a, b = [], []
    
    for i in range(10):
        # 10 рядов и 10 строк
        # 10 столбцов
        #print(i)
        a = [zone[i], zone[10 + i], zone[20 + i], zone[30 + i],\
               zone[40 + i], zone[50 + i], zone[60 + i], zone[70 + i],\
               zone[80 + i], zone[90 + i]]
        # Вставляем проверку по вертикали
        for j in range(10):
            zone[i+10*j][2] = a[j][2]
        a = analize_zone(a)
        # затем 10 строк
        b = [zone[i * 10], zone[1 + i * 10], zone[2 + i * 10],\
               zone[3 + i * 10], zone[4 + i * 10], zone[5 + i * 10],\
               zone[6 + i * 10], zone[7 + i * 10],\
               zone[8 + i * 10], zone[9 + i * 10]]
        # Вставляем проверку по горизонтали
        b = analize_zone(b)
        # функция занесения параметров в изначальный массив
        for j in range(10):
            zone[i*10+j][2] = b[j][2]
        #zone[i]
        #print(a,b)
    return zone

def set_ii(zone):
    # сначала ставим с наименьшим приоритетом
    # затем со следующим.
    x = []
    #print(zone)
    # уберем занятые клетки  и посчитаем 1ш уровень безопасности
    for ind in zone:
        x.append(zone[ind][2])
    st1=min(x)
    for ind in zone:
        #print(ind)
        if zone[ind][3] == 0 and zone[ind][2] == st1:
            zone[ind][3] = 1
            break

    # возвращаем номер поставленной кнопки        
    return ind


def main():
    global zone_ii
    global btn_clicked
    global btn_present
    btn_present = []
    btn_clicked = []
    zone_ii = init_1()
    #zone_ii = search_around(zone_ii)
    def clicked(btn):
        # проверка на уже кликнутую кнопку
        global zone_ii
        global btn_clicked
        global btn_present
        zone_ii = search_around(zone_ii)
        if btn not in btn_clicked:
            btn_clicked.append(btn)
            btn.config(text='+')
            #a = str(btn.grid_info[7:-8])
            # размещаем обработку массива
            # добавляем человека в массив
            zone_ii[int(btn.winfo_name())][3] = 2
            zone_ii = search_around(zone_ii)
            a = set_ii(zone_ii)
            btn_present[a].config(text='0')
            btn_clicked.append(btn_present[a])
            zone_ii = search_around(zone_ii)
            lbl.config(text=text1)
            # затем установку новой клетки ии
            #TODO добавить отсечение значений уже нажатых кнопок
            # отрисовка всех кнопок


    root = tk.Tk()
    root.geometry('400x400+200+200')
    root.resizable(False, False)
    root.title('10х10 избегай 5 в ряд')
    
    for i in range(10):
        for j in range(10):
            '''
            создаем 100 фреймов с кнопками
            .!frame2.!button
            .!frame101.!button'''
            frame = tk.Frame(
                master=root,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j)
            btn = tk.Button(master=frame, text=' ', name = str(i*10+j))
            btn.config(command = lambda btn = btn: clicked(btn))
            btn_present.append(btn)
            btn.pack()
    frame = tk.Frame(
        master=root
    )
    
    frame.grid()
    global text1
    text1 = ''
    lbl = tk.Label(master=frame, text=text1)
    lbl.pack()
    
    
    
    root.mainloop()
    
    
    pass











if __name__ == "__main__":
    main()