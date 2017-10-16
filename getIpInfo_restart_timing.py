import subprocess
import time

if __name__ == '__main__':
    path = r"C:\lgl\my_project\getIpInfo.py"
    # path = r"C:\lgl\my_project\test_getIP.py"
    time_inter = 3600
    while True:
        time.sleep(3)
        popen = subprocess.Popen("python " + path, shell=True)
        pid = popen.pid
        time.sleep(time_inter)
        popen.terminate()
