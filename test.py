from configparser import ConfigParser

cfg_name = input()
cfg = ConfigParser()
ini_path = "config/" + cfg_name + ".ini"
cfg.read(ini_path)

battle1_str = cfg['default_skill']['battle1']
print(battle1_str)
