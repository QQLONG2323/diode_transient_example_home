import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import main_01
import itertools


class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("T3STER SI")
        self.geometry("")
        
        # 先選擇插孔
        LP220_S1_frame = ttk.LabelFrame(self, text="LP220")
        LP220_S1_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NSEW) 
        
        LP220_S3_frame = ttk.LabelFrame(self, text="LP220")
        LP220_S3_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.NSEW)

        MS401_S5_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S5_frame.grid(column=2, row=0, padx=10, pady=10, sticky=tk.NSEW)

        MS401_S6_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S6_frame.grid(column=3, row=0, padx=10, pady=10, sticky=tk.NSEW)

        MS401_S7_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S7_frame.grid(column=4, row=0, padx=10, pady=10, sticky=tk.NSEW)

        MS401_S8_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S8_frame.grid(column=5, row=0, padx=10, pady=10, sticky=tk.NSEW)

        TH800_S9_frame = ttk.LabelFrame(self, text="TH800")
        TH800_S9_frame.grid(column=6, row=0, padx=10, pady=10, sticky=tk.NSEW)

        TH800_S10_frame = ttk.LabelFrame(self, text="TH800")
        TH800_S10_frame.grid(column=7, row=0, padx=10, pady=10, sticky=tk.NSEW)
        

        self.SCh_radio = {
            "S1Ch1": ["Current_source", "Voltage_source"],
            "S1Ch2": ["Current_source", "Voltage_source"],
            "S3Ch1": ["Current_source", "Voltage_source"],
            "S3Ch2": ["Current_source", "Voltage_source"],
            "S5Ch1": ["Current_source", "Measurement_channel", "Both"],
            "S5Ch2": ["Current_source", "Measurement_channel", "Both"],
            "S5Ch3": ["Current_source", "Measurement_channel", "Both"],
            "S5Ch4": ["Current_source", "Measurement_channel", "Both"],
            "S6Ch1": ["Current_source", "Measurement_channel", "Both"],
            "S6Ch2": ["Current_source", "Measurement_channel", "Both"],
            "S6Ch3": ["Current_source", "Measurement_channel", "Both"],
            "S6Ch4": ["Current_source", "Measurement_channel", "Both"],
            "S7Ch1": ["Current_source", "Measurement_channel", "Both"],
            "S7Ch2": ["Current_source", "Measurement_channel", "Both"],
            "S7Ch3": ["Current_source", "Measurement_channel", "Both"],
            "S7Ch4": ["Current_source", "Measurement_channel", "Both"],
            "S8Ch1": ["Current_source", "Measurement_channel", "Both"],
            "S8Ch2": ["Current_source", "Measurement_channel", "Both"],
            "S8Ch3": ["Current_source", "Measurement_channel", "Both"],
            "S8Ch4": ["Current_source", "Measurement_channel", "Both"],
            "S9Ch1": ["Thermometer"],
            "S9Ch2": ["Thermometer"],
            "S9Ch3": ["Thermometer"],
            "S9Ch4": ["Thermometer"],
            "S9Ch5": ["Thermometer"],
            "S9Ch6": ["Thermometer"],
            "S9Ch7": ["Thermometer"],
            "S9Ch8": ["Thermometer"],
            "S10Ch1": ["Thermometer"],
            "S10Ch2": ["Thermometer"],
            "S10Ch3": ["Thermometer"],
            "S10Ch4": ["Thermometer"],
            "S10Ch5": ["Thermometer"],
            "S10Ch6": ["Thermometer"],
            "S10Ch7": ["Thermometer"],
            "S10Ch8": ["Thermometer"]      
        }


        # 創建 Checkbutton 和 RadioButton 的框架
        self.check_sensor = {}   # 儲存 Checkbutton 的變量對象(BooleanVar)
        self.check_radio = {}   # 儲存 RadioButton 中當前選中的選項
        self.radio_buttons_list = {}   # 儲存 Checkbutton 對應的 RadioButton 列表
        self.saved_parameters = {}  # 儲存每個 RadioButton 的參數


        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S1_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(LP220_S1_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2, 4)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S3_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(LP220_S3_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)



        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 4, 8)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S5_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(MS401_S5_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 8, 12)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S6_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(MS401_S6_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 12, 16)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S7_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(MS401_S7_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 16, 20)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S8_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(MS401_S8_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 20, 28)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S9_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(TH800_S9_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 28, 36)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S10_frame, text=text, variable=check_sensor, command=lambda t=text: self.open_parameter_window(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(TH800_S10_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled", command=lambda opt=option: self.open_parameter_window(opt))
            #     radio_buttons_list.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_buttons_list)              
     

    def open_parameter_window(self, text):        
        """彈出一個填寫參數的表單視窗"""
        param_window = tk.Toplevel(self)
        param_window.title(f"{text}")
        param_window.geometry("300x200")

        ttk.Label(param_window, text="請輸入參數:").pack(padx=10, pady=10)

        # 創建參數輸入框
        param_entry = ttk.Entry(param_window)
        param_entry.pack(padx=10, pady=10)

        # 如果之前有保存過該 RadioButton 的參數，則填入到輸入框中
        if (text) in self.saved_parameters:
            param_entry.insert(0, self.saved_parameters[(text)])

        button_frame = ttk.Frame(param_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="提交", command=lambda: self.submit_parameters(param_entry.get(),text, param_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=param_window.destroy).pack(side=tk.LEFT, padx=5)

    def submit_parameters(self, params, option, window):
        """處理提交的參數並保存"""
        self.saved_parameters[(option)] = params  # 保存參數
        print(f"提交的參數 ({option}): {params}")
        window.destroy()  # 關閉窗口  

    
    
    
    






if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()