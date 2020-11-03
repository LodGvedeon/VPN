""" Модуль содержит реализацию класса Application. Класс строит графическое
	приложение, по нажатии кнопки позволяющее сортировать списки vpn по 
	заданным параметрам - скорость, безопасность, сервера, шифрование, цена. 
	Интересуемые параметры выделються красными цветом. Так же при наведении 
	курсора на надпись "Шифрование" будет всплывать информационная подсказка.
	При отрытии окна на весь экран, приложение не мастшабируеться, но 
	выравниваеться по центру.

	В настоящем модуле используютсья библиотеки pandas, numpy, tkinter и 
	idleliv.tooptip.

"""

import pandas as pd
import numpy as np

import tkinter as tk
import idlelib.tooltip as idl 


class Application():
	""" Класс Приложение. Конструктор принимает эксель-таблицу с характеристиками
		VPN и .txt файл с содержанием вспылвающей подсказки tooltip.

		stcurctApi = таблица pd.DataFrame, которая предназначена для хранения всех
		виджетов конструктора.

		row, col = количество строк и столбцов в structApi.

		TextList = коллекция pd.Series со str названиями столбцов scructApi. 
		Используеться в работе для как текстовый параметр виджетов.
	
		ws = виджет Frame, в котором геометрически размещаються виджеты.

		Конструктор по заданному порядкуциклически заносит в scructApi виджеты 
		Label, Entry и Button. Обращение к виджетам по индексам таблицы structApi.

	"""
	def __init__(self, data:pd.DataFrame, tooltip):

		self.data = data
		self.tooltip = tooltip

		self.row = 8
		self.col = 6

		self.structApl = pd.DataFrame(np.zeros((self.row, self.col)))

		self.TextList = pd.Series(["Название","Скорость", "Безопасность", "Сервера",
														 "Шифрование", "Цена"])
		ws = tk.Frame()
		ws.pack(expand=1)

		for i in range(self.row):
			for j in range(self.col):

				if i == 0:
					self.structApl.loc[i, j] = tk.Label(ws, text=self.TextList[j])
					self.structApl.loc[i, j].grid(row=i, column=j)

					if j == 4:
						comments = idl.Hovertip(self.structApl.loc[i, j], text=self.tooltip)

				if i in (1, 3, 5):
					size = (30 if j == 0 else 15)
					self.structApl.loc[i, j] = tk.Entry(ws, width=size)
					self.structApl.loc[i, j].grid(row=i, column=j)

				if i == 7:
					if j != 0:
						size = 10
						self.structApl.loc[i, j] = tk.Button(ws, width=size, text="+", bg='khaki')
						self.structApl.loc[i, j].grid(row=i, column=j)
						self.structApl.loc[i, j].bind("<Button-1>", self.clickprocessing)

				if i in (2, 4, 6, 7):
					if j == 0:
						text = ("СевГУ, кафедра ИВТ, 2020" if i == 7 else "* * *" )
						self.structApl.loc[i, j] = tk.Label(ws, text=text)
						self.structApl.loc[i, j].grid(row=i, column=j)

	def cleartext(self):
		""" Метод удаления текста из виджетов Entry, размещенный в классе.
			Циклически удаляет текст с помощью встроенного метода delete из
			класса Enrty. Автоматически срабатывает привызове классового 
			метода clickprocessing.

		"""
		for i in range(self.row):
			for j in range(self.col):
				if i in (1, 3, 5):
					self.structApl.loc[i, j].delete(first=0, last=100)

	def reverse(self, text:str):
		arr = ['PPTP', 'SSTP', 'IKEv2', 'L2TP/IPSec', 
				'Wireguard', 'OpenVPN']
		for i in range(6):
			if text == str(i+5):
				text = arr[i]
		return text 

	def clickprocessing(self, event):
		""" Интеллектуальный метод-обработчик события "<Button-1>" для 4-х 
			виджетов Button, размещенных в классе. Метод по параметру 
			event.widget и вытекающим из него key, value, asc, view и text
			определяет конкретное поведение обработки события.

			key, value = индекс и значение стобца data. Эти параметры 
			сопоставляют с индексом и значением из sctructApi для 
			опознания источника вызова event. 

			asc = булевый параметр для метода sort_values из модуля Pandas, 
			логически определяемый по ходу работы данного метода. В методе 
			sort_values определяет сортировку: по возрастанию (Trut) или по
			убыванию (False)

			view = отсортированая копия data c новыми индексами. 

			ind = коллекция типа pd.Series,использованная как ограничение в 
			цикле.

			text = str параметр, который передаеться в виджеты Entry.

		"""
		self.cleartext()
		key, value = None, None
		asc = False
		for i in range(len(self.TextList)):
			if event.widget == self.structApl.iloc[7, i]:
				key, value = i, self.TextList[i]
				asc = (True if i == 5 else False)

		view = self.data.sort_values(value, ascending=asc).reset_index(drop=True)
		ind = pd.Series([1, 3, 5])
		for i in range(self.row):
			for j in range(self.col):
				if i in ind: 
					self.structApl.iloc[ind[i], j]['fg'] = 'black'
					self.structApl.iloc[ind[i], key]['fg'] = 'red'
					text = str(view.iloc[i, j])
					if j == 4:
						text = self.reverse(text)
					self.structApl.iloc[ind[i], j].insert(0, string=text)


def main():
	""" Исполнительная часть программы. 

		read = прочтение эксель файла "vpn"
		comments = прочтение текстового файла "tooltip"
		data = создание таблицы pd.DataFrame из read
		window = вызов метода tkinter для создания окна в операционной системе.
		window.title = подписываем  заголовок окна.
		vpn = создание экземпляра класса Application с заданными параметрами.
		window.mainloop = отобразить окно window в используемой ОС.

	"""

	read = pd.read_excel("vpn.xlsx")
	comments = open("tooltip.txt").read()
	data = pd.DataFrame(read)

	window = tk.Tk()
	window.title("vpnChoose")

	vpn = Application(data, comments)

	window.mainloop()


if __name__ == '__main__':
	main()


	





