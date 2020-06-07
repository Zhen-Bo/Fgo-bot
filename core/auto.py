import time
import random
from core import util
from configparser import ConfigParser

class auto():
    def __init__(self, ckp: str, spt: str, apl: (int, str) = (0, ""), timer = 12000):
        self.checkpoint = ckp
        self.support = spt
        self.counts = int(apl[0])  # apple counts
        self.apple = apl[1]
        self.timer = int(timer)
        self.cfg = ConfigParser()
        self.cfg.read('config/core/button.ini')

    def debug(self):
        util.tap(920, 45)
        print("debug")

    def quick_start(self, advance=True):
        self.select_task(self.checkpoint)
        self.advance_support()
        self.start_battle()

    def select_task(self, ckp: str):
        while not util.get_pos(self.checkpoint):
            print("waiting task select")
            time.sleep(0.2)
        util.tap(1100, 170)
        time.sleep(1)
        if util.get_pos("images/noap.png"):
            print("remain apple counts:", self.counts)
            if self.counts > 0:
                print("NO AP!")
                self.eat_apple()
            elif self.counts == -1:
                util.tap(635, 610)
                self.wait_ap(self.timer)
                self.select_task(self.checkpoint)
            else:
                raise Exception("Out of AP!")
        print("[INFO] task selected.")

    def eat_apple(self):
        print("eat apple")
        if self.apple == 'au':
            print("au apple")
            util.tap(375, 320)
        elif self.apple == 'ag':
            print("ag apple")
            util.tap(375, 470)
        elif self.apple == 'sq':
            print("sq apple")
            util.tap(375, 170)
        time.sleep(0.2)
        util.tap(830, 560)
        self.counts -= 1
        print("apple_count:", self.counts)

    def wait_ap(self, timer):
        tStart = time.time()
        tEnd = time.time()
        print("start to wait ap")
        while not int(tEnd - tStart) >= timer:
            remain = timer - int(tEnd - tStart)
            remain /= 60.0
            remain = round(remain, 1)
            print("remain", remain, "minutes")
            for i in range(30):
                tEnd = time.time()
                if int(tEnd - tStart) >= timer:
                    break
                if not i == 0 and not i%15:
                    print("waiting ap recover")
                time.sleep(1)

    def update_support(self) -> bool:
        if util.get_pos("images/update.png"):
            util.tap(835, 125)
            time.sleep(0.5)
            if util.standby("images/close.png"):
                util.tap(640, 560)
                print("wait to refresh")
                time.sleep(2)
            else:
                util.tap(840, 560)
                print("support_list_updata")
            time.sleep(0.5)
            return True

    def advance_support(self, spt: str = None, tms: int = 3):
        time.sleep(0.3)
        if spt is None:
            spt = self.support
        p0 = 220
        p1 = 280
        #times = 9
        while not util.standby(spt):
            print("Friend not found")
            if util.standby("images/friendEnd.png"):
                print("friend_list_reach_end")
                p0 = 220
                p1 = 280
                update = self.update_support()
            else:
                if not util.standby("images/bar.png"):
                    util.swipe((1235, p0), (1235, p1), 1)
                    print("swipe ", p0, p1)
                    p0 = p1
                    p1 += 55
                else:
                    print("no bar")
                    update = self.update_support()
            time.sleep(0.2)
        util.adbtap(util.get_pos(spt))

    def start_battle(self):
        while not util.get_pos("images/start.png"):
            time.sleep(0.2)
        util.tap(1180, 670)
        print("[INFO] Battle started.")

    def select_servant_skill(self, skill: int, tar: int = 0):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        pos = self.cfg['skills']['%s'%skill]
        pos = pos.split(',')
        util.tap(pos[0], pos[1])
        print("tap", pos)
        print("use servent", str(int((skill-1)/3 + 1)) , "skill", str((skill-1)%3 + 1))
        time.sleep(0.5)
        if tar != 0:
            self.select_servant(tar)
            print("to servent", tar)

    def select_servant(self, servant: int):
        while not util.get_pos("images/select.png"):
            print("Waiting for servent select")
            time.sleep(0.2)
        pos = self.cfg['servent']['%s'%servant]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.5)

    def select_cards(self, cards: [int]):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        # tap ATTACK
        pos = self.cfg['attack']['button']
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(1)
        while len(cards) < 3:
            x = random.randrange(1, 6)
            if x in cards:
                continue
            cards.append(x)
        # tap CARDS
        for card in cards:
            pos = self.cfg['attack']['%s'%card]
            pos = pos.split(',')
            util.list_tap(pos)
            time.sleep(0.2)
        print("[INFO] Selected cards: ", cards)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        self.toggle_master_skill()
        pos = self.cfg['master']['%s'%skill]
        pos = pos.split(',')
        util.list_tap(pos)
        print("use master skill", skill)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    def toggle_master_skill(self):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        pos = self.cfg['master']['button']
        pos = pos.split(',')
        util.list_tap(pos)
        print("toggle master skills")

    def change_servant(self, org: int, tar: int):
        while not util.get_pos("images/order_change.png"):
            print("Waiting for order change")
            time.sleep(0.2)
        pos = self.cfg['servent']['s%s',org]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.1)
        pos = self.cfg['servent']['a%s',tar]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.1)
        util.tap(650, 620)  # confirm btn

    def finish_battle(self):
        while not util.get_pos("images/next.png"):
            print("Waiting next button")
            util.tap(920, 45)
            self.needattack()
            time.sleep(0.2)
        util.tap(1105, 670)
        flag = 0
        while not util.get_pos(self.checkpoint):
            if flag ==0 and util.get_pos("images/friendrequest.png"):
                print("check friend request screen")
                util.tap(330, 610)
                print("reject friend request")
                flag = 1
            elif flag == 1:
                util.tap(920, 45)
            else:
                util.tap(920, 45)
            time.sleep(1)
        print("[INFO] Battle Finished.")


    def waiting_phase(self, phase: int):
        if phase == 1:
            while not util.get_pos("images/phase1.png", 0.8):
                util.tap(920, 45)
                print("Waiting for phase1")
                time.sleep(0.2)
        elif phase == 2:
            while not util.get_pos("images/phase2.png", 0.8):
                util.tap(920, 45)
                print("Waiting for phase2")
                self.needattack()
                time.sleep(0.2)
        elif phase == 3:
            while not util.get_pos("images/phase3.png", 0.8):
                util.tap(920, 45)
                print("Waiting for phase3")
                self.needattack()
                time.sleep(0.2)

    def needattack(self):
        if util.get_pos("images/attack.png"):
            print("need attack")
            self.select_cards([1, 2, 3])
        else:
            print("dont need attack")
