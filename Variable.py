#!/usr/bin/env python3

import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request
import os

def websocket_test():
    # 配置 IP 地址
    IP_ADDRESS = "192.168.20.99"

    # 從 saved_parameters.json 中讀取變數
    def load_saved_parameters_json():
        # 從 saved_parameters.json 中讀取變數
        with open('saved_parameters.json', 'r') as file:
            return json.load(file)

    config_data = load_saved_parameters_json()

    # 從 thermostat_config_data.json 中讀取變數
    def load_thermostat_config_data_json():
        # 檢查檔案是否存在
        if not os.path.exists('thermostat_config_data.json'):
            print("檔案不存在，返回預設值")
            return {}

        try:
            # 從 thermostat_config_data.json 中讀取變數
            with open('thermostat_config_data.json', 'r') as file:
                data = json.load(file)
                if not data:
                    print("檔案中沒有值，返回預設值")
                    return {}
                return data
        except json.JSONDecodeError:
            print("檔案格式錯誤，返回預設值")
            return {}

    thermostat_config_data = load_thermostat_config_data_json()

    # 自定義保存的本地路徑
    def download_save_directory():
        save_directory = config_data["storage_path"]  # 可以修改為你希望的路徑

        # 如果目錄不存在，則創建目錄
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        return save_directory

    # 定義命令
    command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
    command_query_api_version = {"Command": "GET_API_VERSION"}
    command_query_alloc_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": config_data["Config_Name"]}
    command_query_measurement_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": f"{config_data['Config_Name']}_transient"}
    command_get_file_list = {"Command": "QUERY_TASK_RESULT_FILE_LIST", "TaskAlias": f"{config_data['Config_Name']}_transient"}
    command_remove_transient_task = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": f"{config_data['Config_Name']}_transient"}
    command_remove_resource_alloc = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": config_data["Config_Name"]}

    # 使用從 JSON 文件中導入的數據
    command_save_config = {
        "Command": "SAVE_CONFIG",
        "Type": "TransientModel",
        "ConfigName": config_data["Config_Name"],
        "ConfigParams": {
            "Description": "Test"
        },
        "Resources": {
            "CurrentSourceParams": config_data["Resources"]["CurrentSourceParams"],
            "CurrentSourceWithActiveloadParams": [ ],
            "DividerParams": [ ],
            "VoltageSourceParams": [ ],
            "MeasCardChParams": config_data["Resources"]["MeasCardChParams"],
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
            "ThermostatParams": config_data["Resources"]["ThermostatParams"],
            "TriggerOutputParams": [ ]
        },
        "TimingParams": {
            "HeatingTime": {"default": config_data["Heating_time"], "locked": False, "min": 0, "max": 4000},
            "CoolingTime": {"default": config_data["Cooling_time"], "locked": False, "min": 0, "max": 4000},
            "DelayTime": {"default": config_data["Delay_time"], "locked": False, "min": 0, "max": 4000},
            "Repeat": {"default": config_data["Repeat_times"], "locked": False, "min": 1, "max": 100},
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
        "TspCalibParams": config_data["TspCalibParams"]
    }

    command_save_thermostat_config = {
        "Command": "TRY_INIT_THEMOSTAT_AND_SAVE_CONFIG",
        "Alias": "/THERMOSTAT/0",
        "Answer": "OK",
        "SerialTransport": {
            "BaudRate": thermostat_config_data["Baudrate"],
            "DataBits": thermostat_config_data["Data bits"],
            "Handshake": thermostat_config_data["Handshake"],
            "InterfaceID": "RS232",
            "Parity": thermostat_config_data["Parity"],
            "StopBits": thermostat_config_data["Stop bits"],
            "Timeout": 2000,
            "WriteSleep": 100
        },
        "StabilityCriteria": {
            "DtMinMax": 0.1,
            "DtTarget": 0.25,
            "TimeWindow": 60,
            "Timeout": 1800,
        },
        "ThermostatType": thermostat_config_data["Thermostat type"]
    }

    command_do_resource_alloc = {
        "Command": "START_TASK",
        "TaskMode": "MONITORING_RESOURCE_ALLOCATION",
        "ConfigName": config_data["Config_Name"],
        "TaskAlias": config_data["Config_Name"],
        "LoadConfig": True,
        # It is recommended to maintain websocket connection (and not use this optional parameter)
        "HandleUserDisconnect": False
    }

    command_start_transient = {
        "Command": "START_TASK",
        "TaskMode": "TRANSIENT",
        "ConfigName": config_data["Config_Name"],
        "TaskAlias": f"{config_data['Config_Name']}_transient",
        "LoadConfig": True
    }

    command_start_tspcalib = {
    "Command": "START_TASK",
    "TaskMode": "TSPCALIB",
    "ConfigName": config_data["Config_Name"],
    "TaskAlias": f"{config_data['Config_Name']}_transient",
    "LoadConfig": True,
    }

    # 啟用 thermostat
    command_enable_thermostat = {
        "Command": "ENABLE_THERMOSTAT",
        "Alias": "/THERMOSTAT/0"
    }

    # 關閉 thermostat
    command_disable_thermostat = {
        "Command": "DISABLE_THERMOSTAT",
        "Alias": "/THERMOSTAT/0"
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


    print("Measurement started")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()


    try:

        print("我是VARI")
        print(f"{config_data['Config_Name']}_transient")

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

        # 是否連接到 thermostat
        if config_data["Connect_to_Thermostat"] == True:
            # 保存 thermostat 設定參數
            if not do_web_socket_bool_query(websocket_transport, command_save_thermostat_config):
                raise Exception("無法保存 thermostat 配置")
            # 啟用 thermostat
            if not do_web_socket_bool_query(websocket_transport, command_enable_thermostat):
                raise Exception("無法啟用 thermostat")           
        else:
            # 關閉 thermostat
            if not do_web_socket_bool_query(websocket_transport, command_disable_thermostat):
                raise Exception("無法關閉 thermostat")              

        # TSP 設定
        if config_data["TSP"] == True:
            if not do_web_socket_bool_query(websocket_transport, command_save_config):
                raise Exception("無法保存配置")     
            
            if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                raise Exception("資源分配失敗")
            while True:
                sleep(1)
                task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                if task_status["Answer"] == "RUN":
                    print("TSP 測量資源分配完成")
                    break          

            # 啟動 TSP
            if not do_web_socket_string_query(websocket_transport, command_start_tspcalib):
                raise Exception("TSP 測量啟動失敗")
            else:
                print("TSP 開始測量")

            busy = True
            while busy:
                sleep(1)
                task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
                print(f"TSP 測量中，請稍候... {task_status['Percentage']}%")
                if task_status["Answer"] != "RUN":
                    busy = False
                    print(f"TSP 測量完成")

            # 取得並下載 TSP 檔案
            file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

            # for file in file_list["Result"]:
            #     if "Filename" in file:
            #         tco_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], 1, "TSP", folder_name)

            # 刪除資源和瞬態任務
            do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
            do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
        else:
            print("不執行 TSP 測量")

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
            link = "http://" + IP_ADDRESS + ":8085" + file["Filename"]
            # 從文件名提取最後一部分，並生成完整的保存路徑
            save_path = os.path.join(download_save_directory(), link[(link.rfind("/")+1):])
            # 放入下載來源 url(link) 以及 包含儲存路徑的檔名
            urllib.request.urlretrieve(link, save_path)

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