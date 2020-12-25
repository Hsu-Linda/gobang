
import pygame
import sys
import traceback
import copy
from pygame.locals import *

pygame.init()


# 顏色
background = (210, 180, 140)
checkerboard = (80, 80, 80)
button = (52, 53, 44)


# 繪製棋盤
def draw_a_chessboard(screen):
    # 填充背景色

    screen.fill(background)
    pygame.display.flip()

    # 畫棋盤
    for i in range(21):
        pygame.draw.line(screen, checkerboard, (40 * i + 3, 3), (40 * i + 3, 803))
        pygame.draw.line(screen, checkerboard, (3, 40 * i + 3), (803, 40 * i + 3))
    # 畫邊線
    pygame.draw.line(screen, checkerboard, (3, 3), (803, 3), 5)
    pygame.draw.line(screen, checkerboard, (3, 3), (3, 803), 5)
    pygame.draw.line(screen, checkerboard, (803, 3), (803, 803), 5)
    pygame.draw.line(screen, checkerboard, (3, 803), (803, 803), 5)

    # 畫定位點
    pygame.draw.circle(screen, checkerboard, (163, 163), 6)
    pygame.draw.circle(screen, checkerboard, (163, 643), 6)
    pygame.draw.circle(screen, checkerboard, (643, 163), 6)
    pygame.draw.circle(screen, checkerboard, (643, 643), 6)
    pygame.draw.circle(screen, checkerboard, (403, 403), 6)

    # 畫‘重新開始’跟‘退出’按鈕
    pygame.draw.rect(screen, button, [900, 380, 200, 100], 5)
    pygame.draw.rect(screen, button, [900, 530, 200, 100], 5)
    s_font = pygame.font.Font('C:\\Windows\\Fonts\\msjh.ttc', 40)
    text2 = s_font.render("重新開始", True, button)
    text3 = s_font.render("退出遊戲", True, button)
    screen.blit(text2, (920, 400))
    screen.blit(text3, (920, 550))


# 繪製棋子（橫座標，縱座標，螢幕，棋子顏色（1代表黑，2代表白））
def draw_a_chessman(x, y, screen, color):
    if color == 1:
        Black_chess = pygame.image.load("C:\\Windows\\black.png").convert_alpha()
        screen.blit(Black_chess, (40 * x - 15, 40 * y - 15))
    if color == 2:
        White_chess = pygame.image.load("C:\\Windows\\white.png").convert_alpha()
        screen.blit(White_chess, (40 * x - 15, 40 * y - 15))


# 繪製帶有棋子的棋盤
def draw_a_chessboard_with_chessman(map, screen):
    screen.fill(background)
    draw_a_chessboard(screen)
    for i in range(24):
        for j in range(24):
            draw_a_chessman(i + 1, j + 1, screen, map[i][j])


# 定義儲存棋盤的列表,
# 列表為24列24行是因為判斷是否勝利函式裡的索引會超出19
# 列表大一點不會對遊戲有什麼影響
map = []
for i in range(24):
    map.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# 清零map列表
def clear():
    global map
    for i in range(24):
        for j in range(24):
            map[i][j] = 0


