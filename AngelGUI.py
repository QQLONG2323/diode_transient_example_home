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

        # 定義每個感測器的選項
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

        # 定義每個選項對應的表單結構
        self.SCh_radio_parameters = {
            "S1_S3_Current_source": [
                ("Output mode", ["Off", "Switching", "On"]),
                ("Current [A]", "entry"),
                ("Voltage limit [V]", "entry")
            ],
            "S1_S3_Voltage_source": [
                ("Output mode", ["Off", "On", "Switching"]),
                ("On-state voltage [V]", "entry"),
                ("Current limit [A]", "entry")
            ],
            "S5_S8_Current_source": [
                ("Output mode", ["Off", "On"]),
                ("Range", ["-0.2 A ~ 0.2 A",
                 "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"]),
                ("Current [A]", "entry")
            ],
            "S5_S8_Measurement_channel": [
                ("Sensitivity [mV/K]", "entry"),
                ("Auto range", ["On", "Off"]),
                ("Range", ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
                           "Fall scale: 10 V, V(in): -10 V ~ 10 V",
                           "Fall scale: 4 V, V(in): -10 V ~ 10 V",
                           "Fall scale: 2 V, V(in): -10 V ~ 10 V",
                           "Fall scale: 1 V, V(in): -10 V ~ 10 V",
                           "Fall scale: 20 V, V(in): -20 V ~ 20 V",
                           "Fall scale: 8 V, V(in): -20 V ~ 20 V",
                           "Fall scale: 4 V, V(in): -20 V ~ 20 V",
                           "Fall scale: 40 V, V(in): -40 V ~ 40 V",
                           "Fall scale: 16 V, V(in): -40 V ~ 40 V",
                           "Fall scale: 8 V, V(in): -40 V ~ 40 V",
                           "Fall scale: 32 V, V(in): -80 V ~ 80 V",
                           "Fall scale: 16 V, V(in): -80 V ~ 80 V",
                           "Fall scale: 8 V, V(in): -80 V ~ 80 V",
                           ]
                 ),
                ("Vref [V]", "entry"),
                ("Separate Vref for heating", ["On", "Off"])
            ],
            "S5_S8_Both": [
                # Combine both lists here
                *[
                    ("Output mode", ["Off", "On"]),
                    ("Range", ["-0.2 A ~ 0.2 A",
                     "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"]),
                    ("Current [A]", "entry")
                ],
                *[
                    ("Sensitivity [mV/K]", "entry"),
                    ("Auto range", ["On", "Off"]),
                    ("Range", ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
                               "Fall scale: 10 V, V(in): -10 V ~ 10 V",
                               "Fall scale: 4 V, V(in): -10 V ~ 10 V",
                               "Fall scale: 2 V, V(in): -10 V ~ 10 V",
                               "Fall scale: 1 V, V(in): -10 V ~ 10 V",
                               "Fall scale: 20 V, V(in): -20 V ~ 20 V",
                               "Fall scale: 8 V, V(in): -20 V ~ 20 V",
                               "Fall scale: 4 V, V(in): -20 V ~ 20 V",
                               "Fall scale: 40 V, V(in): -40 V ~ 40 V",
                               "Fall scale: 16 V, V(in): -40 V ~ 40 V",
                               "Fall scale: 8 V, V(in): -40 V ~ 40 V",
                               "Fall scale: 32 V, V(in): -80 V ~ 80 V",
                               "Fall scale: 16 V, V(in): -80 V ~ 80 V",
                               "Fall scale: 8 V, V(in): -80 V ~ 80 V",
                               ]
                     ),
                    ("Vref [V]", "entry"),
                    ("Separate Vref for heating", ["On", "Off"])
                ]
            ],
            "S9_S10_Thermometer": [("Type", "entry"), ("Sensitivity", "entry"), ("Sample per sec", "entry")]
        }

        # 創建 Checkbutton 和 RadioButton 的框架
        self.check_sensor = {}   # 儲存 Sensor
        self.check_option = {}  # 儲存 Option
        self.saved_parameters = {}  # 儲存 Option 的參數
        self.form_widgets = {}   # 保存所有動態生成的表單控件
        # self.input_data = {}
        # self.widgets = {}

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                LP220_S1_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2, 4)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                LP220_S3_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 4, 8)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S5_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 8, 12)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S6_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 12, 16)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S7_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 16, 20)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S8_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 20, 28)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                TH800_S9_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 28, 36)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                TH800_S10_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # print_button = ttk.Button(self, text="Print Values", command=self.print_all_data)
        # print_button.grid(pady=10)

    # 只有在 Checkbutton 被勾選時才彈出視窗
    def handle_checkbutton(self, sensor):
        if self.check_sensor[sensor].get():
            self.open_parameter_window(sensor)
        else:
            self.check_option[sensor].set("")
            self.update_form(sensor, disable=True)

    # 彈出一個填寫參數的表單視窗

    def open_parameter_window(self, sensor):

        # 建立彈出視窗
        param_window = tk.Toplevel(self)
        param_window.title(f"{sensor}")
        param_window.geometry("")

        # 設定 LabelFrame 字體大小與粗體
        style = ttk.Style()
        style.configure("Large_Bold.TLabelframe.Label",
                        font=("System", 16, "bold"))

        # 建立頂端按鈕框架
        radio_frame = ttk.Frame(param_window)
        radio_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # 建立 LP220 所有的參數 table 框架
        S1_S3_Current_source_frame = ttk.LabelFrame(
            param_window, text="Current source", style="Large_Bold.TLabelframe")
        S1_S3_Current_source_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="ew")

        S1_S3_Voltage_source_frame = ttk.LabelFrame(
            param_window, text="Voltage source", style="Large_Bold.TLabelframe")
        S1_S3_Voltage_source_frame.grid(
            row=2, column=0, padx=20, pady=20, sticky="ew")

        # 建立 MS401 所有的參數 table 框架
        S5_S8_Current_source_frame = ttk.LabelFrame(
            param_window, text="Current source", style="Large_Bold.TLabelframe")
        S5_S8_Current_source_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="ew")

        S5_S8_Measurement_channel_frame = ttk.LabelFrame(
            param_window, text="Measurement channel", style="Large_Bold.TLabelframe")
        S5_S8_Measurement_channel_frame.grid(
            row=2, column=0, padx=20, pady=20, sticky="ew")

        # 建立 TH800 所有的參數 table 框架
        S9_S10_Thermometer_frame = ttk.LabelFrame(
            param_window, text="Thermometer", style="Large_Bold.TLabelframe")
        S9_S10_Thermometer_frame.grid(
            row=1, column=0, padx=20, pady=20, sticky="ew")

        # 建立提交、取消按鈕框架
        button_frame = ttk.Frame(param_window)
        button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # 取得對應的 RadioButton 選項
        radio_options = self.SCh_radio[sensor]

        # 檢查是否有保存的 RadioButton 選項
        default_radio_option = None
        for option in radio_options:
            if (sensor, option) in self.saved_parameters:
                default_radio_option = option
                break

        # 如果已經有保存的選項，將其作為預設選項，否則使用第一個選項
        check_option = tk.StringVar(
            value=default_radio_option or radio_options[0])
        self.check_option[sensor] = check_option  # 保存這個 sensor 的選擇變量

        # Radio 排版
        for i, option in enumerate(radio_options):
            tk.Radiobutton(radio_frame, text=option, variable=check_option, value=option, font=(
                "System", 16, "bold"), command=lambda: self.update_form(sensor)).grid(row=0, column=i+1, padx=20, pady=5)

        # # Retrieve saved parameters and pre-fill the form
        # if (sensor, check_option.get()) in self.saved_parameters:
        #     saved_params = self.saved_parameters[(sensor, check_option.get())]
        #     for widget, value in zip(self.form_widgets[sensor][check_option.get()], saved_params):
        #         if isinstance(widget, ttk.Combobox):
        #             widget.set(value)
        #         else:
        #             widget.insert(0, value)

        # 建立每個 Sensor 中的參數表單
        self.form_widgets[sensor] = {}   

        form_widgets_for_option_S1_S3_current_source = []
        form_widgets_for_option_voltage_source = []

        form_widgets_for_option_S5_S8_current_source = []
        form_widgets_for_option_Measurement_channel = []

        form_widgets_for_option_Thermometer = []

        # # 檢查是否有已保存的參數       
        # saved_parameters_for_sensor = self.saved_parameters.get((sensor, self.check_option[sensor].get()), [])

        # 獲取保存的參數，分別針對 Current_source 和 Voltage_source
        saved_parameters_for_current_source = self.saved_parameters.get((sensor, "Current_source"), [])
        saved_parameters_for_voltage_source = self.saved_parameters.get((sensor, "Voltage_source"), [])

        # 檢查如果有 Voltage_source 保存的參數，那麼禁用 Current_source，反之亦然
        if saved_parameters_for_voltage_source:
            current_source_state = "disabled"
            voltage_source_state = "normal"
        else:
            current_source_state = "normal"
            voltage_source_state = "disabled"
        
        

        if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
            # 填充 Current_source 表單
            for i, (label_text, field_type) in enumerate(self.SCh_radio_parameters["S1_S3_Current_source"]):
                ttk.Label(S1_S3_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_Current_source_frame, values=field_type, state=current_source_state)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_current_source 中的值
                    if i < len(saved_parameters_for_current_source):
                        combobox.set(saved_parameters_for_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(
                        combobox)
                else:
                    entry = ttk.Entry(S1_S3_Current_source_frame, state=current_source_state)  # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_current_source 中的值
                    if i < len(saved_parameters_for_current_source):
                        entry.insert(0, saved_parameters_for_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(entry)

            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1_S3_current_source
            
          

           
           
            # 填充 Voltage_source 表單
            for i, (label_text, field_type) in enumerate(self.SCh_radio_parameters["S1_S3_Voltage_source"]):
                ttk.Label(S1_S3_Voltage_source_frame,
                        text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_Voltage_source_frame, values=field_type, state=voltage_source_state)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_voltage_source 中的值
                    if i < len(saved_parameters_for_voltage_source):
                        print(f"回填 Voltage_source - Combobox: {saved_parameters_for_voltage_source[i]}")
                        combobox.set(saved_parameters_for_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(combobox)
                else:
                    entry = ttk.Entry(
                        S1_S3_Voltage_source_frame, state=voltage_source_state)  # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_voltage_source 中的值
                    if i < len(saved_parameters_for_voltage_source):
                        print(f"回填 Voltage_source - Entry: {saved_parameters_for_voltage_source[i]}")
                        entry.insert(0, saved_parameters_for_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(entry)

            # 保存填充的 Voltage_source
            self.form_widgets[sensor]["Voltage_source"] = form_widgets_for_option_voltage_source

            

            

               


        elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
            for i, (label_text, field_type) in enumerate(self.SCh_radio_parameters["S5_S8_Current_source"]):
                ttk.Label(S5_S8_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S5_S8_Current_source_frame, values=field_type, state="readonly")
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        combobox.set(saved_parameters_for_sensor[i])
                    form_widgets_for_option_S5_S8_current_source.append(
                        combobox)
                else:
                    entry = ttk.Entry(S5_S8_Current_source_frame)
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        entry.insert(0, saved_parameters_for_sensor[i])
                    form_widgets_for_option_S5_S8_current_source.append(entry)

            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S5_S8_current_source

            for i, (label_text, field_type) in enumerate(self.SCh_radio_parameters["S5_S8_Measurement_channel"]):
                ttk.Label(S5_S8_Measurement_channel_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S5_S8_Measurement_channel_frame, values=field_type, state="disabled")
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        combobox.set(saved_parameters_for_sensor[i])
                    form_widgets_for_option_Measurement_channel.append(
                        combobox)
                else:
                    entry = ttk.Entry(
                        S5_S8_Measurement_channel_frame, state="disabled")
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        entry.insert(0, saved_parameters_for_sensor[i])
                    form_widgets_for_option_Measurement_channel.append(entry)

            self.form_widgets[sensor]["Measurement_channel"] = form_widgets_for_option_Measurement_channel

            # 初始化 Both 選項，結合前面兩個選項的所有小部件
            both_widgets = self.form_widgets[sensor]["Current_source"] + \
                self.form_widgets[sensor]["Measurement_channel"]
            self.form_widgets[sensor]["Both"] = both_widgets

        else:
            for i, (label_text, field_type) in enumerate(self.SCh_radio_parameters["S9_S10_Thermometer"]):
                ttk.Label(S9_S10_Thermometer_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S9_S10_Thermometer_frame, values=field_type)
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        combobox.set(saved_parameters_for_sensor[i])
                    form_widgets_for_option_Thermometer.append(combobox)
                else:
                    entry = ttk.Entry(S9_S10_Thermometer_frame)
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters 中的值
                    if i < len(saved_parameters_for_sensor):
                        entry.insert(0, saved_parameters_for_sensor[i])
                    form_widgets_for_option_Thermometer.append(entry)

            self.form_widgets[sensor]["Thermometer"] = form_widgets_for_option_Thermometer

        # 提交按鈕排版
        ttk.Button(button_frame, text="儲存", command=lambda: self.save_parameters(
            sensor, check_option.get(), param_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=param_window.destroy).pack(
            side=tk.LEFT, padx=5)

    def update_form(self, sensor):
        # 根據選中的 RadioButton 選項更新表單的狀態
        selected_radio = self.check_option[sensor].get()

        if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
            for option, widgets in self.form_widgets[sensor].items():
                if selected_radio == option:
                    for widget in widgets:
                        widget.configure(state="normal")
                else:
                    for widget in widgets:
                        widget.configure(state="disabled")

        elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
            # 當選擇 "Both" 時，先禁用所有小部件，再逐一啟用
            if selected_radio == "Both":
                for widgets in self.form_widgets[sensor].values():
                    for widget in widgets:
                        widget.configure(state="normal")
            else:
                # 將所有小部件設置為禁用狀態
                for widgets in self.form_widgets[sensor].values():
                    for widget in widgets:
                        widget.configure(state="disabled")

                # 啟用選中的選項對應的小部件
                for option, widgets in self.form_widgets[sensor].items():
                    if selected_radio == option:
                        for widget in widgets:
                            widget.configure(state="normal")

    def save_parameters(self, sensor, option, window):
        """Handle form submission and save parameters"""

        # Collect the parameters from the form
        params = []

        # option 可以是 "Current_source" 或 "Voltage_source"
        for widget in self.form_widgets[sensor][option]:
            if isinstance(widget, ttk.Combobox):
                # Get the selected value in Combobox
                params.append(widget.get())
            else:
                params.append(widget.get())   # Get the value in Entry

        # Delete previously saved parameters for this sensor-option pair
        for key in list(self.saved_parameters):
            # if key[0] == sensor and key[1] == option:
            #     del self.saved_parameters[key]

            if key == (sensor, option):  # 僅刪除與當前 sensor 和 option 配對的參數
                del self.saved_parameters[key]

        # Save current parameters
        self.saved_parameters[(sensor, option)] = params
        print(f"提交的參數 ({sensor} - {option}): {params}")

        # 清除另一個選項的內容
        if option == "Current_source":
            # 清除 Voltage_source 的內容
            if (sensor, "Voltage_source") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Voltage_source")]
                # 清空界面上的 Voltage_source 表單內容
                for widget in self.form_widgets[sensor]["Voltage_source"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry
        elif option == "Voltage_source":
            # 清除 Current_source 的內容
            if (sensor, "Current_source") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Current_source")]
                # 清空界面上的 Current_source 表單內容
                for widget in self.form_widgets[sensor]["Current_source"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry

        
        

        # Close the window
        window.destroy()


if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()
