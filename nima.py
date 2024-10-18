#!/usr/bin/env python3

# Following modules must be installed:
# py -m pip install websocket-client

import json
from time import sleep
from websocket import WebSocket
from websocket import create_connection
from typing import Dict
import urllib.request
# import GUI

IP_ADDRESS = "192.168.20.99"

command_system_ready = {
    "Command": "QUERY_SYSTEM_INTEGRITY"
}

command_query_api_version = {
    "Command": "GET_API_VERSION"
}

command_enable_thermostat = {
    "Command": "ENABLE_THERMOSTAT",
    "Alias": "/THERMOSTAT/0"
}



command_save_config = {
    
    "Resources": {
        "CurrentSourceParams": [
            {
                "Alias": "/T3STER/0/MS401/SLOT5/CH0",
                "UserAlias": "S5CH1",
                "OutputMode": {
                    "default": "ON",
                    "locked": False
                },
                "SetCurrent": {
                    "default": 0.005,
                    "locked": False,
                    "min": -0.2,
                    "max": 0.2
                },
                "VoltageCorner": {
                    "default": 10.0,
                    "locked": False,
                    "min": -40,
                    "max": 40
                }
            },
            {
                "Alias": "/T3STER/0/LP220/SLOT1/CH0",
                "UserAlias": "S1CH1",
                # "Delay" is optional
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
                "OutputMode": {
                    "default": "PC",
                    "locked": False
                },
                "SetCurrent": {
                    "default": 1,
                    "locked": False,
                    "min": -2,
                    "max": 2
                },
                "VoltageCorner": {
                    "default": 10,
                    "locked": False,
                    "min": -10,
                    "max": 10
                }
            }
        ],
        # "CurrentSourceWithActiveloadParams": [

        # ],
        # "DividerParams": [

        # ],
        # "VoltageSourceParams": [

        # ],
        



        # "ThermometerCardChParams": [
        #     {
        #         "Alias": Unique_system_selected_alias,
        #         "UserAlias": User_defined_alias,
        #         "Sensitivity": {
        #             "default": [ List_of_coefficients_in_volt_per_degrees ],
        #             "locked": False,
        #         },
        #         "PowerStep": PowerStep,
        #         "RangeIdx": {
        #             "default": id,
        #             "locked": False
        #         },
        #         "SamplePerSecIdx": {
        #             "default": id,
        #             "locked": False
        #         }
        #     }
        # ],
        # THERMOSTAT_CONFIG
        # "ThermostatParams": [
        #     {
        #     "Alias": "/THERMOSTAT/0",
        #     "UserAlias": "Th0",
        #     "SetTemperature": {
        #     "default": 30,
        #     "locked": False,
        #     "max": 50,
        #     "min": 0
        #     },
        #     "StabilityCriteria": {
        #     "DtMinMax": {
        #     "default": 0.1,
        #     "locked": False,
        #     "max": 10,
        #     "min": 0
        #     },
        #     "DtTarget": {
        #         "default": 0.25,
        #         "locked": False,
        #         "max": 10,
        #         "min": 0
        #     },
        #     "TimeWindow": {
        #         "default": 60,
        #         "locked": False,
        #         "max": 100,
        #         "min": 0
        #     },
        #     "Timeout": {
        #         "default": 1800,
        #         "locked": False,
        #         "max": 2000,
        #         "min": 0
        #     }
        #     },
        #     "WaitForStabilityBeforeMeas": {
        #     "default": True,
        #     "locked": False
        #     }
        # }
        # ],
        "TriggerOutputParams": [

        ]
    },
    "TimingParams": {
        "TransientMode": {
            "locked": False,
            "default": "Cooling"
        },
        "HeatingTime": {
            "default": 10,
            "locked": False,
            "min": 0,
            "max": 4000
        },
        "CoolingTime": {
            "default": 10,
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
            "max": 100
        }
    },
    # TSP is Optional
    # "TspCalibParams": {
    #     "CustomTemperature": {
    #         "default": 25,
    #         "locked": False,
    #         "max": 160,
    #         "min": -45
    #     },
    #     "DutStability": {
    #         "default": False,
    #         "locked": False,
    #     },
    #     "EndAction": {
    #         "default": "CustomTemp",
    #         "locked": False,
    #     },
    #     "Mode": {
    #         "default": "Upwards",
    #         "locked": False,
    #     },
    #     "ThtIntSensor": {
    #         "default": True,
    #         "locked": False,
    #     },
    #     "Tmax": {
    #         "default": 85,
    #         "locked": False,
    #         "max": 160,
    #         "min": -45
    #     },
    #     "Tmin": {
    #         "default": 25,
    #         "locked": False,
    #         "max": 160,
    #         "min": -45
    #     },
    #     "Tstep": {
    #         "default": 15,
    #         "locked": False,
    #         "max": 205, 
    #         "min": 1
    #     }
        # },
    # SourceTimingControl is Optional
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
    # It is recommended to maintain websocket connection (and not use this optional parameter)
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


        # # ---- Enable Thermostat
        # if do_web_socket_bool_query(websocket_transport, command_enable_thermostat):
        #     print("thermostat is ready")
        # else:
        #     raise Exception("Cannot Enable Thermostat")





        # ---- Save config
        if not do_web_socket_bool_query(websocket_transport, command_save_config):
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
        print(file_list)
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