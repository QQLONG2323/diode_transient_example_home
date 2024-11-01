import pandas as pd
from datetime import datetime
import subprocess
import os

def create_pol_file(slope, intercept, output_file, timestamp, third_line):
    """
    使用給定的斜率和截距生成T3Ster .pol文件
    
    Parameters:
    slope (float): 斜率
    intercept (float): 截距
    output_file (str): 輸出文件路徑
    timestamp (str): 時間戳
    third_line (str): 第三行的內容
    """
    # 準備.pol文件內容
    content = f"""# *T3STER-MASTER* POLYNOMIALS
# {timestamp}
{third_line}
# T3Ster SI control SW ;;FD=11;SET_V_OFFSET=0.000000
CHANNELS=1
CHANNEL01=P 2 {intercept} {slope}"""
    
    # 寫入文件
    with open(output_file, 'w') as f:
        f.write(content)

def calculate_slope_intercept(data_points):
    """
    計算數據點的斜率和截距
    
    Parameters:
    data_points (list of tuples): 每個元組包含一個 (x, y) 數據點
    
    Returns:
    tuple: 斜率和截距
    """
    n = len(data_points)
    sum_x = sum(point[0] for point in data_points)
    sum_y = sum(point[1] for point in data_points)
    sum_x_squared = sum(point[0] ** 2 for point in data_points)
    sum_xy = sum(point[0] * point[1] for point in data_points)
    
    # 計算斜率和截距
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

def process_tco_to_pol(tco_file, output_pol_file, third_line):
    """
    讀取TCO文件並生成對應的POL文件
    
    Parameters:
    tco_file (str): 輸入的.tco文件路徑
    output_pol_file (str): 輸出的.pol文件路徑
    third_line (str): 第三行的內容
    """
    # 從TCO文件讀取數據
    with open(tco_file, 'r') as f:
        lines = f.readlines()
    
    # 提取時間戳並轉換格式
    timestamp = lines[1].strip().replace('# ', '')
    print(timestamp)
    timestamp_dt = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
    print(timestamp_dt)
    formatted_timestamp = timestamp_dt.strftime("%m-%d-%Y %H:%M:%S")
    print(formatted_timestamp)
    
    # 提取數據點
    data_points = []
    for line in lines[7:]:
        y, x = map(float, line.split())  # 將X和Y對調
        data_points.append((x, y))
    
    # 計算斜率和截距
    slope, intercept = calculate_slope_intercept(data_points)

    # 創建POL文件
    create_pol_file(slope, intercept, output_pol_file, formatted_timestamp, third_line)
    
    print(f"原始係數:")
    print(f"斜率: {slope}")
    print(f"截距: {intercept}")
    print(f"\nPOL文件已生成: {output_pol_file}")

def read_sensitivity_from_tco(tco_file):
    """
    讀取 TCO 文件中的靈敏度值（第 6 行）
    
    參數:
        tco_file (str): TCO 文件的路徑
    
    返回:
        float:敏度值
    """
    with open(tco_file, 'r') as f:
        # 讀取所有行並獲取第 6 行（索引 5）
        lines = f.readlines()
        sensitivity_line = lines[5].strip()
        print(sensitivity_line)
        # 移除 '#' 如果存在並去除多餘的空白
        sensitivity = float(sensitivity_line.replace('#', '').strip())
        print(sensitivity)
    return sensitivity

def modify_raw_file(input_file, output_file, new_sensitivity):
    """
    讀取 T3Ster 參數文件並創建一個新的文件，修改第八行的數值為新的靈敏度值，並刪除 '#' 後的第一個 '0' 的索引
    
    參數:
        input_file (str): 輸入的 .raw 文件路徑
        output_file (str): 保存修改後的 .raw 文件路徑
        new_sensitivity (float): 新的 CH_SENSIT 參數值
    """
    # 讀取原始文件
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # 修改第八行的數值為新的靈敏度值
    if len(lines) >= 8:
        lines[7] = f'# {new_sensitivity}\n'
    
    # 刪除第十一行
    if len(lines) >= 11:
        del lines[10]
    
    # 將修改後的內容寫入新文件
    with open(output_file, 'w') as f:
        f.writelines(lines)

