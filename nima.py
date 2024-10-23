{
    'Command': 'SAVE_CONFIG', 
    'Type': 'TransientModel', 
    'ConfigName': 'diode_config', 
    'ConfigParams': {
        'Description': 'Test'
    }, 
    'Resources': {
        'CurrentSourceParams': [
            {
                'Alias': '/T3STER/0/LP220/SLOT1/CH0', 
                'UserAlias': 'S1Ch1', 
                'Delay': {
                    'DelayFallingUs': {
                        'default': 0, 
                        'locked': False, 
                        'min': -16383, 
                        'max': 5000
                    }, 
                    'DelayRisingUs': {
                        'default': 0, 
                        'locked': False, 
                        'min': -16383, 
                        'max': 16383
                    }
                }, 
                'OutputMode': {
                    'default': 'PC', 
                    'locked': False
                }, 
                'SetCurrent': {
                    'default': 2.0, 
                    'locked': False, 
                    'min': -2, 
                    'max': 2
                }, 
                'VoltageCorner': {
                    'default': 10.0, 
                    'locked': False, 
                    'min': -10, 
                    'max': 10
                }
            }, 
            {
                'Alias': '/T3STER/0/MS401/SLOT5/CH0', 
                'UserAlias': 'S5Ch1', 
                'OutputMode': {
                    'default': 'ON', 
                    'locked': False
                }, 
                'SetCurrent': {
                    'default': 0.02, 
                    'locked': False, 
                    'min': -0.2, 
                    'max': 0.2
                }, 
                'VoltageCorner': {
                    'default': 10.0, 
                    'locked': False, 
                    'min': -40, 
                    'max': 40
                }
            }
        ], 
        'MeasCardChParams': [
            {
                'Alias': '/T3STER/0/MS401/SLOT5/CH0', 
                'UserAlias': 'S5Ch1', 
                'Sensitivity': {
                    'default': [
                        0.002
                    ], 
                    'locked': False
                }, 
                'PowerStep': '@POWERSTEP_DIODE;/T3STER/0/MS401/SLOT5/CH0;/T3STER/0/LP220/SLOT1/CH0', 
                'RangeIdx': {
                    'default': 9, 
                    'locked': False
                }, 
                'AutoRange': {
                    'default': False, 
                    'locked': False
                }, 
                'Uref': {
                    'default': 0.0, 
                    'locked': False
                }, 
                'UrefSwitching': {
                    'default': False, 
                    'locked': False
                }, 
                'UrefHeating': {
                    'default': 0.0, 
                    'locked': False
                }
            }
        ], 
        'ThermostatParams': [

        ], 
        'TriggerOutputParams': [

        ]
    }, 
    'TimingParams': {
        'HeatingTime': {
            'default': 0.0, 
            'locked': False, 
            'min': 0, 
            'max': 4000
        }, 
        'CoolingTime': {
            'default': 0.0, 
            'locked': False, 
            'min': 0, 
            'max': 4000
        }, 
        'DelayTime': {
        'default': 0.0, 
        'locked': False, 
        'min': 0, 
        'max': 4000
        }, 
        'Repeat': {
            'default': 1, 
            'locked': False, 
            'min': 1, 
            'max': 100
        }, 
        'TransientMode': {
            'locked': False, 
            'default': 'Cooling'
        }, 
        'SamplePerOctave': {
            'default': 1000, 
            'locked': False, 
            'min': 1000, 
            'max': 1000
        }
    }, 
    'TspCalibParams': [

    ], 
    'SourceTimingControl': {
        'locked': False, 
        'Enabled': False, 
        'ReversePowerOff': True, 
        'WaitForInstrumentDelay': True, 
        'PowerOn': [

        ], 
        'PowerOff': [

        ]
    }
}