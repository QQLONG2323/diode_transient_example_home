import json
from time import sleep
from websocket import WebSocket
import urllib.request
import os
import subprocess
import platform
from datetime import datetime


IP_ADDRESS = "192.168.20.99"

def load_saved_parameters_json():
    # 從 saved_parameters.json 中讀取變數
    with open('saved_parameters.json', 'r') as file:
        return json.load(file)
    

config_data = load_saved_parameters_json()






# 創建新資料夾的函數
def create_new_folder():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"measurement_data_{current_time}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# ---- 常用命令
command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
command_query_api_version = {"Command": "GET_API_VERSION"}
command_query_alloc_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "diode_config"}
command_query_measurement_task_status = {"Command": "QUERY_TASK_STATUS", "TaskAlias": "diode_config_transient"}
command_get_file_list = {"Command": "QUERY_TASK_RESULT_FILE_LIST", "TaskAlias": "diode_config_transient"}
command_remove_transient_task = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "diode_config_transient"}
command_remove_resource_alloc = {"Command": "STOP_AND_REMOVE_TASK", "TaskAlias": "diode_config"}

# 配置保存命令（初始配置）
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
            "default": "Cooling"
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
    "TspCalibParams": config_data["TspCalibParams"]
}

command_save_config_no_wait = {
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
            "default": "Cooling"
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
    "TspCalibParams": config_data["TspCalibParams"]
}

# 修改後的配置（B組）
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
            "default": "Cooling"
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

command_do_resource_alloc = {
    "Command": "START_TASK",
    "TaskMode": "MONITORING_RESOURCE_ALLOCATION",
    "ConfigName": "diode_config",
    "TaskAlias": "diode_config",
    "LoadConfig": True
}

command_start_transient = {
    "Command": "START_TASK",
    "TaskMode": "TRANSIENT",
    "ConfigName": "diode_config",
    "TaskAlias": "diode_config_transient",
    "LoadConfig": True
}

command_start_tspcalib = {
    "Command": "START_TASK",
    "TaskMode": "TSPCALIB",
    "ConfigName": "diode_config",
    "TaskAlias": "diode_config_transient",
    "LoadConfig": True,
}

# WebSocket 查詢
def do_web_socket_string_query(ws: WebSocket, command: dict) -> dict:
    ws.send(json.dumps(command))
    answer_str = ws.recv()
    return json.loads(answer_str)

def do_web_socket_bool_query(ws: WebSocket, command: dict) -> bool:
    answer = do_web_socket_string_query(ws, command)
    return answer["Answer"] == "OK"

# 下載檔案並確保檔名不被覆蓋
def download_file(file_url, original_filename, cycle_index, measurement_index, group, folder_name):
    local_filename = f"measurement_{group}_{cycle_index}_{measurement_index}_{original_filename[(original_filename.rfind('/')+1):]}"
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

