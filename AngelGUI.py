import json
import tkinter as tk
from tkinter import ttk, Frame, filedialog, messagebox, TclError
import os
import itertools
from io import StringIO
import sys
import threading
from PIL import Image, ImageTk 


class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("T3STER SI")
        self.geometry("1280x960")
  
        # 設置 Sensor 字體大小
        ttk.Style().configure("Large_Bold.TCheckbutton", font=("Helvetica", 16, "bold"))
        # 設定 LabelFrame 字體大小與粗體
        ttk.Style().configure("Large_Bold.TLabelframe.Label", font=("system", 16, "bold"))

        # 保存第一頁參數的 JSON 檔(params.json)
        self.params_file = "params.json"   
        # 讀取之前保存過的第一頁參數的 params.json 以及第一頁新的參數也是用這個來暫存，並在第一頁按下 Next 後匯出至 saved_parameters.json
        self.saved_parameters = self.load_params()

        # 初始化用於保存 Sensor 、 Option 、 Parameters 和表單控件的字典
        self.sensor = {}   # 儲存 Sensor 的選項
        self.option = {}   # 儲存 Option 的選項
        self.sensor_widget = {}   # 儲存 Sensor 的控件 
        self.option_widget = {}   # 儲存 Option 的控件
        self.form_widgets = {}   # 儲存所有動態生成的表單控件
        self.any_trigger_selected = False   # 檢查是否有任意 Trigger 被選中    
        
        # 應用程式開始先顯示第一頁
        self.create_page1()

    # "保存"第一頁參數，以便從第二頁返回時回填
    def save_params(self):
        str_keys_saved_parameters = {str(key): value for key, value in self.saved_parameters.items()}
        with open(self.params_file, 'w') as file:
            json.dump(str_keys_saved_parameters, file, ensure_ascii=False, indent=4)

    # "讀取"之前保存過的第一頁參數，以便從第二頁返回時回填
    def load_params(self):
        if os.path.exists(self.params_file):
            with open(self.params_file, 'r') as file:
                str_keys_saved_parameters = json.load(file)
                # 將字典的鍵從 str 轉換回 tuple
                return {eval(key): value for key, value in str_keys_saved_parameters.items()}
        return {}

    # 創建 Sensor 框架的 Function
    def create_sensor_frame(self, text, column):
        frame = ttk.LabelFrame(self.sensors_parent_frame, text=text)
        frame.grid(column=column, row=0, padx=10, pady=10, sticky=tk.NSEW)
        return frame

    # 創建 LP220 的 Sensor 、 Option 、 Parameters 的 Function
    def create_lp220_sensor_option_parameters(self):
        return {
            "Current_source": {
                "Output mode": ["Off", "On", "Switching"],
                "Current [A]": "entry",
                "Voltage limit [V]": "entry"
            },
            "Voltage_source": {
                "Output mode": ["Off", "On", "Switching"],
                "On-state voltage [V]": "entry",
                "Current limit [A]": "entry"
            }
        }
    
    # 創建 MS401 的 Sensor 、 Option 、 Parameters 的 Function
    def create_ms401_sensor_option_parameters(self):
        return {
            "Current_source": {
                "Output mode": ["Off", "ON"],
                "Range [V]": ["10", "20", "40"],
                "Current [A]": "entry"
            },
            "Measurement_channel": {
                "Sensitivity [mV/K]": "entry",
                "Auto range": ["Off", "On"],
                "Range": [
                    "Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                ],
                "Vref [V]": "entry",
                "Separate Vref for heating": ["Off", "On"],
                "Vref,heating [V]": "entry"
            },
            "Both": {
                "Output mode": ["Off", "ON"],
                "Current_source_Range": ["10", "20", "40"],
                "Current [A]": "entry",
                "Sensitivity [mV/K]": "entry",
                "Auto range": ["Off", "On"],
                "Measurement_channel_Range": [
                    "Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                ],
                "Vref [V]": "entry",
                "Separate Vref for heating": ["Off", "On"],
                "Vref,heating [V]": "entry"
            }
        }
    
    # 創建 TH800 的 Sensor 、 Option 、 Parameters 的 Function
    def create_th800_sensor_option_parameters(self):
        return {
            "Thermometer": {
                "Type": "entry",
                "Sensitivity": "entry",
                "Sample per sec": "entry"
            }
        }

    # 創建 Trigger 的 Sensor 、 Option 、 Parameters 的 Function
    def create_trigger_sensor_option_parameters(self):
        return {
            "Trigger": {
                "Mode" :["High", "Low", "Switched", "Switched Inverted", "Disabled"]
            }
        }
    
    # 創建 Booster 的 S1Ch1 Drive 的 Sensor 、 Option 、 Parameters 的 Function
    def create_booster_S1Ch1Drive_option_parameters(self):
        return {
            "Current_source": {
                "Output mode": ["Off", "On", "Switching"],
                "Current [A]": "entry",
                "Voltage limit [V]": "entry"
            }
        }

    # 創建 Booster 的 S1Ch1 Gate 的 Sensor 、 Option 、 Parameters 的 Function
    def create_booster_S1Ch1Gate_option_parameters(self):
        return {
            "Voltage_source": {
                "Output mode": ["Off", "On", "Switching", "Rds on"],
                "On-state voltage [V]": "entry",
            }
        }

    # 創建 Booster 的 S1Ch1 Sense 的 Sensor 、 Option 、 Parameters 的 Function
    def create_booster_S1Ch1Sense_option_parameters(self):
        return {
            "Current_source": {
                "Output mode": ["Off", "ON"],
                "Range [V]": ["11"],
                "Current [A]": "entry"
            }
        }

    # 創建第一頁
    def create_page1(self):

        # 用於儲存第一個頁面上的所有控件
        self.page1_widgets = []

        # 創建一個 Sensor 父框架來容納所有 Sensor 的框架
        self.sensors_parent_frame = ttk.LabelFrame(self, text="T3STER SI Sensor", style="Large_Bold.TLabelframe")  # Sensor 父框架
        self.sensors_parent_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(self.sensors_parent_frame)

        # Sensor 框架
        LP220_S1_frame = self.create_sensor_frame("LP220", 0)
        LP220_S3_frame = self.create_sensor_frame("LP220", 1)
        MS401_S5_frame = self.create_sensor_frame("MS401", 2)
        MS401_S6_frame = self.create_sensor_frame("MS401", 3)
        MS401_S7_frame = self.create_sensor_frame("MS401", 4)
        MS401_S8_frame = self.create_sensor_frame("MS401", 5)
        TH800_S9_frame = self.create_sensor_frame("TH800", 6)
        TH800_S10_frame = self.create_sensor_frame("TH800", 7)
        TRIGGER_frame = self.create_sensor_frame("TRIGGER", 8)

        # 創建一個 Booster 父框架來容納所有 Booster 的框架
        self.booster_parent_frame = ttk.LabelFrame(self, text="BOOSTER", style="Large_Bold.TLabelframe")  # Booster 父框架
        self.booster_parent_frame.grid(column=0, row=1, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(self.booster_parent_frame)

        # Next 按鈕，按下後隱藏當前頁面並進入下一步的頁面
        next_button = ttk.Button(
            self, text="Next", command=self.go_to_page2)
        next_button.grid(column=0, row=2, padx=10, pady=10, sticky="E")
        self.page1_widgets.append(next_button)

        # 定義每個感測器的選項
        self.sensor_option_parameters = {
            "S1Ch1": self.create_lp220_sensor_option_parameters(),
            "S1Ch2": self.create_lp220_sensor_option_parameters(),
            "S3Ch1": self.create_lp220_sensor_option_parameters(),
            "S3Ch2": self.create_lp220_sensor_option_parameters(),
            "S5Ch1": self.create_ms401_sensor_option_parameters(),
            "S5Ch2": self.create_ms401_sensor_option_parameters(),
            "S5Ch3": self.create_ms401_sensor_option_parameters(),
            "S5Ch4": self.create_ms401_sensor_option_parameters(),
            "S6Ch1": self.create_ms401_sensor_option_parameters(),
            "S6Ch2": self.create_ms401_sensor_option_parameters(),
            "S6Ch3": self.create_ms401_sensor_option_parameters(),
            "S6Ch4": self.create_ms401_sensor_option_parameters(),
            "S7Ch1": self.create_ms401_sensor_option_parameters(),
            "S7Ch2": self.create_ms401_sensor_option_parameters(),
            "S7Ch3": self.create_ms401_sensor_option_parameters(),
            "S7Ch4": self.create_ms401_sensor_option_parameters(),
            "S8Ch1": self.create_ms401_sensor_option_parameters(),
            "S8Ch2": self.create_ms401_sensor_option_parameters(),
            "S8Ch3": self.create_ms401_sensor_option_parameters(),
            "S8Ch4": self.create_ms401_sensor_option_parameters(),
            "S9Ch1": self.create_th800_sensor_option_parameters(),
            "S9Ch2": self.create_th800_sensor_option_parameters(),
            "S9Ch3": self.create_th800_sensor_option_parameters(),
            "S9Ch4": self.create_th800_sensor_option_parameters(),
            "S9Ch5": self.create_th800_sensor_option_parameters(),
            "S9Ch6": self.create_th800_sensor_option_parameters(),
            "S9Ch7": self.create_th800_sensor_option_parameters(),
            "S9Ch8": self.create_th800_sensor_option_parameters(),
            "S10Ch1": self.create_th800_sensor_option_parameters(),
            "S10Ch2": self.create_th800_sensor_option_parameters(),
            "S10Ch3": self.create_th800_sensor_option_parameters(),
            "S10Ch4": self.create_th800_sensor_option_parameters(),
            "S10Ch5": self.create_th800_sensor_option_parameters(),
            "S10Ch6": self.create_th800_sensor_option_parameters(),
            "S10Ch7": self.create_th800_sensor_option_parameters(),
            "S10Ch8": self.create_th800_sensor_option_parameters(),
            "S11Ch1": self.create_trigger_sensor_option_parameters(),
            "S11Ch2": self.create_trigger_sensor_option_parameters(),
            "S11Ch3": self.create_trigger_sensor_option_parameters(),
            "S11Ch4": self.create_trigger_sensor_option_parameters(),
            "S11Ch5": self.create_trigger_sensor_option_parameters(),
            "S11Ch6": self.create_trigger_sensor_option_parameters(),
            "S11Ch7": self.create_trigger_sensor_option_parameters(),
            "S11Ch8": self.create_trigger_sensor_option_parameters(),
            "S1Ch1 - Drive": self.create_booster_S1Ch1Drive_option_parameters(),
            "S1Ch1 - Gate": self.create_booster_S1Ch1Gate_option_parameters(),
            "S1Ch1 - Sense": self.create_booster_S1Ch1Sense_option_parameters()
        }

        # 創建 & 排版 Sensor
        self.create_sensor_checkbuttons(LP220_S1_frame, 0, 2)
        self.create_sensor_checkbuttons(LP220_S3_frame, 2, 4)
        self.create_sensor_checkbuttons(MS401_S5_frame, 4, 8)
        self.create_sensor_checkbuttons(MS401_S6_frame, 8, 12)
        self.create_sensor_checkbuttons(MS401_S7_frame, 12, 16)
        self.create_sensor_checkbuttons(MS401_S8_frame, 16, 20)
        self.create_sensor_checkbuttons(TH800_S9_frame, 20, 28)
        self.create_sensor_checkbuttons(TH800_S10_frame, 28, 36)
        self.create_trigger_checkbuttons(TRIGGER_frame, 36, 44)

        # 創建 Booster 的 介面
        # 加載圖片
        self.booster1_image = Image.open("booster1.png")
        self.booster1_photo = ImageTk.PhotoImage(self.booster1_image)

        self.booster2_image = Image.open("booster2.png")
        self.booster2_photo = ImageTk.PhotoImage(self.booster2_image)

        self.s1ch1_drive_image = Image.open("S1Ch1_Drive.png")
        self.s1ch1_drive_photo = ImageTk.PhotoImage(self.s1ch1_drive_image)

        # 創建 booster1 Label 並顯示圖片
        self.booster1_photo_label = ttk.Label(self.booster_parent_frame, image=self.booster1_photo)
        self.booster1_photo_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # 創建 booster2 Label 並顯示圖片
        self.booster2_photo_label = ttk.Label(self.booster_parent_frame, image=self.booster2_photo)
        self.booster2_photo_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # 創建 S1Ch1 Drive Checkbutton 並顯示圖片
        self.sensor["S1Ch1 - Drive"] = tk.BooleanVar()
        # 檢查是否有保存的 sensor 值，並設置勾選狀態
        if any(saved_sensor == "S1Ch1 - Drive" for saved_sensor, _ in self.saved_parameters.keys()):
            self.sensor["S1Ch1 - Drive"].set(True)
        self.s1ch1_drive_checkbutton = ttk.Checkbutton(self.booster_parent_frame, image=self.s1ch1_drive_photo, variable=self.sensor["S1Ch1 - Drive"], command=lambda t="S1Ch1 - Drive": self.toggle_sensor(t))
        self.s1ch1_drive_checkbutton.grid(row=0, column=4, padx=10, pady=10, sticky=tk.E)

        # R-DRIVER 來源
        # 過濾出 S11Ch1 到 S11Ch8
        rdriver_trigger_sensors = [sensor for sensor in self.sensor if sensor.startswith("S11Ch") and self.sensor[sensor].get()]
        # 創建 Combobox 並顯示
        self.rdriver_trigger_combobox = ttk.Combobox(self.booster_parent_frame, values=rdriver_trigger_sensors)
        self.rdriver_trigger_combobox.grid(column=0, row=1, sticky=tk.W, padx=(90,200), pady=5)
        self.rdriver_trigger_combobox.set("選擇 Trigger 來源")
        # 檢查是否有保存的 R-DRIVER Trigger 值，並設置 Combobox 選擇值
        if any(saved_sensor == "R-DRIVER" for saved_sensor, _ in self.saved_parameters.keys()):
            self.rdriver_trigger_combobox.set(self.saved_parameters.get(("R-DRIVER", "Trigger"), {}).get("R-DRIVER Trigger"))
        self.rdriver_trigger_combobox.bind("<<ComboboxSelected>>", self.on_rdriver_trigger_combobox_select)

        # 創建 S1Ch1 Sense Checkbutton
        self.sensor["S1Ch1 - Sense"] = tk.BooleanVar()
        # 檢查是否有保存的 sensor 值，並設置勾選狀態
        if any(saved_sensor == "S1Ch1 - Sense" for saved_sensor, _ in self.saved_parameters.keys()):
            self.sensor["S1Ch1 - Sense"].set(True)
        self.s1ch1_sense_checkbutton = ttk.Checkbutton(self.booster_parent_frame, text="S1Ch1 - Sense", variable=self.sensor["S1Ch1 - Sense"], command=lambda t="S1Ch1 - Sense": self.toggle_sensor(t))
        self.s1ch1_sense_checkbutton.grid(row=2, column=0, padx=0, pady=10, sticky=tk.E)
        self.s1ch1_sense_checkbutton.configure(style="Large_Bold.TCheckbutton")

        # 創建 S1Ch1 Gate Checkbutton
        # 創建四個 Checkbutton 並共用同一個 BooleanVar 變量 (因為機台設定隨便選一個都會連動另外三個)
        self.sensor["S1Ch1 - Gate"] = tk.BooleanVar()
        # 檢查是否有保存的 sensor 值，並設置勾選狀態
        if any(saved_sensor == "S1Ch1 - Gate" for saved_sensor, _ in self.saved_parameters.keys()):
            self.sensor["S1Ch1 - Gate"].set(True)
        self.s1ch1_gate_pos1_checkbutton = ttk.Checkbutton(self.booster_parent_frame, text="Pos 1", variable=self.sensor["S1Ch1 - Gate"], command=lambda t="S1Ch1 - Gate": self.toggle_sensor(t))
        self.s1ch1_gate_pos1_checkbutton.grid(row=2, column=1, padx=(30,0), pady=5, sticky=tk.W)
        self.s1ch1_gate_pos1_checkbutton.configure(style="Large_Bold.TCheckbutton")
        self.s1ch1_gate_pos2_checkbutton = ttk.Checkbutton(self.booster_parent_frame, text="Pos 2", variable=self.sensor["S1Ch1 - Gate"], command=lambda t="S1Ch1 - Gate": self.toggle_sensor(t))
        self.s1ch1_gate_pos2_checkbutton.grid(row=2, column=2, padx=0, pady=5, sticky=tk.W)
        self.s1ch1_gate_pos2_checkbutton.configure(style="Large_Bold.TCheckbutton")
        self.s1ch1_gate_pos3_checkbutton = ttk.Checkbutton(self.booster_parent_frame, text="Pos 3", variable=self.sensor["S1Ch1 - Gate"], command=lambda t="S1Ch1 - Gate": self.toggle_sensor(t))
        self.s1ch1_gate_pos3_checkbutton.grid(row=2, column=3, padx=0, pady=5, sticky=tk.W)
        self.s1ch1_gate_pos3_checkbutton.configure(style="Large_Bold.TCheckbutton")
        self.s1ch1_gate_pos4_checkbutton = ttk.Checkbutton(self.booster_parent_frame, text="Pos 4", variable=self.sensor["S1Ch1 - Gate"], command=lambda t="S1Ch1 - Gate": self.toggle_sensor(t))
        self.s1ch1_gate_pos4_checkbutton.grid(row=2, column=4, padx=(0,390), pady=5, sticky=tk.W)
        self.s1ch1_gate_pos4_checkbutton.configure(style="Large_Bold.TCheckbutton")

        # 隱藏 Booster 框架 (待勾選 Trigger 時再顯示)
        if not self.any_trigger_selected:
            for widget in self.page1_widgets:
                if widget is self.booster_parent_frame:
                    widget.grid_forget()

    # 創建 Sensor 的 Checkbutton
    def create_sensor_checkbuttons(self, frame, start, end):
        for i, sensor in enumerate(itertools.islice(self.sensor_option_parameters.keys(), start, end)):
            self.sensor[sensor] = tk.BooleanVar()
            # 檢查是否有保存的 sensor 值，並設置勾選狀態
            if any(saved_sensor == sensor for saved_sensor, _ in self.saved_parameters.keys()):
                self.sensor[sensor].set(True)
            checkbutton = ttk.Checkbutton(
                frame, text=sensor, variable=self.sensor[sensor], command=lambda t=sensor: self.toggle_sensor(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
            # 設置 Checkbutton 的字體
            checkbutton.configure(style="Large_Bold.TCheckbutton")
            self.sensor_widget[sensor] = checkbutton   # 儲存控件

            # 如果有 Trigger 被選中，則禁用 LP220 框架內的 SENSOR
            if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                if self.any_trigger_selected:
                    checkbutton.configure(state=tk.DISABLED)
            
    # Sensor 被勾選時的反應
    def toggle_sensor(self, sensor):
        if self.sensor[sensor].get():
            self.open_parameter_window(sensor)   # 彈出填寫參數的表單
        else:
            # 刪除 params.json 中對應的 option 以及各個控件的參數
            keys_to_delete = [key for key in self.saved_parameters if key[0] == sensor]
            for key in keys_to_delete:
                del self.saved_parameters[key]
            self.save_params()
            
            if sensor in self.option:
                self.option[sensor].set("")
            if sensor in self.form_widgets:
                self.update_form(sensor)

    # 創建 Trigger 的 Checkbutton
    def create_trigger_checkbuttons(self, frame, start, end):
        
        # Trigger 顯示在 GUI 的標籤
        trigger_labels = {
            "S11Ch1": "Trigger1",
            "S11Ch2": "Trigger2",
            "S11Ch3": "Trigger3",
            "S11Ch4": "Trigger4",
            "S11Ch5": "Trigger5",
            "S11Ch6": "Trigger6",
            "S11Ch7": "Trigger7",
            "S11Ch8": "Trigger8"
        }
        
        for i, sensor in enumerate(itertools.islice(self.sensor_option_parameters.keys(), start, end)):
            self.sensor[sensor] = tk.BooleanVar()
            # 檢查是否有保存的 trigger 值，並設置勾選狀態
            if any(saved_sensor == sensor for saved_sensor, _ in self.saved_parameters.keys()):
                self.sensor[sensor].set(True)

            # 設置顯示的文字
            text = trigger_labels.get(sensor, sensor)

            checkbutton = ttk.Checkbutton(
                frame, text=text, variable=self.sensor[sensor], command=lambda t=sensor: self.toggle_trigger(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
            # 設置 Checkbutton 的字體
            checkbutton.configure(style="Large_Bold.TCheckbutton")
            self.sensor_widget[sensor] = checkbutton   # 儲存控件

    # Trigger 被勾選時的反應
    def toggle_trigger(self, sensor):
        if self.sensor[sensor].get():
            self.open_parameter_window(sensor)   # 彈出填寫參數的表單
        else:
            # 刪除 params.json 中對應的 option 以及各個控件的參數
            keys_to_delete = [key for key in self.saved_parameters if key[0] == sensor]
            for key in keys_to_delete:
                del self.saved_parameters[key]

            # 刪除 self.saved_parameters 中擁有相同 sensor 的 R-DRIVER Trigger 項目
            rdriver_keys_to_delete = [key for key, value in self.saved_parameters.items() if key == ('R-DRIVER', 'Trigger') and value.get('R-DRIVER Trigger') == sensor]
            for key in rdriver_keys_to_delete:
                del self.saved_parameters[key]

            self.save_params()

            self.rdriver_trigger_combobox.set("選擇 Trigger 來源")
            
        # 檢查 Trigger 是否有被選中
        self.any_trigger_selected = any(self.sensor[sensor].get() for sensor in ["S11Ch1", "S11Ch2", "S11Ch3", "S11Ch4", "S11Ch5", "S11Ch6", "S11Ch7", "S11Ch8"])

        if self.any_trigger_selected:
            # 禁用 LP220 框架內的 SENSOR
            for lp220 in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                self.sensor[lp220].set(False)   # 清除選中狀態
                self.disable_lp220_sensors(lp220)   # 禁用 LP220 框架內的 SENSOR 
            # 顯示 Booster 框架   
            self.booster_parent_frame.grid(column=0, row=1, columnspan=8, padx=10, pady=10, sticky=tk.NSEW) 
        else:
            keys_to_delete = [key for key, _ in self.saved_parameters.items() if key[0] in ["R-DRIVER", "S1Ch1 - Drive", "S1Ch1 - Sense", "S1Ch1 - Gate"]]
            for key in keys_to_delete:
                del self.saved_parameters[key]
            # 啟用 LP220 框架內的 SENSOR
            for lp220 in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                self.enable_lp220_sensors(lp220)
            # 隱藏 Booster 框架
            for widget in self.page1_widgets:
                if widget is self.booster_parent_frame:
                    widget.grid_forget()
            
        # 更新保存到 JSON 文件
        self.save_params()

        # 更新 R-DRIVER 來源的 Combobox 選項
        rdriver_trigger_sensors = [sensor for sensor in self.sensor if sensor.startswith("S11Ch") and self.sensor[sensor].get()]
        self.rdriver_trigger_combobox['values'] = rdriver_trigger_sensors

    # 配合 Trigger 被勾選時的反應的 Function
    def disable_lp220_sensors(self, sensor):
        """禁用 LP220 的 Sensor"""
        widget = self.sensor_widget.get(sensor)
        if widget:
            widget.configure(state=tk.DISABLED)

    # 配合 Trigger 被取消勾選時的反應的 Function
    def enable_lp220_sensors(self, sensor):
        """啟用 LP220 的 Sensor"""
        widget = self.sensor_widget.get(sensor)
        if widget:
            widget.configure(state=tk.NORMAL)

    # Trigger Combobox 被選中時的反應
    def on_rdriver_trigger_combobox_select(self, event):
        selected_value = self.rdriver_trigger_combobox.get()
        new_value = {"R-DRIVER Trigger": selected_value}
        # 清除之前保存的值
        keys_to_delete = [key for key, value in self.saved_parameters.items() if key[0] == "R-DRIVER" and value != new_value]
        for key in keys_to_delete:
            del self.saved_parameters[key]
        # 保存新的值
        self.saved_parameters[("R-DRIVER", "Trigger")] = new_value
        self.save_params()

    def on_input_change(self, frame, entry_widget, min_value, max_value):
        """檢查輸入值是否在範圍內，並變更外部框架的背景顏色"""
        content = entry_widget.get().strip()  # 移除前後空白
        
        # 如果是空值，保持白色背景
        if content == "":
            frame.config(background="white")
            return
        try:
            value = float(content)
            if min_value <= value <= max_value:
                frame.config(background="white")
            else:
                frame.config(background="red")
        except ValueError:
            frame.config(background="red")

    def create_ttk_entry_with_validation(self, parent, min_value, max_value, entry_state,entry_width=40):
        """建立帶有範圍檢查的輸入框，模擬背景變色"""
        frame = Frame(parent, background="white")
        frame.pack(anchor=tk.W, pady=5)
    
        entry = ttk.Entry(frame, state=entry_state, width=entry_width)
        entry.pack(padx=1, pady=1)  # 用於增加邊框的效果
        entry.bind("<KeyRelease>", lambda event: self.on_input_change(frame, entry, min_value, max_value))

        # 將 frame 和 entry 成對追蹤
        if not hasattr(self, 'validation_pairs'):
            self.validation_pairs = []
        self.validation_pairs.append((frame, entry))

        return entry
    
    def create_ttk_entry_with_validation_grid(self, parent,entry_state, min_value, max_value, row=0, column=3, padx=10, pady=10):
        """建立帶有範圍檢查的輸入框，模擬背景變色"""
        frame = Frame(parent, background="white")
        frame.grid(row=row, column=column, padx=padx, pady=pady)  # 改用 grid
        
        entry = ttk.Entry(frame, state=entry_state)
        entry.grid(padx=1, pady=1)  # 改用 grid
        entry.bind("<KeyRelease>", lambda event: self.on_input_change(frame, entry, min_value, max_value))

        # 將 frame 和 entry 成對追蹤
        if not hasattr(self, 'validation_pairs'):
            self.validation_pairs = []
        self.validation_pairs.append((frame, entry))
    
        return entry

    def check_input_validation(self):
        """檢查所有輸入框是否有錯誤（紅色背景）和空白"""
        valid_pairs = []
        
        for frame, entry in self.validation_pairs:
            try:
                # 檢查 widget 是否仍然存在
                entry.winfo_exists()
                frame.winfo_exists()
                
                # 檢查 entry 是否啟用
                if str(entry.cget("state")) == "normal":
                    # 檢查是否為空白
                    content = entry.get()
                    if not content.strip():
                        messagebox.showwarning(
                            "數據錯誤",
                            "請填寫所有啟用的輸入欄位！"
                        )
                        return False
                        
                    # 檢查是否有紅框（驗證錯誤）
                    if frame.cget("background") == "red":
                        messagebox.showwarning(
                            "數據錯誤",
                            "請修正紅框內的輸入值！"
                        )
                        return False
                        
                valid_pairs.append((frame, entry))
                
            except (TclError, tk.TclError):
                # Widget 已被銷毀，跳過
                continue
                
        # 更新有效的 validation_pairs
        self.validation_pairs = valid_pairs
        return True

    # 創建 Parameters 框架的 Function
    def create_parameters_frame(self, parameter_window, text, row):
        frame = ttk.LabelFrame(parameter_window, text=text, style="Large_Bold.TLabelframe")
        frame.grid(row=row, column=0, padx=20, pady=20, sticky="ew")
        return frame
    
    # 建立 Option 按鈕的 Function
    def create_option(self, sensor, option_frame):
        # 取得對應的 Option 選項以及其參數
        # 檢查是否有保存的 Option 選項
        default_option = None
        for option in list(self.sensor_option_parameters[sensor].keys()):
            if (sensor, option) in self.saved_parameters:
                default_option = option
                break

        # 如果已經有保存的選項，將其作為預設選項，否則使用第一個選項
        self.option[sensor] = tk.StringVar(
            value=default_option or list(self.sensor_option_parameters[sensor].keys())[0])  # 保存這個 sensor 的選擇變量

        # Option 排版
        for i, option in enumerate(list(self.sensor_option_parameters[sensor].keys())):
            radiobutton = tk.Radiobutton(option_frame, text=option, variable=self.option[sensor], value=option, font=(
                "Helvetica", 16, "bold"), command=lambda: self.update_form(sensor))
            radiobutton.grid(row=0, column=i+1, padx=20, pady=5)
            self.option_widget[option] = radiobutton  # 儲存控件
            
    # 彈出一個填寫參數的表單視窗 (LP220、MS401、TH800)
    def open_parameter_window(self, sensor):
        # 建立彈出視窗
        parameter_window = tk.Toplevel(self)
        parameter_window.title(f"{sensor}")
        parameter_window.geometry("")

        # 建立頂端按鈕框架
        option_frame = ttk.Frame(parameter_window)
        option_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # 建立 LP220、MS401、TH800、TRIGGER 裡面的參數表單框架
        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame = self.create_parameters_frame(parameter_window, "Current source", 1)
        S1_S3_Voltage_source_frame = self.create_parameters_frame(parameter_window, "Voltage source", 2)
        S5_S8_Measurement_channel_frame = self.create_parameters_frame(parameter_window, "Measurement channel", 2)
        S9_S10_Thermometer_frame = self.create_parameters_frame(parameter_window, "Thermometer", 1)
        S11_Trigger_frame = self.create_parameters_frame(parameter_window, "Trigger", 1)
        S1Ch1Gate_Voltage_source_frame = self.create_parameters_frame(parameter_window, "Voltage source", 1)

        # 建立儲存、取消按鈕框架
        button_frame = ttk.Frame(parameter_window)
        button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # 建立 Option 按鈕
        self.create_option(sensor, option_frame)

        # 建立每個 Sensor 中的參數表單
        self.form_widgets[sensor] = {}

        form_widgets_for_option_S1_S3_current_source = []
        form_widgets_for_option_voltage_source = []

        form_widgets_for_option_S5_S8_current_source = []
        form_widgets_for_option_Measurement_channel = []

        form_widgets_for_option_Thermometer = []

        form_widgets_for_option_Trigger = []

        form_widgets_for_option_S1Ch1_Drive_current_source = []

        form_widgets_for_option_S1Ch1_Sense_current_source = []

        form_widgets_for_option_S1Ch1_Gate_Voltage_source = []

        # 檢查是否有保存的 Parameters 選項
        # LP220
        saved_parameters_for_S1_S3_current_source = list(self.saved_parameters.get(
            (sensor, "Current_source"), {}).values())
        saved_parameters_for_S1_S3_voltage_source = list(self.saved_parameters.get(
            (sensor, "Voltage_source"), {}).values())

        # MS401
        saved_parameters_for_S5_S8_current_source = list(self.saved_parameters.get(
            (sensor, "Current_source"), {}).values())
        saved_parameters_for_S5_S8_Measurement_channel = list(self.saved_parameters.get(
            (sensor, "Measurement_channel"), {}).values())
        saved_parameters_for_S5_S8_Both = list(self.saved_parameters.get(
            (sensor, "Both"), {}).values())

        # TH800
        saved_parameters_for_S9_S10_Thermometer = list(self.saved_parameters.get(
            (sensor, "Thermometer"), {}).values())

        # TRIGGER
        saved_parameters_for_S11_Trigger = list(self.saved_parameters.get(
            (sensor, "Trigger"), {}).values())
        
        # S1Ch1 - Drive
        saved_parameters_for_S1Ch1_Drive_current_source = list(self.saved_parameters.get(
            (sensor, "Current_source"), {}).values())
        
        # S1Ch1 - Sense
        saved_parameters_for_S1Ch1_Sense_current_source = list(self.saved_parameters.get(
            (sensor, "Current_source"), {}).values())
        
        # S1Ch1 - Gate
        saved_parameters_for_S1Ch1_Gate_Voltage_source = list(self.saved_parameters.get(
            (sensor, "Voltage_source"), {}).values())

        # 檢查 S1 & S3 如果有 Voltage_source 保存的參數，那麼禁用 Current_source，反之亦然
        if saved_parameters_for_S1_S3_voltage_source:
            S1_S3_current_source_state = "disabled"
            voltage_source_state = "normal"
        else:
            S1_S3_current_source_state = "normal"
            voltage_source_state = "disabled"

        # 檢查 S5 ~ S8 如果有 Current_source 保存的參數，那麼禁用 Measurement_channel，反之亦然; 或者如果為 Both ，則都啟用
        if saved_parameters_for_S5_S8_current_source:
            S5_S8_current_source_state = "normal"
            Measurement_channel_state = "disabled"
        elif saved_parameters_for_S5_S8_Measurement_channel:
            S5_S8_current_source_state = "disabled"
            Measurement_channel_state = "normal"
        elif saved_parameters_for_S5_S8_Both:
            S5_S8_current_source_state = "normal"
            Measurement_channel_state = "normal"
            saved_parameters_for_S5_S8_current_source = saved_parameters_for_S5_S8_Both[:3]
            saved_parameters_for_S5_S8_Measurement_channel = saved_parameters_for_S5_S8_Both[
                3:]

        else:
            S5_S8_current_source_state = "normal"
            Measurement_channel_state = "disabled"

        # S9 & S10 & S11 & S1Ch1_Drive & S1Ch1_Sense & S1Ch1_Gate 只有一個選項，所以不用檢查

        if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
            # 填充 S1_S3_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, values=field_type, state=S1_S3_current_source_state, width=40)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_current_source 中的值
                    if i < len(saved_parameters_for_S1_S3_current_source):
                        combobox.set(saved_parameters_for_S1_S3_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(combobox)
                elif i == 1 :    
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        -2,                                                       # min_value
                        2,                                                        # max_value
                        S1_S3_current_source_state,                               # entry_state
                        40                                                        # entry_width
                    )
                # else:
                #     entry = ttk.Entry(
                #         S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, state=S1_S3_current_source_state, width=40)  # 根據條件禁用或啟用
                #     entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_current_source 中的值
                    if i < len(saved_parameters_for_S1_S3_current_source):
                        entry.insert(0, saved_parameters_for_S1_S3_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(entry)
                elif i == 2 :    
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        -10,                                                       # min_value
                        10,                                                        # max_value
                        S1_S3_current_source_state,                               # entry_state
                        40                                                        # entry_width
                    )
                    if i < len(saved_parameters_for_S1_S3_current_source):
                        entry.insert(0, saved_parameters_for_S1_S3_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(entry)
            
            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1_S3_current_source

            # 填充 S1_S3_Voltage_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Voltage_source"].items()):
                ttk.Label(S1_S3_Voltage_source_frame, text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_Voltage_source_frame, values=field_type, state=voltage_source_state, width=40)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_voltage_source 中的值
                    if i < len(saved_parameters_for_S1_S3_voltage_source):
                        combobox.set(saved_parameters_for_S1_S3_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(combobox)

                else:
                    entry = ttk.Entry(
                        S1_S3_Voltage_source_frame, state=voltage_source_state, width=40)  # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_voltage_source 中的值
                    if i < len(saved_parameters_for_S1_S3_voltage_source):
                        entry.insert(0, saved_parameters_for_S1_S3_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(entry)

            # 保存填充的 Voltage_source
            self.form_widgets[sensor]["Voltage_source"] = form_widgets_for_option_voltage_source

        elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
            # 填充 S5_S8_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, values=field_type, state=S5_S8_current_source_state, width=40)   # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S5_S8_current_source 中的值
                    if i < len(saved_parameters_for_S5_S8_current_source):
                        combobox.set(
                            saved_parameters_for_S5_S8_current_source[i])
                    form_widgets_for_option_S5_S8_current_source.append(
                        combobox)
                else:
                    # entry = ttk.Entry(
                    #     S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, state=S5_S8_current_source_state, width=40)   # 根據條件禁用或啟用
                    # entry.pack(anchor=tk.W, pady=5)
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        -0.2,                                                     # min_value
                        0.2,                                                      # max_value
                        S5_S8_current_source_state,                               # entry_state
                        40                                                        # entry_width
                    )
                    # 回填 saved_parameters_for_S5_S8_current_source 中的值
                    if i < len(saved_parameters_for_S5_S8_current_source):
                        entry.insert(
                            0, saved_parameters_for_S5_S8_current_source[i])
                    form_widgets_for_option_S5_S8_current_source.append(entry)

            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S5_S8_current_source

            # 填充 S5_S8_Measurement_channel 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Measurement_channel"].items()):
                ttk.Label(S5_S8_Measurement_channel_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S5_S8_Measurement_channel_frame, values=field_type, state=Measurement_channel_state, width=40)   # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S5_S8_Measurement_channel 中的值
                    if i < len(saved_parameters_for_S5_S8_Measurement_channel):
                        combobox.set(
                            saved_parameters_for_S5_S8_Measurement_channel[i])
                    form_widgets_for_option_Measurement_channel.append(
                        combobox)

                else:
                    entry = ttk.Entry(
                        S5_S8_Measurement_channel_frame, state=Measurement_channel_state, width=40)   # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S5_S8_Measurement_channel 中的值
                    if i < len(saved_parameters_for_S5_S8_Measurement_channel):
                        entry.insert(
                            0, saved_parameters_for_S5_S8_Measurement_channel[i])
                    form_widgets_for_option_Measurement_channel.append(entry)

            # 保存填充的 Measurement_channel
            self.form_widgets[sensor]["Measurement_channel"] = form_widgets_for_option_Measurement_channel

            # 初始化 S5_S8_Both 選項，結合前面 S5_S8_Current_source 、 S5_S8_Measurement_channel兩個選項的所有小部件
            self.form_widgets[sensor]["Both"] = self.form_widgets[sensor]["Current_source"] + \
                self.form_widgets[sensor]["Measurement_channel"]

        elif sensor in ["S9Ch1", "S9Ch2", "S9Ch3", "S9Ch4", "S9Ch5", "S9Ch6", "S9Ch7", "S9Ch8", "S10Ch1", "S10Ch2", "S10Ch3", "S10Ch4", "S10Ch5", "S10Ch6", "S10Ch7", "S10Ch8"]:
            # 填充 S9_S10_Thermometer 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Thermometer"].items()):
                ttk.Label(S9_S10_Thermometer_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S9_S10_Thermometer_frame, values=field_type, width=40)
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S9_S10_Thermometer 中的值
                    if i < len(saved_parameters_for_S9_S10_Thermometer):
                        combobox.set(
                            saved_parameters_for_S9_S10_Thermometer[i])
                    form_widgets_for_option_Thermometer.append(combobox)

                else:
                    entry = ttk.Entry(S9_S10_Thermometer_frame, width=40)
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S9_S10_Thermometer 中的值
                    if i < len(saved_parameters_for_S9_S10_Thermometer):
                        entry.insert(
                            0, saved_parameters_for_S9_S10_Thermometer[i])
                    form_widgets_for_option_Thermometer.append(entry)

            # 保存填充的 Thermometer
            self.form_widgets[sensor]["Thermometer"] = form_widgets_for_option_Thermometer

        elif sensor in ["S11Ch1", "S11Ch2", "S11Ch3", "S11Ch4", "S11Ch5", "S11Ch6", "S11Ch7", "S11Ch8"]:
            # 填充 S11_Trigger 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Trigger"].items()):
                ttk.Label(S11_Trigger_frame, text=label_text).pack(anchor=tk.W)
                combobox = ttk.Combobox(S11_Trigger_frame, values=field_type, width=40)
                combobox.pack(anchor=tk.W, pady=5)
                # 回填 saved_parameters_for_S11_Trigger 中的值
                if i < len(saved_parameters_for_S11_Trigger):
                    combobox.set(saved_parameters_for_S11_Trigger[i])
                else:
                    combobox.set(field_type[2])
                form_widgets_for_option_Trigger.append(combobox)

            # 保存填充的 Trigger
            self.form_widgets[sensor]["Trigger"] = form_widgets_for_option_Trigger

        elif sensor in ["S1Ch1 - Drive"]:
            # 填充 S1Ch1_Drive_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, values=field_type, width=40)
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1Ch1_Drive_current_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Drive_current_source):
                        combobox.set(
                            saved_parameters_for_S1Ch1_Drive_current_source[i])
                    form_widgets_for_option_S1Ch1_Drive_current_source.append(combobox)
                elif i == 1 :
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        0,                                                       # min_value
                        240,                                                        # max_value
                        "normal",                                                 # entry_state
                        40                                                        # entry_width
                    )
                # else:
                #     entry = ttk.Entry(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, width=40)
                #     entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1Ch1_Drive_current_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Drive_current_source):
                        entry.insert(
                            0, saved_parameters_for_S1Ch1_Drive_current_source[i])
                    form_widgets_for_option_S1Ch1_Drive_current_source.append(entry)
                elif i == 2 :
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        0,                                                       # min_value
                        11,                                                        # max_value
                        "normal",                                                 # entry_state
                        40                                                        # entry_width
                    )
                    if i < len(saved_parameters_for_S1Ch1_Drive_current_source):
                        entry.insert(
                            0, saved_parameters_for_S1Ch1_Drive_current_source[i])
                    form_widgets_for_option_S1Ch1_Drive_current_source.append(entry)

            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1Ch1_Drive_current_source

        elif sensor in ["S1Ch1 - Sense"]:
            # 填充 S1Ch1_Sense_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, values=field_type, width=40)
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1Ch1_Sense_current_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Sense_current_source):
                        combobox.set(
                            saved_parameters_for_S1Ch1_Sense_current_source[i])
                    form_widgets_for_option_S1Ch1_Sense_current_source.append(combobox)

                else:
                    # entry = ttk.Entry(S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame, width=40)
                    # entry.pack(anchor=tk.W, pady=5)
                    entry = self.create_ttk_entry_with_validation(
                        S1_S3_S5_S8_S1Ch1Drive_S1Ch1Sense_Current_source_frame,   # parent
                        -1,                                                       # min_value
                        1,                                                        # max_value
                        "normal",                                                 # entry_state
                        40                                                        # entry_width
                    )
                    # 回填 saved_parameters_for_S1Ch1_Sense_current_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Sense_current_source):
                        entry.insert(
                            0, saved_parameters_for_S1Ch1_Sense_current_source[i])
                    form_widgets_for_option_S1Ch1_Sense_current_source.append(entry)

            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1Ch1_Sense_current_source

        elif sensor in ["S1Ch1 - Gate"]:
            # 填充 S1Ch1_Gate_Voltage_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Voltage_source"].items()):
                ttk.Label(S1Ch1Gate_Voltage_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1Ch1Gate_Voltage_source_frame, values=field_type, width=40)
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1Ch1_Gate_Voltage_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Gate_Voltage_source):
                        combobox.set(
                            saved_parameters_for_S1Ch1_Gate_Voltage_source[i])
                    form_widgets_for_option_S1Ch1_Gate_Voltage_source.append(combobox)

                else:
                    entry = ttk.Entry(S1Ch1Gate_Voltage_source_frame, width=40)
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1Ch1_Gate_Voltage_source 中的值
                    if i < len(saved_parameters_for_S1Ch1_Gate_Voltage_source):
                        entry.insert(
                            0, saved_parameters_for_S1Ch1_Gate_Voltage_source[i])
                    form_widgets_for_option_S1Ch1_Gate_Voltage_source.append(entry)

            # 保存填充的 Voltage_source
            self.form_widgets[sensor]["Voltage_source"] = form_widgets_for_option_S1Ch1_Gate_Voltage_source

        # 儲存、取消按鈕排版
        ttk.Button(button_frame, text="儲存", command=lambda: self.save_parameters(
            sensor, self.option[sensor].get(), parameter_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=parameter_window.destroy).pack(
            side=tk.LEFT, padx=5)
        
        # 若有勾選 Trigger，則禁用 MS401 的 Current_source Option 和 Both Option
        if self.any_trigger_selected:
            if sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
                if "Current_source" in self.option_widget and self.option_widget["Current_source"].winfo_exists():
                    self.option_widget["Current_source"].configure(state=tk.DISABLED)
                if "Both" in self.option_widget and self.option_widget["Both"].winfo_exists():
                    self.option_widget["Both"].configure(state=tk.DISABLED)
                self.option[sensor].set("Measurement_channel")
            self.update_form(sensor)

    # 根據選擇的 Option 來開啟或禁用表單
    def update_form(self, sensor):
        if sensor in self.form_widgets:
            if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                for option, widgets in self.form_widgets[sensor].items():
                    if self.option[sensor].get() == option:
                        for widget in widgets:
                            if widget.winfo_exists():  # 檢查控件是否存在
                                widget.configure(state="normal")
                    else:
                        for widget in widgets:
                            if widget.winfo_exists():  # 檢查控件是否存在
                                widget.configure(state="disabled")

            elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
                # 當選擇 "Both" 時，先禁用所有小部件，再逐一啟用
                if self.option[sensor].get() == "Both":
                    for widgets in self.form_widgets[sensor].values():
                        for widget in widgets:
                            if widget.winfo_exists():  # 檢查控件是否存在
                                widget.configure(state="normal")
                else:
                    # 將所有小部件設置為禁用狀態
                    for widgets in self.form_widgets[sensor].values():
                        for widget in widgets:
                            if widget.winfo_exists():  # 檢查控件是否存在
                                widget.configure(state="disabled")

                    # 啟用選中的選項對應的小部件
                    for option, widgets in self.form_widgets[sensor].items():
                        if self.option[sensor].get() == option:
                            for widget in widgets:
                                if widget.winfo_exists():  # 檢查控件是否存在
                                    widget.configure(state="normal")

            

    def save_parameters(self, sensor, option, window):
        """此為保存參數的函式，將參數輸出至 params.json ， 並將參數保存到 saved_parameters 字典中以便按下 Next 之後輸出至 saved_parameters.json"""

        # 檢查輸入值是否有效
        if self.check_input_validation():
            # Collect the parameters from the form (now using a dictionary to store keys and values)
            params = {}

            # option 可以是 "Current_source" 或 "Voltage_source" 或 "Measurement_channel" 或 "Both"
            # Get the field names
            form_fields = self.sensor_option_parameters[sensor][option].keys()

            # Iterate over the widgets and save both the field names and their values
            for field_name, widget in zip(form_fields, self.form_widgets[sensor][option]):
                if isinstance(widget, ttk.Combobox):
                    # Get the selected value in Combobox
                    params[field_name] = widget.get()
                else:
                    params[field_name] = float(widget.get())   # Get the value in Entry

            # Delete previously saved parameters for this sensor-option pair
            for key in list(self.saved_parameters):
                if key == (sensor, option):  # 僅刪除與當前 sensor 和 option 配對的參數
                    del self.saved_parameters[key]

            # Save current parameters
            self.saved_parameters[(sensor, option)] = params
     
            # Print the saved parameters with keys and values
            print(f"提交的參數 ({sensor} - {option}): ")
            for field, value in params.items():
                print(f"{field}: {value}")

            print(self.saved_parameters)

            # 針對 S1_S3 清除另一個選項的內容
            if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                if option == "Current_source":
                    # 清除 Voltage_source 的內容
                    if (sensor, "Voltage_source") in self.saved_parameters:
                        del self.saved_parameters[(sensor, "Voltage_source")]
                        # 清空界面上的 Voltage_source 表單內容
                        for widget in self.form_widgets[sensor]["Voltage_source"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry
                elif option == "Voltage_source":
                    # 清除 Current_source 的內容
                    if (sensor, "Current_source") in self.saved_parameters:
                        del self.saved_parameters[(sensor, "Current_source")]
                        # 清空界面上的 Current_source 表單內容
                        for widget in self.form_widgets[sensor]["Current_source"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry

            # 針對 S5_S8 清除另一個選項的內容或是選擇 Both 的話兩個選項參數都保留
            if sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
                if option == "Current_source":
                    # 清除 Measurement_channel 的內容
                    if (sensor, "Measurement_channel") in self.saved_parameters:
                        print(sensor, option)
                        del self.saved_parameters[(sensor, "Measurement_channel")]
                        for widget in self.form_widgets[sensor]["Measurement_channel"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry
                    if (sensor, "Both") in self.saved_parameters:
                        print(sensor, option)
                        del self.saved_parameters[(sensor, "Both")]
                        for widget in self.form_widgets[sensor]["Both"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry

                elif option == "Measurement_channel":
                    # 清除 Current_source 的內容
                    if (sensor, "Current_source") in self.saved_parameters:
                        print(sensor, option)
                        del self.saved_parameters[(sensor, "Current_source")]
                        for widget in self.form_widgets[sensor]["Current_source"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry
                    if (sensor, "Both") in self.saved_parameters:
                        print(sensor, option)
                        del self.saved_parameters[(sensor, "Both")]
                        for widget in self.form_widgets[sensor]["Both"]:
                            if isinstance(widget, ttk.Combobox):
                                widget.set("")  # 清空 combobox
                            else:
                                widget.delete(0, tk.END)  # 清空 entry

                elif option == "Both":
                    # 刪除 Current_source 和 Measurement_channel 的 key (不清空表單)
                    if (sensor, "Current_source") in self.saved_parameters:
                        del self.saved_parameters[(sensor, "Current_source")]

                    if (sensor, "Measurement_channel") in self.saved_parameters:
                        del self.saved_parameters[(sensor, "Measurement_channel")]

                    both_params = self.saved_parameters[(sensor, option)]
                    current_source_params = {}
                    measurement_channel_params = {}

                    # 將 both_params 轉換為一個 list，這樣可以按索引操作
                    both_items = list(both_params.items())

                    # 使用 itertools.islice 對前3個和後5個分別切片
                    first_3_items = itertools.islice(both_items, 3)  # 前3個
                    last_5_items = itertools.islice(both_items, 3, 8)  # 第4到第8個

                    # 將前3個分配到 current_source_params
                    for field, value in first_3_items:
                        current_source_params[field] = value

                    # 將後5個分配到 measurement_channel_params
                    for field, value in last_5_items:
                        measurement_channel_params[field] = value  

            # 如果有勾選 Trigger，則將 S1 ~ S3 的所有參數清空以及 S5 ~ S8 的 Current_source 和 Both 的參數清空
            if sensor in ["S11Ch1", "S11Ch2", "S11Ch3", "S11Ch4", "S11Ch5", "S11Ch6", "S11Ch7", "S11Ch8"]:
                sensor_to_delete = [key for key, _ in self.saved_parameters.items() if (key[0] in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]) 
                                    or (key[0] in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"] and key[1] in ["Current_source", "Both"])]
                for sensor in sensor_to_delete:
                    del self.saved_parameters[sensor]

            # Save parameters to JSON file
            self.save_params()
            
            # 成功儲存後顯示訊息
            messagebox.showinfo("成功", "參數儲存成功！")

            # Close the window
            window.destroy()
        else:
            window.lift()
            window.focus_force()
            # 什麼都不做，因為 check_input_validation 已經顯示了警告訊息
            print("資料有誤，不執行儲存")

    # 第一頁按下 Next 按鈕後，將參數匯出至 saved_parameters.json
    def export_to_json(self):
        """Export saved parameters to a JSON file"""

        # Prepare the data for JSON export
        json_data = {}

        # Iterate over saved parameters and prepare them for JSON output
        for (sensor, option), params in self.saved_parameters.items():

            print(self.saved_parameters.items())

            # Create the "sensor-option" key to structure the output
            sensor_option = f"{sensor}_{option}"

            modified_params = {}
            for key, value in params.items():
                if value == "Switching":
                    # 將 "Switching" 轉換為 "PC"
                    modified_params[key] = "PC"
                elif key == "Auto range" or key == "Separate Vref for heating":
                    # 將 "On" 轉換為 True，"Off" 轉換為 False
                    if value == "On":
                        modified_params[key] = True
                    elif value == "Off":
                        modified_params[key] = False
                    else:
                        modified_params[key] = value  # 保持原來的值
                else:
                    # 保持原來的值
                    modified_params[key] = value

            # Store parameters as a dictionary for each sensor-option pair
            json_data[sensor_option] = modified_params

        # Write the json_data to a JSON file
        with open("saved_parameters.json", "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        print("參數已成功匯出到 saved_parameters.json")
    
    # 第一頁按下 Next 按鈕後，將參數匯出至 saved_parameters.json 並前往第二頁
    def go_to_page2(self):
        # 儲存參數至 JSON 檔
        self.export_to_json()
        """隱藏當前頁面，顯示下一頁面"""
        # 隱藏第一頁面的所有控件
        for widget in self.page1_widgets:
            widget.grid_forget()

        # 顯示第二頁面的控件
        self.create_page2()

    # 第二頁按下 Previous 按鈕後，返回第一頁
    def go_to_page1(self):
        """隱藏當前頁面，顯示第一頁"""
        # 隱藏第二頁面的所有控件
        for widget in self.page2_widgets:
            widget.pack_forget()

        # 顯示第一頁面的控件
        self.create_page1()

    # 創建第二頁
    def create_page2(self):
        """創建第二頁面"""

        # 用於儲存第二個頁面上的所有控件
        self.page2_widgets = []

        # 創建存儲第二頁參數的容器
        self.page2_parameters = {}

        # 創建外框架
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.page2_widgets.append(container)

        # 創建Canvas來實現滾動功能
        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        # 添加垂直滾動條
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # 將Canvas和滾動條進行連接
        canvas.configure(yscrollcommand=scrollbar.set)

        # 創建一個框架，放置於Canvas內部
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")   # 將該框架放置在Canvas中

        # 設置框架為Canvas的滾動區域
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 使得滾動輪也能工作
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        # 創建框架
        # 此框架用來放置檔名以及儲存路徑
        config_details_frame = ttk.LabelFrame(scrollable_frame, text="Config details")
        config_details_frame.grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.NSEW)
        
        # 此框架用來放置 Power Steps 、 Isense 選擇器 、 Idrive 選擇器
        power_steps_frame = ttk.LabelFrame(scrollable_frame, text="Power Steps")
        power_steps_frame.grid(column=0, row=1, padx=10,
                               pady=10, sticky=tk.NSEW)
       
        # 此框架用來放置 Measurement settings (加熱幾秒、冷卻幾秒、延遲幾秒、重複幾次)
        measurement_settings_frame = ttk.LabelFrame(
            scrollable_frame, text="Measurement settings")
        measurement_settings_frame.grid(
            column=0, row=2, padx=10, pady=10, sticky=tk.NSEW)
        
        # 創建是否使用重複測量功能按鈕
        self.cycling_test_var = tk.BooleanVar(value=False)  # 默認為未選中
        self.cycling_test_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Cycling Test", variable=self.cycling_test_var, command=self.toggle_cycling_test_checkbutton)
        self.cycling_test_checkbutton.grid(
            row=3, column=0, padx=10, pady=10)
        self.page2_parameters["Cycling_Test"] = self.cycling_test_var.get()

        # 此框架用來放置重複測量功能的參數 (短時間開啟幾秒、短時間關閉幾秒、短時間開關重複幾次、長時間開啟幾秒、長時間關閉幾秒、整個短+長時間完整過程重複幾次、有無要在測量時自動變更 LP220 Current [A] 的值)
        cycling_test_frame = ttk.LabelFrame(
            scrollable_frame, text="Cycling Test")
        cycling_test_frame.grid(
            column=0, row=4, padx=10, pady=10, sticky=tk.NSEW)
     
        # 是否連接 THERMOSTAT 、是否使用 TSP
        self.connect_thermostat_var = tk.BooleanVar(value=False)  # 連接 THERMOSTAT 默認為未選中
        self.tsp_var = tk.BooleanVar(value=False)  # 連接 TSP 默認為未選中

        # 創建是否連接 Thermostat 按鈕
        self.connect_thermostat_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Connect to Thermostat", variable=self.connect_thermostat_var, command=self.toggle_connect_thermostat_checkbutton)
        self.connect_thermostat_checkbutton.grid(
            row=5, column=0, padx=10, pady=10)
        self.page2_parameters["Connect_to_Thermostat"] = self.connect_thermostat_var.get()

        # 創建是否使用 TSP 按鈕
        self.tsp_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Calibration Set (TSP)", variable=self.tsp_var, command=self.toggle_tsp_checkbutton, state="disabled")
        self.tsp_checkbutton.grid(
            row=7, column=0, padx=10, pady=10)
        self.page2_parameters["TSP"] = self.tsp_var.get()

        # 此框架用來放置 Thermostat 溫度設定
        thermostat_settings_for_measurement_frame = ttk.LabelFrame(
            scrollable_frame, text="Thermostat Settings for Measurement")
        thermostat_settings_for_measurement_frame.grid(
            column=0, row=6, padx=10, pady=10, sticky=tk.NSEW)

        # 此框架用來放置 TSP 量測參數
        tsp_calibration_frame = ttk.LabelFrame(scrollable_frame, text="TSP calibration")
        tsp_calibration_frame.grid(
            column=0, row=8, padx=10, pady=10, sticky=tk.NSEW)

        # 此框架 Chrome 裡面有，但我相關參數直接於後端程式碼固定好了，所以目前用不到
        # advanced_thermostat_stability_settings_frame = ttk.LabelFrame(
        #     scrollable_frame, text="Advanced thermostat stability settings")
        # advanced_thermostat_stability_settings_frame.grid(
        #     column=0, row=9, padx=10, pady=10, sticky=tk.NSEW)

        # 添加 Previous 和 Next 按鈕
        previous_button = ttk.Button(
            scrollable_frame, text="Previous", command=self.go_to_page1)
        previous_button.grid(row=10, column=0, padx=10, pady=10, sticky="W")
        
        next_button = ttk.Button(scrollable_frame, text="Next", command=self.page2_export_to_json)
        next_button.grid(row=10, column=0, padx=10, pady=10, sticky="E")
     
        # 添加進度提示框架
        self.progress_text_frame = tk.Frame(scrollable_frame)
        self.progress_text_frame.grid(row=11, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # 進度提示框架內創建滾動條
        self.progress_text_scrollbar = tk.Scrollbar(self.progress_text_frame)
        self.progress_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # 滾動條在右側填充垂直方向

        # 創建放於進度提示框架內的提示訊息文本並綁定滾動條 (提示訊息文本須綁定滾動條，滾動條也需綁定提示訊息文本) ，默認禁用
        self.progress_text = tk.Text(self.progress_text_frame, height=10,  yscrollcommand=self.progress_text_scrollbar.set)
        self.progress_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 提示訊息文本填滿剩下的空間

        # 配置滾動條控制提示訊息文本 (提示訊息文本須綁定滾動條，滾動條也需綁定提示訊息文本)
        self.progress_text_scrollbar.config(command=self.progress_text.yview)

        # 單獨綁定滾輪事件到提示訊息文本，讓提示訊息文本也能使用滑鼠滾輪滾動
        self.progress_text.bind("<Enter>", lambda e: enable_progress_text_scroll())   # 鼠標進入提示訊息文本
        self.progress_text.bind("<Leave>", lambda e: disable_progress_text_scroll())   # 鼠標離開提示訊息文本

        # 啟用提示訊息文本滾動條
        def enable_progress_text_scroll():
            self.progress_text.bind("<MouseWheel>", on_progress_text_scroll)
        
        # 禁用提示訊息文本滾動條
        def disable_progress_text_scroll():
            self.progress_text.unbind("<MouseWheel>")

        # 於提示訊息文本的滾輪事件處理函數
        def on_progress_text_scroll(event):
            # 滾動 progress_text 控件
            self.progress_text.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"  # 阻止事件冒泡 (不讓滾動傳遞到外層的 Canvas 控件)

        '''config_details 框架內的內容'''
        # Config Name 標籤和輸入框
        config_label = ttk.Label(config_details_frame, text="Config Name:")   # Config Name 標籤
        config_label.grid(column=0, row=0, padx=10, pady=10)

        self.config_entry = ttk.Entry(config_details_frame)   # Config Name 輸入框
        self.config_entry.grid(column=1, row=0, padx=10, pady=10)
        self.page2_parameters["Config_Name"] = self.config_entry.get()

        # 儲存路徑選擇
        path_label = ttk.Label(config_details_frame, text="儲存路徑:")   # 儲存路徑標籤
        path_label.grid(column=0, row=1, padx=10, pady=10)

        self.path_display = ttk.Label(config_details_frame, text="未選擇路徑")   # 顯示儲存路徑
        self.path_display.grid(column=1, row=1, padx=10, pady=10)
        self.page2_parameters["storage_path"] = self.path_display.cget("text")

        def select_directory():
            # 打開文件夾選擇儲存路徑
            selected_path = filedialog.askdirectory()
            if selected_path:   # 如果選擇了路徑
                self.path_display.config(text=selected_path)   # 則將選擇的路徑顯示在 self.path_display

        # 選擇儲存路徑按鈕
        select_path_button = ttk.Button(
            config_details_frame, text="選擇路徑", command=select_directory)
        select_path_button.grid(column=2, row=1, padx=10, pady=10)

        '''Power Steps 框架內的內容'''
        # 根據 saved_parameters 中的資料動態生成表格: Sensor (MS401 Measurement_channel 的) 、 Isense 選擇器 (MS401 Current_source 的) 、 Idrive 選擇器 (LP220 Current_source 的)
        # 從 saved_parameters 中抓取 Sensor (MS401 Measurement_channel 的)
        ms401_measurement_channel = [
            sensor for sensor, option in self.saved_parameters if "Measurement_channel" in option or "Both" in option]
        # 從 saved_parameters 中抓取 Isense 選擇器 (MS401 Current_source 的)
        s5_s8_current_source = [sensor for sensor, option in self.saved_parameters if ("Current_source" in option and sensor.startswith(
            ("S5", "S6", "S7", "S8", "S1Ch1 - Sense"))) or ("Both" in option and sensor.startswith(("S5", "S6", "S7", "S8")))]
        # 從 saved_parameters 中抓取 Idrive 選擇器 (LP220 Current_source 的)
        s1_s3_current_source = [
            sensor for sensor, option in self.saved_parameters if "Current_source" in option and sensor.startswith(("S1", "S3", "S1Ch1 - Drive")) and sensor != "S1Ch1 - Sense"]

        # 顯示 "Calculation Method" 字
        method_label = ttk.Label(power_steps_frame, text="Calculation Method")
        method_label.grid(row=0, column=0, padx=10, pady=10)

        # 顯示公式
        formula_label = ttk.Label(
            power_steps_frame, text="Diode — Pstep = ||Vmeas,heat · (Idrive + Isense)| - |Vmeas,cool · Isense||")
        formula_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # 在類的初始化方法中初始化列表
        self.ms_401_labels = []
        self.combo_s5_s8s = []
        self.combo_s1_s3s = []

        row_index = 1  # 用來處理表格的起始行

        # 生成 Diode 、 Sensor (MS401 Measurement_channel 的) 、 Isense 選擇器 (MS401 Current_source 的) 、 Idrive 選擇器 (LP220 Current_source 的)
        for sensor in ms401_measurement_channel:
            # 第一欄：顯示 "Diode" 的欄位
            diode_label = ttk.Label(power_steps_frame, text="Diode")
            diode_label.grid(row=row_index, column=0, padx=10, pady=10)

            # 第二欄：顯示 Measurement_channel 的 Sensor
            self.ms_401_label = ttk.Label(power_steps_frame, text=sensor)
            self.ms_401_label.grid(row=row_index, column=1, padx=10, pady=10, sticky="E")
            # self.page2_parameters 已寫在下面

            # 將 ms_401_label 加入到 ms_401_labels 列表中
            self.ms_401_labels.append(self.ms_401_label)

            # 第三欄：顯示 S5 ~ S8 的 Current_source 選項
            Isense_label = ttk.Label(power_steps_frame, text="Isense: ")
            Isense_label.grid(row=row_index, column=2,
                              padx=10, pady=10, sticky="E")

            self.combo_s5_s8 = ttk.Combobox(
                power_steps_frame, values=s5_s8_current_source)
            self.combo_s5_s8.grid(row=row_index, column=3, padx=10, pady=10)
            # self.page2_parameters 已寫在下面

            # 將 combo_s5_s8 加入到 combo_s5_s8s 列表中
            self.combo_s5_s8s.append(self.combo_s5_s8)
            
            # 第四欄：顯示 S1 ~ S3 的 Current_source 選項
            Idrive_label = ttk.Label(power_steps_frame, text="Idrive: ")
            Idrive_label.grid(row=row_index, column=4, padx=10, pady=10)

            self.combo_s1_s3 = ttk.Combobox(
                power_steps_frame, values=s1_s3_current_source)
            self.combo_s1_s3.grid(row=row_index, column=5, padx=10, pady=10)
            # self.page2_parameters 已寫在下面

            # 將 combo_s1_s3 加入到 combo_s1_s3s 列表中
            self.combo_s1_s3s.append(self.combo_s1_s3)

            row_index += 1

        '''Measurement settings 框架內的內容'''
        # Heating time row
        heating_label = ttk.Label(
            measurement_settings_frame, text="Heating time [s]")
        heating_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        heating_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 0 ~ 4000")
        heating_range_label.grid(row=0, column=1, padx=10, pady=10)

        heating_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        heating_setpoint_label.grid(row=0, column=2, padx=10, pady=10)

        # self.heating_entry = ttk.Entry(measurement_settings_frame)
        # self.heating_entry.grid(row=0, column=3, padx=10, pady=10)
        self.heating_entry = self.create_ttk_entry_with_validation_grid(
                                measurement_settings_frame,   # parent
                                "normal",                     # state
                                0,                            # min_value
                                4000,                         # max_value
                                row=0,                        # grid row
                                column=3,                     # grid column
                                padx=10,                      # grid padx
                                pady=10                       # grid pady
                            )
        self.page2_parameters["Heating_time"] = self.heating_entry.get()

        # Cooling time row
        cooling_label = ttk.Label(
            measurement_settings_frame, text="Cooling time [s]")
        cooling_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        cooling_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 0 ~ 4000")
        cooling_range_label.grid(row=1, column=1, padx=10, pady=10)

        cooling_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        cooling_setpoint_label.grid(row=1, column=2, padx=10, pady=10)

        # self.cooling_entry = ttk.Entry(measurement_settings_frame)
        # self.cooling_entry.grid(row=1, column=3, padx=10, pady=10)
        self.cooling_entry = self.create_ttk_entry_with_validation_grid(
                                measurement_settings_frame,   # parent
                                "normal",                     # state
                                0,                            # min_value
                                4000,                         # max_value
                                row=1,                        # grid row
                                column=3,                     # grid column
                                padx=10,                      # grid padx
                                pady=10                       # grid pady
                            )
        self.page2_parameters["Cooling_time"] = self.cooling_entry.get()

        # Delay time row
        delay_label = ttk.Label(
            measurement_settings_frame, text="Delay time [s]")
        delay_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        delay_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 0 ~ 4000")
        delay_range_label.grid(row=2, column=1, padx=10, pady=10)

        delay_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        delay_setpoint_label.grid(row=2, column=2, padx=10, pady=10)

        # self.delay_entry = ttk.Entry(measurement_settings_frame)
        # self.delay_entry.grid(row=2, column=3, padx=10, pady=10)
        self.delay_entry = self.create_ttk_entry_with_validation_grid(
                                measurement_settings_frame,   # parent
                                "normal",                     # state
                                0,                            # min_value
                                4000,                         # max_value
                                row=2,                        # grid row
                                column=3,                     # grid column
                                padx=10,                      # grid padx
                                pady=10                       # grid pady
                            )
        self.page2_parameters["Delay_time"] = self.delay_entry.get()

        # Repeat times row
        repeat_label = ttk.Label(
            measurement_settings_frame, text="Repeat times")
        repeat_label.grid(row=3, column=0, padx=10, pady=10)

        repeat_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 1 ~ 100")
        repeat_range_label.grid(row=3, column=1, padx=10, pady=10)

        repeat_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        repeat_setpoint_label.grid(row=3, column=2, padx=10, pady=10)

        # self.repeat_entry = ttk.Entry(measurement_settings_frame)
        # self.repeat_entry.grid(row=3, column=3, padx=10, pady=10)
        self.repeat_entry = self.create_ttk_entry_with_validation_grid(
                                measurement_settings_frame,   # parent
                                "normal",                     # state
                                1,                            # min_value
                                100,                          # max_value
                                row=3,                        # grid row
                                column=3,                     # grid column
                                padx=10,                      # grid padx
                                pady=10                       # grid pady
                            )
        self.repeat_entry.insert(0, "1")   # 插入數字 1
        self.page2_parameters["Repeat_times"] = self.repeat_entry.get()

        '''Cycling Test 框架內的內容'''
        # Multi Pulse Cycling 字樣
        multi_pulse_cycling_label = ttk.Label(cycling_test_frame, text="Multi Pulse Cycling")
        multi_pulse_cycling_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        
        # Pulse Cycling On row
        pulse_cycling_on_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling On [s]: ")
        pulse_cycling_on_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_on_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_on_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling On [s]"] = self.pulse_cycling_on_entry.get()

        # Pulse Cycling Off row
        pulse_cycling_off_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Off [s]: ")
        pulse_cycling_off_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_off_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_off_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling Off [s]"] = self.pulse_cycling_off_entry.get()

        # Pulse Cycling Repeat row
        pulse_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Repeat: ")
        pulse_cycling_repeat_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_repeat_entry.grid(row=3, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling Repeat"] =  self.pulse_cycling_repeat_entry.get()

        # Rth Measurement 字樣
        rth_measurement_label = ttk.Label(cycling_test_frame, text="Rth Measurement")
        rth_measurement_label.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # Rth Measurement Heating Times row
        rth_measurement_heating_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Heating Times: ")
        rth_measurement_heating_times_label.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_heating_times_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.rth_measurement_heating_times_entry.grid(row=5, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Rth Measurement Heating Times"] = self.rth_measurement_heating_times_entry.get()

        # Rth Measurement Cooling Times row
        rth_measurement_cooling_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Cooling Times: ")
        rth_measurement_cooling_times_label.grid(row=6, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_cooling_times_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.rth_measurement_cooling_times_entry.grid(row=6, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Rth Measurement Cooling Times"] = self.rth_measurement_cooling_times_entry.get()

        # Total Cycling Test 字樣
        total_cycling_test_label = ttk.Label(cycling_test_frame, text="Total Cycling Test")
        total_cycling_test_label.grid(row=7, column=0, padx=10, pady=10, columnspan=2)

        # Total Measurement Cycling Repeat row
        total_measurement_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Total Measurement Cycling Repeat: ")
        total_measurement_cycling_repeat_label.grid(row=8, column=0, padx=10, pady=10, sticky="W")

        self.total_measurement_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.total_measurement_cycling_repeat_entry.grid(row=8, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["total Measurement Cycling Repeat"] =  self.total_measurement_cycling_repeat_entry.get()

        # 若有其他 LP220 Current [A] 請填下面字樣
        other_lp220_current_label = ttk.Label(
            cycling_test_frame, text="若有其他 LP220 Current [A] 請填下面")
        other_lp220_current_label.grid(row=9, column=0, padx=10, pady=10, columnspan=2)

        # Other LP220 Current [A] 01 row
        other_lp220_current_01_label = ttk.Label(
            cycling_test_frame, text="LP220 Current [A] 01: ")
        other_lp220_current_01_label.grid(row=10, column=0, padx=10, pady=10, sticky="W")
        
        self.other_lp220_current_01_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.other_lp220_current_01_entry.grid(row=10, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Other LP220 Current 01"] =  self.other_lp220_current_01_entry.get()

        # Other LP220 Current [A] 02 row
        other_lp220_current_02_label = ttk.Label(
            cycling_test_frame, text="LP220 Current [A] 02: ")
        other_lp220_current_02_label.grid(row=11, column=0, padx=10, pady=10, sticky="W")

        self.other_lp220_current_02_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.other_lp220_current_02_entry.grid(row=11, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Other LP220 Current 02"] =  self.other_lp220_current_02_entry.get()

        '''Thermostat Settings for Measurement 框架內的內容'''
        # Temperature [°C] row
        temperature_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="Temperature [°C]")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)

        temperature_range_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="範圍: -45 ~ 160")
        temperature_range_label.grid(row=0, column=1, padx=10, pady=10)

        temperature_setpoint_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="Setpoint: ")
        temperature_setpoint_label.grid(row=0, column=2, padx=10, pady=10)

        # self.temperature_entry = ttk.Entry(
        #     thermostat_settings_for_measurement_frame, state="disabled")  # 初始狀態為禁用
        # self.temperature_entry.grid(row=0, column=3, padx=10, pady=10)
        self.temperature_entry = self.create_ttk_entry_with_validation_grid(
                                    thermostat_settings_for_measurement_frame,   # parent
                                    "disabled",                                  # state
                                    -45,                                         # min_value
                                    160,                                         # max_value
                                    row=0,                                       # grid row
                                    column=3,                                    # grid column
                                    padx=10,                                     # grid padx
                                    pady=10                                      # grid pady
                                )
        self.page2_parameters["Temperature"] = self.temperature_entry.get()

        '''TSP calibration 框架內的內容'''
        # Tmin [°C] row
        tmin_label = ttk.Label(tsp_calibration_frame, text="Tmin [°C]")
        tmin_label.grid(row=0, column=0, padx=10, pady=10)

        tmin_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: -45 ~ 160")
        tmin_range_label.grid(row=0, column=1, padx=10, pady=10)

        tmin_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tmin_setpoint_label.grid(row=0, column=2, padx=10, pady=10)

        # self.tmin_entry = ttk.Entry(
        #     tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        # self.tmin_entry.grid(row=0, column=3, padx=10, pady=10)
        self.tmin_entry = self.create_ttk_entry_with_validation_grid(
                            tsp_calibration_frame,   # parent
                            "disabled",              # state
                            -45,                     # min_value
                            160,                     # max_value
                            row=0,                   # grid row
                            column=3,                # grid column
                            padx=10,                 # grid padx
                            pady=10                  # grid pady
                        )
        self.page2_parameters["Tmin"] = self.tmin_entry.get()

        # Tmax [°C] row
        tmax_label = ttk.Label(tsp_calibration_frame, text="Tmax [°C]")
        tmax_label.grid(row=1, column=0, padx=10, pady=10)

        tmax_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: -45 ~ 160")
        tmax_range_label.grid(row=1, column=1, padx=10, pady=10)

        tmax_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tmax_setpoint_label.grid(row=1, column=2, padx=10, pady=10)

        # self.tmax_entry = ttk.Entry(
        #     tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        # self.tmax_entry.grid(row=1, column=3, padx=10, pady=10)
        self.tmax_entry = self.create_ttk_entry_with_validation_grid(
                            tsp_calibration_frame,   # parent
                            "disabled",              # state
                            -45,                     # min_value
                            160,                     # max_value
                            row=1,                   # grid row
                            column=3,                # grid column
                            padx=10,                 # grid padx
                            pady=10                  # grid pady
                        )
        self.page2_parameters["Tmax"] = self.tmax_entry.get()

        # Tstep [°C] row
        tstep_label = ttk.Label(tsp_calibration_frame, text="Tstep [°C]")
        tstep_label.grid(row=2, column=0, padx=10, pady=10)

        tstep_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: 1 ~ 205")
        tstep_range_label.grid(row=2, column=1, padx=10, pady=10)

        tstep_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tstep_setpoint_label.grid(row=2, column=2, padx=10, pady=10)

        # self.tstep_entry = ttk.Entry(
        #     tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        # self.tstep_entry.grid(row=2, column=3, padx=10, pady=10)
        self.tstep_entry = self.create_ttk_entry_with_validation_grid(
                            tsp_calibration_frame,   # parent
                            "disabled",              # state
                            1,                       # min_value
                            205,                     # max_value
                            row=2,                   # grid row
                            column=3,                # grid column
                            padx=10,                 # grid padx
                            pady=10                  # grid pady
                        )
        self.page2_parameters["Tstep"] = self.tstep_entry.get()

        # 於 advanced_thermostat_stability_settings_frame 框架內的參數， Chrome 裡面有，但我相關參數直接於後端程式碼固定好了，所以目前用不到
        # Time window [s]
        # Max. allowed temp. change [°C]
        # ΔT from target [°C]
        # Timeout [s]

        self.update()  # 強制刷新頁面

    def toggle_cycling_test_checkbutton(self):
        """用來啟用或禁用 Cycling Test 的輸入框"""
        if self.cycling_test_var.get():  # 如果 cycling_test_checkbutton 被選中
            self.pulse_cycling_on_entry.config(state="normal")  # 啟用 pulse cycling on 輸入框
            self.pulse_cycling_off_entry.config(state="normal")  # 啟用 pulse cycling off 輸入框
            self.pulse_cycling_repeat_entry.config(state="normal")  # 啟用 pulse cycling repeat 輸入框
            self.rth_measurement_heating_times_entry.config(state="normal")  # 啟用 rth measurement heating times 輸入框
            self.rth_measurement_cooling_times_entry.config(state="normal")  # 啟用 rth measurement cooling times 輸入框
            self.total_measurement_cycling_repeat_entry.config(state="normal")  # 啟用 total measurement cycling repeat 輸入框
            self.other_lp220_current_01_entry.config(state="normal")  # 啟用 other_lp220_current_01_entry 輸入框
            self.other_lp220_current_02_entry.config(state="normal")  # 啟用 other_lp220_current_02_entry 輸入框
            self.heating_entry.delete(0, tk.END)   # 清空 heating 輸入框的內容
            self.heating_entry.config(state="disabled")   #禁用 heating 輸入框
            self.cooling_entry.delete(0, tk.END)   # 清空 cooling 輸入框的內容
            self.cooling_entry.config(state="disabled")   #禁用 cooling 輸入框
            self.delay_entry.delete(0, tk.END)   # 清空 delay 輸入框的內容
            self.delay_entry.config(state="disabled")   #禁用 delay 輸入框
            self.repeat_entry.delete(0, tk.END)   # 清空 repeat 輸入框的內容
            self.repeat_entry.config(state="disabled")   #禁用 repeat 輸入框
        else:
            self.pulse_cycling_on_entry.delete(0, tk.END)  # 清空 pulse cycling on 輸入框的內容
            self.pulse_cycling_on_entry.config(state="disabled")  # 禁用 pulse cycling on 輸入框
            self.pulse_cycling_off_entry.delete(0, tk.END)  # 清空 pulse cycling off 輸入框的內容
            self.pulse_cycling_off_entry.config(state="disabled")  # 禁用 pulse cycling off 輸入框
            self.pulse_cycling_repeat_entry.delete(0, tk.END)  # 清空 pulse cycling repeat 輸入框的內容
            self.pulse_cycling_repeat_entry.config(state="disabled")  # 禁用 pulse cycling repeat 輸入框
            self.rth_measurement_heating_times_entry.delete(0, tk.END)  # 清空 rth measurement heating times 輸入框的內容
            self.rth_measurement_heating_times_entry.config(state="disabled")  # 禁用 rth measurement heating times 輸入框
            self.rth_measurement_cooling_times_entry.delete(0, tk.END)  # 清空 rth measurement cooling times 輸入框的內容
            self.rth_measurement_cooling_times_entry.config(state="disabled")  # 禁用 rth measurement cooling times 輸入框
            self.total_measurement_cycling_repeat_entry.delete(0, tk.END)  # 清空 total measurement cycling repeat 輸入框的內容
            self.total_measurement_cycling_repeat_entry.config(state="disabled")  # 禁用 total measurement cycling repeat 輸入框
            self.other_lp220_current_01_entry.delete(0, tk.END)  # 清空 other_lp220_current_01_entry 輸入框的內容
            self.other_lp220_current_01_entry.config(state="disabled")  # 禁用 other_lp220_current_01_entry 輸入框
            self.other_lp220_current_02_entry.delete(0, tk.END)  # 清空 other_lp220_current_02_entry 輸入框的內容
            self.other_lp220_current_02_entry.config(state="disabled")  # 禁用 other_lp220_current_02_entry 輸入框
            self.heating_entry.config(state="normal")  # 啟用 heating 輸入框
            self.cooling_entry.config(state="normal")  # 啟用 cooling 輸入框
            self.delay_entry.config(state="normal")  # 啟用 delay 輸入框
            self.repeat_entry.config(state="normal")  # 啟用 repeat 輸入框
            self.repeat_entry.delete(0, tk.END)   # 清空 repeat 輸入框的內容
            self.repeat_entry.insert(0, "1")   # 在 repeat 輸入框填入數字 1
    
    def toggle_connect_thermostat_checkbutton(self):
        """用來啟用或禁用 tsp 選項以及 temperature"""
        if self.connect_thermostat_var.get():  # 如果 "Connect to Thermostat" Checkbutton 被選中
            self.open_connect_thermostat_set_up_window()  # 彈出填寫 Thermostat 設定值的視窗
            self.tsp_checkbutton.config(state="normal")  # 啟用 TSP Checkbutton
            self.temperature_entry.config(state="normal")  # 啟用 temperature 輸入框
        else:
            self.tsp_var.set(False)  # 清空 TSP Checkbutton 內容
            self.tsp_checkbutton.config(state="disabled")  # 禁用 TSP Checkbutton
            self.temperature_entry.delete(0, tk.END)  # 清空 temperature 輸入框的內容
            self.temperature_entry.config(
                state="disabled")  # 禁用 temperature 輸入框
            self.tmin_entry.delete(0, tk.END)  # 清空 tmin 輸入框的內容
            self.tmin_entry.config(state="disabled")  # 禁用 tmin 輸入框
            self.tmax_entry.delete(0, tk.END)  # 清空 tmax 輸入框的內容
            self.tmax_entry.config(state="disabled")  # 禁用 tmax 輸入框
            self.tstep_entry.delete(0, tk.END)  # 清空 tstep 輸入框的內容
            self.tstep_entry.config(state="disabled")  # 禁用 tstep 輸入框

    # 創建填寫 Thermostat 設定值的彈出視窗
    def open_connect_thermostat_set_up_window(self):

        self.connect_thermostat_set_up_parameters = {
            "Thermostat type": ["請選擇", "JULABO_HE", "JULABO_F", "JULABO_CF", "MICRED", "ARROYO", "ESPEC", "ESPEC (No Addressing)", "HUBER_PB", "PELNUS (ADR1, BCC)", "LAUDA Variocool", "LAUDA Proline RP"],
            "Interface": ["RS232"],
            "Baudrate": ["請選擇", 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000],
            "Data bits": ["請選擇", 7, 8],
            "Parity": ["請選擇", "NONE", "ODD", "EVEN"],
            "Stop bits": ["請選擇", "SB1", "SB2"],
            "Handshake": ["請選擇", "NONE", "XON/XOFF", "REQUESTTOSEND", "REQUESTTOSENDXONXOFF"]
        }

        # 建立彈出視窗
        self.connect_thermostat_set_up_window = tk.Toplevel(self)
        self.connect_thermostat_set_up_window.title("Thermostat Set Up")
        self.connect_thermostat_set_up_window.geometry("800x600")

        # 初始化用於保存選擇值的字典
        self.save_thermostat_config = {}

        self.create_connect_thermostat_set_up_comboboxes()

        # 儲存、取消按鈕
        ttk.Button(self.connect_thermostat_set_up_window, text="儲存", command=self.save_thermostat_config_to_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.connect_thermostat_set_up_window, text="取消", command=self.connect_thermostat_set_up_window.destroy).pack(
            side=tk.LEFT, padx=5)
    
    # Thermostat 設定值彈出視窗內的表單控件
    def create_connect_thermostat_set_up_comboboxes(self):
        for label_text, options in self.connect_thermostat_set_up_parameters.items():
            # 創建 Label
            label = ttk.Label(self.connect_thermostat_set_up_window, text=label_text)
            label.pack(anchor=tk.W, padx=5, pady=5)

            # 創建 Combobox
            combobox = ttk.Combobox(self.connect_thermostat_set_up_window, values=options)
            combobox.pack(anchor=tk.W, padx=5, pady=5)
            combobox.set(options[0])  # 設置預設值
            combobox.label_text = label_text  # 設置標籤屬性

            # 綁定選擇事件
            combobox.bind("<<ComboboxSelected>>", lambda event, key=label_text: self.on_combobox_selected(event, key))

            # 初始化選擇值
            self.save_thermostat_config[label_text] = options[0]

    # Thermostat 設定值彈出視窗內的下拉式選單選擇事件
    def on_combobox_selected(self, event, key):
        # 更新選擇值
        value = event.widget.get()
        if key in ["Baudrate", "Data bits"]:
            value = int(value)  # 將需要轉換為整數的值進行轉換
        self.save_thermostat_config[key] = value

        # 根據 Thermostat type 來預設其他參數
        if key == "Thermostat type":
            if value == "ARROYO":
                self.update_default_parameters(9600, 8, "NONE", "SB1", "NONE")
            elif value == "MICRED":
                self.update_default_parameters(1200, 8, "NONE", "SB1", "NONE")
            elif value == "JULABO_HE":
                self.update_default_parameters(4800, 7, "EVEN", "SB1", "NONE") 
            elif value == "請選擇":
                self.update_default_parameters("請選擇", "請選擇", "請選擇", "請選擇", "請選擇") 

    # 根據 Thermostat type 來預設其他參數
    def update_default_parameters(self, baudrate, data_bits, parity, stop_bits, handshake):
        self.save_thermostat_config["Baudrate"] = baudrate
        self.save_thermostat_config["Data bits"] = data_bits
        self.save_thermostat_config["Parity"] = parity
        self.save_thermostat_config["Stop bits"] = stop_bits
        self.save_thermostat_config["Handshake"] = handshake
        # 遍歷其餘 Combobox 並預設其值
        for widget in self.connect_thermostat_set_up_window.winfo_children():
            if isinstance(widget, ttk.Combobox) and getattr(widget, 'label_text', '') == "Baudrate":
                widget.set(baudrate)
            if isinstance(widget, ttk.Combobox) and getattr(widget, 'label_text', '') == "Data bits":
                widget.set(data_bits)
            if isinstance(widget, ttk.Combobox) and getattr(widget, 'label_text', '') == "Parity":
                widget.set(parity)
            if isinstance(widget, ttk.Combobox) and getattr(widget, 'label_text', '') == "Stop bits":
                widget.set(stop_bits)
            if isinstance(widget, ttk.Combobox) and getattr(widget, 'label_text', '') == "Handshake":
                widget.set(handshake)

    # 儲存 Thermostat 設定值到 JSON 檔案
    def save_thermostat_config_to_json(self):
        if self.save_thermostat_config["Thermostat type"] == "MICRED":
            self.save_thermostat_config["Thermostat type"] = "MICREDTHT"
        # 將選擇值寫入 JSON 檔案
        with open('thermostat_config_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.save_thermostat_config, f, ensure_ascii=False, indent=4)
        self.connect_thermostat_set_up_window.destroy()
    
    def toggle_tsp_checkbutton(self):
        """用來啟用或禁用 TSP calibration 的輸入框"""
        if self.tsp_var.get():  # 如果 tspCheckbutton 被選中
            self.tmin_entry.config(state="normal")  # 啟用 tmin 輸入框
            self.tmax_entry.config(state="normal")  # 啟用 tmax 輸入框
            self.tstep_entry.config(state="normal")  # 啟用 tstep 輸入框
        else:
            self.tmin_entry.delete(0, tk.END)  # 清空 tmin 輸入框的內容
            self.tmin_entry.config(state="disabled")  # 禁用 tmin 輸入框
            self.tmax_entry.delete(0, tk.END)  # 清空 tmax 輸入框的內容
            self.tmax_entry.config(state="disabled")  # 禁用 tmax 輸入框
            self.tstep_entry.delete(0, tk.END)  # 清空 tstep 輸入框的內容
            self.tstep_entry.config(state="disabled")  # 禁用 tstep 輸入框

    # 獲取 SI 所需的 CurrentSourceParams 參數值
    def fill_current_source_params(self, config_data):

        # Sensor 的 Alias 對應表
        self.sensor_rename = {
            "S1Ch1": "/T3STER/0/LP220/SLOT1/CH0",
            "S1Ch2": "/T3STER/0/LP220/SLOT1/CH1",
            "S3Ch1": "/T3STER/0/LP220/SLOT3/CH0",
            "S3Ch2": "/T3STER/0/LP220/SLOT3/CH1",
            "S5Ch1": "/T3STER/0/MS401/SLOT5/CH0",
            "S5Ch2": "/T3STER/0/MS401/SLOT5/CH1",
            "S5Ch3": "/T3STER/0/MS401/SLOT5/CH2",
            "S5Ch4": "/T3STER/0/MS401/SLOT5/CH3",
            "S6Ch1": "/T3STER/0/MS401/SLOT6/CH0",
            "S6Ch2": "/T3STER/0/MS401/SLOT6/CH1",
            "S6Ch3": "/T3STER/0/MS401/SLOT6/CH2",
            "S6Ch4": "/T3STER/0/MS401/SLOT6/CH3",
            "S7Ch1": "/T3STER/0/MS401/SLOT7/CH0",
            "S7Ch2": "/T3STER/0/MS401/SLOT7/CH1",
            "S7Ch3": "/T3STER/0/MS401/SLOT7/CH2",
            "S7Ch4": "/T3STER/0/MS401/SLOT7/CH3",
            "S8Ch1": "/T3STER/0/MS401/SLOT8/CH0",
            "S8Ch2": "/T3STER/0/MS401/SLOT8/CH1",
            "S8Ch3": "/T3STER/0/MS401/SLOT8/CH2",
            "S8Ch4": "/T3STER/0/MS401/SLOT8/CH3",
            "S11Ch1": "/T3STER/0/EL100/SLOT11/TRIGGER0",
            "S11Ch2": "/T3STER/0/EL100/SLOT11/TRIGGER1",
            "S11Ch3": "/T3STER/0/EL100/SLOT11/TRIGGER2",
            "S11Ch4": "/T3STER/0/EL100/SLOT11/TRIGGER3",
            "S11Ch5": "/T3STER/0/EL100/SLOT11/TRIGGER4",
            "S11Ch6": "/T3STER/0/EL100/SLOT11/TRIGGER5",
            "S11Ch7": "/T3STER/0/EL100/SLOT11/TRIGGER6",
            "S11Ch8": "/T3STER/0/EL100/SLOT11/TRIGGER7",
            "S1Ch1 - Drive": "/PWB240/PWB10018/CH0/DriveSour/0",
            "S1Ch1 - Sense": "/PWB240/PWB10018/CH0/SensSour/0"
        }

        # 若有輸入的 Current Source 參數值，則將其填入 current_source_params
        current_source_params = []    

        for sensor in self.sensor_rename.keys():
            if f"{sensor}_Current_source" in config_data:
                if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
                    current_source_params.append({
                        "Alias": self.sensor_rename[sensor],
                        "UserAlias": sensor,
                        "Delay": {
                            "DelayFallingUs": {
                                "default": 0,
                                "locked": False,
                                "min": -16383,
                                "max": 5000
                            },
                            "DelayRisingUs": {
                                "default": 0,
                                "locked": False,
                                "min": -16383,
                                "max": 16383
                            }
                        },
                        "OutputMode": {"default": config_data[f"{sensor}_Current_source"]["Output mode"], "locked": False},
                        "SetCurrent": {"default": float(config_data[f"{sensor}_Current_source"]["Current [A]"]), "locked": False, "min": -2, "max": 2},
                        "VoltageCorner": {"default": float(config_data[f"{sensor}_Current_source"]["Voltage limit [V]"]), "locked": False, "min": -10, "max": 10}
                    })
                elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2", "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
                    current_source_params.append({
                        "Alias": self.sensor_rename[sensor],
                        "UserAlias": sensor,
                        "OutputMode": {"default": config_data[f"{sensor}_Current_source"]["Output mode"], "locked": False},
                        "SetCurrent": {"default": float(config_data[f"{sensor}_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                        "VoltageCorner": {"default": float(config_data[f"{sensor}_Current_source"]["Range [V]"]), "locked": False, "min": -10, "max": 10}
                    })
                elif sensor in "S1Ch1 - Drive":
                    current_source_params.append({
                        "Alias": self.sensor_rename[sensor],
                        "UserAlias": f"PWB10018 - {sensor}",
                        "OutputMode": {"default": config_data[f"{sensor}_Current_source"]["Output mode"], "locked": False},
                        "SetCurrent": {"default": float(config_data[f"{sensor}_Current_source"]["Current [A]"]), "locked": False, "min": 0, "max": 240},
                        "VoltageCorner": {"default": float(config_data[f"{sensor}_Current_source"]["Voltage limit [V]"]), "locked": False, "min": 0, "max": 11},
                        "TriggerSource": ""
                    })
                elif sensor in "S1Ch1 - Sense":
                    current_source_params.append({
                        "Alias": self.sensor_rename[sensor],
                        "UserAlias": f"PWB10018 - {sensor}",
                        "OutputMode": {"default": config_data[f"{sensor}_Current_source"]["Output mode"], "locked": False},
                        "SetCurrent": {"default": float(config_data[f"{sensor}_Current_source"]["Current [A]"]), "locked": False, "min": -1, "max": 1},
                        "VoltageCorner": {"default": float(config_data[f"{sensor}_Current_source"]["Range [V]"]), "locked": False, "min": 0, "max": 11},
                        "TriggerSource": ""
                    })
            if f"{sensor}_Both" in config_data:
                current_source_params.append({
                    "Alias": self.sensor_rename[sensor],
                    "UserAlias": sensor,
                    "OutputMode": {"default": config_data[f"{sensor}_Both"]["Output mode"], "locked": False},
                    "SetCurrent": {"default": float(config_data[f"{sensor}_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                    "VoltageCorner": {"default": float(config_data[f"{sensor}_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40},
                })

        return current_source_params

    # 獲取 SI 所需的 MeasCardChParams 參數值
    def fill_measurement_params(self, config_data):

        # LP401 的 Measurement channel 的 Range 轉成 SI 機台讀得懂的對應表
        self.range_rename = {
            "Fall scale: 20 V, V(in): -10 V ~ 10 V": 9,
            "Fall scale: 10 V, V(in): -10 V ~ 10 V": 10,
            "Fall scale: 4 V, V(in): -10 V ~ 10 V": 11,
            "Fall scale: 2 V, V(in): -10 V ~ 10 V": 12,
            "Fall scale: 1 V, V(in): -10 V ~ 10 V": 13,
            "Fall scale: 20 V, V(in): -20 V ~ 20 V": 6,
            "Fall scale: 8 V, V(in): -20 V ~ 20 V": 7,
            "Fall scale: 4 V, V(in): -20 V ~ 20 V": 8,
            "Fall scale: 40 V, V(in): -40 V ~ 40 V": 3,
            "Fall scale: 16 V, V(in): -40 V ~ 40 V": 4,
            "Fall scale: 8 V, V(in): -40 V ~ 40 V": 5,
            "Fall scale: 32 V, V(in): -80 V ~ 80 V": 0,
            "Fall scale: 16 V, V(in): -80 V ~ 80 V": 1,
            "Fall scale: 8 V, V(in): -80 V ~ 80 V": 2
        }

        # 若有輸入的 Measurement channel 參數值，則將其填入 measurement_params
        measurement_params = [] 
        measurement_channels = config_data["Measurement_channel"]

        # 遍歷 Measurement_channel 列表
        for channel in measurement_channels:
            ms_401_value = channel["MS_401"]  # 當前的 MS_401 值
            isense_value = channel["Isense"]  # 當前的 Isense 值
            idrive_value = channel["Idrive"]  # 當前的 Idrive 值
            
            # 使用 self.sensor_rename 轉換 Isense 和 Idrive 值
            isense_path = self.sensor_rename.get(isense_value, "")
            idrive_path = self.sensor_rename.get(idrive_value, "")

            # 創建 SI 看得懂的參數列表
            if f"{ms_401_value}_Measurement_channel" in config_data:
                    
                range_value = config_data[f"{ms_401_value}_Measurement_channel"].get("Range", "")
                range_idx = self.range_rename.get(range_value, None)  # 從 range_rename 獲取對應的索引

                measurement_params.append({
                    "Alias": self.sensor_rename.get(ms_401_value, ""),
                    "UserAlias": ms_401_value,
                    "Sensitivity": {"default": [config_data[f"{ms_401_value}_Measurement_channel"]["Sensitivity [mV/K]"]], "locked": False},
                    "PowerStep": f"@POWERSTEP_DIODE;{isense_path};{idrive_path}",
                    "RangeIdx": {"default": range_idx, "locked": False},
                    "AutoRange": {"default": config_data[f"{ms_401_value}_Measurement_channel"]["Auto range"], "locked": False},
                    "Uref": {"default": config_data[f"{ms_401_value}_Measurement_channel"]["Vref [V]"], "locked": False},
                    "UrefSwitching": {"default": config_data[f"{ms_401_value}_Measurement_channel"]["Separate Vref for heating"], "locked": False},
                    "UrefHeating": {"default": config_data[f"{ms_401_value}_Measurement_channel"]["Vref,heating [V]"], "locked": False},                
                })

            if f"{ms_401_value}_Both" in config_data:
                    
                range_value = config_data[f"{ms_401_value}_Both"].get("Measurement_channel_Range", "")
                range_idx = self.range_rename.get(range_value, None)  # 從 range_rename 獲取對應的索引
                    
                measurement_params.append({
                    "Alias": self.sensor_rename.get(ms_401_value, ""),
                    "UserAlias": ms_401_value,
                    "Sensitivity": {"default": [config_data[f"{ms_401_value}_Both"]["Sensitivity [mV/K]"]], "locked": False},
                    "PowerStep": f"@POWERSTEP_DIODE;{isense_path};{idrive_path}",
                    "RangeIdx": {"default": range_idx, "locked": False},
                    "AutoRange": {"default": config_data[f"{ms_401_value}_Both"]["Auto range"], "locked": False},
                    "Uref": {"default": config_data[f"{ms_401_value}_Both"]["Vref [V]"], "locked": False},
                    "UrefSwitching": {"default": config_data[f"{ms_401_value}_Both"]["Separate Vref for heating"], "locked": False},
                    "UrefHeating": {"default": config_data[f"{ms_401_value}_Both"]["Vref,heating [V]"], "locked": False},
                })

        return measurement_params

    # 第二頁按下 Next 按鈕會將所有參數匯出至 saved_parameters.json 並開始運行機台
    def page2_export_to_json(self):

        # 檢查輸入值是否有效
        if self.check_input_validation():

            # 定義 JSON 檔案路徑
            file_path = "saved_parameters.json"

            # 確保控件的值是最新的
            self.page2_parameters["Config_Name"] = self.config_entry.get()
            self.page2_parameters["storage_path"] = self.path_display.cget("text")

            # 確保控件的值是最新的 & 判斷是否有輸入參數，若無，則預設為 0
            try:
                self.page2_parameters["Heating_time"] = float(self.heating_entry.get()) if self.heating_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Heating_time"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Cooling_time"] = float(self.cooling_entry.get()) if self.cooling_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Cooling_time"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Delay_time"] = float(self.delay_entry.get()) if self.delay_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Delay_time"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Repeat_times"] = int(self.repeat_entry.get()) if self.repeat_entry.get() else 0
            except ValueError:
                self.page2_parameters["Repeat_times"] = 0  # 或其他預設值

            self.page2_parameters["Cycling_Test"] = self.cycling_test_var.get()

            try:
                self.page2_parameters["Pulse Cycling On [s]"] = float(self.pulse_cycling_on_entry.get()) if self.pulse_cycling_on_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Pulse Cycling On [s]"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Pulse Cycling Off [s]"] = float(self.pulse_cycling_off_entry.get()) if self.pulse_cycling_off_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Pulse Cycling Off [s]"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Pulse Cycling Repeat"] = int(self.pulse_cycling_repeat_entry.get()) if self.pulse_cycling_repeat_entry.get() else 0
            except ValueError:
                self.page2_parameters["Pulse Cycling Repeat"] = 0  # 或其他預設值
            try:
                self.page2_parameters["Rth Measurement Heating Times"] = float(self.rth_measurement_heating_times_entry.get()) if self.rth_measurement_heating_times_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Rth Measurement Heating Times"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["Rth Measurement Cooling Times"] = float(self.rth_measurement_cooling_times_entry.get()) if self.rth_measurement_cooling_times_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Rth Measurement Cooling Times"] = 0.0  # 或其他預設值
            try:
                self.page2_parameters["total Measurement Cycling Repeat"] = int(self.total_measurement_cycling_repeat_entry.get()) if self.total_measurement_cycling_repeat_entry.get() else 0
            except ValueError:
                self.page2_parameters["total Measurement Cycling Repeat"] = 0  # 或其他預設值
            try:
                self.page2_parameters["Other LP220 Current 01"] =  float(self.other_lp220_current_01_entry.get()) if self.other_lp220_current_01_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Other LP220 Current 01"] = 0.0 # 或其他預設值
            try:
                self.page2_parameters["Other LP220 Current 02"] =  float(self.other_lp220_current_02_entry.get()) if self.other_lp220_current_02_entry.get() else 0.0
            except ValueError:
                self.page2_parameters["Other LP220 Current 02"] = 0.0 # 或其他預設值

            self.page2_parameters["Connect_to_Thermostat"] = self.connect_thermostat_var.get()

            try:
                self.page2_parameters["Temperature"] = int(self.temperature_entry.get()) if self.temperature_entry.get() else 0
            except ValueError:
                self.page2_parameters["Temperature"] = 0  # 或其他預設值

            self.page2_parameters["TSP"] = self.tsp_var.get()

            try:
                self.page2_parameters["Tmin"] = int(self.tmin_entry.get()) if self.tmin_entry.get() else 0
            except ValueError:
                self.page2_parameters["Tmin"] = 0  # 或其他預設值
            try:
                self.page2_parameters["Tmax"] = int(self.tmax_entry.get()) if self.tmax_entry.get() else 0
            except ValueError:
                self.page2_parameters["Tmax"] = 0  # 或其他預設值
            try:
                self.page2_parameters["Tstep"] = int(self.tstep_entry.get()) if self.tstep_entry.get() else 0
            except ValueError:
                self.page2_parameters["Tstep"] = 0  # 或其他預設值

            # 若有其他 LP220 Current 參數
            other_lp220_current_list = []
            
            if self.page2_parameters["Other LP220 Current 01"] != 0:
                other_lp220_current_list.append(self.page2_parameters["Other LP220 Current 01"])
            if self.page2_parameters["Other LP220 Current 02"] != 0:
                other_lp220_current_list.append(self.page2_parameters["Other LP220 Current 02"])
            
            self.page2_parameters["Other LP220 Current list"] = other_lp220_current_list

            # 將每一行的 `ms_401_label`、`combo_s5_s8`、`combo_s1_s3` 的值儲存到列表中
            sensors_data = []

            for i in range(len(self.ms_401_labels)):
                sensor_info = {
                    "MS_401": self.ms_401_labels[i].cget("text"),  # Sensor 名稱
                    "Isense": self.combo_s5_s8s[i].get(),  # 用戶選擇的 Isense 值
                    "Idrive": self.combo_s1_s3s[i].get()   # 用戶選擇的 Idrive 值
                }
                sensors_data.append(sensor_info)

            # 將 Sensors 列表保存到 page2_parameters
            self.page2_parameters["Measurement_channel"] = sensors_data
            
            # 檢查檔案是否存在
            if os.path.exists(file_path):
                # 如果存在，打開檔案並讀取現有內容
                with open(file_path, "r") as file:
                    try:
                        # 讀取已存在的資料
                        saved_data = json.load(file)
                    except json.JSONDecodeError:
                        # 如果檔案是空的或格式錯誤，初始化為空字典
                        saved_data = {}
            else:
                # 如果檔案不存在，初始化為空字典
                saved_data = {}

            # 將新參數添加進去
            saved_data.update(self.page2_parameters)

            # 使用 fill_current_source_params 以及 fill_measurement_params 填充數據
            config_data = saved_data  # 使用已存在的 JSON 檔案數據
            current_source_data = []
            current_source_data.extend(self.fill_current_source_params(config_data))
            measurement_channel_data = []
            measurement_channel_data.extend(self.fill_measurement_params(config_data))
            
            # 如果有數據，將其放入 saved_data 中
            if "Resources" not in saved_data:
                saved_data["Resources"] = {}
            saved_data["Resources"]["CurrentSourceParams"] = current_source_data
            saved_data["Resources"]["MeasCardChParams"] = measurement_channel_data
            
            # 將更新後的資料寫回到 JSON 文件中
            with open(file_path, "w") as file:
                json.dump(saved_data, file, indent=4)

            with open(file_path, "r") as file:
                config_data = json.load(file)

            # 將 Thermostat 參數 (此為等待 Thermostat 平衡好溫度之後再量測的參數表) 填入 config_data 等待寫入 saved_parameters.json
            thermostatParams_data = [{
                        "Alias": "/THERMOSTAT/0",
                        "UserAlias": "Th0",
                        "SetTemperature": {
                            "default": config_data["Temperature"],
                            "locked": False,
                            "max": 50,
                            "min": 0
                        },
                        "StabilityCriteria": {
                            "DtMinMax": {
                                "default": 0.1,
                                "locked": False,
                                "max": 5,
                                "min": 0.0001
                                },
                            "DtTarget": {
                                "default": 0.25,
                                "locked": False,
                                "max": 10,
                                "min": 0.0001
                                },
                            "TimeWindow": {
                                "default": 60,
                                "locked": False,
                                "max": 100,
                                "min": 15
                                },
                            "Timeout": {
                                "default": 1800,
                                "locked": False,
                                "max": 4000,
                                "min": 30
                                }
                        },
                        "WaitForStabilityBeforeMeas": {
                        "default": True,
                        "locked": False
                        }                   
                    }]
            
            if config_data["Temperature"] != 0:
                config_data["Resources"]["ThermostatParams"] = thermostatParams_data
            else:
                config_data["Resources"]["ThermostatParams"] = []

            # 將 Thermostat 參數 (此為不等待 Thermostat 平衡好溫度就直接量測的參數表) 填入 config_data 等待寫入 saved_parameters.json
            thermostatParams_data_no_wait = [{
                        "Alias": "/THERMOSTAT/0",
                        "UserAlias": "Th0",
                        "SetTemperature": {
                            "default": config_data["Temperature"],
                            "locked": False,
                            "max": 50,
                            "min": 0
                        },
                        "StabilityCriteria": {
                            "DtMinMax": {
                                "default": 0.1,
                                "locked": False,
                                "max": 5,
                                "min": 0.0001
                                },
                            "DtTarget": {
                                "default": 0.25,
                                "locked": False,
                                "max": 10,
                                "min": 0.0001
                                },
                            "TimeWindow": {
                                "default": 60,
                                "locked": False,
                                "max": 100,
                                "min": 1
                                },
                            "Timeout": {
                                "default": 1800,
                                "locked": False,
                                "max": 4000,
                                "min": 1
                                }
                        },
                        "WaitForStabilityBeforeMeas": {
                        "default": False,
                        "locked": False
                        }                   
                    }]
            
            if config_data["Temperature"] != 0:
                config_data["Resources"]["ThermostatParams_no_wait"] = thermostatParams_data_no_wait
            else:
                config_data["Resources"]["ThermostatParams_no_wait"] = []

            # 將 TSP 參數填入 config_data 等待寫入 saved_parameters.json
            tspCalibParams = {
                "CustomTemperature": {
                    "default": config_data["Temperature"],
                    "locked": False,
                    "max": 50,
                    "min": 0
                },
                "DutStability": {
                    "default": False,
                    "locked": False,
                },
                "EndAction": {
                    "default": "CustomTemp",
                    "locked": False,
                },
                "Mode": {
                    "default": "Downwards",
                    "locked": False,
                },
                "ThtIntSensor": {
                    "default": True,
                    "locked": False,
                },
                "Tmax": {
                    "default": config_data["Tmax"],
                    "locked": False,
                    "max": 100,
                    "min": 0
                },
                "Tmin": {
                    "default": config_data["Tmin"],
                    "locked": False,
                    "max": 100,
                    "min": 0
                },
                "Tstep": {
                    "default": config_data["Tstep"],
                    "locked": False,
                    "max": 100, 
                    "min": 1
                }
            }

            if config_data["Tmax"] != 0:
                config_data["TspCalibParams"] = tspCalibParams
            else:
                config_data["TspCalibParams"] = []

            with open(file_path, "w") as file:
                json.dump(config_data, file, indent=4)

            print("參數已成功儲存至 saved_parameters.json")

            # 啟用進度提示框
            self.progress_text.config(state="normal")
            self.progress_text.delete(1.0, tk.END)  # 清空現有內容

            # 重定向標準輸出
            self.progress_output = StringIO()
            sys.stdout = self.progress_output

            # 啟用一個線程來執行長時間任務
            threading.Thread(target=self.run_tests_in_thread).start()

            # 通過 after 定期更新進度
            self.update_progress_text()
        else:
            # 什麼都不做，因為 check_input_validation 已經顯示了警告訊息
            print("資料有誤，不執行儲存")

    def run_tests_in_thread(self):
        # 從文件讀取配置
        with open("saved_parameters.json", "r") as file:
            config_data = json.load(file)

        try:
            # 根據配置執行不同的測試
            if config_data["Cycling_Test"] == False:    
                from Variable import websocket_test       
                websocket_test()
            else:
                from CyclingTest import Cycling_Test
                Cycling_Test()
        except Exception as e:
            print(f"Error: {str(e)}")

        # 任務完成後，恢復標準輸出
        sys.stdout = sys.__stdout__

    def update_progress_text(self):
        # 獲取重定向的輸出
        output = self.progress_output.getvalue()

        # 將新的輸出添加到 Text 小部件中
        if output:
            self.progress_text.insert(tk.END, output)
            self.progress_output.truncate(0)
            self.progress_output.seek(0)

            # 自動滾動到最後一行
            self.progress_text.see(tk.END)

        # 繼續定期調用這個函數
        if threading.active_count() > 1:  # 檢查是否有線程仍在運行
            self.progress_text.after(100, self.update_progress_text)
        else:
            self.progress_text.config(state="disabled")  # 禁用编辑    
            self.progress_text.see(tk.END)  # 確保在任務完成時也能滾動到底部


if __name__ == "__main__":

    if os.path.exists("params.json"):
        os.remove("params.json")   # 刪除檔案
        print("params.json 已被刪除")
    else:
        print("params.json 不存在")

    app = ParameterApp()
    app.mainloop()