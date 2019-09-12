"""
By: Cookiery
2018-10-23
manage scene,move,score,collide
"""
from pygame.locals import *
from load import *
from itertools import cycle
import random, sys

# 游戏界面
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 30  # 游戏FPS
PIPE_SPACE = 100  # 管子上下间隔
BASE_Y = SCREEN_HEIGHT * 0.79  # 游戏界面底部图片Y轴固定


def game_manage():
    global SCREEN, FPSCLOCK
    # 初始化pygame
    pg.init()
    # 使用Pygame时钟，控制每个循环多长时间运行一次。
    FPSCLOCK = pg.time.Clock()
    # 游戏界面大小
    SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 游戏窗口标题
    pg.display.set_caption('Flappy Bird')


# 开始界面
def show_welcome_scene():
    """show welcome scene"""
    # 小鸟初始位置
    bird_index = 0
    bird_index_gen = cycle([0, 1, 2, 1])
    # 循环播放小鸟动画
    loop_iter = 0
    bird_x = int(SCREEN_WIDTH * 0.2)
    bird_y = int((SCREEN_HEIGHT - IMAGES['bird'][0].get_height()) / 2)
    # 游戏初始界面图片显示
    gamebegin_x = int((SCREEN_WIDTH - IMAGES['gamebegin'].get_width()) / 2)
    gamebegin_y = int(SCREEN_HEIGHT * 0.12)
    # 底部地面只沿X轴移动移动
    base_x = 0
    base_shift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    bird_shake_vals = {'val': 0, 'dir': 1}
    while True:
        for event in pg.event.get():
            if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                SOUNDS['wing'].play()
                return {
                    'bird_y': bird_y + bird_shake_vals['val'],
                    'base_x': base_x,
                    'bird_index_gen': bird_index_gen,
                }
        if (loop_iter + 1) % 5 == 0:
            bird_index = next(bird_index_gen)
        loop_iter = (loop_iter + 1) % 30
        base_x = -((-base_x + 4) % base_shift)
        bird_shake(bird_shake_vals)
        # 绘制开始界面
        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['bird'][bird_index],
                    (bird_x, bird_y + bird_shake_vals['val']))
        SCREEN.blit(IMAGES['gamebegin'], (gamebegin_x, gamebegin_y))
        SCREEN.blit(IMAGES['base'], (base_x, BASE_Y))
        # 显示开始界面
        pg.display.update()
        FPSCLOCK.tick(FPS)


def bird_shake(bird_shake):
    if abs(bird_shake['val']) == 8:
        bird_shake['dir'] *= -1
    if bird_shake['dir'] == 1:
        bird_shake['val'] += 1
    else:
        bird_shake['val'] -= 1


# 显示分数
def show_score(score):
    """show score"""
    score_num = [int(x) for x in list(str(score))]
    total_width = 0  # 要打印数字的总宽度
    for num in score_num:
        total_width += IMAGES['numbers'][num].get_width()
    x_offset = (SCREEN_WIDTH - total_width) / 2  # 分数居中显示
    for num in score_num:
        # 绘制分数
        SCREEN.blit(IMAGES['numbers'][num], (x_offset, SCREEN_HEIGHT * 0.1))
        x_offset += IMAGES['numbers'][num].get_width()


# 随机生成上下管道
def create_pipe():
    """create pipe"""
    gap_y = random.randrange(0, int(BASE_Y * 0.6 - PIPE_SPACE))
    gap_y += int(BASE_Y * 0.2)
    pipe_height = IMAGES['pipe'][0].get_height()
    pipe_x = SCREEN_WIDTH + 10
    return [
        {'x': pipe_x, 'y': gap_y - pipe_height},  # 上管
        {'x': pipe_x, 'y': gap_y + PIPE_SPACE},  # 下管
    ]


# 检查两个对象是否碰撞
def collision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return False
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


# 判断小鸟是否碰到地面或水管
def check_collision(bird, upper_pipe, lower_pipe):
    """check_collision"""
    pi = bird['index']
    bird['w'] = IMAGES['bird'][0].get_width()
    bird['h'] = IMAGES['bird'][0].get_height()
    # 如果小鸟碰到地面
    if bird['y'] + bird['h'] >= BASE_Y - 1:
        return [True, True]
    else:
        bird_rect = pg.Rect(bird['x'], bird['y'],
                            bird['w'], bird['h'])
        pipe_w = IMAGES['pipe'][0].get_width()
        pipe_h = IMAGES['pipe'][0].get_height()
        for u_pipe, l_pipe in zip(upper_pipe, lower_pipe):
            u_pipe_rect = pg.Rect(u_pipe['x'], u_pipe['y'], pipe_w, pipe_h)
            l_pipe_rect = pg.Rect(l_pipe['x'], l_pipe['y'], pipe_w, pipe_h)
            bird_hit_mask = HITMASKS['bird'][pi]
            u_pipe_hit_mask = HITMASKS['pipe'][0]
            l_pipe_hit_mask = HITMASKS['pipe'][1]
            u_collide = collision(bird_rect, u_pipe_rect, bird_hit_mask, u_pipe_hit_mask)
            l_collide = collision(bird_rect, l_pipe_rect, bird_hit_mask, l_pipe_hit_mask)
            if u_collide or l_collide:
                return [True, True]
    return [False, False]


