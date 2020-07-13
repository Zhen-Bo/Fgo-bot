import time
import random
from core import util
from configparser import ConfigParser


class auto():
    def __init__(self, ckp: str, spt: str, apl: (int, str) = (0, ""), timer=12000):
        self.checkpoint = ckp
        self.support = spt
        self.counts = int(apl[0])  # apple counts
        self.apple = apl[1]
        self.timer = int(timer)
        self.cfg = ConfigParser()
        self.cfg.read("core/ini/button.ini")

    def cfg_list(self, sec, value):
        tmp_list = self.cfg[sec][value]
        tmp_list = tmp_list.split(',')
        return tmp_list

    def quick_start(self, advance=True):
        self.select_task(self.checkpoint)
        self.support_select(self.support)
        self.start_battle()

    def select_task(self, ckp: str):
        while not util.get_pos(self.checkpoint):
            print("waiting task select")
        cpk_ptr = [1100, 170]
        util.list_tap(cpk_ptr)
        time.sleep(0.2)
        flag = util.get_pos("images/noap.png")
        if flag:
            print("NO AP!")
            print("remain apple counts:", self.counts)
            if self.counts > 0:
                self.eat_apple()
            elif self.counts == -1:
                cls_ptr = [635, 610]
                util.list_tap(cls_ptr)
                self.wait_ap(self.timer)
                self.select_task(self.checkpoint)
            else:
                raise Exception("Out of AP!")
        print("[INFO] task selected.")

    def eat_apple(self):
        print("prepare to eat")
        if self.apple == 'au':
            print("eat au apple")
            au = self.cfg_list('apple', 'au')
            util.list_tap(au)
        elif self.apple == 'ag':
            print("eat ag apple")
            ag = self.cfg_list('apple', 'ag')
            util.list_tap(ag)
        elif self.apple == 'sq':
            print("eat sq apple")
            sq = self.cfg_list('apple', 'sq')
            util.list_tap(sq)
        time.sleep(0.2)
        use = self.cfg_list('apple', 'use')
        util.list_tap(use)
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
                if not i == 0 and not i % 15:
                    print("waiting ap recover")
                time.sleep(1)

    def update_support(self) -> bool:
        if util.get_pos("images/update.png"):
            util.tap(835, 125)
            time.sleep(0.5)
            flag = util.standby("images/close.png")
            if flag == False:
                util.tap(640, 560)
                print("wait to refresh")
                time.sleep(2)
            else:
                util.tap(840, 560)
                print("support_list_updata")
            time.sleep(0.5)
            return True

    def support_select(self, spt: str = None):  # tag 選擇助戰
        if spt is None:
            spt = self.support
        flag1 = True
        flag2 = True
        while flag1:
            spt_pos, spt_h, spt_w = util.standby(spt)
            if spt_pos == False:
                print("Friend not found")
                if flag2:
                    bar_pos = util.standby("images/bar.png")
                    bar_pos = bar_pos[:1]
                    if bar_pos == False:
                        print("no bar")
                        self.update_support()
                    else:
                        print("have bar")
                        flag2 = False
                        end_pos = util.standby("images/friendEnd.png")
                        end_pos = end_pos[:1]
                        if end_pos == False:
                            print("friend_list_reach_end")
                            self.update_support()
                            flag2 = True
                        else:
                            gap_pos, gap_h, gap_w = util.standby(
                                "images/friend_gap.png", 0.8, True)
                            util.swipe((int(gap_pos[0]+(gap_w/2)),
                                        int(gap_pos[1]+(gap_h/2))), (int(gap_pos[0]+(gap_w/2)), 210), 1.5)
                else:
                    end_pos = util.standby("images/friendEnd.png")
                    end_pos = end_pos[:1]
                    if end_pos[0] != False:
                        print("friend_list_reach_end")
                        self.update_support()
                        flag2 = True
                    else:
                        print("swipe down")
                        gap_pos, gap_h, gap_w = util.standby(
                            "images/friend_gap.png", 0.8, True)
                        util.swipe((int(gap_pos[0]+(gap_w/2)),
                                    int(gap_pos[1]+(gap_h/2))), (int(gap_pos[0]+(gap_w/2)), 210), 1.5)
            else:
                flag1 = False
                spt_center = [int(spt_pos[0]+(spt_w/2)),
                              int(spt_pos[1]+(spt_h/2))]
                util.list_tap(spt_center)

    """
    def advance_support(self, spt: str = None, tms: int = 3):  # nouse 舊版選助戰
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
                self.update_support()
            else:
                if not util.standby("images/bar.png"):
                    util.swipe((1235, p0), (1235, p1), 1)
                    print("swipe ", p0, p1)
                    p0 = p1
                    p1 += 55
                else:
                    print("no bar")
                    self.update_support()
            time.sleep(0.2)
        util.adbtap(util.get_pos(spt))
    """

    def start_battle(self):
        while not util.get_pos("images/start.png"):
            time.sleep(0.2)
            cpk = [1180, 670]
        util.list_tap(cpk)
        print("[INFO] Battle started.")

    def select_servant_skill(self, skill: int, tar: int = 0):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        pos = self.cfg_list('skills', '%s' % skill)
        util.list_tap(pos)
        print("use servent", str(int((skill-1)/3 + 1)),
              "skill", str((skill-1) % 3 + 1))
        time.sleep(0.5)
        if tar != 0:
            self.select_servant(tar)
            print("to servent", tar)
        time.sleep(0.5)

    def select_servant(self, servant: int):
        pos = self.cfg_list('servent', '%s' % servant)
        util.list_tap(pos)

    def select_cards(self, cards: [int]):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.2)
        # tap ATTACK
        pos = self.cfg_list('attack', 'button')
        util.list_tap(pos)
        while len(cards) < 3:
            x = random.randrange(1, 6)
            if x in cards:
                continue
            cards.append(x)
        # tap CARDS
        time.sleep(0.8)
        for card in cards:
            pos = self.cfg_list('attack', '%s' % card)
            util.list_tap(pos)
            time.sleep(0.1)
        print("[INFO] Selected cards: ", cards)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        while not util.get_pos("images/attack.png"):
            print("Waiting for Attack button")
            time.sleep(0.5)
        self.toggle_master_skill()
        pos = self.cfg_list('master', '%s' % skill)
        util.list_tap(pos)
        print("use master skill", skill)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    def toggle_master_skill(self):
        pos = self.cfg_list('master', 'button')
        util.list_tap(pos)
        print("toggle master skills")

    def change_servant(self, org: int, tar: int):
        time.sleep(0.2)
        pos = self.cfg_list('servent', 's%s' % org)
        util.list_tap(pos)
        time.sleep(0.1)
        pos = self.cfg_list('servent', 'a%s' % tar)
        util.list_tap(pos)
        time.sleep(0.1)
        ckp = [650, 620]
        util.list_tap(ckp)  # confirm btn

    def finish_battle(self):
        while not util.get_pos("images/next.png"):
            print("Waiting next button")
            util.tap(920, 45)
            self.needattack()
            time.sleep(0.2)
        util.tap(1105, 670)
        flag = 0
        while not util.get_pos(self.checkpoint):
            if flag == 0 and util.get_pos("images/friendrequest.png"):
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
            while not util.get_pos("images/phase1.png", 0.78):
                util.tap(920, 45)
                print("Waiting for phase1")
                time.sleep(0.5)
        elif phase == 2:
            while not util.get_pos("images/phase2.png", 0.78):
                util.tap(920, 45)
                print("Waiting for phase2")
                self.needattack()
                time.sleep(0.5)
        elif phase == 3:
            while not util.get_pos("images/phase3.png", 0.78):
                util.tap(920, 45)
                print("Waiting for phase3")
                self.needattack()
                time.sleep(0.5)

    def needattack(self):
        if util.get_pos("images/attack.png"):
            print("need attack")
            self.select_cards([1, 2, 3])
        else:
            print("dont need attack")

    def debug(self):  # debug用
        sq = self.cfg_list('apple', 'sq')
        print(sq)
        print(sq[0], sq[1])