# 判斷是否勝利
def win(i, j):
    k = map[i][j]
    p = []
    for a in range(20):
        p.append(0)
    for i3 in range(i - 4, i + 5):
        for j3 in range(j - 4, j + 5):
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 <= i and j3 <= j):
                p[0] += 1
            if (map[i3][j3] == k and j3 == j and i3 <= i and j3 <= j):
                p[1] += 1
            if (map[i3][j3] == k and i3 == i and i3 <= i and j3 <= j):
                p[2] += 1
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 >= i and j3 >= j):
                p[3] += 1
            if (map[i3][j3] == k and j3 == j and i3 >= i and j3 >= j):
                p[4] += 1
            if (map[i3][j3] == k and i3 == i and i3 >= i and j3 >= j):
                p[5] += 1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i and j3 >= j):
                p[6] += 1
            if (map[i3][j3] == k and i3 - i == j - j3 and i3 >= i and j3 <= j):
                p[7] += 1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[8] += 1
            if (map[i3][j3] == k and j == j3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[9] += 1
            if (map[i3][j3] == k and i == i3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[10] += 1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[11] += 1
            if (map[i3][j3] == k and j == j3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[12] += 1
            if (map[i3][j3] == k and i == i3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[13] += 1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i + 1 and i3 >= i - 3 and j3 >= j - 1 and j3 <= j + 3):
                p[14] += 1
            if (map[i3][j3] == k and i3 - i == j - j3 and i3 >= i - 1 and i3 <= i + 3 and j3 <= j + 1 and j3 >= j - 3):
                p[15] += 1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 <= i + 2 and i3 >= i - 2 and j3 <= j + 2 and j3 >= j - 2):
                p[16] += 1
            if (map[i3][j3] == k and j == j3 and i3 <= i + 2 and i3 >= i - 2 and j3 <= j + 2 and j3 >= j - 2):
                p[17] += 1
            if (map[i3][j3] == k and i == i3 and i3 <= i + 2 and i3 >= i - 2 and j3 <= j + 2 and j3 >= j - 2):
                p[18] += 1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i + 2 and i3 >= i - 2 and j3 <= j + 2 and j3 >= j - 2):
                p[19] += 1
    for b in range(20):
        if p[b] == 5:
            return True
    return False


# 繪製提示器（類容，螢幕，字大小）
def text(s, screen, x):
    # 先把上一次的類容用一個矩形覆蓋
    pygame.draw.rect(screen, background, [850, 100, 1200, 100])
    # 定義字型跟大小
    s_font = pygame.font.Font('C:\\Windows\\Fonts\\msjh.ttc', x)
    # 定義類容，是否抗鋸齒，顏色
    s_text = s_font.render(s, True, button)
    # 將字放在視窗指定位置
    screen.blit(s_text, (880, 100))
    pygame.display.flip()


# 用於控制順序
t = True

# 用於結束遊戲後阻止落子
running = True


# 主函式
def main():
    # 將 t，map，running設定為可改的
    global t, map, running, maps, r, h
    # 將map置零
    clear()
    # 定義儲存所有棋盤狀態的列表（用於悔棋）
    map2 = copy.deepcopy(map)
    maps = [map2]

    # 定義視窗
    screen = pygame.display.set_mode([1200, 806])

    # 定義視窗名字
    pygame.display.set_caption("五子棋")

    # 在視窗畫出棋盤，提示器以及按鈕
    draw_a_chessboard(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        # 只有running為真才能落子，主要用於遊戲結束後防止再次落子
        if running:
            if t:
                color = 1
                text('黑棋落子', screen, 54)
            else:
                color = 2
                text('白棋落子', screen, 54)

        for event in pygame.event.get():
            # 點選x則關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 點選窗口裡面類容則完成相應指令
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    for i in range(19):
                        for j in range(19):
                            # 點選棋盤相應位置
                            if i * 40 + 3 + 20 < x < i * 40 + 3 + 60 and j * 40 + 3 + 20 < y < j * 40 + 3 + 60 and not \
                            map[i][j] and running:
                                # 在棋盤相應位置落相應顏色棋子
                                draw_a_chessman(i + 1, j + 1, screen, color)

                                # 在map裡面記錄落子位置
                                map[i][j] = color

                                # 將map存入maps
                                map3 = copy.deepcopy(map)
                                maps.append(map3)

                                # 判斷落子後是否有五子一線
                                if win(i, j):
                                    if t:
                                        text('黑棋勝利!，''請重新遊戲', screen, 30)
                                    else:
                                        text('白棋勝利!，''請重新遊戲', screen, 30)

                                    # 阻止再往棋盤落子
                                    running = False
                                pygame.display.flip()
                                t = not t
                    # 如果點選‘重新開始’
                    if 900 < x < 1100 and 380 < y < 480:
                        # 取消阻止
                        running = True


                        # 重新開始
                        main()

                    # 點選‘退出遊戲’，退出遊戲
                    elif 900 < x < 1100 and 530 < y < 630:

                        pygame.quit()
                        sys.exit()

        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
