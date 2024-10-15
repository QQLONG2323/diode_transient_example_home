#!/usr/bin/env python3

import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request

# 配置 IP 地址
IP_ADDRESS = "192.168.20.99"

# 從 saved_parameters.json 中讀取變數
with open('saved_parameters.json', 'r') as file:
    config_data = json.load(file)

# 定義命令
command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
command_query_api_version = {"Command": "GET_API_VERSION"}
command_enable_thermostat = {"Command": "ENABLE_THERMOSTAT", "Alias": "/THERMOSTAT/0"}

# 使用從 JSON 文件中導入的數據
command_save_config = {
    "Command": "SAVE_CONFIG",
    "Type": "Config",
    "ConfigName": config_data["Config_Name"],
    "ConfigParams": {
        "Description": "Test configuration"
    },
    "Resources": {
        "CurrentSourceParams": config_data["Resources"]["CurrentSourceParams"]
        ,
        # "MeasCardChParams": [
        #     {
        #         "Alias": "/T3STER/0/MS401/SLOT5/CH0",
        #         "UserAlias": "S6Ch1",
        #         "Sensitivity": {"default": [config_data["S6Ch1_Measurement_channel"]["Sensitivity [mV/K]"]], "locked": False},
        #         "AutoRange": {"default": config_data["S6Ch1_Measurement_channel"]["Auto range"] == "On", "locked": False},
        #         "Uref": {"default": config_data["S6Ch1_Measurement_channel"]["Vref [V]"], "locked": False},
        #         "UrefSwitching": {"default": config_data["S6Ch1_Measurement_channel"]["Separate Vref for heating"] == "On", "locked": False}
        #     }
        # ],
        "ThermostatParams": [
            {
                "Alias": "/THERMOSTAT/0",
                "UserAlias": "Th0",
                "SetTemperature": {"default": config_data["Temperature"], "locked": False}
            }
        ]
    },
    "TimingParams": {
        "HeatingTime": {"default": config_data["Heating_time"], "locked": False},
        "CoolingTime": {"default": config_data["Cooling_time"], "locked": False},
        "DelayTime": {"default": config_data["Delay_time"], "locked": False},
        "Repeat": {"default": config_data["Repeat_times"], "locked": False}
    }
}

# WebSocket 操作的相關函數和測量流程不變

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
    print(command_save_config)
    # print("Measurement started")
    # websocket_url = "ws://" + IP_ADDRESS + ":8085"
    # websocket_transport = WebSocket()
    
    # try:
    #     # ---- Initialize and open websocket
    #     websocket_transport.connect(websocket_url)
    #     websocket_transport.settimeout(10)

    #     # ---- Query system state
    #     if do_web_socket_bool_query(websocket_transport, command_system_ready):
    #         print("System is ready")
    #     else:
    #         raise Exception("System is NOT ready, returning...")

    #     # ---- Check api version
    #     api_version = do_web_socket_string_query(websocket_transport, command_query_api_version)
    #     print("Api version: " + api_version["Answer"])
    #     api_version_str = api_version["Answer"]
    #     api_version_str = api_version_str[:api_version_str.find('.')]
    #     if api_version_str != "2":
    #         raise Exception("Not supported major api version")              

    #     # ---- Enable Thermostat
    #     if not do_web_socket_bool_query(websocket_transport, command_enable_thermostat):
    #         raise Exception("Cannot Enable Thermostat")

    #     # ---- Save config
    #     if not do_web_socket_bool_query(websocket_transport, command_save_config):
    #         raise Exception("Cannot save config")

    #     # ---- Allocate resources and start measurement process...
        
    # except Exception as e:
    #      print("Error: " + str(e))

    # # Close
    # websocket_transport.close()
    print("Exit")
