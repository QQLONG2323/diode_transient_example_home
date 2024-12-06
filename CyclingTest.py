import json
from time import sleep
from websocket import WebSocket
import urllib.request
import os
import subprocess
import platform
from datetime import datetime
import DataModified


IP_ADDRESS = "192.168.20.99"

def load_saved_parameters_json():
    # 從 saved_parameters.json 中讀取變數
    with open('saved_parameters.json', 'r') as file:
        return json.load(file)




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




# 創建新資料夾的函數
def create_new_folder():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"measurement_data_{current_time}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name




# WebSocket 查詢
def do_web_socket_string_query(ws: WebSocket, command: dict) -> dict:
    ws.send(json.dumps(command))
    answer_str = ws.recv()
    return json.loads(answer_str)

def do_web_socket_bool_query(ws: WebSocket, command: dict) -> bool:
    answer = do_web_socket_string_query(ws, command)
    return answer["Answer"] == "OK"

# 下載檔案並確保檔名不被覆蓋
def download_file(file_url, original_filename, cycle_index, group, folder_name):
    local_filename = f"measurement_{group}_{cycle_index}_{original_filename[(original_filename.rfind('/')+1):]}"
    full_path = os.path.join(folder_name, local_filename)
    urllib.request.urlretrieve(file_url, full_path)
    print(f"文件下載完成: {full_path}")
    return full_path

# 讀取.raw檔案的函數
def read_raw_file(file_path):
    data = []
    comments = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                comments.append(line.strip())
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    index = int(parts[0])
                    value = int(parts[1])
                    data.append((index, value))
                except ValueError:
                    continue
    return comments, data


# 將第一個 .par 檔案重新命名為最後合併的檔名 (使用 .par 結尾)
def rename_first_par_file(first_par_file, new_raw_file_path):
    if first_par_file:
        new_par_file_path = new_raw_file_path.replace(".raw", ".par")
        print(f"嘗試將 {first_par_file} 改名為 {new_par_file_path}")
        try:
            if os.path.exists(first_par_file):
                os.rename(first_par_file, new_par_file_path)
                print(f"已將第一個 .par 檔案 {first_par_file} 改名為 {new_par_file_path}")
            else:
                print(f"錯誤：找不到 .par 檔案 {first_par_file}")
        except FileNotFoundError:
            print(f"錯誤：無法找到 .par 檔案 {first_par_file}，無法進行重命名")
        except Exception as e:
            print(f"發生錯誤: {e}")
    else:
        print("未找到第一個 .par 檔案，無法進行重命名")
    
# 根據作業系統自動打開資料夾
def open_folder(folder_path):
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux / Unix
            subprocess.Popen(["xdg-open", folder_path])
        print(f"已自動打開資料夾: {folder_path}")
    except Exception as e:
        print(f"無法打開資料夾: {folder_path}，發生錯誤: {e}")

