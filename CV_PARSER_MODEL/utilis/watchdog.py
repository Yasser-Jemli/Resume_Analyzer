#!/usr/bin/python3


# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : watchdog.py
# @Software: Vscode
# @Description: This module provides a watchdog timer to monitor the execution of a function.
# @License : MIT License

import multiprocessing
import threading

class Watchdog:
    def __init__(self, target, args=(), timeout=10):
        self.target = target
        self.args = args
        self.timeout = timeout
        self.result_queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=self.wrapper)

    def wrapper(self):
        try:
            result = self.target(*self.args)
            self.result_queue.put(result)
        except Exception as e:
            self.result_queue.put(e)

    def start(self):
        self.process.start()
        timer = threading.Timer(self.timeout, self.terminate)
        timer.start()
        self.process.join()
        timer.cancel()

        if not self.result_queue.empty():
            result = self.result_queue.get()
            if isinstance(result, Exception):
                return f"[ERROR] Exception occurred: {result}"
            return f"[SUCCESS] Result: {result}"
        else:
            return "[ERROR] No result returned. Possibly terminated by timeout."

    def terminate(self):
        if self.process.is_alive():
            self.process.terminate()
            print(f"[WATCHDOG] Process timed out after {self.timeout} seconds.")
