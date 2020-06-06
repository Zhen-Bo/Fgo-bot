def get_str(default_skill):
    get_str_str = list()
    if '(1)' in default_skill:
        pos1 = default_skill.find('(1)')   # 從字串開頭往後找
    if '(2)' in default_skill:
        pos2 = default_skill.find('(2)')   # 從字串開頭往後找
    if '(3)' in default_skill:
        pos3 = default_skill.find('(3)')   # 從字串開頭往後找
    get_str_str.append(default_skill[pos1+3:pos2])
    get_str_str.append(default_skill[pos2+3:pos3])
    get_str_str.append(default_skill[pos3+3:])
    return get_str_str

def skill_btn(var):
    return {
    'a': int(1),
    'b': int(2),
    'c': int(3),
    'd': int(4),
    'e': int(5),
    'f': int(6),
    'g': int(7),
    'h': int(8),
    'i': int(9),
    }.get(var,'0')  #'error'為預設返回值，可自設定

def crd_btn(var):
    return {
    'a': int(6),
    'b': int(7),
    'c': int(8),
    '1': int(1),
    '2': int(2),
    '3': int(3),
    '4': int(4),
    '5': int(5),
    }.get(var,'0')  #'error'為預設返回值，可自設定

def chk_skill(skill, tar):
    skillbtn = skill_btn(skill)
    if bool(tar == '0'):
        return "round.select_servant_skill(%s)"%skillbtn
    else:
        return "round.select_servant_skill(%s, %s)"%(skillbtn, tar)

def chk_card(crd):
    crd_list = []
    for i in range(3):
        if crd[i] != 'x':
            crd_list.append(crd_btn(crd[i]))
    return crd_list


def decode(skill_str, crd_str):
    instr = []
    skill_str = get_str(skill_str)
    crd_str = get_str(crd_str)
    instr.append("round.quick_start()")
    for i in range(3):
        instr.append("round.waiting_phase(%s)"%str(i+1))
        for j in range(int(len(skill_str[i])/3)):
            if skill_str[i][j * 3] != 'm':
                instr.append(chk_skill(skill_str[i][j * 3], skill_str[i][j * 3 + 2]))
            elif skill_str[i][j * 3] == 'x':
                instr.append("round.select_master_skill(3, %s, %s)"% (skill_str[i][j * 3 + 1], skill_str[i][j * 3 + 2]))
            else:
                instr.append("round.select_master_skill(%s, %s)"% (skill_str[i][j * 3 + 1], skill_str[i][j * 3 + 2]))
        if len(chk_card(crd_str[i])) == 1:
            seq = chk_card(crd_str[i])
            instr.append("round.select_cards([%d])"%seq[0])
        elif len(chk_card(crd_str[i])) == 2:
            seq = chk_card(crd_str[i])
            instr.append("round.select_cards([%d, %d])"%(seq[0], seq[1]))
        elif len(chk_card(crd_str[i])) == 3:
            seq = chk_card(crd_str[i])
            instr.append("round.select_cards([%d, %d, %d])"%(seq[0], seq[1], seq[2]))

    instr.append("round.finish_battle()")
    return instr
