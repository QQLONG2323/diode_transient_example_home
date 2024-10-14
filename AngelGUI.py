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
        self.geometry("1024x768")

        self.create_page1()

    def create_page1(self):

        # 用於儲存第一個頁面上的所有控件
        self.page1_widgets = []

        # Sensor 框架
        LP220_S1_frame = ttk.LabelFrame(self, text="LP220")
        LP220_S1_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(LP220_S1_frame)

        LP220_S3_frame = ttk.LabelFrame(self, text="LP220")
        LP220_S3_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(LP220_S3_frame)

        MS401_S5_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S5_frame.grid(column=2, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(MS401_S5_frame)

        MS401_S6_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S6_frame.grid(column=3, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(MS401_S6_frame)

        MS401_S7_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S7_frame.grid(column=4, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(MS401_S7_frame)

        MS401_S8_frame = ttk.LabelFrame(self, text="MS401")
        MS401_S8_frame.grid(column=5, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(MS401_S8_frame)

        TH800_S9_frame = ttk.LabelFrame(self, text="TH800")
        TH800_S9_frame.grid(column=6, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(TH800_S9_frame)

        TH800_S10_frame = ttk.LabelFrame(self, text="TH800")
        TH800_S10_frame.grid(column=7, row=0, padx=10, pady=10, sticky=tk.NSEW)
        self.page1_widgets.append(TH800_S10_frame)

        # Next 按鈕，按下後隱藏當前頁面並進入下一步的頁面
        next_button = ttk.Button(
            self, text="Next", command=self.go_to_page2)
        next_button.grid(column=7, row=1, padx=10, pady=10)
        self.page1_widgets.append(next_button)

        # 定義每個感測器的選項
        self.SCh_radio = {
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
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S5Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S5Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S5Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S6Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S6Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S6Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S6Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S7Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S7Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S7Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S7Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S8Ch1": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S8Ch2": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S8Ch3": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                }
            },
            "S8Ch4": {
                "Current_source": {
                    "Output mode": ["Off", "On"],
                    "Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
                },
                "Both": {
                    "Output mode": ["Off", "On"],
                    "Current_source_Range": ["-0.2 A ~ 0.2 A", "-0.1 A ~ 0.1 A", "-0.05 A ~ 0.05 A"],
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
                    "Separate Vref for heating": ["Off", "On"]
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

        # 創建 Checkbutton 和 RadioButton 的框架
        self.check_sensor = {}   # 儲存 Sensor
        self.check_option = {}  # 儲存 Option
        self.saved_parameters = {}  # 儲存 Option 的參數
        self.form_widgets = {}   # 保存所有動態生成的表單控件

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 2)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                LP220_S1_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 2, 4)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                LP220_S3_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 4, 8)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S5_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 8, 12)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S6_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 12, 16)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S7_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 16, 20)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                MS401_S8_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 20, 28)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                TH800_S9_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

        # 排版 Sensor
        for i, sensor in enumerate(itertools.islice(self.SCh_radio.keys(), 28, 36)):
            check_sensor = tk.BooleanVar()
            self.check_sensor[sensor] = check_sensor
            checkbutton = ttk.Checkbutton(
                TH800_S10_frame, text=sensor, variable=check_sensor, command=lambda t=sensor: self.handle_checkbutton(t))
            checkbutton.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)

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

        # 建立儲存、取消按鈕框架
        button_frame = ttk.Frame(param_window)
        button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # 取得對應的 RadioButton 選項
        radio_options = list(self.SCh_radio[sensor].keys())

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

        # 建立每個 Sensor 中的參數表單
        self.form_widgets[sensor] = {}

        form_widgets_for_option_S1_S3_current_source = []
        form_widgets_for_option_voltage_source = []

        form_widgets_for_option_S5_S8_current_source = []
        form_widgets_for_option_Measurement_channel = []

        form_widgets_for_option_Thermometer = []

        # 獲取保存的參數
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
            for i, (label_text, field_type) in enumerate(self.SCh_radio[sensor]["Current_source"].items()):
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
            for i, (label_text, field_type) in enumerate(self.SCh_radio[sensor]["Voltage_source"].items()):
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
            for i, (label_text, field_type) in enumerate(self.SCh_radio[sensor]["Current_source"].items()):
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
            for i, (label_text, field_type) in enumerate(self.SCh_radio[sensor]["Measurement_channel"].items()):
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
            for i, (label_text, field_type) in enumerate(self.SCh_radio[sensor]["Thermometer"].items()):
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

    def save_parameters(self, sensor, check_option, window):
        """Handle form submission and save parameters"""

        # Collect the parameters from the form (now using a dictionary to store keys and values)
        params = {}

        # check_option 可以是 "Current_source" 或 "Voltage_source" 或 "Measurement_channel" 或 "Both"
        # Get the field names
        form_fields = self.SCh_radio[sensor][check_option].keys()

        # Iterate over the widgets and save both the field names and their values
        for field_name, widget in zip(form_fields, self.form_widgets[sensor][check_option]):
            if isinstance(widget, ttk.Combobox):
                # Get the selected value in Combobox
                params[field_name] = widget.get()
            else:
                params[field_name] = widget.get()   # Get the value in Entry

        # Delete previously saved parameters for this sensor-option pair
        for key in list(self.saved_parameters):
            if key == (sensor, check_option):  # 僅刪除與當前 sensor 和 check_option 配對的參數
                del self.saved_parameters[key]

        # Save current parameters
        self.saved_parameters[(sensor, check_option)] = params

        # Print the saved parameters with keys and values
        print(f"提交的參數 ({sensor} - {check_option}): ")
        for field, value in params.items():
            print(f"{field}: {value}")

        print(self.saved_parameters)

        # 針對 S1_S3 清除另一個選項的內容
        if check_option == "Current_source":
            # 清除 Voltage_source 的內容
            if (sensor, "Voltage_source") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Voltage_source")]
                # 清空界面上的 Voltage_source 表單內容
                for widget in self.form_widgets[sensor]["Voltage_source"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry
        elif check_option == "Voltage_source":
            # 清除 Current_source 的內容
            if (sensor, "Current_source") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Current_source")]
                # 清空界面上的 Current_source 表單內容
                for widget in self.form_widgets[sensor]["Current_source"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry

        # 針對 S5_S8 清除另一個選項的內容或是選擇 Both 的話兩個選項參數都保留
        if check_option == "Current_source":
            # 清除 Measurement_channel 的內容
            if (sensor, "Measurement_channel") in self.saved_parameters:
                print(sensor, check_option)
                del self.saved_parameters[(sensor, "Measurement_channel")]
                for widget in self.form_widgets[sensor]["Measurement_channel"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry
            if (sensor, "Both") in self.saved_parameters:
                print(sensor, check_option)
                del self.saved_parameters[(sensor, "Both")]
                for widget in self.form_widgets[sensor]["Both"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry

        elif check_option == "Measurement_channel":
            # 清除 Current_source 的內容
            if (sensor, "Current_source") in self.saved_parameters:
                print(sensor, check_option)
                del self.saved_parameters[(sensor, "Current_source")]
                for widget in self.form_widgets[sensor]["Current_source"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry
            if (sensor, "Both") in self.saved_parameters:
                print(sensor, check_option)
                del self.saved_parameters[(sensor, "Both")]
                for widget in self.form_widgets[sensor]["Both"]:
                    if isinstance(widget, ttk.Combobox):
                        widget.set('')  # 清空 combobox
                    else:
                        widget.delete(0, tk.END)  # 清空 entry

        elif check_option == "Both":
            # 刪除 Current_source 和 Measurement_channel 的 key (不清空表單)
            if (sensor, "Current_source") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Current_source")]

            if (sensor, "Measurement_channel") in self.saved_parameters:
                del self.saved_parameters[(sensor, "Measurement_channel")]

            both_params = self.saved_parameters[(sensor, check_option)]
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
        for (sensor, check_option), params in self.saved_parameters.items():
            # Create the "sensor_option" key to structure the output
            sensor_check_option = f"{sensor}_{check_option}"

            # Store parameters as a dictionary for each sensor-option pair
            json_data[sensor_check_option] = params

        # Write the json_data to a JSON file
        with open('saved_parameters.json', 'w', encoding='utf-8') as json_file:
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
      

        cycling_test_frame = ttk.LabelFrame(
            scrollable_frame, text="Cycling Test")
        cycling_test_frame.grid(
            column=0, row=3, padx=10, pady=10, sticky=tk.NSEW)
     

        # connect to THERMOSTAT
        # 使用 tk.BooleanVar 來控制 connect to THERMOSTAT 的選中狀態
        self.connect_thermostat_var = tk.BooleanVar(value=False)  # 默認為未選中
        self.tsp_var = tk.BooleanVar(value=False)  # 默認為未選中

        self.connect_thermostat_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Connect to Thermostat", variable=self.connect_thermostat_var, command=self.toggle_tspCheckbutton_temperature)
        self.connect_thermostat_checkbutton.grid(
            row=4, column=0, padx=10, pady=10)
        self.page2_parameters['Connect_to_Thermostat'] = self.connect_thermostat_var.get()

        self.tsp_checkbutton = ttk.Checkbutton(
            scrollable_frame, text="Calibration Set (TSP)", variable=self.tsp_var, command=self.toggle_tsp_calibration_entry, state="disabled")
        self.tsp_checkbutton.grid(
            row=6, column=0, padx=10, pady=10)
        self.page2_parameters['TSP'] = self.tsp_var.get()

        thermostat_settings_for_measurement_frame = ttk.LabelFrame(
            scrollable_frame, text="Thermostat Settings for Measurement")
        thermostat_settings_for_measurement_frame.grid(
            column=0, row=5, padx=10, pady=10, sticky=tk.NSEW)

        tsp_calibration_frame = ttk.LabelFrame(scrollable_frame, text="TSP calibration")
        tsp_calibration_frame.grid(
            column=0, row=7, padx=10, pady=10, sticky=tk.NSEW)

        advanced_thermostat_stability_settings_frame = ttk.LabelFrame(
            scrollable_frame, text="Advanced thermostat stability settings")
        advanced_thermostat_stability_settings_frame.grid(
            column=0, row=8, padx=10, pady=10, sticky=tk.NSEW)

        # 添加 Previous 和 Next 按鈕
        previous_button = ttk.Button(
            scrollable_frame, text="Previous", command=self.go_to_page1)
        previous_button.grid(row=9, column=0, padx=10, pady=10, sticky="W")
        

        next_button = ttk.Button(scrollable_frame, text="Next", command=self.page2_export_to_json)
        next_button.grid(row=9, column=2, padx=10, pady=10)
     

        # Config Name 輸入框和標籤
        config_label = ttk.Label(config_details_frame, text="Config Name:")
        config_label.grid(column=0, row=0, padx=10, pady=10)

        self.config_entry = ttk.Entry(config_details_frame)
        self.config_entry.grid(column=1, row=0, padx=10, pady=10)
        self.page2_parameters['Config_Name'] = self.config_entry.get()

        # 儲存路徑選擇
        path_label = ttk.Label(config_details_frame, text="儲存路徑:")
        path_label.grid(column=0, row=1, padx=10, pady=10)

        self.path_display = ttk.Label(config_details_frame, text="未選擇路徑")
        self.path_display.grid(column=1, row=1, padx=10, pady=10)
        self.page2_parameters['storage_path'] = self.path_display.cget("text")

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
            sensor for sensor, check_option in self.saved_parameters if "Measurement_channel" in check_option or "Both" in check_option]
        current_sources_s5_s8 = [sensor for sensor, check_option in self.saved_parameters if ("Current_source" in check_option and sensor.startswith(
            ('S5', 'S6', 'S7', 'S8'))) or ("Both" in check_option and sensor.startswith(('S5', 'S6', 'S7', 'S8')))]
        current_sources_s1_s3 = [
            sensor for sensor, check_option in self.saved_parameters if "Current_source" in check_option and sensor.startswith(('S1', 'S3'))]

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
        self.page2_parameters['Heating_time'] = self.heating_entry.get()

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
        self.page2_parameters['Cooling_time'] = self.cooling_entry.get()

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
        self.page2_parameters['Delay_time'] = self.delay_entry.get()

        # Repeat
        # 使用 tk.BooleanVar 來控制 Repeat 的選中狀態
        self.repeat_var = tk.BooleanVar(value=False)  # 默認為未選中

        # 使用 ttk.Checkbutton 來啟用或禁用 repeat_entry
        self.repeat_checkbutton = ttk.Checkbutton(
            measurement_settings_frame, text="Repeat [times]", variable=self.repeat_var, command=self.toggle_repeat_entry)
        self.repeat_checkbutton.grid(row=4, column=0, padx=10, pady=10)
        self.page2_parameters['Repeat'] = self.repeat_var.get()

        repeat_range_label = ttk.Label(
            measurement_settings_frame, text="範圍: 1 ~ 100")
        repeat_range_label.grid(row=4, column=1, padx=10, pady=10)

        repeat_setpoint_label = ttk.Label(
            measurement_settings_frame, text="Setpoint: ")
        repeat_setpoint_label.grid(row=4, column=2, padx=10, pady=10)

        # Repeat 的 Entry
        self.repeat_entry = ttk.Entry(
            measurement_settings_frame, state="disabled")  # 初始狀態為禁用
        self.repeat_entry.grid(row=4, column=3, padx=10, pady=10)
        self.page2_parameters['Repeat_times'] = self.repeat_entry.get()

        # Cycling Test
        multi_pulse_cycling_label = ttk.Label(cycling_test_frame, text="Multi Pulse Cycling")
        multi_pulse_cycling_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        pulse_cycling_on_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling On [s]: ")
        pulse_cycling_on_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_on_entry = ttk.Entry(
            cycling_test_frame)
        self.pulse_cycling_on_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Pulse Cycling On [s]'] = self.pulse_cycling_on_entry.get()

        pulse_cycling_off_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Off [s]: ")
        pulse_cycling_off_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_off_entry = ttk.Entry(
            cycling_test_frame)
        self.pulse_cycling_off_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Pulse Cycling Off [s]'] = self.pulse_cycling_off_entry.get()

        pulse_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Pulse Cycling Repeat: ")
        pulse_cycling_repeat_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        self.pulse_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame)
        self.pulse_cycling_repeat_entry.grid(row=3, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Pulse Cycling Repeat'] =  self.pulse_cycling_repeat_entry.get()

        rth_measurement_label = ttk.Label(cycling_test_frame, text="Rth Measurement")
        rth_measurement_label.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        rth_measurement_heating_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Heating Times: ")
        rth_measurement_heating_times_label.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_heating_times_entry = ttk.Entry(
            cycling_test_frame)
        self.rth_measurement_heating_times_entry.grid(row=5, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Rth Measurement Heating Times'] = self.rth_measurement_heating_times_entry.get()

        rth_measurement_cooling_times_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Cooling Times: ")
        rth_measurement_cooling_times_label.grid(row=6, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_cooling_times_entry = ttk.Entry(
            cycling_test_frame)
        self.rth_measurement_cooling_times_entry.grid(row=6, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Rth Measurement Cooling Times'] = self.rth_measurement_cooling_times_entry.get()

        rth_measurement_cycling_repeat_label = ttk.Label(
            cycling_test_frame, text="Rth Measurement Cycling Repeat: ")
        rth_measurement_cycling_repeat_label.grid(row=7, column=0, padx=10, pady=10, sticky="W")

        self.rth_measurement_cycling_repeat_entry = ttk.Entry(
            cycling_test_frame)
        self.rth_measurement_cycling_repeat_entry.grid(row=7, column=1, padx=10, pady=10, sticky="W")
        self.page2_parameters['Rth Measurement Cycling Repeat'] =  self.rth_measurement_cycling_repeat_entry.get()

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
        self.page2_parameters['Temperature'] = self.temperature_entry.get()

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
        self.page2_parameters['Tmin'] = self.tmin_entry.get()

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
        self.page2_parameters['Tmax'] = self.tmax_entry.get()

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
        self.page2_parameters['Tstep'] = self.tstep_entry.get()


        # Time window [s]
        # Max. allowed temp. change [°C]
        # ΔT from target [°C]
        # Timeout [s]

        self.update()  # 強制刷新頁面

    def toggle_repeat_entry(self):
        """用來啟用或禁用 repeat_entry 的回調函數"""
        if self.repeat_var.get():  # 如果 Checkbutton 被選中
            self.repeat_entry.config(state="normal")  # 啟用輸入框
        else:
            self.repeat_entry.delete(0, tk.END)  # 清空輸入框的內容
            self.repeat_entry.config(state="disabled")  # 禁用輸入框

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


    def page2_export_to_json(self):
        # 定義 JSON 檔案路徑
        file_path = 'saved_parameters.json'


        # 確保控件的值是最新的
        self.page2_parameters['Config_Name'] = self.config_entry.get()
        self.page2_parameters['storage_path'] = self.path_display.cget("text")
        self.page2_parameters['Heating_time'] = self.heating_entry.get()
        self.page2_parameters['Cooling_time'] = self.cooling_entry.get()
        self.page2_parameters['Delay_time'] = self.delay_entry.get()
        self.page2_parameters['Repeat'] = self.repeat_var.get()
        self.page2_parameters['Repeat_times'] = self.repeat_entry.get()
        self.page2_parameters['Pulse Cycling On [s]'] = self.pulse_cycling_on_entry.get()
        self.page2_parameters['Pulse Cycling Off [s]'] = self.pulse_cycling_off_entry.get()
        self.page2_parameters['Pulse Cycling Repeat'] =  self.pulse_cycling_repeat_entry.get()
        self.page2_parameters['Rth Measurement Heating Times'] = self.rth_measurement_heating_times_entry.get()
        self.page2_parameters['Rth Measurement Cooling Times'] = self.rth_measurement_cooling_times_entry.get()
        self.page2_parameters['Rth Measurement Cycling Repeat'] =  self.rth_measurement_cycling_repeat_entry.get()
        self.page2_parameters['Connect_to_Thermostat'] = self.connect_thermostat_var.get()
        self.page2_parameters['Temperature'] = self.temperature_entry.get()
        self.page2_parameters['TSP'] = self.tsp_var.get()
        self.page2_parameters['Tmin'] = self.tmin_entry.get()
        self.page2_parameters['Tmax'] = self.tmax_entry.get()
        self.page2_parameters['Tstep'] = self.tstep_entry.get()

        # 初始化 Sensors 列表
        sensors_data = []

        # 將每一行的 `ms_401_label`、`combo_s5_s8`、`combo_s1_s3` 的值儲存到列表中
        for i in range(len(self.ms_401_labels)):
            sensor_info = {
                'MS_401': self.ms_401_labels[i].cget("text"),  # 传感器标签
                'Isense': self.combo_s5_s8s[i].get(),  # 用户选择的 Isense 值
                'Idrive': self.combo_s1_s3s[i].get()   # 用户选择的 Idrive 值
            }
            sensors_data.append(sensor_info)

        # 將 Sensors 列表保存到 page2_parameters
        self.page2_parameters['Measurement_channel'] = sensors_data


        # 檢查檔案是否存在
        if os.path.exists(file_path):
            # 如果存在，打開檔案並讀取現有內容
            with open(file_path, 'r') as file:
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

        # 將更新後的資料寫回到 JSON 文件中
        with open(file_path, 'w') as file:
            json.dump(saved_data, file, indent=4)

        print("參數已成功儲存至 saved_parameters.json")


if __name__ == '__main__':
    app = ParameterApp()
    app.mainloop()