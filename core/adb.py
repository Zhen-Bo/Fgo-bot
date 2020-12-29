"""ADB"""
import os


class adbKit(object):
    def screenshots(self):
        os.system('/adb/adb.exe shell screencap -p /sdcard/screencap.png')
        os.system('/adb/adb.exe pull /sdcard/screencap.png > $null')

    def click(self, pointx, pointy):
        Px = str(pointx)
        Py = str(pointy)
        print('adb shell input tap ' + Px + ' ' + Py)
        return os.system('/adb/adb.exe shell input tap ' + Px + ' ' + Py)

    def swipe(self, x1, y1, x2, y2, delay):
        cmdSwipe = '/adb/adb.exe shell input swipe {0} {1} {2} {3} {4}'.format(
            int(x1), int(y1), int(x2), int(y2), int(delay*1000))
        print(cmdSwipe)
        os.system(cmdSwipe)