# 游戏主界面和逻辑
def main_game(begin_game):
    score = bird_index = loop_iter = 0
    # 获得飞行姿势
    bird_index_gen = begin_game['bird_index_gen']
    # 小鸟所在位置
    bird_x, bird_y = int(SCREEN_WIDTH * 0.2), begin_game['bird_y']
    # 底面所在位置
    base_x = begin_game['base_x']
    base_shift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    # 获得两个管道
    pipe_1 = create_pipe()
    pipe_2 = create_pipe()
    # 上管道信息
    upper_pipe = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe_1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': pipe_2[0]['y']},
    ]
    # 下管道信息
    lower_pipe = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe_1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': pipe_2[1]['y']},
    ]
    pipe_vel_x = -4
    # 小鸟的速度，最大速度，向下的加速度，向上的加速度
    bird_vel_y = -9  # 小鸟沿y轴的速度
    bird_max_vel_y = 10  # 小鸟沿y轴的最大下降速度
    bird_acc_y = 1  # 小鸟向下的加速度
    bird_rot = 45  # 小鸟旋转
    bird_vel_rot = 3  # 小鸟旋转的角速度
    bird_rot_thr = 20  # 小鸟旋转的阈值
    bird_flap_acc = -9  # 小鸟拍打速度
    bird_flapped = False  # 小鸟是否在拍打

    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if bird_y > -2 * IMAGES['bird'][0].get_height():
                    bird_vel_y = bird_flap_acc
                    bird_flapped = True
                    SOUNDS['wing'].play()
        crash_info = check_collision({'x': bird_x, 'y': bird_y, 'index': bird_index},
                                    upper_pipe, lower_pipe)
        if crash_info[0]:
            return {
                'y': bird_y,
                'ground_crash': crash_info[1],
                'base_x': base_x,
                'upper_pipe': upper_pipe,
                'lower_pipe': lower_pipe,
                'score': score,
                'bird_vel_y': bird_vel_y,
                'bird_rot': bird_rot
            }
        # 判断得分
        bird_mid_pos = bird_x + IMAGES['bird'][0].get_width() / 2
        for pipe in upper_pipe:
            pipe_mid_pos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipe_mid_pos <= bird_mid_pos < pipe_mid_pos + 4:
                score += 1
                SOUNDS['point'].play()
        if (loop_iter + 1) % 3 == 0:
            bird_index = next(bird_index_gen)
        loop_iter = (loop_iter + 1) % 30
        base_x = -((-base_x + 100) % base_shift)
        # 旋转小鸟
        if bird_rot > -90:
            bird_rot -= bird_vel_rot
        # 小鸟运动
        if bird_vel_y < bird_max_vel_y and not bird_flapped:
            bird_vel_y += bird_acc_y
        if bird_flapped:
            bird_flapped = False
            bird_rot = 45
        bird_height = IMAGES['bird'][bird_index].get_height()
        bird_y += min(bird_vel_y, BASE_Y - bird_y - bird_height)
        # 向左移动管道
        for u_pipe, l_pipe in zip(upper_pipe, lower_pipe):
            u_pipe['x'] += pipe_vel_x
            l_pipe['x'] += pipe_vel_x
        # 当第一个管道即将接触屏幕左侧时添加新的管道
        if 0 < upper_pipe[0]['x'] < 5:
            new_pipe = create_pipe()
            upper_pipe.append(new_pipe[0])
            lower_pipe.append(new_pipe[1])
        # 如果没有屏幕，移除第一个管道
        if upper_pipe[0]['x'] < -IMAGES['pipe'][0].get_width():
            upper_pipe.pop(0)
            lower_pipe.pop(0)
        SCREEN.blit(IMAGES['background'], (0, 0))
        for u_pipe, l_pipe in zip(upper_pipe, lower_pipe):
            SCREEN.blit(IMAGES['pipe'][0], (u_pipe['x'], u_pipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (l_pipe['x'], l_pipe['y']))
        SCREEN.blit(IMAGES['base'], (base_x, BASE_Y))
        # 打印分数
        show_score(score)
        visible_rot = bird_rot_thr
        if bird_rot <= bird_rot_thr:
            visible_rot = bird_rot
        bird_surface = pg.transform.rotate(IMAGES['bird'][bird_index], visible_rot)
        SCREEN.blit(bird_surface, (bird_x, bird_y))
        pg.display.update()
        FPSCLOCK.tick(FPS)


# 游戏结束
def show_gameover_screen(crash_info):
    # 死亡后显示小鸟动画
    score = crash_info['score']
    bird_x = SCREEN_WIDTH * 0.2
    bird_y = crash_info['y']
    bird_height = IMAGES['bird'][0].get_height()
    bird_vel_y = crash_info['bird_vel_y']
    bird_acc_y = 2
    bird_rot = crash_info['bird_rot']
    bird_vel_rot = 7
    base_x = crash_info['base_x']
    upper_pipe, lower_pipe = crash_info['upper_pipe'], crash_info['lower_pipe']
    # 撞击声音和死亡声音
    SOUNDS['hit'].play()
    if not crash_info['ground_crash']:
        SOUNDS['die'].play()
    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if bird_y + bird_height >= BASE_Y - 1:
                    return True
        # 小鸟y轴移动
        if bird_y + bird_height < BASE_Y - 1:
            bird_y += min(bird_vel_y, BASE_Y - bird_y - bird_height)
        # 小鸟速度的变化
        if bird_vel_y < 15:
            bird_vel_y += bird_acc_y
        if not crash_info['ground_crash']:
            if bird_rot > -90:
                bird_rot -= bird_vel_rot
        SCREEN.blit(IMAGES['background'], (0, 0))
        for u_pipe, l_pipe in zip(upper_pipe, lower_pipe):
            SCREEN.blit(IMAGES['pipe'][0], (u_pipe['x'], u_pipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (l_pipe['x'], l_pipe['y']))
        SCREEN.blit(IMAGES['base'], (base_x, BASE_Y))
        show_score(score)
        bird_surface = pg.transform.rotate(IMAGES['bird'][1], bird_rot)
        SCREEN.blit(bird_surface, (bird_x, bird_y))
        FPSCLOCK.tick(FPS)
        pg.display.update()
