import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650 #1600, 900を修正
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP: (0, -5),  
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect):

    """引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値:真理値タプル(横,縦)/画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return yoko, tate

def game_over(screen:pg.Surface):
    """
    ゲームオーバー画面を表示する
    引数:screen
    戻り値:なし
    """
    background = pg.Surface(screen.get_size())#画面と同じサイズのSurfaceを作成
    pg.draw.rect(background, (0, 0, 0), (0,0,WIDTH, HEIGHT))#黒色の背景を描画
    pg.Surface.set_alpha(background, 100)#透明度を100に設定
    screen.blit(background, (0, 0))#背景を画面に描画

    font = pg.font.Font(None, 80)#フォントを指定
    moji = font.render("GAME OVER", True, (255, 255, 255))#文字の内容と色を指定
    screen.blit(moji, [WIDTH/3, HEIGHT/2 - 50])#文字を画面に描画

    emoji = pg.image.load("fig/8.png")#絵文字を読み込む
    screen.blit(emoji, [WIDTH/3-70, HEIGHT/2 -50])#絵文字を画面に描画
    emoji2 = pg.image.load("fig/8.png")#絵文字を読み込む
    screen.blit(emoji2, [WIDTH/3*2, HEIGHT/2 -50])#絵文字を画面に描画
    
    pg.display.update()
    time.sleep(5)#5秒間待つ


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs, bb_accs = init_bb_imgs()
    avx = vx*bb_accs[min(tmr//500, 9)]
    bb_imgs = bb_imgs[min(tmr//500, 9)]
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_imgs = pg.Surface((20*r, 20*r))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)#2.0を0.9に修正
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200 #修正
    bb_img = pg.Surface((20, 20))#爆弾の空のSurfaceを作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10),10)#爆弾を描画
    bb_img.set_colorkey((0, 0, 0))#黒色を透明化
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)#位置を表す乱数
    vx, vy = +5, +5#横方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key in DELTA:
            if key_lst[key]:
                sum_mv[0] += DELTA[key][0]
                sum_mv[1] += DELTA[key][1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら,元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
#c
