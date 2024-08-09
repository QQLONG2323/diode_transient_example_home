#!/usr/bin/env python3

# Following modules must be installed:
# py -m pip install websocket-client

import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request
import tkinter as tk
from tkinter import ttk

IP_ADDRESS = "192.168.20.99"

command_system_ready = {
    "Command": "QUERY_SYSTEM_INTEGRITY"
}

command_query_api_version = {
    "Command": "GET_API_VERSION"
}

class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Parameter Configuration")
        self.geometry("800x600")

        # Frame

        Save_frame = ttk.LabelFrame(self, text="Save_frame")
        Save_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

        Resources_CurrentSourceParams_MS401_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceParams_MS401_frame")
        Resources_CurrentSourceParams_MS401_frame.grid(column=0, row=1, padx=10, pady=10, sticky=tk.EW)
     
        Resources_CurrentSourceParams_LP220_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceParams_LP220_frame")
        Resources_CurrentSourceParams_LP220_frame.grid(column=0, row=2, padx=10, pady=10, sticky=tk.EW)

        Resources_CurrentSourceWithActiveloadParams_frame = ttk.LabelFrame(self, text="Resources_CurrentSourceWithActiveloadParams_frame")
        Resources_CurrentSourceWithActiveloadParams_frame.grid(column=0, row=3, padx=10, pady=10, sticky=tk.EW)

        Resources_DividerParams_frame = ttk.LabelFrame(self, text="Resources_DividerParams_frame")
        Resources_DividerParams_frame.grid(column=0, row=4, padx=10, pady=10, sticky=tk.EW)

        Resources_VoltageSourceParams_frame = ttk.LabelFrame(self, text="Resources_VoltageSourceParams_frame")
        Resources_VoltageSourceParams_frame.grid(column=0, row=5, padx=10, pady=10, sticky=tk.EW)    

        Resources_MeasCardChParams_frame = ttk.LabelFrame(self, text="Resources_MeasCardChParams_frame")
        Resources_MeasCardChParams_frame.grid(column=0, row=6, padx=10, pady=10, sticky=tk.EW)

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

        self.create_widgets()

    def create_widgets(self):

        self.command_save_config = {
            "Command": "SAVE_CONFIG",
            "Type": "Config",
            "ConfigName": "diode_config",
            "ConfigParams": {
                "Description": ""
            },
            "Resources": {
                "CurrentSourceParams": [
                    {
                        "Alias": "/T3STER/0/MS401/SLOT3/CH0",
                        "UserAlias": "",
                        "OutputMode": {
                            "default": "ON",
                            "locked": False
                        },
                        "SetCurrent": {
                            "default": 0.01,
                            "locked": False,
                            "min": -0.2,
                            "max": 0.2
                        },
                        "VoltageCorner": {
                            "default": 10,
                            "locked": False,
                            "min": -40,
                            "max": 40
                        }
                    },
                    {
                        "Alias": "/T3STER/0/LP220/SLOT1/CH0",
                        "UserAlias": "",
                        "Delay": {
                            "DelayFallingUs": {
                                "default": 0,
                                "locked": False,
                                "min": 0,
                                "max": 0
                            },
                            "DelayRisingUs": {
                                "default": 0,
                                "locked": False,
                                "min": 0,
                                "max": 0
                            }
                        },
                        "OutputMode": {
                            "default": "PC",
                            "locked": False
                        },
                        "SetCurrent": {
                            "default": 0.1,
                            "locked": False,
                            "min": -1,
                            "max": 1
                        },
                        "VoltageCorner": {
                            "default": 4,
                            "locked": False,
                            "min": -10,
                            "max": 10
                        }
                    }
                ],
                "CurrentSourceWithActiveloadParams": [

                ],
                "DividerParams": [

                ],
                "VoltageSourceParams": [

                ],
                "MeasCardChParams": [
                    {
                        "Alias": "/T3STER/0/MS401/SLOT3/CH0",
                        "UserAlias": "",
                        "Sensitivity": {
                            "locked": False,
                            "default": [
                                0.002
                            ]
                        },
                        "PowerStep":"@POWERSTEP_DIODE;/T3STER/0/MS401/SLOT3/CH0;/T3STER/0/LP220/SLOT1/CH0",
                        "RangeIdx":{
                            "locked": False,
                            "default": 13
                        },
                        "AutoRange": {
                            "locked": False,
                            "default": False
                        },
                        "Uref": {
                            "locked": False,
                            "default": 0.7
                        },
                        "UrefSwitching": {
                            "locked": False,
                            "default": False
                        },
                        "UrefHeating": {
                            "locked": False,
                            "default": 0
                        }
                    }
                ],
                "ThermometerCardChParams": [

                ],
                "ThermostatParams": [

                ],
                "TriggerOutputParams": [

                ]
            },
            "TimingParams": {
                "TransientMode": {
                    "locked": False,
                    "default": "Cooling"
                },
                "HeatingTime": {
                    "default": 5,
                    "locked": False,
                    "min": 0,
                    "max": 4000
                },
                "CoolingTime": {
                    "default": 5,
                    "locked": False,
                    "min": 0,
                    "max": 4000
                },
                "DelayTime": {
                    "default": 0,
                    "locked": False,
                    "min": 0,
                    "max": 4000
                },
                "SamplePerOctave": {
                    "default": 1000,
                    "locked": False,
                    "min": 1000,
                    "max": 1000
                },
                "Repeat": {
                    "default": 1,
                    "locked": False,
                    "min": 1,
                    "max": 1
                }
            },
            "SourceTimingControl": {
                "locked": False,
                "Enabled": False,
                "ReversePowerOff": True,
                "WaitForInstrumentDelay": True,
                "PowerOn": [

                ],
                "PowerOff": [

                ]
            }
        }

