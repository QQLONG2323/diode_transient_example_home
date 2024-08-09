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

        self.title("Parameter Configuration")
        self.geometry("")
        
        # 先選擇插孔
        LP220_S1_frame = ttk.LabelFrame(self, text="先選擇插孔 LP220 S1")
        LP220_S1_frame.grid(column=1, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        LP220_S3_frame = ttk.LabelFrame(self, text="先選擇插孔 LP220 S3")
        LP220_S3_frame.grid(column=3, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        MS401_S5_frame = ttk.LabelFrame(self, text="先選擇插孔 MS401 S5")
        MS401_S5_frame.grid(column=5, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        MS401_S6_frame = ttk.LabelFrame(self, text="先選擇插孔 MS401 S6")
        MS401_S6_frame.grid(column=7, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        MS401_S7_frame = ttk.LabelFrame(self, text="先選擇插孔 MS401 S7")
        MS401_S7_frame.grid(column=9, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        MS401_S8_frame = ttk.LabelFrame(self, text="先選擇插孔 MS401 S8")
        MS401_S8_frame.grid(column=11, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        TH800_S9_frame = ttk.LabelFrame(self, text="先選擇插孔 TH800 S9")
        TH800_S9_frame.grid(column=13, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)

        TH800_S10_frame = ttk.LabelFrame(self, text="先選擇插孔 TH800 S10")
        TH800_S10_frame.grid(column=15, row=1, padx=10, pady=10, sticky=tk.EW, rowspan=2)
        
        

        # self.LP220_S1Ch1 = tk.BooleanVar()
        # self.LP220_S1Ch2 = tk.BooleanVar()
        # self.LP220_S3Ch1 = tk.BooleanVar()
        # self.LP220_S3Ch2 = tk.BooleanVar()
        # self.MS401_S5Ch1 = tk.BooleanVar()
        # self.MS401_S5Ch2 = tk.BooleanVar()
        # self.MS401_S5Ch3 = tk.BooleanVar()
        # self.MS401_S5Ch4 = tk.BooleanVar()
        # self.MS401_S6Ch1 = tk.BooleanVar()
        # self.MS401_S6Ch2 = tk.BooleanVar()
        # self.MS401_S6Ch3 = tk.BooleanVar()
        # self.MS401_S6Ch4 = tk.BooleanVar()
        # self.MS401_S7Ch1 = tk.BooleanVar()
        # self.MS401_S7Ch2 = tk.BooleanVar()
        # self.MS401_S7Ch3 = tk.BooleanVar()
        # self.MS401_S7Ch4 = tk.BooleanVar()
        # self.MS401_S8Ch1 = tk.BooleanVar()
        # self.MS401_S8Ch2 = tk.BooleanVar()
        # self.MS401_S8Ch3 = tk.BooleanVar()
        # self.MS401_S8Ch4 = tk.BooleanVar()
        # self.TH800_S9Ch1 = tk.BooleanVar()
        # self.TH800_S9Ch2 = tk.BooleanVar()
        # self.TH800_S9Ch3 = tk.BooleanVar()
        # self.TH800_S9Ch4 = tk.BooleanVar()
        # self.TH800_S9Ch5 = tk.BooleanVar()
        # self.TH800_S9Ch6 = tk.BooleanVar()
        # self.TH800_S9Ch7 = tk.BooleanVar()
        # self.TH800_S9Ch8 = tk.BooleanVar()
        # self.TH800_S10Ch1 = tk.BooleanVar()
        # self.TH800_S10Ch2 = tk.BooleanVar()
        # self.TH800_S10Ch3 = tk.BooleanVar()
        # self.TH800_S10Ch4 = tk.BooleanVar()
        # self.TH800_S10Ch5 = tk.BooleanVar()
        # self.TH800_S10Ch6 = tk.BooleanVar()
        # self.TH800_S10Ch7 = tk.BooleanVar()
        # self.TH800_S10Ch8 = tk.BooleanVar()
        # ttk.Checkbutton(S_Ch_frame, text="LP220_S1Ch1", variable=self.LP220_S1Ch1).grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="LP220_S1Ch2", variable=self.LP220_S1Ch2).grid(column=1, row=0, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="LP220_S3Ch1", variable=self.LP220_S3Ch1).grid(column=2, row=0, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="LP220_S3Ch2", variable=self.LP220_S3Ch2).grid(column=3, row=0, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S5Ch1", variable=self.MS401_S5Ch1).grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S5Ch2", variable=self.MS401_S5Ch2).grid(column=1, row=1, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S5Ch3", variable=self.MS401_S5Ch3).grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S5Ch4", variable=self.MS401_S5Ch4).grid(column=3, row=1, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S6Ch1", variable=self.MS401_S6Ch1).grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S6Ch2", variable=self.MS401_S6Ch2).grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S6Ch3", variable=self.MS401_S6Ch3).grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S6Ch4", variable=self.MS401_S6Ch4).grid(column=3, row=2, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S7Ch1", variable=self.MS401_S7Ch1).grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S7Ch2", variable=self.MS401_S7Ch2).grid(column=1, row=3, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S7Ch3", variable=self.MS401_S7Ch3).grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S7Ch4", variable=self.MS401_S7Ch4).grid(column=3, row=3, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S8Ch1", variable=self.MS401_S8Ch1).grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S8Ch2", variable=self.MS401_S8Ch2).grid(column=1, row=4, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S8Ch3", variable=self.MS401_S8Ch3).grid(column=2, row=4, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="MS401_S8Ch4", variable=self.MS401_S8Ch4).grid(column=3, row=4, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch1", variable=self.TH800_S9Ch1).grid(column=0, row=5, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch2", variable=self.TH800_S9Ch2).grid(column=1, row=5, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch3", variable=self.TH800_S9Ch3).grid(column=2, row=5, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch4", variable=self.TH800_S9Ch4).grid(column=3, row=5, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch5", variable=self.TH800_S9Ch5).grid(column=0, row=6, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch6", variable=self.TH800_S9Ch6).grid(column=1, row=6, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch7", variable=self.TH800_S9Ch7).grid(column=2, row=6, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S9Ch8", variable=self.TH800_S9Ch8).grid(column=3, row=6, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch1", variable=self.TH800_S10Ch1).grid(column=0, row=7, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch2", variable=self.TH800_S10Ch2).grid(column=1, row=7, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch3", variable=self.TH800_S10Ch3).grid(column=2, row=7, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch4", variable=self.TH800_S10Ch4).grid(column=3, row=7, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch5", variable=self.TH800_S10Ch5).grid(column=0, row=8, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch6", variable=self.TH800_S10Ch6).grid(column=1, row=8, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch7", variable=self.TH800_S10Ch7).grid(column=2, row=8, sticky=tk.W, padx=10, pady=5)
        # ttk.Checkbutton(S_Ch_frame, text="TH800_S10Ch8", variable=self.TH800_S10Ch8).grid(column=3, row=8, sticky=tk.W, padx=10, pady=5)

        SCh_radio = {
            "LP220_S1Ch1": ["Current_source", "Voltage_source"],
            "LP220_S1Ch2": ["Current_source", "Voltage_source"],
            "LP220_S3Ch1": ["Current_source", "Voltage_source"],
            "LP220_S3Ch2": ["Current_source", "Voltage_source"],
            "MS401_S5Ch1": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S5Ch2": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S5Ch3": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S5Ch4": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S6Ch1": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S6Ch2": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S6Ch3": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S6Ch4": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S7Ch1": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S7Ch2": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S7Ch3": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S7Ch4": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S8Ch1": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S8Ch2": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S8Ch3": ["Current_source", "Measurement_channel", "Both"],
            "MS401_S8Ch4": ["Current_source", "Measurement_channel", "Both"],
            "TH800_S9Ch1": ["Thermometer"],
            "TH800_S9Ch2": ["Thermometer"],
            "TH800_S9Ch3": ["Thermometer"],
            "TH800_S9Ch4": ["Thermometer"],
            "TH800_S9Ch5": ["Thermometer"],
            "TH800_S9Ch6": ["Thermometer"],
            "TH800_S9Ch7": ["Thermometer"],
            "TH800_S9Ch8": ["Thermometer"],
            "TH800_S10Ch1": ["Thermometer"],
            "TH800_S10Ch2": ["Thermometer"],
            "TH800_S10Ch3": ["Thermometer"],
            "TH800_S10Ch4": ["Thermometer"],
            "TH800_S10Ch5": ["Thermometer"],
            "TH800_S10Ch6": ["Thermometer"],
            "TH800_S10Ch7": ["Thermometer"],
            "TH800_S10Ch8": ["Thermometer"]      
        }

        # 創建 Checkbutton 和 RadioButton 的框架
        self.check_sensor = {}   # 儲存 Checkbutton 的變量對象(BooleanVar)
        self.check_radio = {}   #儲存 RadioButton 中當前選中的選項
        self.radio_buttons_list = {}   #儲存 Checkbutton 對應的 RadioButton 列表

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 2)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S1_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # 創建 RadioButton 框架
            check_radio = tk.StringVar(value=radio_options[0])
            self.check_radio[text] = check_radio
            radio_button_frame = ttk.Frame(LP220_S1_frame)
            radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            self.radio_buttons_list[text] = []

            for j, option in enumerate(radio_options):
                radio_buttons_list = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled")
                radio_buttons_list.pack(side=tk.LEFT, padx=2)
                self.radio_buttons_list[text].append(radio_buttons_list)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 2, 4)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S3_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)



        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 4, 8)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S5_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 8, 12)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S6_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 12, 16)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S7_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 16, 20)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S8_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 20, 28)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S9_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (text, radio_options) in enumerate(itertools.islice(SCh_radio.items(), 28, 36)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[text] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S10_frame, text=text, variable=check_sensor, command=lambda t=text: self.toggle_radiobuttons(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

            # # 創建 RadioButton 框架
            # check_radio = tk.StringVar(value=radio_options[0])
            # self.check_radio[text] = check_radio
            # radio_button_frame = ttk.Frame(LP220_S1_frame)
            # radio_button_frame.grid(column=1, row=i, sticky=tk.W, padx=10, pady=5)
            # self.radio_buttons_list[text] = []

            # for j, option in enumerate(radio_options):
            #     radio_button = tk.Radiobutton(radio_button_frame, text=option, variable=check_radio, value=option, state="disabled")
            #     radio_button.pack(side=tk.LEFT, padx=2)
            #     self.radio_buttons_list[text].append(radio_button)

    def toggle_radiobuttons(self, text):
        """切換 RadioButton 的狀態"""
        if self.check_vars[text].get():
            for radio_button in self.radio_buttons[text]:
                radio_button.configure(state="normal")
        else:
            for radio_button in self.radio_buttons[text]:
                radio_button.configure(state="disabled")






if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()