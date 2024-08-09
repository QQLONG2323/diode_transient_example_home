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

class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Parameter Configuration")
        self.geometry("1024x768")

        # Frame



        # Save Config
        Save_frame = ttk.LabelFrame(self, text="Save_Config")
        Save_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

        



        # Resources___CurrentSourceParams_MS401
        Resources_CurrentSourceParams_MS401_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceParams_MS401")
        Resources_CurrentSourceParams_MS401_frame.grid(column=0, row=1, padx=10, pady=10, sticky=tk.EW)

        # Alias_MS401
        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Alias MS401").grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
        self.alias_MS401 = ttk.Combobox(Resources_CurrentSourceParams_MS401_frame, values=[
            "/T3STER/0/MS401/SLOT5/CH0",
            "/T3STER/0/MS401/SLOT5/CH1",
            "/T3STER/0/MS401/SLOT5/CH2",
            "/T3STER/0/MS401/SLOT5/CH3",
            "/T3STER/0/MS401/SLOT6/CH0",
            "/T3STER/0/MS401/SLOT6/CH1",
            "/T3STER/0/MS401/SLOT6/CH2",
            "/T3STER/0/MS401/SLOT6/CH3",
            "/T3STER/0/MS401/SLOT7/CH0",
            "/T3STER/0/MS401/SLOT7/CH1",
            "/T3STER/0/MS401/SLOT7/CH2",
            "/T3STER/0/MS401/SLOT7/CH3",
            "/T3STER/0/MS401/SLOT8/CH0",
            "/T3STER/0/MS401/SLOT8/CH1",
            "/T3STER/0/MS401/SLOT8/CH2",
            "/T3STER/0/MS401/SLOT8/CH3"
        ])
        self.alias_MS401.current(0)  # set default value
        self.alias_MS401.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5, columnspan=2)

        # OutputMode_MS401
        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Output Mode MS401").grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
        self.output_mode_var_MS401 = tk.BooleanVar(value="ON")
        self.output_mode_MS401 = ttk.Checkbutton(Resources_CurrentSourceParams_MS401_frame, variable=self.output_mode_var_MS401)
        self.output_mode_MS401.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Output Mode MS401 (locked)").grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)
        self.output_mode_locked_var_MS401 = tk.BooleanVar(value=False)
        self.output_mode_locked_MS401 = ttk.Checkbutton(Resources_CurrentSourceParams_MS401_frame, variable=self.output_mode_locked_var_MS401)
        self.output_mode_locked_MS401.grid(column=3, row=1, sticky=tk.EW, padx=10, pady=5)

        # SetCurrent_MS401
        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Current[A] Setpoint MS401 ( -2.0 ~ 2.0 )").grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)
        self.setCurrent_MS401 = ttk.Entry(Resources_CurrentSourceParams_MS401_frame)
        self.setCurrent_MS401.grid(column=1, row=2, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Current[A] MS401 (locked)").grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)
        self.setCurrent_locked_var_MS401 = tk.BooleanVar(value=False)
        self.setCurrent_locked_MS401 = ttk.Checkbutton(Resources_CurrentSourceParams_MS401_frame, variable=self.setCurrent_locked_var_MS401)
        self.setCurrent_locked_MS401.grid(column=3, row=2, sticky=tk.EW, padx=10, pady=5)

        # VoltageCorner_MS401
        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Range MS401 ( -40 ~ 40 )").grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_MS401 = ttk.Entry(Resources_CurrentSourceParams_MS401_frame)
        self.voltage_corner_MS401.grid(column=1, row=3, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_MS401_frame, text="Range MS401 (locked)").grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_locked_var_MS401 = tk.BooleanVar(value=False)
        self.voltage_corner_locked_MS401 = ttk.Checkbutton(Resources_CurrentSourceParams_MS401_frame, variable=self.voltage_corner_locked_var_MS401)
        self.voltage_corner_locked_MS401.grid(column=3, row=3, sticky=tk.EW, padx=10, pady=5)


        # Resources___CurrentSourceParams_LP220     
        Resources_CurrentSourceParams_LP220_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceParams_LP220")
        Resources_CurrentSourceParams_LP220_frame.grid(column=0, row=2, padx=10, pady=10, sticky=tk.EW)

        # Alias_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Alias LP220").grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
        self.alias_LP220 = ttk.Combobox(Resources_CurrentSourceParams_LP220_frame, values=[
            "/T3STER/0/LP220/SLOT1/CH0",
            "/T3STER/0/LP220/SLOT1/CH1",
            "/T3STER/0/LP220/SLOT3/CH0",
            "/T3STER/0/LP220/SLOT3/CH1"
        ])
        self.alias_LP220.current(0)  # set default value
        self.alias_LP220.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5, columnspan=2)

        # DelayFallingUs_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Source switching delay (falling) [μs] LP220 ( -16383 ~ 5000 )").grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
        self.DelayFallingUs_LP220 = ttk.Entry(Resources_CurrentSourceParams_LP220_frame)
        self.DelayFallingUs_LP220.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Source switching delay (falling) [μs] LP220 (locked)").grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)
        self.DelayFallingUs_locked_var_LP220 = tk.BooleanVar(value=False)
        self.DelayFallingUs_locked_LP220 = ttk.Checkbutton(Resources_CurrentSourceParams_LP220_frame, variable=self.DelayFallingUs_locked_var_LP220)
        self.DelayFallingUs_locked_LP220.grid(column=3, row=1, sticky=tk.EW, padx=10, pady=5)

        # DelayRisingUs_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Source switching delay (rising) [μs] LP220 ( -16383 ~ 16383 )").grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)
        self.DelayRisingUs_LP220 = ttk.Entry(Resources_CurrentSourceParams_LP220_frame)
        self.DelayRisingUs_LP220.grid(column=1, row=2, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Source switching delay (rising) [μs] LP220 (locked)").grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)
        self.DelayRisingUs_locked_var_LP220 = tk.BooleanVar(value=False)
        self.DelayRisingUs_locked_LP220 = ttk.Checkbutton(Resources_CurrentSourceParams_LP220_frame, variable=self.DelayRisingUs_locked_var_LP220)
        self.DelayRisingUs_locked_LP220.grid(column=3, row=2, sticky=tk.EW, padx=10, pady=5)

        # OutputMode_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Output Mode LP220").grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)
        self.output_mode_var_LP220 = ttk.Combobox(Resources_CurrentSourceParams_LP220_frame, values=[
            "PC",
            "ON",
            "OFF"
        ])
        self.output_mode_var_LP220.current(0)  # set default value
        self.output_mode_var_LP220.grid(column=1, row=3, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Output Mode LP220 (locked)").grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)
        self.output_mode_locked_var_LP220 = tk.BooleanVar(value=False)
        self.output_mode_locked_LP220 = ttk.Checkbutton(Resources_CurrentSourceParams_LP220_frame, variable=self.output_mode_locked_var_LP220)
        self.output_mode_locked_LP220.grid(column=3, row=3, sticky=tk.EW, padx=10, pady=5)

        # SetCurrent_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Current[A] Setpoint LP220 ( -2.0 ~ 2.0 )").grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
        self.setCurrent_LP220 = ttk.Entry(Resources_CurrentSourceParams_LP220_frame)
        self.setCurrent_LP220.grid(column=1, row=4, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Current[A] LP220 (locked)").grid(column=2, row=4, sticky=tk.W, padx=10, pady=5)
        self.setCurrent_locked_var_LP220 = tk.BooleanVar(value=False)
        self.setCurrent_locked_LP220 = ttk.Checkbutton(Resources_CurrentSourceParams_LP220_frame, variable=self.setCurrent_locked_var_LP220)
        self.setCurrent_locked_LP220.grid(column=3, row=4, sticky=tk.EW, padx=10, pady=5)

        # VoltageCorner_LP220
        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Range LP220 ( -10 ~ 10 )").grid(column=0, row=5, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_LP220 = ttk.Entry(Resources_CurrentSourceParams_LP220_frame)
        self.voltage_corner_LP220.grid(column=1, row=5, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_CurrentSourceParams_LP220_frame, text="Range LP220 (locked)").grid(column=2, row=5, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_locked_var_LP220 = tk.BooleanVar(value=False)
        self.voltage_corner_locked_LP220 = ttk.Checkbutton(Resources_CurrentSourceParams_LP220_frame, variable=self.voltage_corner_locked_var_LP220)
        self.voltage_corner_locked_LP220.grid(column=3, row=5, sticky=tk.EW, padx=10, pady=5)






        Resources_CurrentSourceWithActiveloadParams_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceWithActiveloadParams_frame")
        Resources_CurrentSourceWithActiveloadParams_frame.grid(column=0, row=3, padx=10, pady=10, sticky=tk.EW)

        Resources_DividerParams_frame = ttk.LabelFrame(self, text="Resources_DividerParams_frame")
        Resources_DividerParams_frame.grid(column=0, row=4, padx=10, pady=10, sticky=tk.EW)

        Resources_VoltageSourceParams_frame = ttk.LabelFrame(self, text="Resources_VoltageSourceParams_frame")
        Resources_VoltageSourceParams_frame.grid(column=0, row=5, padx=10, pady=10, sticky=tk.EW)    



        Resources_MeasCardChParams_frame = ttk.LabelFrame(self, text="Resources_MeasCardChParams_frame")
        Resources_MeasCardChParams_frame.grid(column=0, row=6, padx=10, pady=10, sticky=tk.EW)

        # MeasCardChParams_MS401
        ttk.Label(Resources_MeasCardChParams_frame, text="Alias MeasCardChParams MS401").grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
        self.Alias_MeasCardChParams_MS401 = ttk.Combobox(Resources_MeasCardChParams_frame, values=[
            "/T3STER/0/MS401/SLOT5/CH0",
            "/T3STER/0/MS401/SLOT5/CH1",
            "/T3STER/0/MS401/SLOT5/CH2",
            "/T3STER/0/MS401/SLOT5/CH3",
            "/T3STER/0/MS401/SLOT6/CH0",
            "/T3STER/0/MS401/SLOT6/CH1",
            "/T3STER/0/MS401/SLOT6/CH2",
            "/T3STER/0/MS401/SLOT6/CH3",
            "/T3STER/0/MS401/SLOT7/CH0",
            "/T3STER/0/MS401/SLOT7/CH1",
            "/T3STER/0/MS401/SLOT7/CH2",
            "/T3STER/0/MS401/SLOT7/CH3",
            "/T3STER/0/MS401/SLOT8/CH0",
            "/T3STER/0/MS401/SLOT8/CH1",
            "/T3STER/0/MS401/SLOT8/CH2",
            "/T3STER/0/MS401/SLOT8/CH3"
        ])
        self.Alias_MeasCardChParams_MS401.current(0)  # set default value
        self.Alias_MeasCardChParams_MS401.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5, columnspan=2)

        # Sensitivity_MS401
        ttk.Label(Resources_MeasCardChParams_frame, text="Sensitivity MS401").grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
        self.Sensitivity_MS401 = ttk.Entry(Resources_MeasCardChParams_frame)
        self.Sensitivity_MS401.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(Resources_MeasCardChParams_frame, text="Sensitivity MS401 (locked)").grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)
        self.Sensitivity_locked_var_MS401 = tk.BooleanVar(value=False)
        self.Sensitivity_locked_MS401 = ttk.Checkbutton(Resources_MeasCardChParams_frame, variable=self.Sensitivity_locked_var_MS401)
        self.Sensitivity_locked_MS401.grid(column=3, row=1, sticky=tk.EW, padx=10, pady=5)









        Resources_ThermometerCardChParams_frame = ttk.LabelFrame(self, text="Resources_ThermometerCardChParams_frame")
        Resources_ThermometerCardChParams_frame.grid(column=0, row=7, padx=10, pady=10, sticky=tk.EW)    

        Resources_ThermostatParams_frame = ttk.LabelFrame(self, text="Resources_ThermostatParams_frame")
        Resources_ThermostatParams_frame.grid(column=0, row=8, padx=10, pady=10, sticky=tk.EW)    

        Resources_TriggerOutputParams_frame = ttk.LabelFrame(self, text="Resources_TriggerOutputParams_frame")
        Resources_TriggerOutputParams_frame.grid(column=0, row=9, padx=10, pady=10, sticky=tk.EW) 

        TimingParams_frame = ttk.LabelFrame(self, text="TimingParams_frame")
        TimingParams_frame.grid(column=0, row=10, padx=10, pady=10, sticky=tk.EW)   

        SourceTimingControl_frame = ttk.LabelFrame(self, text="SourceTimingControl_frame")
        SourceTimingControl_frame.grid(column=0, row=11, padx=10, pady=10, sticky=tk.EW)


        # # Buttons
        # submit_btn = ttk.Button(self, text="Submit", command=self.submit)
        # submit_btn.grid(column=0, row=12, padx=10, pady=20, columnspan=2)

        # save_btn = ttk.Button(self, text="Save Config", command=self.save_config)
        # save_btn.grid(column=2, row=12, padx=10, pady=20, columnspan=2)

        # load_btn = ttk.Button(self, text="Load Config", command=self.load_config)
        # load_btn.grid(column=4, row=12, padx=10, pady=20, columnspan=2)


if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()