import time
from core import decoder
from core.auto import auto

if __name__ == '__main__':
    while True:
        print('請輸入設定檔名稱(不需輸入.py):')
        config = input()
        exec("from config import %s"%config)
        setting = []
        exec("setting.append(%s.run_time)"%config)
        exec("setting.append(%s.support)"%config)
        exec("setting.append(%s.ap_recover)"%config)
        exec("setting.append(%s.recover_time)"%config)
        exec("setting.append(%s.default_skill)"%config)
        exec("setting.append(%s.default_card)"%config)

        round = auto("images/menu.png", setting[1], setting[2], setting[3] * 60)
        tstart = time.time()
        for i in range(setting[0]):
            print("Round:", i+1)
            instr = decoder.decode(setting[4], setting[5])
            for i in range(len(instr)):
                exec(instr[i])
        tend = time.time()
        print("執行 %s 次;耗時 %d 秒"%(setting[0], int(tend - tstart)))
