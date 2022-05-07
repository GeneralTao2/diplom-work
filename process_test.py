import multiprocessing
import time
import os
import signal
import subprocess

def func(str):
    time.sleep(2)
    print(str)

def kill_pr(pr_pid):
    time.sleep(3)
    print("Thread had stopped!")
    subprocess.check_output("Taskkill /PID %d /F" % pr_pid)
    #if pr.is_alive():
    #    pr.terminate()

if __name__ == '__main__':
    pr = multiprocessing.Process(target=func, args=("me!",))
    pr.start()
    print(pr.pid)
    killer = multiprocessing.Process(target=kill_pr, args=(pr.pid,))
    killer.start()