command_do_resource_alloc = {
    "Command": "START_TASK",
    "TaskMode": "MONITORING_RESOURCE_ALLOCATION",
    "ConfigName": "diode_config",
    "TaskAlias": "diode_config",
    "LoadConfig": True,
    "HandleUserDisconnect": False
}

command_start_transient = {
    "Command": "START_TASK",
    "TaskMode": "TRANSIENT",
    "ConfigName": "diode_config",
    "TaskAlias": "diode_config_transient",
    "LoadConfig": True
}

command_query_alloc_task_status = {
    "Command": "QUERY_TASK_STATUS",
    "TaskAlias": "diode_config"
}

command_query_measurement_task_status = {
    "Command": "QUERY_TASK_STATUS",
    "TaskAlias": "diode_config_transient"
}

command_get_file_list = {
    "Command": "QUERY_TASK_RESULT_FILE_LIST",
    "TaskAlias": "diode_config_transient"
}

command_query_task_list = {
    "Command": "QUERY_TASKLIST"
}

command_query_transient_task_presence = {
    "Command": "QUERY_TASK_PRESENCE",
    "TaskAlias": "diode_config_transient"
}

command_remove_transient_task = {
    "Command": "STOP_AND_REMOVE_TASK",
    "TaskAlias": "diode_config_transient"
}

command_query_resource_alloc_task_presence = {
    "Command": "QUERY_TASK_PRESENCE",
    "TaskAlias": "diode_config"
}

command_remove_resource_alloc = {
    "Command": "STOP_AND_REMOVE_TASK",
    "TaskAlias": "diode_config"
}


def do_web_socket_string_query(ws: WebSocket, command: Dict) -> Dict:
    ws.send(json.dumps(command))
    answer_str = ws.recv()
    answer = json.loads(answer_str)
    if answer["Answer"] == "ERR":
        raise Exception("Error on command '"+ json.dumps(command) + "': " + answer["Message"])
    return answer


def do_web_socket_bool_query(ws: WebSocket, command: Dict) -> bool:
    answer = do_web_socket_string_query(ws, command)
    return answer["Answer"] == "OK"


if __name__ == '__main__':

    print("Measurement started")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()
    
    # Create an instance of ParameterApp
    app = ParameterApp()

    try:
        # ---- Initialize and open websocket
        websocket_transport.connect(websocket_url)
        websocket_transport.settimeout(10)

        # ---- Query system state
        if do_web_socket_bool_query(websocket_transport, command_system_ready):
            print("System is ready")
        else:
            raise Exception("System is NOT ready, returning...")

        # ---- Check api version
        api_version = do_web_socket_string_query(websocket_transport, command_query_api_version)
        print("Api version: " + api_version["Answer"])
        api_version_str = api_version["Answer"]
        api_version_str = api_version_str[:api_version_str.find('.')]
        if api_version_str != "2":
            raise Exception("Not supported major api version")              

        # ---- Save config
        if not do_web_socket_bool_query(websocket_transport, app.command_save_config):
            raise Exception("Cannot save config")

        # ---- Allocate resources
        if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
            raise Exception("Cannot allocate resources")
        while True:
            sleep(1)
            task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
            print("Waiting allocation to finish...")
            if task_status["Answer"] == "RUN":
                break

        # ---- Start thermal transient measurement
        if not do_web_socket_string_query(websocket_transport, command_start_transient):
            raise Exception("Cannot start measurement")

        # ---- Query measurement status
        busy = True
        while busy:
            sleep(1)
            task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
            print("Measuring, please wait..." + str(task_status["Percentage"]) + "%")
            if task_status["Answer"] != "RUN":
                busy = False

        # ---- Get and download measurement data
        file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)
        print("Results:")
        for file in file_list['Result']:
            print("Downloading " + file["Filename"])
            link = "http://" + IP_ADDRESS + ":8085" + file["Filename"]
            urllib.request.urlretrieve(link, link[(link.rfind("/")+1):])

        # ---- Release resources: thermal transient task and resource allocation
        if not do_web_socket_bool_query(websocket_transport, command_remove_transient_task):
            raise Exception("Cannot remove transient task")

        if not do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc):
            raise Exception("Cannot remove allocation task")
        

        print("Measurement finished")
    except Exception as e:
         print("Error: " + str(e))

    # Close
    websocket_transport.close()
    print("Exit")