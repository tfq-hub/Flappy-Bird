"""
By: Cookiery
2018-10-23
"""
from manage import *


def main():
    # pygame初始化操作
    game_manage()
    # 游戏图片加载
    load_images()
    # 游戏声音加载
    load_sound()
    # 碰撞体的mask
    load_mask()
    gameover = True
    while gameover:
        # 加载游戏开始界面
        begin_game = show_welcome_scene()
        # 进入游戏主界面
        crash_info = main_game(begin_game)
        # 游戏结束
        gameover = show_gameover_screen(crash_info)
        print(gameover)


if __name__ == '__main__':
    main()

