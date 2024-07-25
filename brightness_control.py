'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-07-25 21:03:22
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2024-07-25 22:19:56
FilePath: \code\Mypython\brightness-control\brightness_control.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pyautogui
from screeninfo import get_monitors
import time
import wmi

def get_screens():
    """
    获取所有屏幕的信息
    :return: 一个包含所有屏幕信息的列表
    """
    return get_monitors()

def get_mouse_position():
    """
    获取当前鼠标的位置
    :return: 一个包含鼠标X和Y坐标的元组
    """
    return pyautogui.position()

def get_screen_with_mouse(screens, mouse_position):
    """
    根据鼠标位置判断在哪个屏幕上
    :param screens: 所有屏幕的信息
    :param mouse_position: 当前鼠标的位置
    :return: 鼠标所在的屏幕对象，如果不在任何屏幕上则返回None
    """
    for screen in screens:
        if screen.x <= mouse_position[0] < screen.x + screen.width:
            return screen
    return None

def set_notebook_brightness(brightness):
    """
    设置笔记本屏幕的亮度
    :param brightness: 亮度值 (0-100)
    """
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()
    for method in methods:
        method.WmiSetBrightness(Brightness=brightness, Timeout=0)
    print(f"Notebook brightness set to {brightness}")

def smooth_set_brightness(current_brightness, target_brightness):
    """
    平滑地调整亮度
    :param current_brightness: 当前亮度值
    :param target_brightness: 目标亮度值
    """
    step = 10 if target_brightness > current_brightness else -10
    for brightness in range(current_brightness, target_brightness + step, step):
        set_notebook_brightness(brightness)
        time.sleep(0.1)  # 调整每一步的间隔时间以控制变化速度

def main():
    """
    主函数，定期检测鼠标位置并调整笔记本屏幕亮度
    """
    screens = get_screens()  # 获取所有屏幕信息
    last_position = None  # 记录上一次鼠标位置
    current_brightness = 0  # 初始亮度为0
    while True:
        mouse_position = get_mouse_position()  # 获取当前鼠标位置
        
        if mouse_position != last_position:
            last_position = mouse_position
            screen_with_mouse = get_screen_with_mouse(screens, mouse_position)
            
            if screen_with_mouse:
                print(f"Mouse is on screen: {screen_with_mouse}")
                if screen_with_mouse.width_mm == 344:  # 判断是否为笔记本屏幕的宽
                    target_brightness = 70  # 设置目标亮度为75
                else:
                    target_brightness = 0  # 设置目标亮度为0
                
                if target_brightness != current_brightness:
                    smooth_set_brightness(current_brightness, target_brightness)
                    current_brightness = target_brightness  # 更新当前亮度值
            else:
                print("Mouse is not on any known screen.")
        
        time.sleep(1)  # 每5秒检测一次

if __name__ == "__main__":
    main()
