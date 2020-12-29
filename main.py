from configparser import ConfigParser
import time
from core import decoder
from core.auto import auto

if __name__ == '__main__':
    while True:
        print('請輸入設定檔名稱(不需輸入.ini):')

        cfg_name = input()
        cfg = ConfigParser()
        ini_path = "UserData/config/" + cfg_name + ".ini"
        cfg.read(ini_path)

        run_times = cfg['run_times']['times']
        support = cfg['support']['support']
        apple_count = cfg['ap_recover']['count']
        apple = cfg['ap_recover']['apple']
        recover_time = cfg['recover_time']['recover_time']
        battle1_str = cfg['default_skill']['battle1']
        battle2_str = cfg['default_skill']['battle2']
        battle3_str = cfg['default_skill']['battle3']
        crd1_str = cfg['default_card']['battle1']
        crd2_str = cfg['default_card']['battle2']
        crd3_str = cfg['default_card']['battle3']
        images_path = cfg['path']['image_path']

        codelist = [battle1_str, battle2_str,
                    battle3_str, crd1_str, crd2_str, crd3_str]

        ckp = images_path + "/menu.png"
        round = auto(ckp, support, (int(apple_count), apple),
                     int(recover_time) * 60)
        tstart = time.time()
        counter = 0
        for i in range(int(run_times)):
            print("Round:", i+1)
            instr = decoder.decode(codelist)
            for i in range(len(instr)):
                exec(instr[i])
            tend = time.time()
            counter += 1
            print("執行 %s 次;耗時 %d 秒" % (counter, int(tend - tstart)))
