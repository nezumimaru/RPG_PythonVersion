# 必要なライブラリをインポート
import random
import pygame
from pygame.locals import *
import sys

# 画面サイズの定義
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pygameの画面領域定義（矩形）
SCR_RECT = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# ===== マップクラス =====
class Map:
    # マップ情報：2次元リスト
    # 0: 草、1: 水（壁）、2: 宝箱（ゴール）
    map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,1],
        [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1],
        [1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,5,1,1,1],
        [1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,1,1],
        [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1],
        [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,2,0,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    row, col = len(map), len(map[0])  # マップの行数・列数を計算
    imgs = [None] * 256  # 画像を格納するリスト（最大256種類まで想定）
    msize = 32  # 1マスの大きさ（ピクセル）

    # マップの描画処理（画面に1マスずつ画像を描く）
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                # 各マスの画像を取得して、画面の適切な位置に描画
                screen.blit(self.imgs[self.map[i][j]], (j * self.msize, i * self.msize))


# ===== 画像読み込み関数 =====
def load_img(filename, colorkey=None):
    # 画像ファイルを読み込む
    img = pygame.image.load(filename)
    img = img.convert()  # 速く描画できる形式に変換
    if colorkey is not None:
        if colorkey == -1:  # colorkeyが-1なら左上の色を透明色に設定
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)  # 透明色設定（高速化オプション付き）
    return img  # 読み込んだ画像を返す

