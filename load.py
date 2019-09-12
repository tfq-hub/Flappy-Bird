"""
By: Cookiery
2018-10-23
load images,sounds,mask
"""
import pygame as pg


IMAGES = {}  # 游戏所有图片字典
SOUNDS = {}  # 游戏所有音效字典
HITMASKS = {}  # 游戏碰撞体mask
# 加载小鸟图片,黄色和红色
BIRDS_LIST = (
    # 黄色小鸟
    (
        'images/yellowbird-upflap.png',
        'images/yellowbird-midflap.png',
        'images/yellowbird-downflap.png',
    ),
    # 红色小鸟
    (
        'images/redbird-upflap.png',
        'images/redbird-midflap.png',
        'images/redbird-downflap.png',
    ),
)


# 加载图片
def load_images():
    """load images"""
    # 游戏开始界面
    IMAGES['gamebegin'] = pg.image.load('images/gamebegin.png')
    # 游戏底面
    IMAGES['base'] = pg.image.load('images/base.png')
    # 游戏结束界面
    IMAGES['gameover'] = pg.image.load('images/gameover.png')
    # 得分数字图片
    IMAGES['numbers'] = (
        pg.image.load('images/0.png').convert_alpha(),
        pg.image.load('images/1.png').convert_alpha(),
        pg.image.load('images/2.png').convert_alpha(),
        pg.image.load('images/3.png').convert_alpha(),
        pg.image.load('images/4.png').convert_alpha(),
        pg.image.load('images/5.png').convert_alpha(),
        pg.image.load('images/6.png').convert_alpha(),
        pg.image.load('images/7.png').convert_alpha(),
        pg.image.load('images/8.png').convert_alpha(),
        pg.image.load('images/9.png').convert_alpha()
    )
    # 背景图片
    IMAGES['background'] = pg.image.load('images/background-day.png')
    # 小鸟图片,黄色小鸟
    IMAGES['bird'] = (
        pg.image.load(BIRDS_LIST[0][0]).convert_alpha(),
        pg.image.load(BIRDS_LIST[0][1]).convert_alpha(),
        pg.image.load(BIRDS_LIST[0][2]).convert_alpha(),
    )
    # 管道图片
    IMAGES['pipe'] = (
        pg.image.load('images/pipe_upper.png').convert_alpha(),
        pg.image.load('images/pipe_lower.png').convert_alpha(),
    )


# 加载声音
def load_sound():
    """load sound"""
    SOUNDS['die'] = pg.mixer.Sound('audio/die.ogg')
    SOUNDS['hit'] = pg.mixer.Sound('audio/hit.ogg')
    SOUNDS['point'] = pg.mixer.Sound('audio/point.ogg')
    SOUNDS['swoosh'] = pg.mixer.Sound('audio/swoosh.ogg')
    SOUNDS['wing'] = pg.mixer.Sound('audio/wing.ogg')


# 得到碰撞体的mask
def load_mask():
    HITMASKS['bird'] = (
        get_mask(IMAGES['bird'][0]),
        get_mask(IMAGES['bird'][1]),
        get_mask(IMAGES['bird'][2]),
    )
    HITMASKS['pipe'] = (
        get_mask(IMAGES['pipe'][0]),
        get_mask(IMAGES['pipe'][1]),
    )


def get_mask(image):
    """get mask"""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask
