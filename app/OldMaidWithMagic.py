#cording:shift-jis

import random as rn

#各カードの説明
#-----------攻撃魔法--------------
Fire =  "炎:互いの手札から1種類を指定して燃やす（墓地に捨てる）ことが出来る。その際、相手も同じカードを墓地に捨てることが出来る（原則、そのカードの効果は発動しない）。"
Wind =  "風:相手の手札から1枚をランダムで墓地に飛ばす（墓地に捨てる）ことが出来る。その際、自分も同じカードを墓地に捨てることが出来る（原則、そのカードの効果は発動しない）。もし指定したカードがJockerだった場合、その時点で「敗北」する。"
Thief ="盗み:相手の場所を1箇所指定してその場所にあるカードを奪って手札に加える事が出来る。揃った場合、そのペアを墓地に捨てるが効果は発動しない。"
#-----------防御魔法--------------
Water = "水:このカードは攻撃魔法カードの効果を一切受けない。"
Guardian="守護者:このカードは攻撃魔法カードの効果を一切受けない。"
#-----------特殊魔法--------------
Freeze ="吹雪:相手を凍らせる。相手は次のターンを1度飛ばされ、もう一度君がカードを引くことが出来る。"
Open =  "開示:相手の手札カードの場所をすべて見ることが出来る（相手のカードが3枚以下の場合は発動できない）。Openの効果を発動した次のターンに相手がDoubleの効果を発動した場合、始めの1回のみOpenの効果が適応される。"
Double ="二倍:次のターン、相手に2枚カードを引かれる（相手は引いたカードの効果をどちらも発動可能）。"
Declare="宣言:このカードを墓地に送ったとき、何ターン目に試合が終わるかを予想し、宣言通り試合が終了した場合にはたとえJockerを持って負ける状況だったとしても勝利する。"
#-----------逆転魔法--------------
Rotate ="入れ替え:このカードが2枚そろって墓地に捨てられた瞬間、自分と相手の手札のカードをすべて交換する。"
Road_to_win = "勝利への道:このカードを墓地に送ったとき、自分がJockerを持っていた場合相手に渡す。"
Road_to_lose= "敗北への道:このカードを墓地に送ったとき、相手がJockerを持っている場合Jockerを受け取る。" 
#------------Jocker---------------
# Joker ="道化師"


