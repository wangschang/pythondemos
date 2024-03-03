import threading
import time

# 定义要执行的函数
def task(arg):
    # 模拟耗时操作
    print(f"任务 {arg} 开始")
    time.sleep(1)
    print(f"任务 {arg} 已完成")

# 创建线程并执行
for i in range(5):
    thread = threading.Thread(target=task, args=(i,))
    thread.start()

# 主线程等待所有子线程完成
for thread in threading.enumerate():
    if thread is not threading.current_thread():
        thread.join()

print("所有任务已完成")
