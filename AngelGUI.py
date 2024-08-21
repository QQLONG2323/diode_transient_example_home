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

        


                   
        
    # 只有在 Checkbutton 被勾選時才彈出視窗
    def handle_checkbutton(self, sensor):    
        if self.check_sensor[sensor].get():
            self.open_parameter_window(sensor)
        else:
            self.radio_vars[sensor].set("")
            self.update_form(sensor, disable=True)
    
     
    # 彈出一個填寫參數的表單視窗
    def open_parameter_window(self, sensor):   
        param_window = tk.Toplevel(self)
        param_window.title(f"{sensor}")
        param_window.geometry("")

        radio_frame = ttk.Frame(param_window)
        radio_frame.pack(padx=5, pady=5, anchor=tk.NW)

        form_frame = ttk.Frame(param_window)
        form_frame.pack(padx=5, pady=5, anchor=tk.NW)

        button_frame = ttk.Frame(param_window)
        button_frame.pack(padx=5, pady=5, fill=tk.BOTH, anchor=tk.S, expand=True)
      

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
        for option in radio_options:
            tk.Radiobutton(radio_frame, text=option, variable=check_radio, value=option, command=lambda: self.update_form(sensor)).pack(anchor=tk.W, padx=20, pady=5)
       
        # 根據選中的選項動態生成表單
        self.form_widgets[sensor] = {}
        for key in self.SCh_radio:
            if key == :
                form_widgets_for_option = []
                for label_text, field_type in self.SCh_radio_parameters[option]:
                    ttk.Label(form_frame, text=label_text).pack(anchor=tk.W)
                    if isinstance(field_type, list):
                        combobox = ttk.Combobox(form_frame, values=field_type, state="disabled")
                        combobox.pack(anchor=tk.W, pady=5)
                        form_widgets_for_option.append(combobox)
                    else:
                        entry = ttk.Entry(form_frame, state="disabled")
                        entry.pack(anchor=tk.W, pady=5)
                        form_widgets_for_option.append(entry)

                self.form_widgets[sensor][option] = form_widgets_for_option

        

        # 創建參數輸入框
        
         
        
        
        


        

        # # 如果之前有保存過該 RadioButton 的參數，則填入到輸入框中
        # if (sensor, check_radio.get()) in self.saved_parameters:
        #     param_entry.insert(0, self.saved_parameters[(sensor, check_radio.get())])        










        # # 提交按鈕排版
        # ttk.Button(button_frame, text="提交", command=lambda: self.submit_parameters(param_entry.get(), sensor, check_radio.get(), param_window)).pack(side=tk.LEFT, padx=5)
        # ttk.Button(button_frame, text="取消", command=param_window.destroy).pack(side=tk.LEFT, padx=5)


    def submit_parameters(self, params, sensor, option, window):
        """處理提交的參數並保存"""

        # 刪除該感測器的所有已保存參數
        for key in list(self.saved_parameters):
            if key[0] == sensor:
                del self.saved_parameters[key]

        # 保存當前選中的選項和參數
        self.saved_parameters[(sensor, option)] = params
        print(f"提交的參數 ({sensor} - {option}): {params}")
        window.destroy()  # 關閉窗口






if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()


