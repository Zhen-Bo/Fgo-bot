"""ADB"""
import os

class adbKit(object):
    def screenshots(self, serialNumber=None):
        os.system('adb shell screencap -p /sdcard/screencap.png')
        os.system('adb pull /sdcard/screencap.png')
    def click(self, pointx, pointy, serialNumber=None):
        Px = pointx
        Py = pointy
        return os.system('adb shell input tap '+str(Px)+' '+str(Py))
    def attackClick(self):
        return os.system('adb shell input tap 1120 600')
