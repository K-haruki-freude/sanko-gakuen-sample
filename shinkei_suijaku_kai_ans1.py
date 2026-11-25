# 2026年 Python課題演習⑪ 解答例
# 問1：1-1 / 1-2 <制限時間を過ぎたら強制終了>
import tkinter
import random
import time  # 1-2 追加：残り時間の計算に使用

img = [None]*14
card = [0]*26
face = [0]*26
memo = [0]*26
proc = 0
tmr = 0
sel1 = 0
sel2 = 0
you = 0
com = 0
FNT = ("Times New Roman", 36)

# ---- 1-2 追加（関数外のコード）----
TIME_LIMIT = 5      # 1枚めくるまでの制限時間（秒）
start_time = 0      # タイマー開始時刻
timer_id = None     # root.after() の予約ID
time_up = False     # 時間切れになったか

def draw_card():
    cvs.delete("all")
    for i in range(26):
        x = (i%7)*120+60
        y = int(i/7)*168+84
        if face[i]==0:
            cvs.create_image(x, y, image=img[0])
        if face[i]==1:
            cvs.create_image(x, y, image=img[card[i]])

def shuffle_card():
    for i in range(26):
        card[i] = 1+i%13
        face[i] = 0
        memo[i] = 0
    for i in range(100):
        r1 = random.randint(0, 12)
        r2 = random.randint(13, 25)
        card[r1], card[r2] = card[r2], card[r1]

# ---- 1-2 新規追加 ----
def start_player_timer():  # プレイヤーの制限時間を（再）スタート
    global start_time, timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
    start_time = time.time()
    timer_id = root.after(TIME_LIMIT*1000, handle_timeout)

def handle_timeout():  # 制限時間を過ぎたら強制終了
    global proc, tmr, timer_id, time_up
    timer_id = None
    if proc==1 or proc==2:
        time_up = True
        proc = 7
        tmr = 0

def click(e):
    global proc, tmr, sel1, sel2, you, com, timer_id, time_up
    if proc == 0:
        shuffle_card()
        you = 0
        com = 0
        time_up = False
        proc = 1               # 1-1：プレイヤーから開始
        tmr = 0
        start_player_timer()   # 1-2：タイマー開始
        return
    x = int(e.x/120)
    y = int(e.y/168)
    if 0<=x and x<=6 and 0<=y and y<=3:
        n = x+y*7
        if n >= 26:
            return
        if face[n]==0:
            if proc==1:
                face[n] = 1
                sel1 = n
                proc = 2
                start_player_timer()   # 2枚目用にタイマー再スタート
            elif proc==2:
                face[n] = 1
                sel2 = n
                proc = 3
                tmr = 0
                if timer_id is not None:   # 2枚めくったのでタイマー停止
                    root.after_cancel(timer_id)
                    timer_id = None

def main():
    global proc, tmr, sel1, sel2, you, com
    tmr += 1
    draw_card()
    if proc==0 and tmr%10<5: # スタート待ち
        cvs.create_text(780, 580, text="Click to start.", fill="green", font=FNT)
    if 1<=proc and proc<=3:
        cvs.create_rectangle(840, 60, 960, 200, fill="blue", width=0)
    cvs.create_text(900, 100, text="YOU", fill="silver", font=FNT)
    cvs.create_text(900, 160, text=you, fill="white", font=FNT)
    if 4<=proc and proc<=6:
        cvs.create_rectangle(840, 260, 960, 400, fill="red", width=0)
    cvs.create_text(900, 300, text="COM", fill="silver", font=FNT)
    cvs.create_text(900, 360, text=com, fill="white", font=FNT)
    # 1-2：残り時間を表示する
    if proc==1 or proc==2:
        remain = TIME_LIMIT - int(time.time()-start_time)
        if remain < 0: remain = 0
        cvs.create_text(900, 460, text="TIME", fill="silver", font=FNT)
        cvs.create_text(900, 520, text=remain, fill="yellow", font=FNT)
    # 1-2：残り時間の直下（時間切れの表示）
    if time_up:
        cvs.create_text(900, 520, text="0", fill="yellow", font=FNT)
        cvs.create_text(780, 640, text="TIME UP!", fill="orange", font=FNT)
    if proc==3 and tmr==15: # 揃ったか判定
        if card[sel1]==card[sel2]:
            face[sel1] = 2
            face[sel2] = 2
            you += 2
            proc = 1
            if you+com==26: proc = 7
            else: start_player_timer()   # 続けてプレイヤーの番
        else:
            face[sel1] = 0
            face[sel2] = 0
            memo[sel1] = card[sel1]
            memo[sel2] = card[sel2]
            proc = 4
        tmr = 0
    if proc==4 and tmr==5: # COM 1枚目をめくる
        sel1 = random.randint(0, 25)
        while face[sel1]!=0: sel1 = (sel1+1)%26
        face[sel1] = 1
        proc = 5
        tmr = 0
    if proc==5 and tmr==5: # COM 2枚目をめくる
        sel2 = random.randint(0, 25)
        while face[sel2]!=0: sel2 = (sel2+1)%26
        for i in range(26):
            if memo[i]==card[sel1] and face[i]==0:
                sel2 = i
        face[sel2] = 1
        proc = 6
        tmr = 0
    if proc==6 and tmr==15: # COMのペア判定
        if card[sel1]==card[sel2]:
            face[sel1] = 2
            face[sel2] = 2
            com += 2
            proc = 4
            if you+com==26: proc = 7
        else:
            face[sel1] = 0
            face[sel2] = 0
            memo[sel1] = card[sel1]
            memo[sel2] = card[sel2]
            proc = 1
            start_player_timer()   # 1-2：プレイヤーの番になったらタイマー開始
        tmr = 0
    if proc==7: # ゲーム終了時の表示
        if time_up:
            cvs.create_text(780, 580, text="COM WIN!", fill="pink", font=FNT)
        elif you>com:
            cvs.create_text(780, 580, text="YOU WIN!", fill="skyblue", font=FNT)
        elif com>you:
            cvs.create_text(780, 580, text="COM WIN!", fill="pink", font=FNT)
        else:
            cvs.create_text(780, 580, text="DRAW", fill="white", font=FNT)
        if tmr==25:
            proc = 0
    root.after(200, main)

root = tkinter.Tk()
root.title("神経衰弱")
root.resizable(False, False)
root.bind("<Button>", click)
cvs = tkinter.Canvas(width=960, height=672, bg="black")
cvs.pack()
for i in range(14):
    # 1-1：画像の読み込み先（このファイルと同じ場所に cat フォルダを置くこと）
    img[i] = tkinter.PhotoImage(file="cat/"+str(i)+".png")
main()
root.mainloop()
