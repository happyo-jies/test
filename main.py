import pyautogui
import time
import os

# --- 安全设置 ---
pyautogui.PAUSE = 0.5  # 每次操作后暂停1秒
pyautogui.FAILSAFE = True # 启用紧急终止功能（鼠标移到左上角可中止）
_wait = 0.2
_confidence=0.8

# 1. 获取当前脚本所在的目录
current_dir = 'D:\Python Project\DingTalk Timesheet Automation\.venv'

# 2. 拼接图片路径
# 这样写无论你在 Windows 还是 Mac 上都能跑
def mouse_moveclick(stepname,wait=_wait,confidence=_confidence):
    print(stepname+"开始运行")
    image_path = os.path.join(current_dir, 'assets', 'images', stepname+'.png')
    rtb = False
    print(image_path)
    try:
        save_button_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        
        if save_button_location:
            # 点击图片的中心点
            # pyautogui.center() 可以根据区域坐标计算出中心点的 (x, y)
            x, y = pyautogui.center(save_button_location)
            pyautogui.click(x, y)
            print(f"找到“{stepname}”按钮[{x},{y}]，正在点击..." )
            rtb = True
        else:
            print("未找到“"+stepname+"”按钮！")
    except pyautogui.ImageNotFoundException:
        print("捕获到异常：屏幕上没有找到指定的图片。")
    time.sleep(wait) # 等待
    return rtb

def mouse_movedrag(stepname,wait=_wait,confidence=_confidence):
    print(stepname+"开始运行")
    image_path = os.path.join(current_dir, 'assets', 'images', stepname+'.png')
    rtb =False
    #print(image_path)
    try:
        save_button_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        
        if save_button_location:
            x, y = pyautogui.center(save_button_location)
            print(f"找到“{stepname}”按钮[{x},{y}]，正在拖拽..." )
            pyautogui.moveTo(x, y)
            pyautogui.dragTo(x+300, y ,0.5)
            rtb = True
        else:
            print("未找到“"+stepname+"”按钮！")
    except pyautogui.ImageNotFoundException:
        print("捕获到异常：屏幕上没有找到指定的图片。")
    time.sleep(wait) # 等待
    return rtb

def mouse_moveOffsetclick(stepname,xoffset=0,yoffset=0,wait=_wait,confidence=_confidence):
    print(stepname+"开始运行")
    image_path = os.path.join(current_dir,'assets','images', stepname+'.png')
    rtb = False
    #print(image_path)
    try:
        save_button_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        
        if save_button_location:
            # 点击图片的中心点
            # pyautogui.center() 可以根据区域坐标计算出中心点的 (x, y)
            x, y=pyautogui.center(save_button_location)
            print(f"找到“{stepname}”按钮[{x},{y}]，正在点击..." )
            pyautogui.click(x+xoffset, y+yoffset)
            rtb = True
        else:
            print("未找到“"+stepname+"”按钮！")
    except pyautogui.ImageNotFoundException:
        print("捕获到异常：屏幕上没有找到指定的图片。")
    time.sleep(wait) # 等待
    return rtb

def keyboard_input(text,wait=_wait):
    print(text+"开始运行")
    rtb = False
    #print(image_path)
    try:
        # pyautogui.write('文本', interval=间隔) # 模拟打字。
        # pyautogui.press('键名') # 按下并释放一个键，如 'enter', 'tab', 'f1'。
        # pyautogui.hotkey('ctrl', 'c') # 模拟组合快捷键，如 Ctrl+C（复制）。
        pyautogui.press('8')
        print("模拟输入"+text+"成功！" )
        rtb = True
    except Exception as e:
        print(f"发生异常: {e}")
    time.sleep(wait) # 等待
    return rtb

def LoopDo(step_func, *args, **kwargs):
    """
    step_func: 传入的函数 (例如 mouse_moveclick)
    """
    wait = kwargs.pop('wait', 1)
    timeout = kwargs.pop('timeout', 10)
    start_time = time.time()  # 记录开始时间
    print(">>> 开始循环检测...")
    while True:
        if step_func(*args, **kwargs):
            break
        if timeout is not None:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                print(f">>> 警告：已超过最大等待时间 ({timeout}秒)，强制退出循环。")
                break
        time.sleep(wait)


# 运行自动化脚本
if __name__ == "__main__":
    try:
        LoopDo(mouse_moveclick,'dingtalk mini',timeout=2)
        # mouse_moveclick("测试")
        mouse_moveclick("Workbench")
        mouse_moveclick("Finalize Timesheet")
        mouse_moveclick("Refresh",wait=0.5)
        LoopDo(mouse_moveclick,"Quick Fill")
        LoopDo(mouse_movedrag,"Scrollbar",timeout=2)
        # mouse_moveOffsetclick("working time",0,30)
        count = 0
        while count < 7:
            if mouse_moveOffsetclick("Need Fill",0,70,0.1,0.95):
                 keyboard_input('8')
            else:
                break
            mouse_moveOffsetclick("Need Fill",0,140,0.1,0.95)
            # if mouse_moveclick("input",0.1,0.8):
            #     keyboard_input('8')
            count+=1
        mouse_moveclick("commit")
        mouse_moveclick("exit")
        mouse_moveclick("message")
    except pyautogui.FailSafeException:
        print("脚本因触发紧急终止而中止。")