#--------------同じ名前のカードを墓地に送る関数------------
def move_to_graveyard(hand, graveyard):
    hand_dict = {}
    for card in hand:
        if card in hand_dict:
            hand_dict[card] += 1
        else:
            hand_dict[card] = 1
    
    for card, count in hand_dict.items():
        if count > 1:
            for _ in range(count // 2):
                hand.remove(card)
                hand.remove(card)
                graveyard.extend([card, card])
    return hand, graveyard


#--------------カード効果を発動する関数----------------
def activate_card_effect(card, player_hand, cpu_hand, graveyard, current_player,path,open_path,Double_path,forecast,forecast_p):
    
    #階層深すぎるかも
    if card == "Fire":
        # 相手の手札から1枚を指定して燃やす
        if current_player == "player":
            #例外処理のwhile
            while 1:
                #残り手札がJokerしかない場合の処理 残り手札合計3枚の時、2枚はFire,1枚はJoker
                if len(player_hand) + len(cpu_hand) < 4:
                    print("＊何も起こらなかった。＊\n")
                    break
                #燃やせるカード名の表示
                for card_name in player_hand:
                    if card_name!="Joker" and card_name != "Fire":
                        print(card_name,end=" ")
                target_card = input(f"\n＊上記の中から燃やすカード名を指定してください。＊\n-->")
                #燃やす処理/例外処理済み
                if (target_card in cpu_hand) and (target_card != "Fire") and (target_card != "Joker") :
                    if (target_card == "Water") or (target_card == "Guardian"):
                        print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                        break
                    else:
                        cpu_hand.remove(target_card)
                        graveyard.append(target_card)
                        if target_card in player_hand:
                            player_hand.remove(target_card)
                            graveyard.append(target_card)
                        print(f"＊{target_card}が燃やされました。＊")
                        #Doubleの1回目でFireを引いた場合、シャッフルをするため
                        rn.shuffle(cpu_hand)
                        break
                else:
                    print("正しいカード名を再度入力してください。")
                    continue
        #cpuの処理
        else:
            #残り手札がJokerしかない場合の処理 残り手札合計3枚の時、2枚はFire,1枚はJoker
            if len(player_hand) + len(cpu_hand) < 4:
                print("＊何も起こらなかった。＊\n")
            else:
                #CPUがFireを選ばないような処理
                while 1:
                    target_card = rn.choice(player_hand)
                    if (target_card != "Fire") and (target_card != "Joker") :
                        break
                    else:
                        continue
                if (target_card == "Water") or (target_card == "Guardian"):
                    print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                else:
                    player_hand.remove(target_card)
                    graveyard.append(target_card)
                    if target_card in cpu_hand:
                        cpu_hand.remove(target_card)
                        graveyard.append(target_card)
                    print(f"＊CPUが{target_card}を燃やしました。＊")
            

    elif card == "Wind":
        # 相手の手札から1枚をランダムで墓地に飛ばす
        if current_player == "player":
            #残り手札がJokerしかない場合の処理
            if len(player_hand) + len(cpu_hand) < 4:
                print("＊何も起こらなかった。＊\n")
            else:
                target_card = rn.choice(cpu_hand)
                #randomでWindを選ばないような処理
                while 1:
                    target_card = rn.choice(player_hand)
                    if (target_card in cpu_hand) and (target_card != "Wind") and (target_card != "Joker") :
                        break
                    else:
                        continue
                if (target_card == "Water") or (target_card == "Guardian"):
                    print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                else:
                    cpu_hand.remove(target_card)
                    graveyard.append(target_card)
                    if target_card in player_hand:
                        player_hand.remove(target_card)
                        graveyard.append(target_card)
                    print(f"＊{target_card}がランダムで墓地に飛ばされました。＊")
        else:
            #残り手札がJokerしかない場合の処理
            if len(player_hand) + len(cpu_hand) < 4:
                print("＊何も起こらなかった。＊\n")
            else:
                #CPUがWindを選ばないような処理
                while 1:
                    target_card = rn.choice(player_hand)
                    if (target_card != "Wind")  or (target_card != "Joker") :
                        break
                    else:
                        continue
                if (target_card == "Water") or (target_card == "Guardian"):
                    print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                else:
                    player_hand.remove(target_card)
                    graveyard.append(target_card)
                    if target_card in cpu_hand:
                        cpu_hand.remove(target_card)
                        graveyard.append(target_card)
                    print(f"＊CPUがランダムで{target_card}を墓地に飛ばしました。＊")


    elif card == "Thief":
        # 相手の場所を1箇所指定してその場所にあるカードを奪う
        if current_player == "player":
            while 1:
                #残り手札がJokerあるいは何もない場合の処理 残り手札合計3枚の時、2枚はFire,1枚はJoker
                if (len(cpu_hand)+len(player_hand)==3) and ("Joker" in player_hand):
                    print("＊何も奪うことが出来なかった。＊\n")
                    break
                else:
                    #指定できる場所一覧の生成
                    print("指定できる位置：")
                    for i in range(1,len(cpu_hand)+1):
                        if cpu_hand[i-1] != "Thief":
                            print(i,end=" ")
                    #index-1することでindex番号ではなくす->順番は0からではなく1からに変更
                    index = int(input(f"\n＊上記の数字を参考に相手の手札から奪うカードの位置を指定してください。＊\n-->"))-1
                    #盗み処理/例外処理済み
                    if 0 <= index < len(cpu_hand):
                        target_card = cpu_hand[index]
                        if (target_card == "Water") or (target_card == "Guardian"):
                            print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                            break
                        else:
                            target_card = cpu_hand.pop(index)
                            player_hand.append(target_card)
                            print(f"＊{target_card}を奪いました。＊")
                            player_hand, graveyard = move_to_graveyard(player_hand, graveyard)
                            break
                    else:
                        print("正しい数字を入力してください。\n\n")
                        continue

        else:
            if (len(cpu_hand)+len(player_hand)==3) and ("Joker" in cpu_hand):
                print("＊CPUは何も奪うことが出来なかった。＊")
            else:
                #CPUがThiefを選ばないような処理
                while 1:
                    target_card = rn.choice(player_hand)
                    if target_card != "Thief":
                        break
                    else:
                        continue
                if (target_card == "Water") or (target_card == "Guardian"):
                    print(f"＊{target_card}を選んだが、このカードには魔法は効かなかった。＊")
                else:
                    player_hand.remove(target_card)
                    cpu_hand.append(target_card)
                    cpu_hand, graveyard = move_to_graveyard(player_hand, graveyard)
                    print(f"＊CPUが{target_card}を奪いました。＊")

    elif card == "Freeze":
        # 相手を凍らせる
        if current_player == "player":
            path = 1
        elif current_player == "cpu":
            path = 2
        print(f"＊{current_player}がFreezeを使用しました。次のターンはスキップされます。＊")

    elif card == "Open":
        # 相手の手札カードの場所をすべて見る
        if current_player == "player" and len(cpu_hand) > 3:
            print("＊次のターン、PlayerはCPUの手札カードの位置を把握した上でで引くことが出来ます。＊")
            open_path = 1
        elif current_player == "cpu" and len(player_hand) > 3:
            print("＊次のターン、CPUはPlayerの手札カードの位置を把握した上で引くことが出来ます。＊")
            open_path = 2
        else:
            #例外処理済み
            print("＊何も起こらなかった。＊")

    elif card == "Double":
        if current_player=="player":
            Double_path = 2
        elif current_player=="cpu":
            Double_path = 1
        # 次のターン、相手に2枚カードを引かれる
        print(f"＊{current_player}がDoubleを使用しました。次のターン、{current_player}はカードを2枚引かれます。＊")

    elif card == "Declare":
        forecast_p = current_player   
        if current_player == "player": 
            # 試合終了を予想する 例外処理済み
            while 1:
                forecast = int(input(f"＊{current_player}がDeclareを使用しました。試合終了まで残り何ターンかを予想してください。＊"))
                if forecast >= 0:
                    print(f"＊Playerは試合終了までの残りターン数を{forecast}と予想しました。\n＊宣言により、{forecast}ターン後に試合が終了した場合、Playerの勝利となります。＊")
                    break
                else:
                    print("＊0以上の数字を入力してください。＊")
                    continue
        else:
            if ("Fire" in cpu_hand) or ("Wind" in cpu_hand) or ("Thief" in cpu_hand):
                #攻撃魔法が入っている場合、その枚数次第で終了までのターン数が減る
                forecast = (len(player_hand) + len(cpu_hand) - 3)/2-1
            else:
                # このターン以降、攻撃魔法による影響がないと仮定した時、これが最善手。
                forecast = (len(player_hand) + len(cpu_hand) - 3)/2
            print(f"\n＊{current_player}がDeclareを使用しました。CPUは試合終了までの残りターン数を{forecast}と予想しました。\n＊宣言により、{forecast}ターン後に試合が終了した場合、CPUの勝利となります。＊\n")

    elif card == "Rotate":
        # 手札をすべて交換する
        if current_player == "player":
            player_hand, cpu_hand = cpu_hand, player_hand
            print("＊手札を交換しました。＊")
        else:
            cpu_hand, player_hand = player_hand, cpu_hand
            print("＊CPUが手札を交換しました。＊")

    elif card == "Road_to_win":
        # Jockerを相手に渡す
        if current_player == "player":
            if "Joker" in player_hand:
                player_hand.remove("Joker")
                cpu_hand.append("Joker")
                print("＊JokerをCPUに渡しました。＊")
            elif "Joker" in cpu_hand:
                print("＊何も起こらなかった。＊")
        else:
            if "Joker" in cpu_hand:
                cpu_hand.remove("Joker")
                player_hand.append("Joker")
                print("＊CPUがJokerをPlayerに渡しました。＊")
            else:
                print("＊何も起こらなかった。＊")
            
                

    elif card == "Road_to_lose":
        # Jockerを受け取る
        if current_player == "player":    
            if "Joker" in cpu_hand:
                cpu_hand.remove("Joker")
                player_hand.append("Joker")
                print("＊Jokerを受け取りました。＊")
            else:
                print("＊何も起こらなかった。＊")
        else:
            if "Joker" in player_hand:
                player_hand.remove("Joker")
                cpu_hand.append("Joker")
                print("＊CPUがJokerを受け取りました。＊")
            else:
                print("＊何も起こらなかった。＊")

    return player_hand, cpu_hand, graveyard,path,open_path,Double_path,forecast,forecast_p


#----------プレイヤーとCPUがカードを引く関数------------
def draw_card(player, opponent_hand, player_hand, graveyard,path,open_path,Double_path,forecast,forecast_p):
    if player == "player":
        while 1:
            #index-1することでindex番号ではなくす->順番は0からではなく1からに変更
            index = int(input(f"\n相手の手札から引くカードの位置を指定してください。\n相手の残り枚数：{len(opponent_hand)}\n-->"))-1
            if 0 <= index < len(opponent_hand):
                drawn_card = opponent_hand.pop(index)
                player_hand.append(drawn_card)
                print(f"\n\nあなたが引いたカード: {drawn_card}")
                player_hand, opponent_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = activate_card_effect(drawn_card, player_hand, opponent_hand, graveyard, "player",path,open_path,Double_path,forecast,forecast_p)
                break
            else:
                print("適切な数字を入力してください。")
                continue
    else:
        index = rn.randint(0, len(player_hand) - 1)
        drawn_card = player_hand.pop(index)
        opponent_hand.append(drawn_card)
        print(f"\n\nCPUが引いたカード: {drawn_card}")
        player_hand, opponent_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = activate_card_effect(drawn_card, player_hand, opponent_hand, graveyard, "cpu",path,open_path,Double_path,forecast,forecast_p)

    return player_hand, opponent_hand, graveyard,path,open_path,Double_path,forecast,forecast_p


#-----------------Openの関数---------------------
def open(open_path,cpu_hand,order):
    if open_path == 1 and order == 1:
        print(f"openの効果によって、CPUの手札位置を表示します。")
        for i in range(0,len(cpu_hand)):
            print(f"{i+1},{cpu_hand[i]}",end=" ")
        open_path = 0
    elif open_path == 2 and order == 2:
        print(f"openの効果によって、CPUはplayerの手札位置を見ています。")
        open_path = 0
    return open_path


#-------------------Double-----------------------
def double(Double_path,player_hand, cpu_hand, graveyard,path,open_path,turn,forecast,forecast_p):
    if Double_path == 1:
        player_hand, cpu_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = draw_card("player", cpu_hand, player_hand, graveyard,path,open_path,Double_path,forecast,forecast_p)
        #シャッフルして格納場所を変更する
        rn.shuffle(cpu_hand)
    else:
        player_hand, cpu_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = draw_card("cpu", cpu_hand, player_hand, graveyard,path,open_path,Double_path,forecast,forecast_p)

    player_hand,graveyard,cpu_hand,turn = organize(player_hand,graveyard,cpu_hand,turn)
    Double_path = 0
    return Double_path,player_hand, cpu_hand, graveyard,path,open_path,turn,forecast,forecast_p 


#-------手札の整理、状況把握、ターンの増加-------
def organize(player_hand,graveyard,cpu_hand,turn):
    #手札の整理
    player_hand,graveyard = move_to_graveyard(player_hand,graveyard)
    cpu_hand,graveyard = move_to_graveyard(cpu_hand,graveyard)

    print("あなたの手札状況:", player_hand)
    print(f"あなたの手札枚数: {len(player_hand)} 枚")

    turn += 1

    return player_hand,graveyard,cpu_hand,turn


#-------------ゲームのメインループ---------------
def game_loop():
    # タイトル
    for i in range(2):
        for j in range(2):
            print("************************")
        if i == 0:
            print("****Joker with Magic****")

    # 説明の有無
    while True:
        explain = input("\nルールを見ますか？数字を入力してください。\n１，やり方と簡単なルール\n２，各種カード説明\n３，必要ない\n-->")
        if explain == "1"or explain == "１":
            print("このゲームはババ抜きを基に制作されたゲームであり、基本的なルールは同じです。\nしかし、このゲームには「攻撃魔法、防御魔法、特殊魔法、逆転魔法」の４種類に分類されている魔法カードが存在します。\nそれぞれのカードが特異な効果を持っているため、カードを上手く利用して勝利を目指します。")
            print("ここからは、具体的なルールを手短に説明します。\n\n")
            print("１，同じ名前のカードは2枚揃った時、墓地に送る（プログラムにより揃ったものは自動で墓地に送られる）。")
            print("２，自分のターンになったら相手の手札からカードを原則1枚引く。")
            print("３，相手の手札からカードを引き、同じ名前のカードがそろった際にそのカードが持つ効果を発動する。効果発動後は墓地に送る。\n\n")
            print("----------------------------------------------------------------------------")
            print("以上が簡単なルール説明となります。あとは実際にプレイして覚えてみてください！")
        elif explain == "2" or explain == "２":
            print("各種カードについての説明をします。\n\n")
            print(f"#-----------攻撃魔法--------------#\nFire   {Fire}\nWind    {Wind}\nThief   {Thief}\n")
            print(f"#-----------防御魔法--------------#\nWater  {Water}\nGuardian   {Guardian}\n")
            print(f"#-----------特殊魔法--------------#\nFreeze {Freeze}\nOpen  {Open}\nDouble  {Double}\nDeclare   {Declare}\n")
            print(f"#-----------逆転魔法--------------#\nRotate    {Rotate}\nRoad_to_win    {Road_to_win}\nRoad_to_lose {Road_to_lose}\n")
            print(f"##-----------Jocker---------------#\nJoker  Jocker:最後に所持していた場合、原則負ける。\n")
        elif explain == "3"or explain == "３":
            break
        else:
            print("適切な数字を入力してください。")


    print("---------それではゲームを始めます----------\n\n")


    # トランプデッキの定義
    Tramp = ["Fire", "Water", "Freeze", "Wind", "Thief", "Guardian", "Open", "Rotate", "Double", "Declare", "Road_to_win", "Road_to_lose"] * 4 + ["Joker"]
    rn.shuffle(Tramp)
    print("Shuffled Deck:>") 

    # プレイヤーとCPUの手札、墓地の初期化
    player_hand = []
    cpu_hand = []
    graveyard = []

    # トランプの分配
    for i in range(len(Tramp)):
        if i % 2 == 0:
            player_hand.append(Tramp[i])
        else:
            cpu_hand.append(Tramp[i])

    # プレイヤーとCPUの手札をチェックして墓地に送る
    player_hand, graveyard = move_to_graveyard(player_hand, graveyard)
    cpu_hand, graveyard = move_to_graveyard(cpu_hand, graveyard)

    print("あなたの手札状況:", player_hand)

    # カードを引く順番を決める
    print("カードを引く順番を決めます。")
    x = rn.random() * 10
    if x < 5:
        order = 1
        print("先行：プレイヤー\n後攻：CPU\n\n")
    else:
        order = 2
        print("先行：CPU\n後攻：プレイヤー\n\n")

    # ゲームの進行
    turn = 1
    path = 0 #Freezeでターンを飛ばすときのみ使用
    open_path = 0 #Openで相手の手札を開示するときのみ使用
    Double_path = 0 #Doubleで2回カードを引かせるときのパス
    forecast = -1 #Declareの際に宣言した数字
    forecast_p = "" #Declareを使用した人の名前
    d_win = 0 #Declareによる勝利の為の変数

    while player_hand and cpu_hand:
        print(f"\n---- ターン {turn} ----")

        #Declareの処理
        if forecast >= 0:
            print(f"＊Declare＊あと{forecast}ターンで試合が終わった場合、Jokerの有無にかかわらず{forecast_p}が勝利します。")
        #openの開示処理
        if open_path != 0: 
            open_path = open(open_path,cpu_hand,order)
        #Doubleの処理
        if Double_path != 0:
            Double_path,player_hand, cpu_hand, graveyard,path,open_path,turn,forecast,forecast_p = double(Double_path,player_hand, cpu_hand, graveyard,path,open_path,turn,forecast,forecast_p)
            #この時点で手札が空の時の処理
            if (not player_hand) or (not cpu_hand):
                break
            print("\n\n＊もう一度カードをドローします。＊")
        #Freezeの処理（Pathを０に戻す。orderが１なら２に、２なら1に変える。）
        if path >0:
            if order == 1:
                order = 2
            elif order == 2:
                order = 1
            print("Freezeの効果により、1ターン飛ばされます。")
            path = 0

        #ターンを制御する処理
        if order == 1:
            player_hand, cpu_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = draw_card("player", cpu_hand, player_hand, graveyard,path,open_path,Double_path,forecast,forecast_p)
            order = 2
        elif order == 2:
            player_hand, cpu_hand, graveyard,path,open_path,Double_path,forecast,forecast_p = draw_card("cpu", cpu_hand, player_hand, graveyard,path,open_path,Double_path,forecast,forecast_p)
            #シャッフルして格納場所を変更する
            rn.shuffle(cpu_hand)
            order = 1
        
        #手札の整理
        player_hand,graveyard,cpu_hand,turn = organize(player_hand,graveyard,cpu_hand,turn)

        #Declareの処理2  elifだと判定が上手くいかなかったため深層構造
        if forecast >= 0 :
            
            if forecast == 0:
                if (not player_hand) or (not cpu_hand):
                    d_win = 1
                    break
            forecast -= 1
                

        #一気にターンが進行してしまうのを防ぐ
        if player_hand and cpu_hand:
            input("\n\n次のターンに遷移します。Enterキーを押してください。\n")


    if d_win == 0:
        if not player_hand:
            print("\n\n****プレイヤーの勝利です！****\n＊Congulaturations!!＊ ")
        else:
            print("\n\n****CPUの勝利です！****")
    elif d_win == 1:
            print(f"\n\n                  ＊＊＊＊Declare＊＊＊＊\n{forecast_p}の宣言ターン数丁度で試合が終了したため、{forecast_p}勝利です。")



game_loop()
#cmdで実行したときに、ゲーム終了後システムが即終了してしまうのを止める為。
input("Thank you for playing")


