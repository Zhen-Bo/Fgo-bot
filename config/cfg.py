run_time = 1

support = "support/cba.png" #在support目錄下

ap_recover = (1, 'au') #(數量,蘋果種類) 數量填-1為自然回體,會無視後面蘋果種類; 蘋果種類 'sq' = 彩蘋果 'au' = 金蘋果 'ag' = 銀蘋果

recover_time = 200 #自動回體時間(分鐘)

default_skill = '(1)b30d31g31m21(2)f31(3)i31e30h30a30'
#技能格式
#(1~3)代表回合,用以分隔3回合的技能施放
#會依照你輸入的技能從左到右放
#從者技能:{a~i(小寫)} 3(固定) 目標 EX:放第一個非選擇技能=a30(3是固定的0表示非目標) 第7個技能(從者3技能1)給第1個從者=g31
#衣服技能:m(固定) 第幾個技能(1~3) 目標(1~3)
#換人技能:x(固定) 第幾個先發隊員(1~3) 要換上來的後備隊員(1~3)
default_card = '(1)axx(2)axx(3)axx'
#選擇卡片格式
#(1~3)代表回合,用以分隔3回合的選卡
#會依照你輸入的技能從左到右放
#a代表從者1寶具 b代表從者2寶具 c代表從者3寶具
#1~5代表指令卡(從左到右)
#x為1~5中隨機選兩張普通指令卡
