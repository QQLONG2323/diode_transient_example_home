import json
from time import sleep
from websocket import WebSocket
import urllib.request

IP_ADDRESS = "192.168.20.99"

command_system_ready = {"Command": "QUERY_SYSTEM_INTEGRITY"}
command_query_api_version = {"Command": "GET_API_VERSION"}
command_reboot={"Command": "REBOOT"}
Command_STOP = {
 "Command": "STOP_TASK",
 "TaskAlias": "diode_config_transient"}
Command_Remove = {
 "Command": "REMOVE_TASK",
 "TaskAlias": "diode_config_transient"
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

        Command_STOP =  do_web_socket_string_query(websocket_transport, Command_STOP)
        print(Command_STOP)

        Command_Remove =  do_web_socket_string_query(websocket_transport, Command_Remove)
        print(Command_Remove)
        
        # Command_Reboot =  do_web_socket_string_query(websocket_transport, command_reboot)
        # print(command_reboot)


    except Exception as e:
        print("錯誤: " + str(e))

    websocket_transport.close()
    print("測量結束")
