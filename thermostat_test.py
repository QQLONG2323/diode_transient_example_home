import json
from time import sleep
from websocket import WebSocket
import urllib.request

IP_ADDRESS = "192.168.20.99"

command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
command_query_api_version = {"Command": "GET_API_VERSION"}


# 查詢 thermostat 設定參數
command_get_thermostat_config = {
    "Command": "GET_THERMOSTAT_CONFIG",
    "Alias": "/THERMOSTAT/0"
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

# 查詢 thermostat 狀態
command_query_thermostat_status = {
    "Command": "QUERY_THERMOSTAT_STATUS",
    "Alias": "/THERMOSTAT/0"
}

# 保存 thermostat 設定參數
command_save_thermostat_config = {
    # "Command": "SAVE_THERMOSTAT_CONFIG",
    # "Alias": "/THERMOSTAT/0",
    # "SerialTransport": {
    #     "BaudRate": thermostat_config_data["Baudrate"],
    #     "DataBits": thermostat_config_data["Data bits"],
    #     "Handshake": thermostat_config_data["Handshake"],
    #     "InterfaceID": "RS232",
    #     "Parity": thermostat_config_data["Parity"],
    #     "StopBits": thermostat_config_data["Stop bits"],
    #     "Timeout": 2000,
    #     "WriteSleep": 100
    # },
    # "StabilityCriteria": {
    #     "DtMinMax": 0.1,
    #     "DtTarget": 0.25,
    #     "TimeWindow": 60,
    #     "Timeout": 1800,
    # },
    # "ThermostatType": thermostat_config_data["Thermostat type"]
}

command_query_external_devices = {
    "Command": "QUERY_EXTERNAL_DEVICES"
}

# WebSocket 查詢
def do_web_socket_string_query(ws: WebSocket, command: dict) -> dict:
    ws.send(json.dumps(command))
    answer_str = ws.recv()
    return json.loads(answer_str)

def do_web_socket_bool_query(ws: WebSocket, command: dict) -> bool:
    answer = do_web_socket_string_query(ws, command)
    return answer["Answer"] == "OK"

if __name__ == '__main__':
    print("測量開始")
    websocket_url = "ws://" + IP_ADDRESS + ":8085"
    websocket_transport = WebSocket()
    try:
        websocket_transport.connect(websocket_url)
        websocket_transport.settimeout(10)

        if not do_web_socket_bool_query(websocket_transport, command_system_ready):
            raise Exception("系統尚未準備好")

        api_version = do_web_socket_string_query(websocket_transport, command_query_api_version)
        print("API 版本: " + api_version["Answer"])

        # 查詢 thermostat 設定參數
        # command_get_thermostat_config = do_web_socket_string_query(websocket_transport, command_get_thermostat_config)
        # print(command_get_thermostat_config)

        # 啟用 thermostat
        # command_enable_thermostat = do_web_socket_bool_query(websocket_transport, command_enable_thermostat)
        # print(command_enable_thermostat)

        # 關閉 thermostat
        # command_disable_thermostat = do_web_socket_bool_query(websocket_transport, command_disable_thermostat)
        # print(command_disable_thermostat)

        # 查詢 thermostat 狀態
        # command_query_thermostat_status = do_web_socket_string_query(websocket_transport, command_query_thermostat_status)
        # print(command_query_thermostat_status)

        # 保存 thermostat 設定參數
        # command_save_thermostat_config = do_web_socket_bool_query(websocket_transport, command_save_thermostat_config)
        # print(command_save_thermostat_config)

        # 查詢 booster 外部設備
        command_query_external_devices = do_web_socket_string_query(websocket_transport, command_query_external_devices)
        print(command_query_external_devices)


    except Exception as e:
        print("錯誤: " + str(e))

    websocket_transport.close()
    print("測量結束")
