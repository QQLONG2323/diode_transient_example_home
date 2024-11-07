import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import itertools
from io import StringIO
import sys
import threading


class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("T3STER SI")
        self.geometry("1280x960")

        # self.params_file = "params.json"
        # self.params = self.load_params()

        self.create_page1()


    # 定義一個函數，用於創建 Sensor 框架
    def create_sensor_frame(self, text, column):
        frame = ttk.LabelFrame(self, text=text)
        frame.grid(column=column, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(frame)
        return frame


    def create_page1(self):

        # 用於儲存第一個頁面上的所有控件
        self.page1_widgets = []

        # Sensor 框架
        LP220_S1_frame = self.create_sensor_frame("LP220", 0)
        LP220_S3_frame = self.create_sensor_frame("LP220", 1)
        MS401_S5_frame = self.create_sensor_frame("MS401", 2)
        MS401_S6_frame = self.create_sensor_frame("MS401", 3)
        MS401_S7_frame = self.create_sensor_frame("MS401", 4)
        MS401_S8_frame = self.create_sensor_frame("MS401", 5)
        TH800_S9_frame = self.create_sensor_frame("TH800", 6)
        TH800_S10_frame = self.create_sensor_frame("TH800", 7)

        # Next 按鈕，按下後隱藏當前頁面並進入下一步的頁面
        next_button = ttk.Button(
            self, text="Next", command=self.go_to_page2)
        next_button.grid(column=7, row=1, padx=10, pady=10)
        self.page1_widgets.append(next_button)

        # 定義每個感測器的選項
        self.sensor_option_parameters = {
            "S1Ch1": {
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
            },
            "S1Ch2": {
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
            },
            "S3Ch1": {
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
            },
            "S3Ch2": {
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
            },
            "S5Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S5Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S5Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S5Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S6Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S6Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S6Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S6Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S7Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S7Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S7Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S7Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S8Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S8Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S8Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S8Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "ON"],
                    "Range [V]": ["10", "20", "40"],
                    "Current [A]": "entry"
                },
                "Measurement_channel": {
                    "Sensitivity [mV/K]": "entry",
                    "Auto range": ["Off", "On"],
                    "Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
                    "Measurement_channel_Range": ["Fall scale: 20 V, V(in): -10 V ~ 10 V",
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
            },
            "S9Ch1": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch2": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch3": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch4": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch5": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch6": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch7": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S9Ch8": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch1": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch2": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch3": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch4": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch5": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch6": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch7": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
            "S10Ch8": {
                "Thermometer": {
                    "Type": "entry",
                    "Sensitivity": "entry",
                    "Sample per sec": "entry"
                }
            },
        }

        # 初始化用於保存 Sensor 、 Option 、 Parameters 和表單控件的字典
        self.sensor = {}   # 儲存 Sensor
        self.option = {}  # 儲存 Option
        self.saved_parameters = {}  # 儲存 Parameters
        self.form_widgets = {}   # 儲存所有動態生成的表單控件

        # 創建 & 排版 Sensor
        self.create_sensor_checkbuttons(LP220_S1_frame, 0, 2)
        self.create_sensor_checkbuttons(LP220_S3_frame, 2, 4)
        self.create_sensor_checkbuttons(MS401_S5_frame, 4, 8)
        self.create_sensor_checkbuttons(MS401_S6_frame, 8, 12)
        self.create_sensor_checkbuttons(MS401_S7_frame, 12, 16)
        self.create_sensor_checkbuttons(MS401_S8_frame, 16, 20)
        self.create_sensor_checkbuttons(TH800_S9_frame, 20, 28)
        self.create_sensor_checkbuttons(TH800_S10_frame, 28, 36)


    # 創建 Sensor 的 Checkbutton
    def create_sensor_checkbuttons(self, frame, start, end):
        for i, sensor in enumerate(itertools.islice(self.sensor_option_parameters.keys(), start, end)):
            self.sensor[sensor] = tk.BooleanVar()
            checkbutton = ttk.Checkbutton(
                frame, text=sensor, variable=self.sensor[sensor], command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)


    # 只有在 Checkbutton 被勾選時才彈出視窗
    def handle_checkbutton(self, sensor):
        if self.sensor[sensor].get():
            self.open_parameter_window(sensor)
        else:
            self.option[sensor].set("")
            self.update_form(sensor)


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
        option_frame = ttk.Frame(param_window)
        option_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

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

        # 建立儲存、取消按鈕框架
        button_frame = ttk.Frame(param_window)
        button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")





        # 取得對應的 Option 選項以及其參數
        # 檢查是否有保存的 Option 選項
        default_option = None
        for option in list(self.sensor_option_parameters[sensor].keys()):
            if (sensor, option) in self.saved_parameters:
                default_option = option
                break

        # 如果已經有保存的選項，將其作為預設選項，否則使用第一個選項
        self.option[sensor] = tk.StringVar(
            value=default_option or list(self.sensor_option_parameters[sensor].keys())[0]) # 保存這個 sensor 的選擇變量

        # Option 排版
        for i, option in enumerate(list(self.sensor_option_parameters[sensor].keys())):
            tk.Radiobutton(option_frame, text=option, variable=self.option[sensor], value=option, font=(
                "System", 16, "bold"), command=lambda: self.update_form(sensor)).grid(row=0, column=i+1, padx=20, pady=5)
        
            



        # 建立每個 Sensor 中的參數表單
        self.form_widgets[sensor] = {}

        form_widgets_for_option_S1_S3_current_source = []
        form_widgets_for_option_voltage_source = []

        form_widgets_for_option_S5_S8_current_source = []
        form_widgets_for_option_Measurement_channel = []

        form_widgets_for_option_Thermometer = []

        # 檢查是否有保存的 Parameters 選項
        saved_parameters_for_S1_S3_current_source = self.saved_parameters.get(
            (sensor, "Current_source"), [])
        saved_parameters_for_S1_S3_voltage_source = self.saved_parameters.get(
            (sensor, "Voltage_source"), [])

        saved_parameters_for_S5_S8_current_source = self.saved_parameters.get(
            (sensor, "Current_source"), [])
        saved_parameters_for_S5_S8_Measurement_channel = self.saved_parameters.get(
            (sensor, "Measurement_channel"), [])
        saved_parameters_for_S5_S8_Both = self.saved_parameters.get(
            (sensor, "Both"), [])

        saved_parameters_for_S9_S10_Thermometer = self.saved_parameters.get(
            (sensor, "Thermometer"), [])

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

        # S9 & S10 只有一個選項，所以不用檢查

        if sensor in ["S1Ch1", "S1Ch2", "S3Ch1", "S3Ch2"]:
            # 填充 S1_S3_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S1_S3_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_Current_source_frame, values=field_type, state=S1_S3_current_source_state, width=40)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_current_source 中的值
                    if i < len(saved_parameters_for_S1_S3_current_source):
                        combobox.set(
                            saved_parameters_for_S1_S3_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(
                        combobox)
                else:
                    entry = ttk.Entry(
                        S1_S3_Current_source_frame, state=S1_S3_current_source_state, width=40)  # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_current_source 中的值
                    if i < len(saved_parameters_for_S1_S3_current_source):
                        entry.insert(
                            0, saved_parameters_for_S1_S3_current_source[i])
                    form_widgets_for_option_S1_S3_current_source.append(entry)

            # 保存填充的 Current_source
            self.form_widgets[sensor]["Current_source"] = form_widgets_for_option_S1_S3_current_source

            # 填充 Voltage_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Voltage_source"].items()):
                ttk.Label(S1_S3_Voltage_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S1_S3_Voltage_source_frame, values=field_type, state=voltage_source_state, width=40)  # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_voltage_source 中的值
                    if i < len(saved_parameters_for_S1_S3_voltage_source):
                        combobox.set(
                            saved_parameters_for_S1_S3_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(combobox)

                else:
                    entry = ttk.Entry(
                        S1_S3_Voltage_source_frame, state=voltage_source_state, width=40)  # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S1_S3_voltage_source 中的值
                    if i < len(saved_parameters_for_S1_S3_voltage_source):
                        entry.insert(
                            0, saved_parameters_for_S1_S3_voltage_source[i])
                    form_widgets_for_option_voltage_source.append(entry)

            # 保存填充的 Voltage_source
            self.form_widgets[sensor]["Voltage_source"] = form_widgets_for_option_voltage_source

        elif sensor in ["S5Ch1", "S5Ch2", "S5Ch3", "S5Ch4", "S6Ch1", "S6Ch2", "S6Ch3", "S6Ch4", "S7Ch1", "S7Ch2",  "S7Ch3", "S7Ch4", "S8Ch1", "S8Ch2", "S8Ch3", "S8Ch4"]:
            # 填充 S5_S8_Current_source 表單
            for i, (label_text, field_type) in enumerate(self.sensor_option_parameters[sensor]["Current_source"].items()):
                ttk.Label(S5_S8_Current_source_frame,
                          text=label_text).pack(anchor=tk.W)
                if isinstance(field_type, list):
                    combobox = ttk.Combobox(
                        S5_S8_Current_source_frame, values=field_type, state=S5_S8_current_source_state, width=40)   # 根據條件禁用或啟用
                    combobox.pack(anchor=tk.W, pady=5)
                    # 回填 saved_parameters_for_S5_S8_current_source 中的值
                    if i < len(saved_parameters_for_S5_S8_current_source):
                        combobox.set(
                            saved_parameters_for_S5_S8_current_source[i])
                    form_widgets_for_option_S5_S8_current_source.append(
                        combobox)

                else:
                    entry = ttk.Entry(
                        S5_S8_Current_source_frame, state=S5_S8_current_source_state, width=40)   # 根據條件禁用或啟用
                    entry.pack(anchor=tk.W, pady=5)
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

            # 初始化 Both 選項，結合前面兩個選項的所有小部件
            self.form_widgets[sensor]["Both"] = self.form_widgets[sensor]["Current_source"] + \
                self.form_widgets[sensor]["Measurement_channel"]

        else:
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

        # 儲存、取消按鈕排版
        ttk.Button(button_frame, text="儲存", command=lambda: self.save_parameters(
            sensor, self.option[sensor].get(), param_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=param_window.destroy).pack(
            side=tk.LEFT, padx=5)

    def update_form(self, sensor):

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
                        widget.configure(state="normal")
            else:
                # 將所有小部件設置為禁用狀態
                for widgets in self.form_widgets[sensor].values():
                    for widget in widgets:
                        widget.configure(state="disabled")

                # 啟用選中的選項對應的小部件
                for option, widgets in self.form_widgets[sensor].items():
                    if self.option[sensor].get() == option:
                        for widget in widgets:
                            widget.configure(state="normal")


    def save_parameters(self, sensor, option, window):
        """Handle form submission and save parameters"""

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

        # Close the window
        window.destroy()

    def export_to_json(self):
        """Export saved parameters to a JSON file"""

        # Prepare the data for JSON export
        json_data = {}

        # Iterate over saved parameters and prepare them for JSON output
        for (sensor, option), params in self.saved_parameters.items():

            print(self.saved_parameters.items())

            # Create the "sensor_option" key to structure the output
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


    def go_to_page1(self):
        """隱藏當前頁面，顯示上一頁面"""
        # 隱藏第二頁面的所有控件
        for widget in self.page2_widgets:
            widget.pack_forget()

        # 顯示第一頁面的控件
        self.create_page1()

        for (sensor, option), params in self.saved_parameters:
            if sensor in self.form_widgets and option in self.form_widgets[sensor]:
                # 填充表單控件
                for idx, widget in enumerate(self.form_widgets[sensor][option]):
                    if isinstance(widget, ttk.Combobox):
                        # 重新設置 Combobox 的選定項目
                        widget.set(params[idx])
                    else:
                        # 重新設置 Entry 的值
                        widget.delete(0, tk.END)
                        widget.insert(0, params[idx])

    def go_to_page2(self):
        # 儲存參數至 JSON 檔
        self.export_to_json()
        """隱藏當前頁面，顯示下一頁面"""
        # 隱藏第一頁面的所有控件
        for widget in self.page1_widgets:
            widget.grid_forget()

        # 顯示第二頁面的控件
        self.create_page2()

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
   

        # 設置框架為Canvas的滾動區域
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 將該框架放置在Canvas中
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # 使得滾動輪也能工作
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))


        # 創建框架
        config_details_frame = ttk.LabelFrame(scrollable_frame, text="Config details")
        config_details_frame.grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.NSEW)
        

        power_steps_frame = ttk.LabelFrame(scrollable_frame, text="Power Steps")
        power_steps_frame.grid(column=0, row=1, padx=10,
                               pady=10, sticky=tk.NSEW)
       

        measurement_settings_frame = ttk.LabelFrame(
            scrollable_frame, text="Measurement settings")
        measurement_settings_frame.grid(
            column=0, row=2, padx=10, pady=10, sticky=tk.NSEW)
        

        # 是否使用重複測量功能
        # 使用 tk.BooleanVar 來控制 Cycling Test 的選中狀態
        self.cycling_test_var = tk.BooleanVar(value=False)  # 默認為未選中
        
        self.cycling_test_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Cycling Test", variable=self.cycling_test_var, command=self.toggle_cycling_test_checkbutton)
        self.cycling_test_checkbutton.grid(
            row=3, column=0, padx=10, pady=10)
        self.page2_parameters["Cycling_Test"] = self.cycling_test_var.get()


        cycling_test_frame = ttk.LabelFrame(
            scrollable_frame, text="Cycling Test")
        cycling_test_frame.grid(
            column=0, row=4, padx=10, pady=10, sticky=tk.NSEW)
     

        # connect to THERMOSTAT 、是否使用 TSP
        # 使用 tk.BooleanVar 來控制 connect to THERMOSTAT 、 是否使用 TSP 的選中狀態
        self.connect_thermostat_var = tk.BooleanVar(value=False)  # 默認為未選中
        self.tsp_var = tk.BooleanVar(value=False)  # 默認為未選中

        self.connect_thermostat_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Connect to Thermostat", variable=self.connect_thermostat_var, command=self.toggle_tspCheckbutton_temperature)
        self.connect_thermostat_checkbutton.grid(
            row=5, column=0, padx=10, pady=10)
        self.page2_parameters["Connect_to_Thermostat"] = self.connect_thermostat_var.get()

        self.tsp_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Calibration Set (TSP)", variable=self.tsp_var, command=self.toggle_tsp_calibration_entry, state="disabled")
        self.tsp_checkbutton.grid(
            row=7, column=0, padx=10, pady=10)
        self.page2_parameters["TSP"] = self.tsp_var.get()

        thermostat_settings_for_measurement_frame = ttk.LabelFrame(
            scrollable_frame, text="Thermostat Settings for Measurement")
        thermostat_settings_for_measurement_frame.grid(
            column=0, row=6, padx=10, pady=10, sticky=tk.NSEW)

        tsp_calibration_frame = ttk.LabelFrame(scrollable_frame, text="TSP calibration")
        tsp_calibration_frame.grid(
            column=0, row=8, padx=10, pady=10, sticky=tk.NSEW)

        advanced_thermostat_stability_settings_frame = ttk.LabelFrame(
            scrollable_frame, text="Advanced thermostat stability settings")
        advanced_thermostat_stability_settings_frame.grid(
            column=0, row=9, padx=10, pady=10, sticky=tk.NSEW)

        # 添加 Previous 和 Next 按鈕
        previous_button = ttk.Button(
            scrollable_frame, text="Previous", command=self.go_to_page1)
        previous_button.grid(row=10, column=0, padx=10, pady=10, sticky="W")
        
        next_button = ttk.Button(scrollable_frame, text="Next", command=self.page2_export_to_json)
        next_button.grid(row=10, column=0, padx=10, pady=10, sticky="E")
     
        # 添加進度提示框，默認禁用
        self.progress_text = tk.Text(scrollable_frame, height=10, state="disabled")
        self.progress_text.grid(row=11, column=0, padx=10, pady=10, sticky=tk.NSEW)
        


        # Config Name 輸入框和標籤
        config_label = ttk.Label(config_details_frame, text="Config Name:")
        config_label.grid(column=0, row=0, padx=10, pady=10)

        self.config_entry = ttk.Entry(config_details_frame)
        self.config_entry.grid(column=1, row=0, padx=10, pady=10)
        self.page2_parameters["Config_Name"] = self.config_entry.get()

        # 儲存路徑選擇
        path_label = ttk.Label(config_details_frame, text="儲存路徑:")
        path_label.grid(column=0, row=1, padx=10, pady=10)

        self.path_display = ttk.Label(config_details_frame, text="未選擇路徑")
        self.path_display.grid(column=1, row=1, padx=10, pady=10)
        self.page2_parameters["storage_path"] = self.path_display.cget("text")

        def select_directory():
            # 打開文件夾選擇對話框
            selected_path = filedialog.askdirectory()
            if selected_path:  # 如果選擇了路徑
                self.path_display.config(text=selected_path)

        select_path_button = ttk.Button(
            config_details_frame, text="選擇路徑", command=select_directory)
        select_path_button.grid(column=2, row=1, padx=10, pady=10)

        # 根據 saved_parameters 中的數據動態生成表格
        measurement_channels = [
            sensor for sensor, option in self.saved_parameters if "Measurement_channel" in option or "Both" in option]
        current_sources_s5_s8 = [sensor for sensor, option in self.saved_parameters if ("Current_source" in option and sensor.startswith(
            ("S5", "S6", "S7", "S8"))) or ("Both" in option and sensor.startswith(("S5", "S6", "S7", "S8")))]
        current_sources_s1_s3 = [
            sensor for sensor, option in self.saved_parameters if "Current_source" in option and sensor.startswith(("S1", "S3"))]

        # 顯示 "Calculation Method" 字
        method_label = ttk.Label(power_steps_frame, text="Calculation Method")
        method_label.grid(row=0, column=0, padx=10, pady=10)

        # 顯示公式
        formula_label = ttk.Label(
            power_steps_frame, text="Diode — Pstep = ||Vmeas,heat · (Idrive + Isense)| - |Vmeas,cool · Isense||")
        formula_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        row_index = 1  # 用來處理表格的起始行

        # 在類的初始化方法中初始化列表
        self.ms_401_labels = []
        self.combo_s5_s8s = []
        self.combo_s1_s3s = []

        for sensor in measurement_channels:
            # 第一欄：顯示 "Diode" 的欄位
            diode_label = ttk.Label(power_steps_frame, text="Diode")
            diode_label.grid(row=row_index, column=0, padx=10, pady=10)

            # 第二欄：顯示 Measurement_channel 的感測器
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
                power_steps_frame, values=current_sources_s5_s8)
            self.combo_s5_s8.grid(row=row_index, column=3, padx=10, pady=10)
            # self.page2_parameters 已寫在下面

            # 將 combo_s5_s8 加入到 combo_s5_s8s 列表中
            self.combo_s5_s8s.append(self.combo_s5_s8)
            
            # 第四欄：顯示 S1 ~ S3 的 Current_source 選項
            Idrive_label = ttk.Label(power_steps_frame, text="Idrive: ")
            Idrive_label.grid(row=row_index, column=4, padx=10, pady=10)

            self.combo_s1_s3 = ttk.Combobox(
                power_steps_frame, values=current_sources_s1_s3)
            self.combo_s1_s3.grid(row=row_index, column=5, padx=10, pady=10)
            # self.page2_parameters 已寫在下面

            # 將 combo_s1_s3 加入到 combo_s1_s3s 列表中
            self.combo_s1_s3s.append(self.combo_s1_s3)

            row_index += 1

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

        self.heating_entry = ttk.Entry(measurement_settings_frame)
        self.heating_entry.grid(row=0, column=3, padx=10, pady=10)
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

        self.cooling_entry = ttk.Entry(measurement_settings_frame)
        self.cooling_entry.grid(row=1, column=3, padx=10, pady=10)
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

        self.delay_entry = ttk.Entry(measurement_settings_frame)
        self.delay_entry.grid(row=2, column=3, padx=10, pady=10)
        self.page2_parameters["Delay_time"] = self.delay_entry.get()

        # Repeat
        # # 使用 tk.BooleanVar 來控制 Repeat 的選中狀態
        # self.repeat_var = tk.BooleanVar(value=False)  # 默認為未選中

        # # 使用 ttk.Checkbutton 來啟用或禁用 repeat_entry
        # self.repeat_checkbutton = ttk.Checkbutton(
        #     measurement_settings_frame, text="Repeat [times]", variable=self.repeat_var, command=self.toggle_repeat_entry)
        # self.repeat_checkbutton.grid(row=4, column=0, padx=10, pady=10)
        # self.page2_parameters["Repeat"] = self.repeat_var.get()

        repeat_label = ttk.Label(
            measurement_settings_frame, text="Repeat times")
        repeat_label.grid(row=3, column=0, padx=10, pady=10)

        repeat_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 1 ~ 100")
        repeat_range_label.grid(row=3, column=1, padx=10, pady=10)

        repeat_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        repeat_setpoint_label.grid(row=3, column=2, padx=10, pady=10)

        # Repeat 的 Entry
        self.repeat_entry = ttk.Entry(measurement_settings_frame)
        self.repeat_entry.grid(row=3, column=3, padx=10, pady=10)
        self.repeat_entry.insert(0, "1")   # 插入數字 1
        self.page2_parameters["Repeat_times"] = self.repeat_entry.get()

        # Cycling Test
        multi_pulse_cycling_label = ttk.Label(cycling_test_frame, text="Multi Pulse Cycling")
        multi_pulse_cycling_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        pulse_cycling_on_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling On [s]: ")
        pulse_cycling_on_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_on_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_on_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling On [s]"] = self.pulse_cycling_on_entry.get()

        pulse_cycling_off_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Off [s]: ")
        pulse_cycling_off_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_off_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_off_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling Off [s]"] = self.pulse_cycling_off_entry.get()

        pulse_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Repeat: ")
        pulse_cycling_repeat_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.pulse_cycling_repeat_entry.grid(row=3, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Pulse Cycling Repeat"] =  self.pulse_cycling_repeat_entry.get()

        rth_measurement_label = ttk.Label(cycling_test_frame, text="Rth Measurement")
        rth_measurement_label.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        rth_measurement_heating_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Heating Times: ")
        rth_measurement_heating_times_label.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_heating_times_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.rth_measurement_heating_times_entry.grid(row=5, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Rth Measurement Heating Times"] = self.rth_measurement_heating_times_entry.get()

        rth_measurement_cooling_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Cooling Times: ")
        rth_measurement_cooling_times_label.grid(row=6, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_cooling_times_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.rth_measurement_cooling_times_entry.grid(row=6, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Rth Measurement Cooling Times"] = self.rth_measurement_cooling_times_entry.get()

        total_cycling_test_label = ttk.Label(cycling_test_frame, text="Total Cycling Test")
        total_cycling_test_label.grid(row=7, column=0, padx=10, pady=10, columnspan=2)

        total_measurement_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Total Measurement Cycling Repeat: ")
        total_measurement_cycling_repeat_label.grid(row=8, column=0, padx=10, pady=10, sticky="W")

        self.total_measurement_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.total_measurement_cycling_repeat_entry.grid(row=8, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["total Measurement Cycling Repeat"] =  self.total_measurement_cycling_repeat_entry.get()

        other_lp220_current_label = ttk.Label(
            cycling_test_frame, text="若有其他 LP220 Current [A] 請填下面")
        other_lp220_current_label.grid(row=9, column=0, padx=10, pady=10, columnspan=2)

        other_lp220_current_01_label = ttk.Label(
            cycling_test_frame, text="LP220 Current [A] 01: ")
        other_lp220_current_01_label.grid(row=10, column=0, padx=10, pady=10, sticky="W")
        
        self.other_lp220_current_01_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.other_lp220_current_01_entry.grid(row=10, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Other LP220 Current 01"] =  self.other_lp220_current_01_entry.get()

        other_lp220_current_02_label = ttk.Label(
            cycling_test_frame, text="LP220 Current [A] 02: ")
        other_lp220_current_02_label.grid(row=11, column=0, padx=10, pady=10, sticky="W")

        self.other_lp220_current_02_entry = ttk.Entry(
            cycling_test_frame, state="disabled")
        self.other_lp220_current_02_entry.grid(row=11, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters["Other LP220 Current 02"] =  self.other_lp220_current_02_entry.get()


        # Temperature [°C]
        temperature_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="Temperature [°C]")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)

        temperature_range_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="範圍: -45 ~ 160")
        temperature_range_label.grid(row=0, column=1, padx=10, pady=10)

        temperature_setpoint_label = ttk.Label(
            thermostat_settings_for_measurement_frame, text="Setpoint: ")
        temperature_setpoint_label.grid(row=0, column=2, padx=10, pady=10)

        self.temperature_entry = ttk.Entry(
            thermostat_settings_for_measurement_frame, state="disabled")  # 初始狀態為禁用
        self.temperature_entry.grid(row=0, column=3, padx=10, pady=10)
        self.page2_parameters["Temperature"] = self.temperature_entry.get()

        # TSP calibration
        # Tmin [°C]
        tmin_label = ttk.Label(tsp_calibration_frame, text="Tmin [°C]")
        tmin_label.grid(row=0, column=0, padx=10, pady=10)

        tmin_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: -45 ~ 160")
        tmin_range_label.grid(row=0, column=1, padx=10, pady=10)

        tmin_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tmin_setpoint_label.grid(row=0, column=2, padx=10, pady=10)

        self.tmin_entry = ttk.Entry(
            tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        self.tmin_entry.grid(row=0, column=3, padx=10, pady=10)
        self.page2_parameters["Tmin"] = self.tmin_entry.get()

        # Tmax [°C]
        tmax_label = ttk.Label(tsp_calibration_frame, text="Tmax [°C]")
        tmax_label.grid(row=1, column=0, padx=10, pady=10)

        tmax_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: -45 ~ 160")
        tmax_range_label.grid(row=1, column=1, padx=10, pady=10)

        tmax_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tmax_setpoint_label.grid(row=1, column=2, padx=10, pady=10)

        self.tmax_entry = ttk.Entry(
            tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        self.tmax_entry.grid(row=1, column=3, padx=10, pady=10)
        self.page2_parameters["Tmax"] = self.tmax_entry.get()

        # Tstep [°C]
        tstep_label = ttk.Label(tsp_calibration_frame, text="Tstep [°C]")
        tstep_label.grid(row=2, column=0, padx=10, pady=10)

        tstep_range_label = ttk.Label(
            tsp_calibration_frame, text="範圍: 1 ~ 205")
        tstep_range_label.grid(row=2, column=1, padx=10, pady=10)

        tstep_setpoint_label = ttk.Label(
            tsp_calibration_frame, text="Setpoint: ")
        tstep_setpoint_label.grid(row=2, column=2, padx=10, pady=10)

        self.tstep_entry = ttk.Entry(
            tsp_calibration_frame, state="disabled")  # 初始狀態為禁用
        self.tstep_entry.grid(row=2, column=3, padx=10, pady=10)
        self.page2_parameters["Tstep"] = self.tstep_entry.get()


        # Time window [s]
        # Max. allowed temp. change [°C]
        # ΔT from target [°C]
        # Timeout [s]

        self.update()  # 強制刷新頁面

    # def toggle_repeat_entry(self):
    #     """用來啟用或禁用 repeat_entry 的回調函數"""
    #     if self.repeat_var.get():  # 如果 Checkbutton 被選中
    #         self.repeat_entry.config(state="normal")  # 啟用輸入框
    #     else:
    #         self.repeat_entry.delete(0, tk.END)  # 清空輸入框的內容
    #         self.repeat_entry.config(state="disabled")  # 禁用輸入框


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
            self.heating_entry.config(state="normal")
            self.cooling_entry.config(state="normal")
            self.delay_entry.config(state="normal")
            self.repeat_entry.config(state="normal")
            self.repeat_entry.delete(0, tk.END)   # 清空當前的內容
            self.repeat_entry.insert(0, "1")   # 插入數字 1
    
    
    def toggle_tspCheckbutton_temperature(self):
        """用來啟用或禁用 tsp 選項以及 temperature"""
        if self.connect_thermostat_var.get():  # 如果 "Connect to Thermostat" Checkbutton 被選中
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

    def toggle_tsp_calibration_entry(self):
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
            "S8Ch4": "/T3STER/0/MS401/SLOT8/CH3"
        }

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

       





        current_source_params = []    

       
        if "S1Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S1Ch1"],
                "UserAlias": "S1Ch1",
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
                "OutputMode": {"default": config_data["S1Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S1Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -1, "max": 1},
                "VoltageCorner": {"default": float(config_data["S1Ch1_Current_source"]["Voltage limit [V]"]), "locked": False, "min": -10, "max": 10},
            })
        
        if "S1Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S1Ch2"],
                "UserAlias": "S1Ch2",
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
                "OutputMode": {"default": config_data["S1Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S1Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -2, "max": 2},
                "VoltageCorner": {"default": float(config_data["S1Ch2_Current_source"]["Voltage limit [V]"]), "locked": False, "min": -10, "max": 10}
            })
        
        if "S3Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S3Ch1"],
                "UserAlias": "S3Ch1",
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
                "OutputMode": {"default": config_data["S3Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S3Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -2, "max": 2},
                "VoltageCorner": {"default": float(config_data["S3Ch1_Current_source"]["Voltage limit [V]"]), "locked": False, "min": -10, "max": 10}
            })
        
        if "S3Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S3Ch2"],
                "UserAlias": "S3Ch2",
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
                "OutputMode": {"default": config_data["S3Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S3Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -2, "max": 2},
                "VoltageCorner": {"default": float(config_data["S3Ch2_Current_source"]["Voltage limit [V]"]), "locked": False, "min": -10, "max": 10}
            })

        if "S5Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch1"],
                "UserAlias": "S5Ch1",
                "OutputMode": {"default": config_data["S5Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch1_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40},
            })

        if "S5Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch2"],
                "UserAlias": "S5Ch2",
                "OutputMode": {"default": config_data["S5Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch2_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch3_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch3"],
                "UserAlias": "S5Ch3",
                "OutputMode": {"default": config_data["S5Ch3_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch3_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch3_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch4_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch4"],
                "UserAlias": "S5Ch4",
                "OutputMode": {"default": config_data["S5Ch4_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch4_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch4_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch1"],
                "UserAlias": "S6Ch1",
                "OutputMode": {"default": config_data["S6Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch1_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch2"],
                "UserAlias": "S6Ch2",
                "OutputMode": {"default": config_data["S6Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch2_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch3_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch3"],
                "UserAlias": "S6Ch3",
                "OutputMode": {"default": config_data["S6Ch3_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch3_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch3_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch4_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch4"],
                "UserAlias": "S6Ch4",
                "OutputMode": {"default": config_data["S6Ch4_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch4_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch4_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch1"],
                "UserAlias": "S7Ch1",
                "OutputMode": {"default": config_data["S7Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch1_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch2"],
                "UserAlias": "S7Ch2",
                "OutputMode": {"default": config_data["S7Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch2_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch3_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch3"],
                "UserAlias": "S7Ch3",
                "OutputMode": {"default": config_data["S7Ch3_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch3_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch3_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch4_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch4"],
                "UserAlias": "S7Ch4",
                "OutputMode": {"default": config_data["S7Ch4_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch4_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch4_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch1_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch1"],
                "UserAlias": "S8Ch1",
                "OutputMode": {"default": config_data["S8Ch1_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch1_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch1_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch2_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch2"],
                "UserAlias": "S8Ch2",
                "OutputMode": {"default": config_data["S8Ch2_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch2_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch2_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch3_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch3"],
                "UserAlias": "S8Ch3",
                "OutputMode": {"default": config_data["S8Ch3_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch3_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch3_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch4_Current_source" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch4"],
                "UserAlias": "S8Ch4",
                "OutputMode": {"default": config_data["S8Ch4_Current_source"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch4_Current_source"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch4_Current_source"]["Range [V]"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch1_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch1"],
                "UserAlias": "S5Ch1",
                "OutputMode": {"default": config_data["S5Ch1_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch1_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch1_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch2_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch2"],
                "UserAlias": "S5Ch2",
                "OutputMode": {"default": config_data["S5Ch2_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch2_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch2_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch3_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch3"],
                "UserAlias": "S5Ch3",
                "OutputMode": {"default": config_data["S5Ch3_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch3_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch3_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S5Ch4_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S5Ch4"],
                "UserAlias": "S5Ch4",
                "OutputMode": {"default": config_data["S5Ch4_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S5Ch4_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S5Ch4_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch1_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch1"],
                "UserAlias": "S6Ch1",
                "OutputMode": {"default": config_data["S6Ch1_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch1_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch1_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch2_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch2"],
                "UserAlias": "S6Ch2",
                "OutputMode": {"default": config_data["S6Ch2_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch2_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch2_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch3_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch3"],
                "UserAlias": "S6Ch3",
                "OutputMode": {"default": config_data["S6Ch3_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch3_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch3_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S6Ch4_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S6Ch4"],
                "UserAlias": "S6Ch4",
                "OutputMode": {"default": config_data["S6Ch4_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S6Ch4_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S6Ch4_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch1_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch1"],
                "UserAlias": "S7Ch1",
                "OutputMode": {"default": config_data["S7Ch1_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch1_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch1_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch2_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch2"],
                "UserAlias": "S7Ch2",
                "OutputMode": {"default": config_data["S7Ch2_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch2_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch2_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch3_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch3"],
                "UserAlias": "S7Ch3",
                "OutputMode": {"default": config_data["S7Ch3_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch3_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch3_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S7Ch4_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S7Ch4"],
                "UserAlias": "S7Ch4",
                "OutputMode": {"default": config_data["S7Ch4_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S7Ch4_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S7Ch4_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch1_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch1"],
                "UserAlias": "S8Ch1",
                "OutputMode": {"default": config_data["S8Ch1_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch1_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch1_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch2_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch2"],
                "UserAlias": "S8Ch2",
                "OutputMode": {"default": config_data["S8Ch2_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch2_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch2_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch3_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch3"],
                "UserAlias": "S8Ch3",
                "OutputMode": {"default": config_data["S8Ch3_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch3_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch3_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        if "S8Ch4_Both" in config_data:
            current_source_params.append({
                "Alias": self.sensor_rename["S8Ch4"],
                "UserAlias": "S8Ch4",
                "OutputMode": {"default": config_data["S8Ch4_Both"]["Output mode"], "locked": False},
                "SetCurrent": {"default": float(config_data["S8Ch4_Both"]["Current [A]"]), "locked": False, "min": -0.2, "max": 0.2},
                "VoltageCorner": {"default": float(config_data["S8Ch4_Both"]["Current_source_Range"]), "locked": False, "min": -40, "max": 40}
            })

        return current_source_params

    # 獲取 SI 所需的 MeasCardChParams 參數值
    def fill_measurement_params(self, config_data):

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
                range_idx = self.range_rename.get(range_value, None)  # 从 range_rename 获取对应的索引
                    
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



    def page2_export_to_json(self):
        # 定義 JSON 檔案路徑
        file_path = "saved_parameters.json"


        # 確保控件的值是最新的
        self.page2_parameters["Config_Name"] = self.config_entry.get()
        self.page2_parameters["storage_path"] = self.path_display.cget("text")

        # 判斷是否有輸入參數，若無，則預設為 0
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

        # self.page2_parameters["Repeat"] = self.repeat_var.get()
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
                "MS_401": self.ms_401_labels[i].cget("text"),  # 传感器标签
                "Isense": self.combo_s5_s8s[i].get(),  # 用户选择的 Isense 值
                "Idrive": self.combo_s1_s3s[i].get()   # 用户选择的 Idrive 值
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

        # 重定向标准输出
        self.progress_output = StringIO()
        sys.stdout = self.progress_output

        # 启动一个线程来执行长时间任务
        threading.Thread(target=self.run_tests_in_thread).start()

        # 通过 after 定期更新进度
        self.update_progress_text()

    def run_tests_in_thread(self):
        # 從文件讀取配置
        with open("saved_parameters.json", "r") as file:
            config_data = json.load(file)

        try:
            # 根据配置执行不同的测试
            if config_data["Cycling_Test"] == False:    
                from Variable import websocket_test       
                websocket_test()
            else:
                from CyclingTest import Cycling_Test
                Cycling_Test()
        except Exception as e:
            print(f"Error: {str(e)}")

        # 任务完成后，恢复标准输出
        sys.stdout = sys.__stdout__

    def update_progress_text(self):
        # 获取重定向的输出
        output = self.progress_output.getvalue()

        # 将新的输出添加到 Text 小部件中
        if output:
            self.progress_text.insert(tk.END, output)
            self.progress_output.truncate(0)
            self.progress_output.seek(0)

            # 自动滚动到最后一行
            self.progress_text.see(tk.END)

        # 继续定期调用这个函数
        if threading.active_count() > 1:  # 检查是否有线程仍在运行
            self.progress_text.after(100, self.update_progress_text)
        else:
            self.progress_text.config(state="disabled")  # 禁用编辑    
            self.progress_text.see(tk.END)  # 确保在任务完成时也能滚动到底部


if __name__ == "__main__":
    app = ParameterApp()
    app.mainloop()