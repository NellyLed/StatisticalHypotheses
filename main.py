#!/usr/bin/env python
#coding: utf-8

import numpy as np
from scipy.stats import chi2
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import requests

ALPHABET = ('абвгдеёжзиклмнопрстуфхчшщъыьэюя'
            'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')

#шифрование текста методом Цезаря
def shifr_func(text, k):
    letters = []
    for letter in text:
        if letter.isalpha():
            alph_index = ord("А") if letter.istitle() else ord("а")
            letters.append(chr((ord(letter) - alph_index + k) % 33 + alph_index))
        else:
            letters.append(letter)
    res="".join(letters)
    return res

#дешифрование текста методом Цезаря
def deshifr_func(text, k):
    letters = []
    for letter in text:
        if letter.isalpha():
            alph_index = ord("А") if letter.istitle() else ord("а")
            letters.append(chr((ord(letter) - alph_index - k) % 33 + alph_index))
        else:
            letters.append(letter)
    res="".join(letters)
    return res

#эталонное распределение
def select_func(test):
    char_list = list(test)
    df = pd.DataFrame({'chars': char_list})
    df = df[df.chars != ' ']
    df['num'] = 1
    df = df.groupby('chars').sum().sort_values('num', ascending=False) / len(df)
    return df

#критерий Пирсона
def Pircone(ndeg,alfa):
    x = np.linspace(chi2.ppf(alfa, ndeg), chi2.ppf(1.0 - alfa, ndeg), 100)
    return x

#построение графика
def Graf(name):
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(name)
    plt.grid(True)
    plt.show()

def encryption_caesar(msg, offset):
    encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
    encrypted = []
    for char in msg:
        index = get_char_index(char, ALPHABET)
        encrypted_char = encrypted_alphabet[index] if index >= 0 else char
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

#индекс символа в строке
def get_char_index(char, alphabet):
    char_index = alphabet.find(char)
    return char_index

#поиск вхождений слов из словаря
def decryption_caesar(msg, offset=None):
    encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
    decrypted = []
    ff_1=open('auto.txt', "r", encoding="utf-8")
    dictionary=['Уже', 'пока', 'что']
    for offset in range(len(ALPHABET)):
        # Каждого смещения, начиная с 0 создаем смещенный алфавит
        encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
        for char in msg:
            index = get_char_index(char, encrypted_alphabet)
            encrypted_char = ALPHABET[index] if index >= 0 else char
            decrypted.append(encrypted_char)
        decrypted = ''.join(decrypted)
        for word in dictionary:
            # Если слово из словаря входит в дешифрованную строку,
            # возвращаем её
            if word in decrypted:
                return decrypted
        decrypted = []  # Обнуляем расшифрованное сообщение
    return 'Не удалось расшифровать сообщение %s' % msg

if __name__ == '__main__':
    #шифрование
    a = input("Хотите зашифровать текст?")
    if a == 'да':
        fi1 = input("Введите файл с текстом для шифрования:")
        f = open(fi1, "r", encoding="utf-8")
        text = f.read()
        k = int(input("Параметр шифрования: "))
        print("Результат: " + '\n' + shifr_func(text, k))
        m = str(shifr_func(text, k))
        f.close()
    else:
        if a == 'нет':
            print('Идем далее')

    #дешифрование
    a2 = input("Хотите дешифровать текст?")
    if a2 == 'да':
        fi2 = input("Введите файл с текстом для дешифрования:")
        ff = open(fi2, 'w', encoding="utf-8")  # открытие в режиме записи
        ff.seek(0)
        ff.write(m)
        k1 = int(input("Параметр шифрования: "))
        print("Результат: " + '\n' + deshifr_func(m, k1))
        ff.close()
    else:
        if a2 == 'нет':
            print('Идем далее')

    #эталонное распределение
    e1 = input("Построить эталонное распределение по буквам?")
    if e1 == 'да':
        fi3 = input("Введите файл с текстом для построения эталонного распределения:")
        f2 = open(fi3, "r", encoding="utf-8")
        text_2 = f2.read()
        plt.bar(select_func(text_2).index, select_func(text_2).num, width=0.5, color='orange',
                label='Эталонное распределение')
        print(Graf('Эталонное распределение'))
    else:
        if e1 == 'нет':
            print('Идем далее')

    #распределение хи-квадрат
    e2 = input("Построить распределение хи-квадрат встречаемости различных букв?")
    if e2 == 'да':
        fi4 = input("Введите файл с текстом для построения распределения хи-квадрат:")
        f3 = open(fi4, "r", encoding="utf-8")
        text_3 = f3.read()
        ch_s = len(text_3)
        print("Число степеней свободы равно:", ch_s)
        alfa = 0.01
        print("Уровень значимости:", alfa)
        plt.plot(Pircone(ch_s, alfa), chi2.pdf(Pircone(ch_s, alfa), ch_s), label='Критерий Пирсона', color='blue', lw=2)
        print(Graf('Критерий Пирсона'))
    else:
        if e2 == 'нет':
            print('Идем далее')

    #сравнение
    e3 = input("Проверить соответствие эталонного и хи-квадрат распределения?")
    if e3 == 'да':
        fi5 = input("Введите файл с текстом, использующийся в распределении:")
        f4 = open(fi5, "r", encoding="utf-8")
        text_4 = f4.read()
        km1 = select_func(text_4).num
        print('Число степеней свободы:')
        ch_s_1=len(text_4)
        print(ch_s_1)
        alfa_1=0.01
        print('Уровень значимости:',alfa_1)
        km2 = Pircone(ch_s_1, alfa_1)
        U1, p = mannwhitneyu(km1, km2, method="exact")
        print('Коэффициент равенства распределений:', U1)
    else:
        if e3 == 'нет':
            print('Идем далее')

    #автоматическая дешифрация
    e4 = input("Расшифровать текст автоматически?")
    if e4 == 'да':
        fi1 = input("Введите файл с исходным текстом:")
        ff_3=open(fi1, "r", encoding="utf-8")
        message=ff_3.read()
        k1 = int(input("Параметр шифрования: "))
        print('Исходный текст: %s' % message)
        message_1 = encryption_caesar(message, k1)
        print('Зашифрованный текст: %s' % message_1)
        print('Расшифрованный текст: %s' % decryption_caesar(message_1))
    else:
        if e4=='нет':
            print('Конец кода')