def modify_parameter_file(input_file, output_file, new_sensitivity):
    """
    讀取 T3Ster 參數文件並創建一個新的文件，修改 CH_SENSIT 值
    
    參數:
        input_file (str): 輸入的 .par 文件路徑
        output_file (str): 保存修改後的 .par 文件路徑
        new_sensitivity (float): 新的 CH_SENSIT 參數值
    """
    # 讀取原始文件
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # 修改 CH_SENSIT 行
    modified_lines = []
    for line in lines:
        if line.startswith('CH_SENSIT='):
            modified_lines.append(f'CH_SENSIT={new_sensitivity}\n')
        else:
            modified_lines.append(line)
    
    # 將修改後的內容寫入新文件
    with open(output_file, 'w') as f:
        f.writelines(modified_lines)

def get_third_line_from_file(file_path):
    """
    讀取文件的第三行
    
    參數:
        file_path (str): 文件路徑
    
    返回:
        str: 第三行的內容
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) >= 3:
            print("讀取任務ID成功")
            return lines[2].strip()
        else:
            raise IndexError("File does not have at least 3 lines")

# 使用示例
# if __name__ == "__main__":
def process_files(tco_file, par_file, raw_file, output_dir):
    # 生成唯一的時間戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # tco_file = "C:\\Users\\jeff.lien\\Desktop\\JEFF\\measurement_TSP_1_tsp_calib_diode_config_transient_T3STER_1_MS401_SLOT5_CH1.tco"
    # par_file = "C:\\Users\\jeff.lien\\Desktop\\JEFF\\measurement_B_1_heating_diode_config_transient_T3STER_1_MS401_SLOT5_CH1.par"
    # raw_file = "C:\\Users\\jeff.lien\\Desktop\\JEFF\\measurement_B_1_heating_diode_config_transient_T3STER_1_MS401_SLOT5_CH1.raw"
    # output_dir = "C:\\Users\\jeff.lien\\Desktop\\JEFF\\output\\"

    # 生成唯一的輸出檔案名稱
    output_pol_file = os.path.join(output_dir, f"modified_measurement_{timestamp}.pol")
    output_par_file = os.path.join(output_dir, f"modified_measurement_{timestamp}.par")
    output_raw_file = os.path.join(output_dir, f"modified_measurement_{timestamp}.raw")

    try:
        # 從 PAR 或 RAW 文件中讀取第三行
        third_line = get_third_line_from_file(par_file)
        
        # 生成POL文件
        process_tco_to_pol(tco_file, output_pol_file, third_line)
        
        # 讀取TCO文件中的靈敏度
        sensitivity = read_sensitivity_from_tco(tco_file)
        print(f"Read sensitivity value: {sensitivity}")
        
        # 修改PAR文件中的靈敏度
        modify_parameter_file(par_file, output_par_file, sensitivity)
        print(f"Successfully created modified PAR file: {output_par_file}")
        
        # 修改RAW文件中的第八行數值和刪除 '#' 後的第一個 '0'
        modify_raw_file(raw_file, output_raw_file, sensitivity)
        print(f"Successfully created modified RAW file: {output_raw_file}")

        # 定义命令和参数
        commands = [
            [
                'T3STERmastercmd.exe',  # 可执行文件
                '-e --transient-correction M(0.001,0.01)',  # 参数标志
                output_par_file  # 使用變數而不是硬編碼路徑
            ],
            [
                'T3STERmastercmd.exe',  # 可执行文件
                '-p',  # 参数标志
                'STF',  # 参数
                output_par_file  # 使用變數而不是硬編碼路徑
            ]
        ]

        # 运行命令并捕获输出
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True)
            
            # 檢查命令執行結果
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Command failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                    
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except IndexError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: Could not convert sensitivity value to float - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")