# 合併多個檔案的數據
def merge_files(file_paths):
    combined_comments = []
    combined_data = []
    last_index = 0

    # Filter for raw files
    raw_file_paths = [file for file in file_paths if file.endswith('.raw')]
    
    if not file_paths:
        print("警告：沒有找到可合併的文件")
        return combined_comments, combined_data

    for idx, file_path in enumerate(raw_file_paths):
        comments, data = read_raw_file(file_path)
        
        if not data:
            print(f"警告：文件 {file_path} 不包含任何數據")
            continue

        if idx == 0:
            combined_comments = comments
            combined_data = data
        else:
            adjusted_data = [(last_index + data[i][0] + 1, value[1]) for i, value in enumerate(data)]
            combined_data.extend(adjusted_data)
        
        if combined_data:
            last_index = combined_data[-1][0]
        else:
            print(f"警告：合併後的數據為空")

    return combined_comments, combined_data

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
    measurement_count = config_data["Pulse Cycling Repeat"]
    cycle_count = config_data["total Measurement Cycling Repeat"]
    print("測量開始")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()
    downloaded_files = []
    group_a_files = []
    group_b_files = []  # 用來儲存 B 組檔案
    # first_a_par_file = None  # 用來儲存 A 組的第一個 .par 檔案
    # first_b_par_file = None  # 用來儲存 B 組的第一個 .par 檔案
    try:
        websocket_transport.connect(websocket_url)
        websocket_transport.settimeout(10)

        if not do_web_socket_bool_query(websocket_transport, command_system_ready):
            raise Exception("系統尚未準備好")

        # 查詢API版本
        api_version = do_web_socket_string_query(websocket_transport, command_query_api_version)
        print(f"API 版本: {api_version['Answer']}")

        
        # TSP 設定
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
            print(f"測量中，請稍候... {task_status['Percentage']}%")
            if task_status["Answer"] != "RUN":
                busy = False
                print(f"TSP 測量完成")

        # 取得並下載 TSP 檔案
        file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

        for file in file_list["Result"]:
            if "Filename" in file:
                downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], 1, 1, "TSP", folder_name)

        # 刪除資源和瞬態任務
        do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
        do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
        
        
        
        # 開始迴圈測量
        for j in range(1, cycle_count + 1):
            # 進行 A 組測量  
            first_a_par_file = None # 每個循環都重置 first_a_par_file
            cycle_a_files = []  # 追蹤此循環中的 A 組檔案
            
            for i in range(1, measurement_count + 1):
                print(f"進行第 {j} 組，第 {i} 次測量 (A組)")

                if j == 1 and i == 1:
                    if not do_web_socket_bool_query(websocket_transport, command_save_config):
                        raise Exception("無法保存配置")
                else:
                    if not do_web_socket_bool_query(websocket_transport, command_save_config_no_wait):
                        raise Exception("無法保存配置")
                    
                # 啟動資源分配並開始測量
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量資源分配完成 (A組，第 {j} 組，第 {i} 次)")
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
                        print(f"瞬態測量完成 (A組，第 {j} 組，第 {i} 次)")

                # 取得並下載檔案 (A組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, i, "A", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_a_files.append(downloaded_file)  # 將 A 組檔案加到追蹤列表

                    # 找到第一個 .par 檔案
                    if "Filename" in file and file["Filename"].endswith(".par") and first_a_par_file is None:
                        first_a_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, i, "A", folder_name)
                
                # 刪除資源和瞬態任務
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)

            # 合併當前循環的 A 組文件
            if cycle_a_files:
                comments, combined_data = merge_files(cycle_a_files)
                output_file_path = os.path.join(folder_name, f'group_A_combined_cycle_{j}.raw')
                
                with open(output_file_path, 'w') as output_file:
                    for line in comments:
                        output_file.write(f"{line}\n")
                    for item in combined_data:
                        output_file.write(f"{item[0]} {item[1]}\n")

                print(f"A組文件已合併並寫入: {output_file_path}")
                group_a_files.append(output_file_path)

                # 嘗試將每個循環的第一個 .par 檔案改名為合併檔名
                rename_first_par_file(first_a_par_file, output_file_path)

            # 進行 B 組測量
            if not do_web_socket_bool_query(websocket_transport, command_save_config_b_no_wait):
                raise Exception("無法保存 B 組配置")
            
            first_b_par_file = None  # 每個循環重置 first_b_par_file
            cycle_b_files = []  # 追蹤此循環中的 B 組檔案

            for i in range(1, 2):
                print(f"進行第 {j} 組，第 {i} 次測量 (B組)")

                # 啟動資源分配並開始測量 (B組)
                if not do_web_socket_bool_query(websocket_transport, command_do_resource_alloc):
                    raise Exception("B組資源分配失敗")

                while True:
                    sleep(1)
                    task_status = do_web_socket_string_query(websocket_transport, command_query_alloc_task_status)
                    if task_status["Answer"] == "RUN":
                        print(f"測量資源分配完成 (B組，第 {j} 組，第 {i} 次)")
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
                        print(f"瞬態測量完成 (B組，第 {j} 組，第 {i} 次)")


                # 取得並下載檔案 (B組)
                file_list = do_web_socket_string_query(websocket_transport, command_get_file_list)

                for file in file_list["Result"]:
                    if "Filename" in file:
                        downloaded_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, i, "B", folder_name)
                        downloaded_files.append(downloaded_file)
                        cycle_b_files.append(downloaded_file)  # 將 B 組檔案加到追蹤列表
                    # 找到第一個 .par 檔案
                    if "Filename" in file and file["Filename"].endswith(".par") and first_b_par_file is None:
                        first_b_par_file = download_file(f"http://{IP_ADDRESS}:8085{file['Filename']}", file["Filename"], j, i, "B", folder_name)

                # 刪除資源和瞬態任務 (B組)
                do_web_socket_bool_query(websocket_transport, command_remove_transient_task)
                do_web_socket_bool_query(websocket_transport, command_remove_resource_alloc)
        

            # 合併當前循環的 B 組文件
            if cycle_b_files:
                comments, combined_data = merge_files(cycle_b_files)
                output_file_path = os.path.join(folder_name, f'group_B_combined_cycle_{j}.raw')
                
                with open(output_file_path, 'w') as output_file:
                    for line in comments:
                        output_file.write(f"{line}\n")
                    for item in combined_data:
                        output_file.write(f"{item[0]} {item[1]}\n")

                print(f"B組文件已合併並寫入: {output_file_path}")
                group_b_files.append(output_file_path)

                # 嘗試將每個循環的第一個 .par 檔案改名為合併檔名
                rename_first_par_file(first_b_par_file, output_file_path)

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        websocket_transport.close()
    
    # 程式執行完畢後，打開存檔資料夾
    open_folder(folder_name)

    return downloaded_files

# 主程序
# if __name__ == "__main__":
def Cycling_Test():
    global config_data
    config_data = load_saved_parameters_json()

    print("我是CYCLING")
    print(config_data["Pulse Cycling Repeat"])
    print(config_data["total Measurement Cycling Repeat"])
    print(config_data["Heating_time"])
    print(config_data["Cooling_time"])
    print(config_data["Config_Name"])
    print(config_data["Tmin"])
    print(config_data["Tmax"])
    print(config_data["Tstep"])
    print(config_data["TspCalibParams"])


    

    # 創建新資料夾
    folder_name = create_new_folder()
    print(f"創建新資料夾: {folder_name}")

    # 執行測量並獲取下載的文件列表
    downloaded_files = execute_measurements(folder_name)

    if not downloaded_files:
        print("錯誤：沒有下載到任何文件")
    else:
        # 合併下載的文件
        comments, combined_data = merge_files(downloaded_files)

        if not combined_data:
            print("錯誤：合併後沒有數據")
            # 將合併後的結果輸出到新檔案
            output_file_path = os.path.join(folder_name, 'processed_data_with_comments_and_multiple_files.raw')
            with open(output_file_path, 'w') as output_file:
                for line in comments:
                    output_file.write(f"{line}\n")
                for item in combined_data:
                    output_file.write(f"{item[0]} {item[1]}\n")