# ------ 執行測量 -----
def execute_measurements(folder_name):
    # 測量次數設定
    # measurement_count = config_data["Pulse Cycling Repeat"]
    cycle_count = config_data["total Measurement Cycling Repeat"]
    print("測量開始")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()
    downloaded_files = []
    # first_b_par_file = None  # 每個循環重置 first_b_par_file
    cycle_b_files = []  # 追蹤此循環中的 B 組檔案
    tco_file = None

    try:
        websocket_transport.connect(websocket_url)
        websocket_transport.settimeout(10)

        if not do_web_socket_bool_query(websocket_transport, command_system_ready):
            raise Exception("系統尚未準備好")

        # 查詢API版本
        api_version = do_web_socket_string_query(websocket_transport, command_query_api_version)
        print(f"API 版本: {api_version['Answer']}")

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

            for file in file_list["Result"]:
                if "Filename" in file:
                    tco_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], 1, "TSP", folder_name)

            # 刪除資源和瞬態任務
            do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
            do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
        else:
            print("不執行 TSP 測量")
        
        
        
        # 開始迴圈測量
        for j in range(1, cycle_count + 1):
            # 如果是第一次循環，或者 other_lp220_current_list 沒有值，或者 other_lp220_current_list 沒有足夠的值時，都執行 A 組和 B 組測量的基礎邏輯
            print("Start cycling test" + str(j))
            if j == 1 or not config_data.get("Other LP220 Current list", []) or j - 2 >= len(config_data.get("Other LP220 Current list", [])):
                # 進行 A 組測量  
                first_a_par_file = None # 每個循環都重置 first_a_par_file
                cycle_a_files = []  # 追蹤此循環中的 A 組檔案


                if not do_web_socket_bool_query(websocket_transport, command_save_config):
                    raise Exception("無法保存配置")
                        
                # 啟動資源分配並開始測量
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量參數設定完成，開始測量")
                        break

                # 啟動瞬態測量
                if not do_web_socket_bool_query(websocket_transport, command_start_transient):
                    raise Exception("瞬態測量啟動失敗")

                busy = True
                while busy:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
                    print(f"測量中，請稍候... {task_status['Percentage']}%")
                    if task_status["Answer"] != "RUN":
                        busy = False
                        print(f"瞬態測量完成")
                            
                # 取得並下載檔案 (A組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "A", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_a_files.append(downloaded_file)  # 將 A 組檔案加到追蹤列表

                    # 找到第一個 .par 檔案
                    # if "Filename" in file and file["Filename"].endswith(".par") and first_a_par_file is None:
                    #     first_a_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "A", folder_name)
                    
                # 刪除資源和瞬態任務
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)


                # 進行 B 組測量
                if not do_web_socket_bool_query(websocket_transport, command_save_config_b_no_wait):
                    raise Exception("無法保存 B 組配置")
            

                # 啟動資源分配並開始測量 (B組)
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("B組資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量資源分配完成")
                        break

                # 啟動瞬態測量 (B組)
                if not do_web_socket_bool_query(websocket_transport, command_start_transient):
                    raise Exception("瞬態測量啟動失敗 (B組)")

                busy = True
                while busy:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
                    print(f"測量中，請稍候... {task_status['Percentage']}%")
                    if task_status["Answer"] != "RUN":
                        busy = False
                        print(f"瞬態測量完成")


                # 取得並下載檔案 (B組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "B", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_b_files.append(downloaded_file)  # 將 B 組檔案加到追蹤列表
                    # 找到第一個 .par 檔案
                    # if "Filename" in file and file["Filename"].endswith(".par") and first_b_par_file is None:
                    #     first_b_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "B", folder_name)

                # 刪除資源和瞬態任務 (B組)
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
               
                # # 呼叫 DataModified 中的函數來處理下載的文件
                # par_file = None
                # raw_file = None
                # for file in cycle_b_files:
                #     if "cooling" in file and file.endswith(".par"):
                #         par_file = file
                #     elif "cooling" in file and file.endswith(".raw"):
                #         raw_file = file

                #     if par_file and raw_file:
                #         DataModified.process_files(tco_file, par_file, raw_file, folder_name)

            else: 
                # 如果不是第一次循環，且 other_lp220_current_list 有足夠的值時，執行這部分邏輯
                other_lp220_current_list = config_data.get("Other LP220 Current list", [])
                
                # 檢查 "Other LP220 Current list" 是否有值，並確保不超出索引範圍
                if other_lp220_current_list and j - 2 < len(other_lp220_current_list):
                    # 更新 command_save_config 中 "SetCurrent" 的值
                    current_value = other_lp220_current_list[j - 2]  # 按照迴圈次數取出對應值
                    command_save_config["Resources"]["CurrentSourceParams"][0]["SetCurrent"]["default"] = current_value
                    command_save_config_b_no_wait["Resources"]["CurrentSourceParams"][0]["SetCurrent"]["default"] = current_value
                    print(f"第 {j} 次測量設置 'SetCurrent' 為: {current_value}")

                if not do_web_socket_bool_query(websocket_transport, command_save_config):
                    raise Exception("無法保存配置")
                        
                # 啟動資源分配並開始測量
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量資源分配完成")
                        break

                # 啟動瞬態測量
                if not do_web_socket_bool_query(websocket_transport, command_start_transient):
                    raise Exception("瞬態測量啟動失敗")

                busy = True
                while busy:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
                    print(f"測量中，請稍候... {task_status['Percentage']}%")
                    if task_status["Answer"] != "RUN":
                        busy = False
                        print(f"瞬態測量完成")
                            
                # 取得並下載檔案 (A組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "A", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_a_files.append(downloaded_file)  # 將 A 組檔案加到追蹤列表

                    # 找到第一個 .par 檔案
                    # if "Filename" in file and file["Filename"].endswith(".par") and first_a_par_file is None:
                    #     first_a_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "A", folder_name)
                    
                # 刪除資源和瞬態任務
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)

                # 進行 B 組測量
                if not do_web_socket_bool_query(websocket_transport, command_save_config_b_no_wait):
                    raise Exception("無法保存 B 組配置")

                # 啟動資源分配並開始測量 (B組)
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("B組資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量資源分配完成")
                        break

                # 啟動瞬態測量 (B組)
                if not do_web_socket_bool_query(websocket_transport, command_start_transient):
                    raise Exception("瞬態測量啟動失敗 (B組)")

                busy = True
                while busy:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_measurement_task_status)
                    print(f"測量中，請稍候... {task_status['Percentage']}%")
                    if task_status["Answer"] != "RUN":
                        busy = False
                        print(f"瞬態測量完成")


                # 取得並下載檔案 (B組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "B", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_b_files.append(downloaded_file)  # 將 B 組檔案加到追蹤列表
                    # 找到第一個 .par 檔案
                    # if "Filename" in file and file["Filename"].endswith(".par") and first_b_par_file is None:
                    #     first_b_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, "B", folder_name)

                # 刪除資源和瞬態任務 (B組)
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)

                # # 呼叫 DataModified 中的函數來處理下載的文件
                # par_file = None
                # raw_file = None
                # for file in cycle_b_files:
                #     if "cooling" in file and file.endswith(".par"):
                #         par_file = file
                #     elif "cooling" in file and file.endswith(".raw"):
                #         raw_file = file

                #     if par_file and raw_file:
                #         DataModified.process_files(tco_file, par_file, raw_file, folder_name)




    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        websocket_transport.close()
    
            
    # 呼叫 DataModified 中的函數來處理下載的文件
    par_file = None
    raw_file = None

    # 過濾出所有包含 "cooling" 的檔案
    cooling_files = [file for file in cycle_b_files if "cooling" in file]

    # 從 cooling_files 中過濾出 .par 檔案
    par_files = [file for file in cooling_files if file.endswith(".par")]

    print("par_files: ", par_files)
    for par_file in par_files:
        # 找到與 par_file 對應的 raw_file
        base_name = par_file.rsplit('.', 1)[0]
        raw_file = next((file for file in cooling_files if file.startswith(base_name) and file.endswith(".raw")), None)

        if par_file and raw_file:
            DataModified.process_files(tco_file, par_file, raw_file, folder_name)

    # 程式執行完畢後，打開存檔資料夾
    open_folder(folder_name)

    return downloaded_files

