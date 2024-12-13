#!/usr/bin/env python3

import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request
import os
from datetime import datetime
import platform
import subprocess

def websocket_test():
    # 配置 IP 地址
    IP_ADDRESS = "192.168.20.99"

    # 定義命令
    command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
    command_query_api_version = {"Command": "GET_API_VERSION"}
    command_query_alloc_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "jeff_booster_test"}
    command_query_measurement_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "jeff_booster_test_transient"}
    command_get_file_list = {"Command": "QUERY_TASK_RESULT_FILE_LIST", "TaskAlias": "jeff_booster_test_transient"}
    command_remove_transient_task = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "jeff_booster_test_transient"}
    command_remove_resource_alloc = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "jeff_booster_test"}

    # 使用從 JSON 文件中導入的數據
    command_save_config = {
        "Command": "SAVE_CONFIG",
        "Type": "TransientModel",
        "ConfigName": "jeff_booster_test",
        "ConfigParams": {
            "Description": "Test"
        },
        "Resources": {
            "CurrentSourceParams": [
                {
                    "Alias": "/PWB240/PWB10018/CH0/DriveSour/0",
                    "UserAlias": "PWB10018 - S1Ch1 - Drive",
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
                    "OutputMode": {"default": "PC", "locked": False},
                    "SetCurrent": {"default": 0.1, "locked": False, "min": 0, "max": 240},
                    "VoltageCorner": {"default": 10.0, "locked": False, "min": 0, "max": 11}
                },
                {
                    "Alias": "/PWB240/PWB10018/CH0/SensSour/0",
                    "UserAlias": "PWB10018 - S1Ch1 - Sense",
                    "OutputMode": {"default": "ON", "locked": False},
                    "SetCurrent": {"default": 0.001, "locked": False, "min": -1, "max": 1},
                    "VoltageCorner": {"default": 1.0, "locked": False, "min": 0, "max": 11}
                }
            ],
            "CurrentSourceWithActiveloadParams": [ ],
            "DividerParams": [ ],
            "VoltageSourceParams": [ ],
            "MeasCardChParams": [
                {
                    "Alias": "/T3STER/0/MS401/SLOT5/CH0",
                    "UserAlias": "S5Ch1",
                    "Sensitivity": {"default": [0.002], "locked": False},
                    "PowerStep": "@POWERSTEP_DIODE;/PWB240/PWB10018/CH0/SensSour/0;/PWB240/PWB10018/CH0/DriveSour/0",
                    "RangeIdx": {"default": 9, "locked": False},
                    "AutoRange": {"default": False, "locked": False},
                    "Uref": {"default": 0.0, "locked": False},
                    "UrefSwitching": {"default": False, "locked": False},
                    "UrefHeating": {"default": 0.0, "locked": False},                
                }
            ],
            "ThermometerCardChParams": [
                # {
                #     "Alias": Unique_system_selected_alias,
                #     "UserAlias": User_defined_alias,
                #     "Sensitivity": {
                #         "default": [ List_of_coefficients_in_volt_per_degrees ],
                #         "locked": False,
                #     },
                #     "PowerStep": PowerStep,
                #     "RangeIdx": {
                #         "default": id,
                #         "locked": False
                #     },
                #     "SamplePerSecIdx": {
                #         "default": id,
                #         "locked": False
                #     }
                # }
            ],
            "ThermostatParams": [{
                    "Alias": "/THERMOSTAT/0",
                    "UserAlias": "Th0",
                    "SetTemperature": {
                        "default": 25,
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
                }],
        },
        
        "TimingParams": {
            "HeatingTime": {"default": 5, "locked": False, "min": 0, "max": 4000},
            "CoolingTime": {"default": 5, "locked": False, "min": 0, "max": 4000},
            "DelayTime": {"default": 0, "locked": False, "min": 0, "max": 4000},
            "Repeat": {"default": 1, "locked": False, "min": 1, "max": 100},
            "TransientMode": {
                "locked": False,
                "default": "REPEATED_COOLING"
            },
            "SamplePerOctave": {
                "default": 1000,
                "locked": False,
                "min": 1000,
                "max": 1000
            }
        },
        "SourceTimingControl": {
            "locked": False,
            "Enabled": False,
            "ReversePowerOff": True,
            "WaitForInstrumentDelay": True,
            "PowerOn": [ ],
            "PowerOff": [ ]
        },
        "TspCalibParams": [ ]
    }

    # command_save_thermostat_config = {
    #     "Command": "TRY_INIT_THEMOSTAT_AND_SAVE_CONFIG",
    #     "Alias": "/THERMOSTAT/0",
    #     "Answer": "OK",
    #     "SerialTransport": {
    #         "BaudRate": thermostat_config_data["Baudrate"],
    #         "DataBits": thermostat_config_data["Data bits"],
    #         "Handshake": thermostat_config_data["Handshake"],
    #         "InterfaceID": "RS232",
    #         "Parity": thermostat_config_data["Parity"],
    #         "StopBits": thermostat_config_data["Stop bits"],
    #         "Timeout": 2000,
    #         "WriteSleep": 100
    #     },
    #     "StabilityCriteria": {
    #         "DtMinMax": 0.1,
    #         "DtTarget": 0.25,
    #         "TimeWindow": 60,
    #         "Timeout": 1800,
    #     },
    #     "ThermostatType": thermostat_config_data["Thermostat type"]
    # }

    command_do_resource_alloc = {
        "Command": "START_TASK",
        "TaskMode": "MONITORING_RESOURCE_ALLOCATION",
        "ConfigName": "jeff_booster_test",
        "TaskAlias": "jeff_booster_test",
        "LoadConfig": True,
        # It is recommended to maintain websocket connection (and not use this optional parameter)
        "HandleUserDisconnect": False
    }

    command_start_transient = {
        "Command": "START_TASK",
        "TaskMode": "TRANSIENT",
        "ConfigName": "jeff_booster_test",
        "TaskAlias": "jeff_booster_test_transient",
        "LoadConfig": True
    }

    command_start_tspcalib = {
    "Command": "START_TASK",
    "TaskMode": "TSPCALIB",
    "ConfigName": "jeff_booster_test",
    "TaskAlias": "jeff_booster_test_transient",
    "LoadConfig": True,
    }

    # # 啟用 thermostat
    # command_enable_thermostat = {
    #     "Command": "ENABLE_THERMOSTAT",
    #     "Alias": "/THERMOSTAT/0"
    # }

    # # 關閉 thermostat
    # command_disable_thermostat = {
    #     "Command": "DISABLE_THERMOSTAT",
    #     "Alias": "/THERMOSTAT/0"
    # }

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


    print("Measurement started")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()


    try:
        print("我是VARI")
        print("jeff_booster_test_transient")

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

        # # 是否連接到 thermostat
        # if config_data["Connect_to_Thermostat"] == True:
        #     # 保存 thermostat 設定參數
        #     if not do_web_socket_bool_query(websocket_transport, command_save_thermostat_config):
        #         raise Exception("無法保存 thermostat 配置")
        #     # 啟用 thermostat
        #     if not do_web_socket_bool_query(websocket_transport, command_enable_thermostat):
        #         raise Exception("無法啟用 thermostat")           
        # else:
        #     # 關閉 thermostat
        #     if not do_web_socket_bool_query(websocket_transport, command_disable_thermostat):
        #         raise Exception("無法關閉 thermostat")              

        # # TSP 設定
        # if config_data["TSP"] == True:
        #     if not do_web_socket_bool_query(websocket_transport, command_save_config):
        #         raise Exception("無法保存配置")     
            
        #     if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
        #         raise Exception("資源分配失敗")
        #     while True:
        #         sleep(1)
        #         task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
        #         if task_status["Answer"] == "RUN":
        #             print("TSP 測量資源分配完成")
        #             break          

        #     # 啟動 TSP
        #     if not do_web_socket_string_query(websocket_transport, command_start_tspcalib):
        #         raise Exception("TSP 測量啟動失敗")
        #     else:
        #         print("TSP 開始測量")

        #     busy = True
        #     while busy:
        #         sleep(1)
        #         task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
        #         print(f"TSP 測量中，請稍候... {task_status['Percentage']}%")
        #         if task_status["Answer"] != "RUN":
        #             busy = False
        #             print(f"TSP 測量完成")

        #     # 取得並下載 TSP 檔案
        #     file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)
        #     print(file_list)
        #     print("Results:")
        #     for file in file_list["Result"]:
        #         print("Downloading " + file["Filename"])
        #         download_file("http://" + IP_ADDRESS + ":8085" + file["Filename"], file["Filename"], folder)

        #     # 刪除資源和瞬態任務
        #     do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
        #     do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
        # else:
        #     print("不執行 TSP 測量")

        # ---- Save config
        if not do_web_socket_bool_query(websocket_transport, command_save_config):
            raise Exception("Cannot save config")

        # ---- Allocate resources and start measurement process...
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
        print(file_list)
        print("Results:")
        for file in file_list['Result']:
            print("Downloading " + file["Filename"])
            urllib.request.urlretrieve("http://" + IP_ADDRESS + ":8085" + file["Filename"], file["Filename"][(file["Filename"].rfind('/')+1):])

        # ---- Release resources: thermal transient task and resource allocation
        if not do_web_socket_bool_query(websocket_transport, command_remove_transient_task):
            raise Exception("Cannot remove transient task")

        if not do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc):
            raise Exception("Cannot remove allocation task")

        print("Measurement finished")
        
    except Exception as e:
        print("Error: " + str(e))
    finally:
        websocket_transport.close()

    # Close
    websocket_transport.close()
    print("Exit")

    # # 程式執行完畢後，打開存檔資料夾
    # open_folder(folder)

if __name__ == "__main__":
    websocket_test()