#オープニング
def show_opening_screen(screen, clock):
    opening_image = pygame.image.load("images/opening.png")
    opening_image = pygame.transform.scale(opening_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 画像を1枚表示して5秒待ってから終了
    screen.blit(opening_image, (0, 0))
    pygame.display.update()

    pygame.time.wait(3000)  # 3秒間表示

def show_opening02_screen(screen, clock):
    opening_image02 = pygame.image.load("images/MAPkaisetu.png")
    opening_image02 = pygame.transform.scale(opening_image02, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 画像を1枚表示して5秒待ってから終了
    screen.blit(opening_image02, (0, 0))
    pygame.display.update()

    pygame.time.wait(4000)  # 4秒間表示

# ===== 名前入力画面 =====
def name_input_screen(screen, clock, font):
    show_opening_screen(screen, clock)
    show_opening02_screen(screen, clock)
    input_text = ""  # 入力中のテキスト
    prompt_text = "キャラクター名を入力してください（英数字のみ）:\n※ちなみに、ステータスはランダムです！！"
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)  # 入力欄の位置と大きさ
    active = True  # 入力中フラグ

    pygame.key.start_text_input()  # OSにテキスト入力開始を通知（スマホ等の入力支援のため）

    while active:
        for event in pygame.event.get():  # イベント処理
            if event.type == QUIT:  # 閉じるボタン押下時
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN and input_text:  # Enterで入力確定（テキストありの場合のみ）
                    active = False
                elif event.key == K_BACKSPACE:  # バックスペースで1文字削除
                    input_text = input_text[:-1]
            elif event.type == pygame.TEXTINPUT:  # 文字入力イベント
                if event.text.isalnum():  # 入力が英数字なら追加
                    input_text += event.text

        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶし

        # プロンプトの複数行を分割して順番に描画
        lines = prompt_text.split("\n")
        for i, line in enumerate(lines):
            prompt_surface = font.render(line, True, (255, 255, 255))  # 白色文字
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75 + i * 35))
            screen.blit(prompt_surface, prompt_rect)

        # 入力欄の枠を描く
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        # 入力文字を描画（中央揃え）
        text_surface = font.render(input_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=input_rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()  # 画面更新
        clock.tick(30)  # 30FPS制限

    pygame.key.stop_text_input()  # テキスト入力終了を通知
    return input_text  # 入力した文字列を返す


# ===== メインゲーム処理 =====
def game_main():
    pygame.init()  # Pygame初期化
    screen = pygame.display.set_mode(SCR_RECT.size)  # 画面生成
    pygame.display.set_caption("RPGゲーム")  # ウィンドウタイトル
    clock = pygame.time.Clock()  # フレーム制御用

    # タイル画像を読み込み（マップ用）
    Map.imgs[0] = load_img("images/grass.png")  # 草地（通行可能）
    Map.imgs[1] = load_img("images/water.png")  # 水や壁（通行不可）
    Map.imgs[2] = load_img("images/takarabako.png")  # 宝箱（ゴール）
    Map.imgs[4] = load_img("images/hamsuMAP.png")  # ボス①画像
    Map.imgs[5] = load_img("images/berudexiaMAP.png")  # ボス②画像

    map = Map()  # マップオブジェクト生成

    player_pos = [3, 1]  # プレイヤー初期座標（マス座標）
    player_image = load_img("images/senshi.png")  # プレイヤー画像読み込み

    font = pygame.font.Font("NotoSansJP-VariableFont_wght.ttf", 25)  # フォント設定

    # 名前入力画面を表示し、結果を取得
    player_name = name_input_screen(screen, clock, font)
    print(f"入力された名前: {player_name}")

    # プレイヤー初期化（ランダムなステータス）
    player = Player(
        name=player_name,
        hp=random.randint(40, 100),
        attack_power=random.randint(10, 15),
        mp=random.randint(40, 60),
        magic_power=random.randint(5, 10)
    )
    herb_message = ""  # 薬草取得メッセージ（初期は空）
    herb_message_timer = 0  # メッセージ表示タイマー初期化
    ether_message = ""  # エーテル取得メッセージ（初期は空）
    ether_message_timer = 0  # メッセージ表示タイマー初期化

    # ===== メインループ =====
    while True:
        screen.fill((0, 0, 0))  # 画面クリア（黒）
        map.draw(screen)  # マップ描画

        # プレイヤーをマップ上の座標に描画（タイルサイズ×マス座標）
        screen.blit(player_image, (player_pos[1] * 32, player_pos[0] * 32))

        # ステータス表示（名前、HP、MP、攻撃力、魔法力、薬草所持数,MP回復（エーテル））
        player_info = f"{player.name}: HP {player.hp}/{player.max_hp}, MP {player.mp}/{player.max_mp}, 攻撃 {player.attack_power}, 魔力 {player.magic_power}, 薬草 {player.herb_count}, エーテル {player.ether_count}"
        text_surface = font.render(player_info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        guide_surface = font.render("H: 薬草でHP回復   E: エーテルでMP回復", True, (255, 255, 255))
        screen.blit(guide_surface, (10, 40))

        # 薬草メッセージを一定時間表示
        if herb_message and pygame.time.get_ticks() - herb_message_timer < 500:  # 0.5秒間表示
            herb_surface = font.render(herb_message, True, (0, 255, 0))  # 緑色
            screen.blit(herb_surface, (SCREEN_WIDTH // 2 - herb_surface.get_width() // 2, SCREEN_HEIGHT - 40))
        else:
            herb_message = ""  # 表示時間超えたらメッセージリセット

        if ether_message and pygame.time.get_ticks() - ether_message_timer < 500:  # 0.5秒間表示
            ether_surface = font.render(ether_message, True, (255, 0, 0))  # 赤色
            screen.blit(ether_surface, (SCREEN_WIDTH // 2 - ether_surface.get_width() // 2, SCREEN_HEIGHT - 40))
        else:
            ether_message = ""  # 表示時間超えたらメッセージリセット
        pygame.display.update()  # 画面更新
        clock.tick(10)  # 10FPS制限（動作速度調整）

        # 薬草メッセージ表示（500ms）
        if herb_message and pygame.time.get_ticks() - herb_message_timer < 500:
            herb_surface = font.render(herb_message, True, (0, 255, 0))
            screen.blit(herb_surface, (SCREEN_WIDTH // 2 - herb_surface.get_width() // 2, SCREEN_HEIGHT - 60))
        else:
            herb_message = ""

        # エーテルメッセージ表示（500ms）
        if ether_message and pygame.time.get_ticks() - ether_message_timer < 500:
            ether_surface = font.render(ether_message, True, (255, 0, 0))
            screen.blit(ether_surface, (SCREEN_WIDTH // 2 - ether_surface.get_width() // 2, SCREEN_HEIGHT - 30))
        else:
            ether_message = ""

        # イベント処理（キー操作、ウィンドウ閉じるなど）
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                new_pos = player_pos[:]  # 新しい移動先座標のコピー
                if event.key == K_UP:
                    new_pos[0] -= 1
                elif event.key == K_DOWN:
                    new_pos[0] += 1
                elif event.key == K_LEFT:
                    new_pos[1] -= 1
                elif event.key == K_RIGHT:
                    new_pos[1] += 1


                elif event.key == pygame.K_h:  # Hキー：薬草使用

                    if player.herb_count > 0:

                        player.herb_count -= 1

                        recovery = random.randint(20, 50)

                        player.hp = min(player.hp + recovery, player.max_hp)

                        print(f"{player.name}は薬草でHPを{recovery}回復（現在HP: {player.hp}）")

                        herb_message = f"{player.name}はHPを{recovery}回復した！"

                        herb_message_timer = pygame.time.get_ticks()

                    else:

                        herb_message = "薬草がない！"

                        herb_message_timer = pygame.time.get_ticks()


                elif event.key == pygame.K_e:  # Eキー：エーテル使用

                    if player.ether_count > 0:

                        player.ether_count -= 1

                        mp_recovery = random.randint(20, 50)

                        player.mp = min(player.mp + mp_recovery, player.max_mp)

                        print(f"{player.name}はエーテルでMPを{mp_recovery}回復（現在MP: {player.mp}）")

                        ether_message = f"{player.name}はMPを{mp_recovery}回復した！"

                        ether_message_timer = pygame.time.get_ticks()

                    else:

                        ether_message = "エーテルがない！"

                        ether_message_timer = pygame.time.get_ticks()

                # 移動先がマップ内か確認
                if (0 <= new_pos[0] < map.row and 0 <= new_pos[1] < map.col):
                    tile = map.map[new_pos[0]][new_pos[1]]  # 移動先の地形判定
                    if tile != 1:  # 壁（水）でなければ移動可能
                        player_pos = new_pos

                        event_roll = random.random()

                        if event_roll < 0.1 and not event.key == pygame.K_h and not event.key == pygame.K_e:
                            if tile not in [2, 4, 5]:  # 通常マスのみ戦闘
                                monster_name, monster_image = encounter_monster()
                                enemy = Enemy(name=monster_name, hp=random.randint(15, 35),
                                              attack_power=random.randint(6, 12))

                                battle_result = battle_scene(screen, clock, player, font)

                                if battle_result == "lose":
                                    print("ゲームオーバー")
                                    show_gameover_screen(screen, clock)
                                    pygame.quit()
                                    return

                                # 戦闘に勝利した場合は何もしない = 自然と移動ループへ戻る
                                # つまりここで return しないし、ループを break/continue しない

                        elif event_roll < 0.4 and not event.key == pygame.K_h and not event.key == pygame.K_e:
                            player.ether_count += 1
                            ether_message = "エーテルを見つけた!!"
                            ether_message_timer = pygame.time.get_ticks()

                        elif event_roll < 0.7 and not event.key == pygame.K_h and not event.key == pygame.K_e:
                            player.herb_count += 1
                            herb_message = "薬草を見つけた!!"
                            herb_message_timer = pygame.time.get_ticks()

                        # ゴール判定
                        if tile == 2:
                            show_clear_screen(screen, clock)
                            pygame.quit()
                            return

                        if tile == 4:
                            boss1 = Enemy(hp=80, attack_power=20, name="ハンス")
                            result = boss_battle_scene(screen, clock, player, boss1, font)
                            if result == "lose":
                                show_gameover_screen(screen, clock)
                                pygame.quit()
                                return

                        elif tile == 5:
                            boss2 = Enemy(hp=80, attack_power=30, name="ベルディア")
                            result = boss_battle_scene(screen, clock, player, boss2, font)
                            if result == "lose":
                                show_gameover_screen(screen, clock)
                                pygame.quit()
                                return

                        elif random.random() < 0.2:
                            if tile not in [2, 4, 5]:  # tileがイベントやボスでないとき
                                monster_name, monster_image = encounter_monster()
                                enemy = Enemy(name=monster_name, hp=random.randint(15, 35),
                                               attack_power=random.randint(6, 12))
                                battle_result = battle_scene(screen, clock, player, font)
                                if battle_result == "lose":
                                    print("ゲームオーバー")
                                    show_gameover_screen(screen, clock)
                                    pygame.quit()
                                    return


def show_clear_screen(screen, clock):
    # クリア画像を読み込む（例: "clear.png"）
    clear_image = pygame.image.load("images/huri-ren.png")
    clear_image = pygame.transform.scale(clear_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 画像を1枚表示して5秒待ってから終了
    screen.blit(clear_image, (0, 0))
    pygame.display.update()

    pygame.time.wait(8000)  # 8秒間表示

def show_gameover_screen(screen, clock):
    gameover_image = pygame.image.load("images/remu.png")
    gameover_image = pygame.transform.scale(gameover_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(gameover_image, (0, 0))
    pygame.display.update()

    pygame.time.wait(3000)  # 3秒間表示
    pygame.quit()
    sys.exit()

# ===== キャラクター基底クラス =====
class Character:
    def __init__(self, name, hp, attack_power, mp=0, magic_power=0):
        self.name = name  # 名前
        self.hp = hp  # 体力
        self.attack_power = attack_power  # 攻撃力
        self.mp = mp  # 魔法力ポイント
        self.magic_power = magic_power  # 魔法攻撃力

    def is_alive(self):
        return self.hp > 0  # 生存判定

    def attack(self, other, screen=None, font=None, rect_x=20, rect_y=450, rect_width=760, rect_height=130):
        damage = random.randint(1, self.attack_power) * 2
        other.hp -= damage
        msg = f"{self.name}の攻撃！{other.name}に{damage}のダメージを与えた。"
        if screen and font:
            show_battle_message(msg, screen, font, rect_x, rect_y, rect_width, rect_height)
        else:
            print(msg)
        if not other.is_alive():
            win_msg = f"{other.name}を倒した！"
            if screen and font:
                show_battle_message(win_msg, screen, font, rect_x, rect_y, rect_width, rect_height)
            else:
                print(win_msg)

    def magic_list(self):
        return [
            {"name": "メラ", "MP": 5, "damage": 25},
            {"name": "メラミ", "MP": 12, "damage": 60},
            {"name": "メラゾーマ", "MP": 25, "damage": 100},
        ]

    def use_magic(self, other, magic_id, screen=None, font=None, rect_x=20, rect_y=450, rect_width=760,
                  rect_height=130):
        spells = self.magic_list()
        if not (0 <= magic_id < len(spells)):
            print("その魔法は存在しません")
            return

        spell = spells[magic_id]

        if self.mp >= spell["MP"]:
            self.mp -= spell["MP"]
            base_damage = spell["damage"]
            bonus = random.randint(0, self.magic_power)
            total_damage = base_damage + bonus
            other.hp -= total_damage
            msg = f"{self.name}の「{spell['name']}」魔法！{other.name}に{total_damage}のダメージを与えた。"
        else:
            msg = f"MPが足りない！通常攻撃を行います。"
            if screen and font:
                show_battle_message(msg, screen, font, rect_x, rect_y, rect_width, rect_height)
            else:
                print(msg)

            self.attack(other, screen, font, rect_x, rect_y, rect_width, rect_height)
            return

        # 表示処理
        if screen and font:
            show_battle_message(msg, screen, font, rect_x, rect_y, rect_width, rect_height)
        else:
            print(msg)

        if not other.is_alive():
            win_msg = f"{other.name}を倒した！"
            if screen and font:
                show_battle_message(win_msg, screen, font, rect_x, rect_y, rect_width, rect_height)
            else:
                print(win_msg)

    # battle_scene関数の中（またはbattle_sceneから呼ばれる別関数として）

def handle_magic_selection(player, enemy, screen, font, rect_x, rect_y, rect_width, rect_height):
    spells = player.magic_list()
    # 魔法リストからメッセージ作成
    descriptions = " ".join(
        [f"{i}:{spell['name']}(消費MP {spell['MP']})" for i, spell in enumerate(spells)]
        )
    show_battle_message(descriptions, screen, font, rect_x, rect_y, rect_width, rect_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for i in range(len(spells)):
                    if event.key in (pygame.K_0 + i, getattr(pygame, f"K_KP{i}")):
                        player.use_magic(enemy, i, screen, font, rect_x, rect_y, rect_width, rect_height)
                        return
# ===== プレイヤークラス =====
class Player(Character):
    def __init__(self, name, hp, attack_power, mp, magic_power):
        super().__init__(name, hp, attack_power, mp, magic_power)
        self.herb_count = 0
        self.ether_count = 0
        self.max_hp = hp
        self.max_mp = mp


# ===== 敵キャラクタークラス =====
class Enemy(Character):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp, attack_power)


def encounter_monster():
    monster_list = [
        {"name": "キャベツ", "image": "images/kyabetu.png"},
        {"name": "ジャイアントトード", "image": "images/jaianntoTodo.png"},
        {"name": "巨大ゴーレム", "image": "images/goremu.png"},
        {"name": "初心者殺し", "image": "images/syosinnsyaGoroshi.png"}
    ]
    monster = random.choice(monster_list)
    monster_image = pygame.image.load(monster["image"])
    return monster["name"], monster_image

def encounter_boss_monster(boss_id):
    boss_list = [
        {"name": "デュラハン", "image": "images/berudexiaBT.png"},
        {"name": "ハンス", "image": "images/hamsuBT.png"}
    ]
    if 0 <= boss_id < len(boss_list):
        boss = boss_list[boss_id]
        boss_image = pygame.image.load(boss["image"])
        return boss["name"], boss_image
    else:
        raise ValueError("不正なボスIDが指定されました")

# ===== バトルメッセージ表示関数 =====
def show_battle_message(message, screen, font, rect_x, rect_y, rect_width, rect_height):
    # メッセージ背景を黒で描画（前のメッセージを消す）
    pygame.draw.rect(screen, (0, 0, 0), (rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10))
    # メッセージテキストを描画
    text_surface = font.render(message, True, (255, 255, 255))
    screen.blit(text_surface, (rect_x + 20, rect_y + 20))
    pygame.display.update()  # 画面更新
    pygame.time.wait(1300)  # 1.3秒待機してメッセージを表示

# ===== バトル処理 =====
def battle_scene(screen, clock, player, font):
    monster_name, monster_image = encounter_monster()
    monster_image = pygame.transform.scale(monster_image, (300, 300))  # サイズ調整（任意）

    # 特別な敵は強化ステータス
    if monster_name == "巨大ゴーレム":
        enemy = Enemy(name=monster_name, hp=40, attack_power=15)
    elif monster_name == "初心者殺し":
        enemy = Enemy(name=monster_name, hp=40, attack_power=20)
    else:
        # 通常の敵（キャベツ、ジャイアントトードなど）
        enemy = Enemy(name=monster_name, hp=random.randint(10, 20), attack_power=random.randint(6, 12))

    rect_x, rect_y = 20, 450
    rect_width = SCREEN_WIDTH - rect_x * 2
    rect_height = SCREEN_HEIGHT - rect_y - 20

    info_rect_x, info_rect_y = 20, 350
    info_rect_width = SCREEN_WIDTH - 40
    info_rect_height = 50

    while player.is_alive() and enemy.is_alive():
        screen.fill((0, 0, 0))
        screen.blit(monster_image, (SCREEN_WIDTH // 2 - 200, 0))

        # プレイヤー情報
        pygame.draw.rect(screen, (0, 0, 0), (info_rect_x, info_rect_y, info_rect_width, info_rect_height))
        player_info = f"{player.name}: HP {player.hp}/{player.max_hp}, MP {player.mp}/{player.max_mp}, 攻撃 {player.attack_power}, 魔力 {player.magic_power}, 薬草 {player.herb_count}, エーテル {player.ether_count}"
        text_surface = font.render(player_info, True, (255, 255, 255))
        screen.blit(text_surface, (info_rect_x + 20, info_rect_y + 10))

        # コマンドUI
        pygame.draw.rect(screen, (255, 255, 255), Rect(rect_x, rect_y, rect_width, rect_height), 3)
        pygame.draw.rect(screen, (0, 0, 0), Rect(rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10))
        guide = font.render("1: こうげき　2: まほう　3：やくそう　4：エーテル　5:にげる", True, (255, 255, 255))
        screen.blit(guide, (40, rect_y + 20))

        pygame.display.update()

        # 入力待ち
        action_chosen = False
        while not action_chosen:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in (K_1, K_KP1):
                        player.attack(enemy, screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_2, K_KP2):
                        handle_magic_selection(player, enemy, screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_3, K_KP3):
                        if player.herb_count > 0:
                            player.herb_count -= 1
                            recovery = random.randint(20, 50)
                            player.hp = min(player.hp + recovery, player.max_hp)
                            show_battle_message(f"{player.name}はHPを{recovery}回復した。", screen, font, rect_x, rect_y,
                                                rect_width, rect_height)

                        else:
                            show_battle_message("薬草がない！", screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    # ほかのキー処理も同様にここに続ける

                    elif event.key in(K_5,K_KP5):
                        if random.random() < 0.5:  # 50%の確率で逃走成功
                            show_battle_message("うまく逃げられた！", screen, font, rect_x, rect_y, rect_width,
                                                rect_height)
                            return "escape"
                        else:
                            show_battle_message("逃げられなかった！", screen, font, rect_x, rect_y, rect_width,
                                                rect_height)
                            action_chosen = True  # 敵のターンへ
                            break
                    elif event.key in(K_4,K_KP4):
                        if player.ether_count > 0:
                            player.ether_count -= 1
                            mprecovery=random.randint(20, 50)
                            player.mp = min(player.mp + mprecovery, player.max_mp)
                            show_battle_message(f"{player.name}はMPを{mprecovery}回復した。", screen, font, rect_x, rect_y,
                                                rect_width, rect_height)

                        else:
                            show_battle_message("エーテルがない！", screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True

            clock.tick(10)

        # 敵が生きているときのみ攻撃
        if enemy.is_alive():
            enemy.attack(player, screen, font, rect_x, rect_y, rect_width, rect_height)

            if not player.is_alive():
                show_battle_message("敗北。。。また挑戦しよう！", screen, font, rect_x, rect_y, rect_width, rect_height)
                show_gameover_screen(screen, clock)
                return "lose"
        else:
            show_battle_message(f"{enemy.name}を倒した！", screen, font, rect_x, rect_y, rect_width, rect_height)
            return "win"


def boss_battle_scene(screen, clock, player, boss, font):
    # 画像読み込み（boss.name に応じて）
    if boss.name == "ハンス":
        boss_image = pygame.image.load("images/hamsuBT.png")
    elif boss.name == "ベルディア":
        boss_image = pygame.image.load("images/berudexiaBT.png")
    else:
        boss_image = pygame.Surface((300, 300))  # デフォルトの仮画像

    boss_image = pygame.transform.scale(boss_image, (300, 300))

    rect_x, rect_y = 20, 450
    rect_width = SCREEN_WIDTH - rect_x * 2
    rect_height = SCREEN_HEIGHT - rect_y - 20

    info_rect_x, info_rect_y = 20, 350
    info_rect_width = SCREEN_WIDTH - 40
    info_rect_height = 50

    while player.is_alive() and boss.is_alive():
        screen.fill((0, 0, 0))
        screen.blit(boss_image, (SCREEN_WIDTH // 2 - 200, 0))

        # プレイヤー情報
        pygame.draw.rect(screen, (0, 0, 0), (info_rect_x, info_rect_y, info_rect_width, info_rect_height))
        player_info = f"{player.name}: HP {player.hp}/{player.max_hp}, MP {player.mp}/{player.max_mp}, 攻撃 {player.attack_power}, 魔力 {player.magic_power}, 薬草 {player.herb_count}, エーテル {player.ether_count}"
        text_surface = font.render(player_info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        # コマンドUI
        pygame.draw.rect(screen, (255, 0, 0), Rect(rect_x, rect_y, rect_width, rect_height), 3)
        pygame.draw.rect(screen, (0, 0, 0), Rect(rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10))
        guide = font.render("1: こうげき　2: まほう　3：やくそう　4：エーテル　5:にげる", True, (255, 255, 255))
        screen.blit(guide, (40, rect_y + 20))

        pygame.display.update()

        # 入力待ち
        action_chosen = False
        while not action_chosen:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key in (K_1, K_KP1):
                        player.attack(boss, screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_2, K_KP2):
                        handle_magic_selection(player, boss, screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_3, K_KP3):
                        if player.herb_count > 0:
                            player.herb_count -= 1
                            recovery = random.randint(20, 50)
                            player.hp = min(player.hp + recovery, player.max_hp)
                            show_battle_message(f"{player.name}はHPを{recovery}回復した。", screen, font, rect_x, rect_y, rect_width, rect_height)
                        else:
                            show_battle_message("薬草がない！", screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_4, K_KP4):
                        if player.ether_count > 0:
                            player.ether_count -= 1
                            mprecovery = random.randint(20, 50)
                            player.mp = min(player.mp + mprecovery, player.max_mp)
                            show_battle_message(f"{player.name}はMPを{mprecovery}回復した。", screen, font, rect_x, rect_y, rect_width, rect_height)
                        else:
                            show_battle_message("エーテルがない！", screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True
                    elif event.key in (K_5, K_KP5):
                        # ボス戦では逃げられない
                        show_battle_message("ボス戦からは逃げられない！", screen, font, rect_x, rect_y, rect_width, rect_height)
                        action_chosen = True

            clock.tick(10)

        if boss.hp <= 0:
            show_battle_message(f"{boss.name}を倒した！", screen, font, rect_x, rect_y, rect_width, rect_height)
            return "win"

        # ボスのターン
        show_battle_message(f"{boss.name}の攻撃！", screen, font, rect_x, rect_y, rect_width, rect_height)
        damage = random.randint(10, boss.attack_power)
        player.hp -= damage
        show_battle_message(f"{player.name}に{damage}のダメージ！", screen, font, rect_x, rect_y, rect_width, rect_height)

        if not player.is_alive():
            show_battle_message("敗北。。。また挑戦しよう！", screen, font, rect_x, rect_y, rect_width, rect_height)
            show_gameover_screen(screen, clock)
            return "lose"

# ===== 起動処理 =====
if __name__ == "__main__":
    game_main()
