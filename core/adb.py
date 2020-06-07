"""ADB"""
import os

class adbKit(object):
    def screenshots(self):
        os.system('adb shell screencap -p /sdcard/screencap.png')
        os.system('adb pull /sdcard/screencap.png')
    def click(self, pointx, pointy):
        Px = str(pointx)
        Py = str(pointy)
        print('adb shell input tap '+ Px +' '+ Py)
        return os.system('adb shell input tap '+ Px +' '+ Py)