# 主程序
# if __name__ == "__main__":
def Cycling_Test():
    global config_data
    config_data = load_saved_parameters_json()

    global thermostat_config_data
    thermostat_config_data = load_thermostat_config_data_json()

    # 常用命令
    global command_system_ready
    command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
    global command_query_api_version
    command_query_api_version = {"Command": "GET_API_VERSION"}
    global command_query_alloc_task_status
    command_query_alloc_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "diode_config"}
    global command_query_measurement_task_status
    command_query_measurement_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "diode_config_transient"}
    global command_get_file_list
    command_get_file_list = {"Command": "QUERY_TASK_RESULT_FILE_LIST", "TaskAlias": "diode_config_transient"}
    global command_remove_transient_task
    command_remove_transient_task = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "diode_config_transient"}
    global command_remove_resource_alloc
    command_remove_resource_alloc = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "diode_config"}

    global command_do_resource_alloc
    command_do_resource_alloc = {
        "Command": "START_TASK",
        "TaskMode": "MONITORING_RESOURCE_ALLOCATION",
        "ConfigName": "diode_config",
        "TaskAlias": "diode_config",
        "LoadConfig": True
    }

    global command_start_transient
    command_start_transient = {
        "Command": "START_TASK",
        "TaskMode": "TRANSIENT",
        "ConfigName": "diode_config",
        "TaskAlias": "diode_config_transient",
        "LoadConfig": True
    }

    global command_start_tspcalib
    command_start_tspcalib = {
        "Command": "START_TASK",
        "TaskMode": "TSPCALIB",
        "ConfigName": "diode_config",
        "TaskAlias": "diode_config_transient",
        "LoadConfig": True,
    }

    # 啟用 thermostat
    global command_enable_thermostat
    command_enable_thermostat = {
        "Command": "ENABLE_THERMOSTAT",
        "Alias": "/THERMOSTAT/0"
    }

    # 關閉 thermostat
    global command_disable_thermostat
    command_disable_thermostat = {
        "Command": "DISABLE_THERMOSTAT",
        "Alias": "/THERMOSTAT/0"
    }

    # 配置保存命令（初始配置）
    global command_save_config
    command_save_config = {
        "Command": "SAVE_CONFIG",
        "Type": "Config",
        "ConfigName": "diode_config",
        "ConfigParams": {"Description": "Test"},
        "Resources": {
            "CurrentSourceParams": config_data["Resources"]["CurrentSourceParams"],
            "CurrentSourceWithActiveloadParams": [ ],
            "DividerParams": [ ],
            "VoltageSourceParams": [ ],
            "MeasCardChParams":config_data["Resources"]["MeasCardChParams"],
            "ThermometerCardChParams": [ ],
            "ThermostatParams": config_data["Resources"]["ThermostatParams"],
            "TriggerOutputParams": [ ]
        },
        "TimingParams": {
            "TransientMode": {
                "locked": False,
                "default": "REPEATED_COOLING"
            },
            "SamplePerOctave": {
                "default": 1000,
                "locked": False,
                "min": 1000,
                "max": 1000
            },
            "HeatingTime": {"default": config_data["Pulse Cycling On [s]"], "locked": False},
            "CoolingTime": {"default": config_data["Pulse Cycling Off [s]"], "locked": False},
            "DelayTime": {"default": 0, "locked": False},
            "Repeat": {"default": config_data["Pulse Cycling Repeat"], "locked": False}
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

    # 修改後的配置（B組）
    global command_save_config_b_no_wait
    command_save_config_b_no_wait = {
        "Command": "SAVE_CONFIG",
        "Type": "Config",
        "ConfigName": "diode_config",
        "ConfigParams": {"Description": "Test"},
        "Resources": {
            "CurrentSourceParams": config_data["Resources"]["CurrentSourceParams"],
            "CurrentSourceWithActiveloadParams": [ ],
            "DividerParams": [ ],
            "VoltageSourceParams": [ ],
            "MeasCardChParams":config_data["Resources"]["MeasCardChParams"],
            "ThermometerCardChParams": [ ],
            "ThermostatParams": config_data["Resources"]["ThermostatParams_no_wait"],
            "TriggerOutputParams": [ ]
        },
        "TimingParams": {
            "TransientMode": {
                "locked": False,
                "default": "REPEATED_COOLING"
            },
            "SamplePerOctave": {
                "default": 1000,
                "locked": False,
                "min": 1000,
                "max": 1000
            },
            "HeatingTime": {"default": config_data["Rth Measurement Heating Times"], "locked": False},
                "CoolingTime": {"default": config_data["Rth Measurement Cooling Times"], "locked": False},
                "DelayTime": {"default": 0, "locked": False},
                "Repeat": {"default": 1, "locked": False}
        },
        "SourceTimingControl": {
            "locked": False,
            "Enabled": False,
            "ReversePowerOff": True,
            "WaitForInstrumentDelay": True,
            "PowerOn": [ ],
            "PowerOff": [ ]
        },
        "TspCalibParams": config_data["TspCalibParams"],
    }

    # 保存 thermostat 設定參數
    global command_save_thermostat_config
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

    # 創建新資料夾
    folder_name = create_new_folder()
    print(f"創建新資料夾: {folder_name}")

    # 執行測量並獲取下載的文件列表
    downloaded_files = execute_measurements(folder_name)

    if not downloaded_files:
        print("錯誤：沒有下載到任何文件")
