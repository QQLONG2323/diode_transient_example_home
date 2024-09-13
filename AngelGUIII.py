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

        # # 初始化字典
        # self.entries = {}
        # self.comboboxes = {}
        
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
        
        self.input_data = {}
        self.widgets = {}
        
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
                ("Range", ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"]), 
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
                    ("Range", ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"]), 
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

            
        #創建 Checkbutton 和 RadioButton 的框架
        self.check_sensor = {}   # 儲存 Checkbutton 的變量對象(BooleanVar)
        self.radio_vars = {}  # 儲存每個 Checkbutton 對應的 StringVar
        self.saved_parameters = {}  # 儲存每個 RadioButton 的參數        
        self.form_widgets = {}   # 保存所有動態生成的表單控件

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S1_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
            
        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 2, 4)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(LP220_S3_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 4, 8)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S5_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 8, 12)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S6_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 12, 16)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S7_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 16, 20)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(MS401_S8_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 20, 28)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S9_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, (sensor, radio_options) in enumerate(itertools.islice(self.SCh_radio.items(), 28, 36)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(TH800_S10_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
      
        print_button = ttk.Button(self, text="Print Values", command=self.print_all_data)
        print_button.grid(pady=10)
                        
    # 只有在 Checkbutton 被勾選時才彈出視窗
    def handle_checkbutton(self, sensor):  
        selected_check_sensor = self.check_sensor[sensor].get() 

        if self.check_sensor[sensor].get():
            self.open_parameter_window(sensor)
        else:
            self.radio_vars[sensor].set("")
            self.update_form(sensor, disable=True)
    
     

    # 彈出一個填寫參數的表單視窗
    def open_parameter_window(self, sensor):   

        # 建立彈出視窗
        param_window = tk.Toplevel(self)
        param_window.title(f"{sensor}")
        param_window.geometry("")

        # 設定 LabelFrame 字體大小與粗體
        style = ttk.Style()
        style.configure("Large_Bold.TLabelframe.Label", font=("System", 16, "bold"))

        # 建立頂端按鈕框架
        radio_frame = ttk.Frame(param_window)
        radio_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # 建立 LP220 所有的參數 table 框架
        S1_S3_Current_source_frame = ttk.LabelFrame(param_window, text="Current source", style="Large_Bold.TLabelframe")
        S1_S3_Current_source_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        S1_S3_Voltage_source_frame = ttk.LabelFrame(param_window, text="Voltage source", style="Large_Bold.TLabelframe")
        S1_S3_Voltage_source_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # 建立 MS401 所有的參數 table 框架
        S5_S8_Current_source_frame = ttk.LabelFrame(param_window, text="Current source", style="Large_Bold.TLabelframe")
        S5_S8_Current_source_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        S5_S8_Measurement_channel_frame = ttk.LabelFrame(param_window, text="Measurement channel", style="Large_Bold.TLabelframe")
        S5_S8_Measurement_channel_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # 建立 TH800 所有的參數 table 框架
        S9_S10_Thermometer_frame = ttk.LabelFrame(param_window, text="Thermometer", style="Large_Bold.TLabelframe")
        S9_S10_Thermometer_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

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
        check_radio = tk.StringVar(value=default_radio_option or radio_options[0])
        self.radio_vars[sensor] = check_radio  # 保存這個 sensor 的選擇變量
        
        # Radio 排版
        for i, option in enumerate(radio_options):
            tk.Radiobutton(radio_frame, text=option, variable=check_radio, value=option, font=("System", 16, "bold"), command=lambda: self.update_form(sensor)).grid(row=0, column=i+1, padx=20, pady=5)


 

        # 需修改區
        # Retrieve saved parameters and pre-fill the form
        # if (sensor, check_radio.get()) in self.saved_parameters:
        #     saved_params = self.saved_parameters[(sensor, check_radio.get())]
        #     for widget, value in zip(self.form_widgets[sensor][check_radio.get()], saved_params):
        #         if isinstance(widget, ttk.Combobox):
        #             widget.set(value)
        #         else:
        #             widget.insert(0, value)

        # 根據選中的選項動態生成表單
        self.form_widgets[sensor] = {}
        
        if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:            
            form_widgets_for_option_S1_S3_current_source = []
            form_widgets_for_option_voltage_source = []

            for label_text, field_type in self.SCh_radio_parameters["S1_S3_Current_source"]:
                ttk.Label(S1_S3_Current_source_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    param = label_text
                    combobox = ttk.Combobox(S1_S3_Current_source_frame, values=field_type, state="readonly")
                    combobox.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_S1_S3_current_source.append(combobox)
                    self.widgets[param] = combobox
                else:
                    param = label_text
                    entry = ttk.Entry(S1_S3_Current_source_frame)
                    entry.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_S1_S3_current_source.append(entry)
                    self.widgets[param] = entry 

                    
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1_S3_current_source

            for label_text, field_type in self.SCh_radio_parameters["S1_S3_Voltage_source"]:
                ttk.Label(S1_S3_Voltage_source_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    param = label_text
                    combobox = ttk.Combobox(S1_S3_Voltage_source_frame, values=field_type, state="disabled")
                    combobox.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_voltage_source.append(combobox)
                    self.widgets[param] = combobox
                else:
                    param = label_text
                    entry = ttk.Entry(S1_S3_Voltage_source_frame, state="disabled")
                    entry.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_voltage_source.append(entry)
                    self.widgets[param] = entry

            self.form_widgets[sensor]["Voltage_source"] = form_widgets_for_option_voltage_source

        elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:            
            form_widgets_for_option_S5_S8_current_source = []
            form_widgets_for_option_Measurement_channel = []

            for label_text, field_type in self.SCh_radio_parameters["S5_S8_Current_source"]:
                ttk.Label(S5_S8_Current_source_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    param = label_text
                    combobox = ttk.Combobox(S5_S8_Current_source_frame, values=field_type, state="readonly")
                    combobox.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_S5_S8_current_source.append(combobox)
                    self.widgets[param] = combobox
                else:
                    param = label_text
                    entry = ttk.Entry(S5_S8_Current_source_frame)
                    entry.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_S5_S8_current_source.append(entry)
                    self.widgets[param] = entry
                    
            
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S5_S8_current_source

            for label_text, field_type in self.SCh_radio_parameters["S5_S8_Measurement_channel"]:
                ttk.Label(S5_S8_Measurement_channel_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    param = label_text
                    combobox = ttk.Combobox(S5_S8_Measurement_channel_frame, values=field_type, state="disabled")
                    combobox.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_Measurement_channel.append(combobox)
                    self.widgets[param] = combobox
                else:
                    param = label_text
                    entry = ttk.Entry(S5_S8_Measurement_channel_frame, state="disabled")
                    entry.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_Measurement_channel.append(entry)
                    self.widgets[param] = entry

            self.form_widgets[sensor]["Measurement_channel"] = form_widgets_for_option_Measurement_channel

            # 初始化 Both 選項，結合前面兩個選項的所有小部件
            both_widgets = self.form_widgets[sensor]["Current_source"] + self.form_widgets[sensor]["Measurement_channel"]
            self.form_widgets[sensor]["Both"] = both_widgets

        else:           
            form_widgets_for_option_Thermometer = []
            for label_text, field_type in self.SCh_radio_parameters["S9_S10_Thermometer"]:
                ttk.Label(S9_S10_Thermometer_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    param = label_text
                    combobox = ttk.Combobox(S9_S10_Thermometer_frame, values=field_type)
                    combobox.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_Thermometer.append(combobox)
                    self.widgets[param] = combobox
                else:
                    param = label_text
                    entry = ttk.Entry(S9_S10_Thermometer_frame)
                    entry.pack(anchor=tk.W, pady=5)
                    form_widgets_for_option_Thermometer.append(entry)
                    self.widgets[param] = entry

            self.form_widgets[sensor]["Thermometer"] = form_widgets_for_option_Thermometer

        # mode = mode_combobox.get()      # 从模式选择的下拉菜单中获取值（"Current" 或 "Voltage"）
        print(self.saved_parameters)
        # 提交按鈕排版
        ttk.Button(button_frame, text="儲存", command=lambda: self.save_data_to_json(sensor)).pack(side=tk.LEFT, padx=5)
                   #lambda: self.save_parameters(sensor, check_radio.get(), param_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=param_window.destroy).pack(side=tk.LEFT, padx=5)

        self.load_data_from_json(sensor)

    def update_form(self, sensor):
        # 根據選中的 RadioButton 選項更新表單的狀態
        selected_radio = self.radio_vars[sensor].get()
        # print(selected_radio)
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

    def save_data_to_json(self, sensor):
        data = {}  # 主字典

        selected_radio = self.radio_vars[sensor].get()

        print(sensor)
        print(selected_radio)
        # 根据 mode 动态决定存储的是 Current 还是 Voltage
        if selected_radio == "Current_source":
            data[f"{sensor}_Current"] = {}
            for key, widget in self.widgets.items():
                print(f"Current source widget: {key} -> {widget.get()}")
                if key in ["Output mode", "Current [A]", "Voltage limit [V]"]:
                    data[f"{sensor}_Current"][key] = widget.get()

        elif selected_radio == "Voltage_source":
            data[f"{sensor}_Voltage"] = {}
            for key, widget in self.widgets.items():
                print(f"Voltage source widget: {key} -> {widget.get()}")
                if key in ["Output mode", "On-state voltage [V]", "Current limit [A]"]:
                    data[f"{sensor}_Voltage"][key] = widget.get()

        # 将数据保存到 JSON 文件
        with open("form_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存到 form_data.json，传感器: {sensor}，模式: {selected_radio}")

    def load_data_from_json(self, sensor):
        selected_radio = self.radio_vars[sensor].get()
        try:
            with open("form_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # 动态加载当前模式的数据 (Current 或 Voltage)
            if selected_radio == "Current_source" and f"{sensor}_Current" in data:
                sensor_data = data[f"{sensor}_Current"]
            elif selected_radio == "Voltage_source" and f"{sensor}_Voltage" in data:
                sensor_data = data[f"{sensor}_Voltage"]
            else:
                print(f"未找到传感器 {sensor} 的 {selected_radio} 数据")
                return

            # 遍历并填充数据到控件中
            for key, value in sensor_data.items():
                if key in self.widgets:
                    widget = self.widgets[key]
                    if isinstance(widget, ttk.Entry):
                        widget.delete(0, tk.END)  # 清除旧内容
                        widget.insert(0, value)  # 插入新内容
                    elif isinstance(widget, ttk.Combobox):
                        widget.set(value)  # 设置 Combobox 的选中值

            print(f"数据已成功加载，传感器: {sensor}，模式: {selected_radio}")

        except FileNotFoundError:
            print("未找到 JSON 文件")



    # def save_data_to_json(self):
    #     data = {
    #         "S1_S3_Current_source": {
    #         "Output mode": self.widgets["Output mode"].get(),
    #         "Current [A]": self.widgets["Current [A]"].get(),
    #         "Voltage limit [V]": self.widgets["Voltage limit [V]"].get()
    #     },
    #         "S1_S3_Voltage_source": {
    #         "Output mode": self.widgets["Output mode"].get(),
    #         "Current [A]": self.widgets["Current [A]"].get(),
    #         "Voltage limit [V]": self.widgets["Voltage limit [V]"].get()
    #     },
    #         "S1_S3_Voltage_source": {
    #         "Output mode": self.widgets["Output mode"].get(),
    #         "Current [A]": self.widgets["Current [A]"].get(),
    #         "Voltage limit [V]": self.widgets["Voltage limit [V]"].get()
    #     }
    
    #     }
    #     # 遍历所有控件，提取其值
    #     for key, widget in self.widgets.items():
    #         if isinstance(widget, ttk.Entry):
    #             data[key] = widget.get()  # 获取 Entry 的文本内容
    #         elif isinstance(widget, ttk.Combobox):
    #             data[key] = widget.get()  # 获取 Combobox 的选中值

    #     # 将数据保存到 JSON 文件
    #     with open("form_data.json", "w", encoding="utf-8") as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)
    #     print("数据已保存到 form_data.json")

    # def load_data_from_json(self):
    #     try:
    #         with open("form_data.json", "r", encoding="utf-8") as f:
    #             data = json.load(f)
            
    #         # 将数据填充到控件中
    #         for key, value in data.items():
    #             if key in self.widgets:
    #                 widget = self.widgets[key]
    #                 if isinstance(widget, ttk.Entry):
    #                     widget.delete(0, tk.END)  # 清除旧内容
    #                     widget.insert(0, value)  # 插入新内容
    #                 elif isinstance(widget, ttk.Combobox):
    #                     widget.set(value)  # 设置 Combobox 的选中值
    #         print("数据已成功加载")
        
    #     except FileNotFoundError:
    #         print("未找到 JSON 文件") 

    # def save_values(self):
    #     # 從 widgets 中獲取各項輸入值並更新字典
    #     for param, widget in self.widgets.items():
    #         self.input_data[param] = widget.get()

    #     # 顯示輸入資料 (可以替換成存檔、提交等操作)
    #     print("輸入的資料:", self.input_data)

    def print_all_data(self):
        print("input: " + str(self.input_data))
        print(self.widgets)

    # 需修改
    def save_parameters(self, sensor, option, window):
        """Handle form submission and save parameters"""

        # Collect the parameters from the form
        params = []
        for widget in self.form_widgets[sensor][option]:
            if isinstance(widget, ttk.Combobox):
                params.append(widget.get())
            else:
                params.append(widget.get())
        
        # Delete previously saved parameters for this sensor
        for key in list(self.saved_parameters):
            if key[0] == sensor:
                del self.saved_parameters[key]

        # Save current parameters
        self.saved_parameters[(sensor, option)] = params
        print(f"提交的參數 ({sensor} - {option}): {params}")

        # Close the window
        window.destroy()

    
    # sensor_parameters = {}
    # def save_parameters(sensor, mode):
        
    #     params = {}
    #     # 遍歷所有的控件（輸入框、下拉選單等），並將它們的值保存到params字典中
    #     for key, entry in entry.items():
    #         params[key] = entry.get()
    #     for key, combobox in combobox.items():
    #         params[key] = combobox.get()
        
    #     # 將params字典保存到sensor_parameters中，對應於特定的感測器和模式
    #     sensor_parameters[sensor][mode] = params

    # def load_parameters(sensor, mode):
    #     if sensor in sensor_parameters and mode in sensor_parameters[sensor]:
    #         params = sensor_parameters[sensor][mode]
    #     # 將params字典中的值加載到控件中
    #     for key, value in params.items():
    #         if key in entries:
    #             entries[key].delete(0, tk.END)
    #             entries[key].insert(0, value)
    #         if key in comboboxes:
    #             comboboxes[key].set(value)

if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()