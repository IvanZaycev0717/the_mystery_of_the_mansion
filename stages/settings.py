# Главное окно игры
TITLE = 'The Mystery of the Mansion'
ICON_PATH = 'images/icons/logo.png'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 120

# Данные автора
GIT_HUB = 'github.com/IvanZaycev0717'
TELEGRAM = 'Telegram: @ivanzaycev0717'
CHRISTIAN = "Based on Christian Koch's videos (https://www.youtube.com/@ClearCode)"
AUTHOR_TIME = 10_000


# Шрифты
FONT_PATH_1 = 'font/font1.ttf'
FONT_PATH_2 = 'font/font2.ttf'
FONT_PATH_3 = 'font/font3.ttf'

# Режим редактора(конструктора) уровней
TILE_SIZE = 64
ANIMATION_SPEED = 8

# Меню выбора языка
LANG_WIDTH = 800
LANG_HEIGHT = 600
LANG_X = 240
LANG_Y = 60
BG_COLOR = '#966A4A'

# Главное меню
MM_BUTTON_W = 200
MM_BUTTON_H = 40
MM_BUT_COLOR = (0, 104, 55)


# Цвета
BLACK_GRAY = '#11151C'
LINE_COLOR = '#f8ff2e'
ORIGIN_COLOR = 'yellow'

#ENVOIREMENT BACKGROUNG
SKY_COLOR = '#d3e4ef'
HORIZON_TOP_COLOR = '#f2f5f7'
SEA_COLOR = '#a8c9e0'
HORIZON_COLOR = '#bfcdd6'

CURTAIN_COLOR = '#640000'

# LEVELS BACKGROUND
LV_BG = {
    'common': {'SKY': '#acd3e9', 'GRD': '#345833'},
    'cementry': {'SKY': '#b9b5b4', 'GRD': '#504744'},
    'inside': {'SKY': '#e4afa0', 'GRD': '#e4afa0'},
    'heaven': {'SKY': '#9bd5fe', 'GRD': '#0597fd'},
    'desert': {'SKY': '#f2d80f', 'GRD': '#dd9b21'},
    'garden': {'SKY': '#4f17b7', 'GRD': '#109730'},
    'poison': {'SKY': '#e3fa7c', 'GRD': '#97fc38'},
}


LEVEL_LAYERS = {
	'clouds': 1,
	'ocean': 2,
	'bg': 3,
	'main': 4
}

# Словарь ассетов к игре
EDITOR_DATA = {

    # PLAYER SECTION

    0: {
        'style': 'player',
        'type': 'object',
        'menu': None,
        'menu_surf': None,
        'preview': None,
        'graphics': 'images/player/idle_right'
    },

    # SKY SECTION

    1: {
        'style': 'sky',
        'type': 'object',
        'menu': None,
        'menu_surf': None,
        'preview': None,
        'graphics': None
    },

    # TERRAIN SECTION

    2: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/common/1.png',
            'images/tile/common/2.png',
            'images/tile/common/3.png',
            'images/tile/common/4.png',
            'images/tile/common/5.png',
            'images/tile/common/6.png',
            'images/tile/common/7.png',
            'images/tile/common/8.png',
            'images/tile/common/9.png',
            'images/tile/common/10.png',
            ),
        'preview': 'images/preview/com_tile.png',
        'graphics': None
    },

    3: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/cementry/1.png',
            'images/tile/cementry/2.png',
            'images/tile/cementry/3.png',
            'images/tile/cementry/4.png',
            'images/tile/cementry/5.png',
            'images/tile/cementry/6.png',
            'images/tile/cementry/7.png',
            ),
        'preview': 'images/preview/cem_tile.png',
        'graphics': None
    },

    4: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/heaven/1.png',
            'images/tile/heaven/2.png',
            'images/tile/heaven/3.png',
            'images/tile/heaven/4.png',
            'images/tile/heaven/5.png',
            'images/tile/heaven/6.png',
            'images/tile/heaven/7.png',
            ),
        'preview': 'images/preview/heav_tile.png',
        'graphics': None
    },

    5: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/desert/1.png',
            'images/tile/desert/2.png',
            'images/tile/desert/3.png',
            'images/tile/desert/4.png',
            'images/tile/desert/5.png',
            'images/tile/desert/6.png',
            'images/tile/desert/7.png',
            ),
        'preview': 'images/preview/des_tile.png',
        'graphics': None
    },

    6: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/garden/1.png',
            'images/tile/garden/2.png',
            'images/tile/garden/3.png',
            'images/tile/garden/4.png',
            'images/tile/garden/5.png',
            'images/tile/garden/6.png',
            'images/tile/garden/7.png',
            ),
        'preview': 'images/preview/gar_tile.png',
        'graphics': None
    },

    7: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/poison/1.png',
            'images/tile/poison/2.png',
            'images/tile/poison/3.png',
            'images/tile/poison/4.png',
            'images/tile/poison/5.png',
            'images/tile/poison/6.png',
            'images/tile/poison/7.png',
            ),
        'preview': 'images/preview/poison_tile.png',
        'graphics': None
    },

    8: {
        'style': 'common',
        'type': 'tile',
        'menu': 'common',
        'menu_surf': (
            'images/tile/floor/1.png',
            'images/tile/floor/2.png',
            'images/tile/floor/3.png',
            ),
        'preview': 'images/preview/floor_tile.png',
        'graphics': None
    },

    # ENEMIES SECTION

    9: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/angel.png',
        'preview': 'images/preview/angel.png',
        'graphics': 'images/enemies/heaven/angel/run_left'
    },

    10: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/bat.png',
        'preview': 'images/preview/bat.png',
        'graphics': 'images/enemies/cementry/bat'
    },

    11: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/bird.png',
        'preview': 'images/preview/bird.png',
        'graphics': 'images/enemies/desert/fire_bird/fly_left'
    },

    12: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/bug.png',
        'preview': 'images/preview/bug.png',
        'graphics': 'images/enemies/cementry/bug'
    },

    13: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/camel.png',
        'preview': 'images/preview/camel.png',
        'graphics': 'images/enemies/desert/camel'
    },

    14: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/cem_spike.png',
        'preview': 'images/preview/cem_spike.png',
        'graphics': 'images/enemies/cementry/spikes'
    },

    15: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/dispultes.png',
        'preview': 'images/preview/dispultes.png',
        'graphics': 'images/enemies/poison/disputes'
    },

    16: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/fire.png',
        'preview': 'images/preview/fire.png',
        'graphics': 'images/enemies/desert/fire'
    },

    17: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/gar_spike.png',
        'preview': 'images/preview/gar_spike.png',
        'graphics': 'images/enemies/garden/spikes'
    },

    18: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/goat.png',
        'preview': 'images/preview/goat.png',
        'graphics': 'images/enemies/desert/goat/idle_left'
    },

    19: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/harp.png',
        'preview': 'images/preview/harp.png',
        'graphics': 'images/enemies/heaven/harp'
    },

    20: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/heav_spike.png',
        'preview': 'images/preview/heav_spike.png',
        'graphics': 'images/enemies/heaven/spikes'
    },

    21: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/hedgenhog.png',
        'preview': 'images/preview/hedgenhog.png',
        'graphics': 'images/enemies/garden/hedgehog'
    },

    22: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/scroll.png',
        'preview': 'images/preview/scroll.png',
        'graphics': 'images/enemies/heaven/scrolls'
    },

    23: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/slime.png',
        'preview': 'images/preview/slime.png',
        'graphics': 'images/enemies/poison/slime'
    },

    24: {
        'style': 'enemy',
        'type': 'tile',
        'menu': 'enemy',
        'menu_surf': 'images/menu/wasp.png',
        'preview': 'images/preview/wasp.png',
        'graphics': 'images/enemies/garden/wasp'
    },

    # KEYS SECTION

    25: {
        'style': 'key',
        'type': 'tile',
        'menu': 'key',
        'menu_surf': 'images/menu/green_key.png',
        'preview': 'images/preview/green_key.png',
        'graphics': 'images/objects/keys/green'
    },

    26: {
        'style': 'key',
        'type': 'tile',
        'menu': 'key',
        'menu_surf': 'images/menu/hammer.png',
        'preview': 'images/preview/hammer.png',
        'graphics': 'images/objects/keys/hammer'
    },

    27: {
        'style': 'key',
        'type': 'tile',
        'menu': 'key',
        'menu_surf': 'images/menu/pink_key.png',
        'preview': 'images/preview/pink_key.png',
        'graphics': 'images/objects/keys/pink'
    },

    28: {
        'style': 'key',
        'type': 'tile',
        'menu': 'key',
        'menu_surf': 'images/menu/yellow_key.png',
        'preview': 'images/preview/yellow_key.png',
        'graphics': 'images/objects/keys/yellow'
    },

    # GEAR SECTION

    29: {
        'style': 'gear',
        'type': 'tile',
        'menu': 'gear',
        'menu_surf': 'images/menu/gear.png',
        'preview': 'images/preview/gear.png',
        'graphics': 'images/objects/gear/rolated'
    },

    # STATIC SECTION

    30: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/book_shelf.png',
        'preview': 'images/preview/book_shelf.png',
        'graphics': 'images/objects/first_floor/shelf'
    },

    31: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cauldron.png',
        'preview': 'images/preview/cauldron.png',
        'graphics': 'images/objects/cupboard/cauldron'
    },

    32: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cem_bush1.png',
        'preview': 'images/preview/cem_bush1.png',
        'graphics': 'images/objects/cementry/bush1'
    },

    33: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cem_bush2.png',
        'preview': 'images/preview/cem_bush2.png',
        'graphics': 'images/objects/cementry/bush2'
    },

    34: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cem_fence.png',
        'preview': 'images/preview/cem_fence.png',
        'graphics': 'images/objects/cementry/gravefence'
    },

    35: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cem_tree1.png',
        'preview': 'images/preview/cem_tree1.png',
        'graphics': 'images/objects/cementry/gravetree1'
    },

    36: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/cem_tree2.png',
        'preview': 'images/preview/cem_tree2.png',
        'graphics': 'images/objects/cementry/gravetree2'
    },

    37: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/chair.png',
        'preview': 'images/preview/chair.png',
        'graphics': 'images/objects/first_floor/chair'
    },

    38: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/chest.png',
        'preview': 'images/preview/chest.png',
        'graphics': 'images/objects/first_floor/chest'
    },

    39: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_hedge.png',
        'preview': 'images/preview/com_hedge.png',
        'graphics': 'images/objects/common/hedge'
    },

    40: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_plant1.png',
        'preview': 'images/preview/com_plant1.png',
        'graphics': 'images/objects/common/plant1'
    },

    41: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_plant2.png',
        'preview': 'images/preview/com_plant2.png',
        'graphics': 'images/objects/common/plant2'
    },

    42: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_plant3.png',
        'preview': 'images/preview/com_plant3.png',
        'graphics': 'images/objects/common/plant3'
    },

    43: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_post.png',
        'preview': 'images/preview/com_post.png',
        'graphics': 'images/objects/common/lightpost'
    },

    44: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/com_woodgfence.png',
        'preview': 'images/preview/com_woodgfence.png',
        'graphics': 'images/objects/common/woodfence'
    },

    45: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/couch.png',
        'preview': 'images/preview/couch.png',
        'graphics': 'images/objects/first_floor/couch'
    },

    46: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/devil.png',
        'preview': 'images/preview/devil.png',
        'graphics': 'images/objects/cupboard/devil'
    },

    47: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/door.png',
        'preview': 'images/preview/door.png',
        'graphics': 'images/objects/floor/door'
    },

    48: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/dune1.png',
        'preview': 'images/preview/dune1.png',
        'graphics': 'images/objects/desert/dune1'
    },

    49: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/dune2.png',
        'preview': 'images/preview/dune2.png',
        'graphics': 'images/objects/desert/dune2'
    },

    50: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/dune3.png',
        'preview': 'images/preview/dune3.png',
        'graphics': 'images/objects/desert/dune3'
    },

    51: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gar_fence.png',
        'preview': 'images/preview/gar_fence.png',
        'graphics': 'images/objects/garden/wood_fence'
    },

    52: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gar_tree1.png',
        'preview': 'images/preview/gar_tree1.png',
        'graphics': 'images/objects/garden/tree1'
    },

    53: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gar_tree2.png',
        'preview': 'images/preview/gar_tree2.png',
        'graphics': 'images/objects/garden/tree2'
    },

    54: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gravestn1.png',
        'preview': 'images/preview/gravestn1.png',
        'graphics': 'images/objects/cementry/gravestone1'
    },

    55: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gravestn2.png',
        'preview': 'images/preview/gravestn2.png',
        'graphics': 'images/objects/cementry/gravestone2'
    },

    56: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gravestn3.png',
        'preview': 'images/preview/gravestn3.png',
        'graphics': 'images/objects/cementry/gravestone3'
    },

    57: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/gravestn4.png',
        'preview': 'images/preview/gravestn4.png',
        'graphics': 'images/objects/cementry/gravestone4'
    },

    58: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_fortress.png',
        'preview': 'images/preview/heav_fortress.png',
        'graphics': 'images/objects/heaven/fortress'
    },

    59: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_gate_1.png',
        'preview': 'images/preview/heav_gate_1.png',
        'graphics': 'images/objects/heaven/gate1'
    },

    60: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_gate_2.png',
        'preview': 'images/preview/heav_gate_2.png',
        'graphics': 'images/objects/heaven/gate2'
    },

    61: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_stair1.png',
        'preview': 'images/preview/heav_stair1.png',
        'graphics': 'images/objects/heaven/stair1'
    },

    62: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_stair2.png',
        'preview': 'images/preview/heav_stair2.png',
        'graphics': 'images/objects/heaven/stair2'
    },

    63: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/heav_stair3.png',
        'preview': 'images/preview/heav_stair3.png',
        'graphics': 'images/objects/heaven/stair3'
    },

    64: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/lamp.png',
        'preview': 'images/preview/lamp.png',
        'graphics': 'images/objects/floor/lamp'
    },

    65: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/mansion.png',
        'preview': 'images/preview/mansion.png',
        'graphics': 'images/objects/common/mansion'
    },

    66: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/monument.png',
        'preview': 'images/preview/monument.png',
        'graphics': 'images/objects/cementry/monument'
    },

    67: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/mush1.png',
        'preview': 'images/preview/mush1.png',
        'graphics': 'images/objects/poison/mush1'
    },

    68: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/mush2.png',
        'preview': 'images/preview/mush2.png',
        'graphics': 'images/objects/poison/mush2'
    },

    69: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/palm.png',
        'preview': 'images/preview/palm.png',
        'graphics': 'images/objects/desert/palm'
    },

    70: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic1.png',
        'preview': 'images/preview/pic1.png',
        'graphics': 'images/objects/first_floor/picture1'
    },

    71: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic2.png',
        'preview': 'images/preview/pic2.png',
        'graphics': 'images/objects/first_floor/picture2'
    },

    72: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic3.png',
        'preview': 'images/preview/pic3.png',
        'graphics': 'images/objects/first_floor/picture3'
    },

    73: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic4.png',
        'preview': 'images/preview/pic4.png',
        'graphics': 'images/objects/floor/picture1'
    },

    74: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic5.png',
        'preview': 'images/preview/pic5.png',
        'graphics': 'images/objects/floor/picture2'
    },

    75: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic6.png',
        'preview': 'images/preview/pic6.png',
        'graphics': 'images/objects/floor/picture3'
    },

    76: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic7.png',
        'preview': 'images/preview/pic7.png',
        'graphics': 'images/objects/floor/picture4'
    },

    77: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/pic8.png',
        'preview': 'images/preview/pic8.png',
        'graphics': 'images/objects/floor/picture5'
    },

    78: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/plant1.png',
        'preview': 'images/preview/plant1.png',
        'graphics': 'images/objects/garden/plant1'
    },

    79: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/plant2.png',
        'preview': 'images/preview/plant2.png',
        'graphics': 'images/objects/garden/plant2'
    },

    80: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/rockfence1.png',
        'preview': 'images/preview/rockfence1.png',
        'graphics': 'images/objects/common/rockfence1'
    },

    81: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/rockfence2.png',
        'preview': 'images/preview/rockfence2.png',
        'graphics': 'images/objects/common/rockfence2'
    },

    82: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/round_window.png',
        'preview': 'images/preview/round_window.png',
        'graphics': 'images/objects/floor/window'
    },

    83: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/shelf.png',
        'preview': 'images/preview/shelf.png',
        'graphics': 'images/objects/cupboard/shelf'
    },

    84: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/stair.png',
        'preview': 'images/preview/stair.png',
        'graphics': 'images/objects/floor/stair'
    },

    85: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/stand.png',
        'preview': 'images/preview/stand.png',
        'graphics': 'images/objects/first_floor/stand'
    },

    86: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/statue.png',
        'preview': 'images/preview/statue.png',
        'graphics': 'images/objects/common/statue'
    },

    87: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/table.png',
        'preview': 'images/preview/table.png',
        'graphics': 'images/objects/first_floor/table'
    },

    88: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/wall.png',
        'preview': 'images/preview/wall.png',
        'graphics': 'images/objects/first_floor/wall'
    },

    89: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/wardrobe.png',
        'preview': 'images/preview/wardrobe.png',
        'graphics': 'images/objects/floor/wardrobe'
    },

    90: {
        'style': 'static',
        'type': 'object',
        'menu': 'static',
        'menu_surf': 'images/menu/window.png',
        'preview': 'images/preview/window.png',
        'graphics': 'images/objects/first_floor/window'
    },

    # ACTIVATOR SECTION

    91: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/act_wall.png',
        'preview': 'images/preview/act_wall.png',
        'graphics': 'images/objects/activators/wall'
    },

    92: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/blue_door_in.png',
        'preview': 'images/preview/blue_door_in.png',
        'graphics': 'images/objects/activators/blue_door_in'
    },

    93: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/blue_door_out.png',
        'preview': 'images/preview/blue_door_out.png',
        'graphics': 'images/objects/activators/blue_door_out'
    },

    94: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/cem_gates.png',
        'preview': 'images/preview/cem_gates.png',
        'graphics': 'images/objects/activators/cementry_gates'
    },

    95: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/cup_bed.png',
        'preview': 'images/preview/cup_bed.png',
        'graphics': 'images/objects/activators/cupboard_bed'
    },

    96: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/cup_door_in.png',
        'preview': 'images/preview/cup_door_in.png',
        'graphics': 'images/objects/activators/cupboard_door_in'
    },

    97: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/cup_door_out.png',
        'preview': 'images/preview/cup_door_out.png',
        'graphics': 'images/objects/activators/cupboard_door_out'
    },

    98: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/ff_bed_in.png',
        'preview': 'images/preview/ff_bed_in.png',
        'graphics': 'images/objects/activators/ff_bed_in'
    },

    99: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/green_door_in.png',
        'preview': 'images/preview/green_door_in.png',
        'graphics': 'images/objects/activators/green_door_in'
    },

    100: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/green_door_out.png',
        'preview': 'images/preview/green_door_out.png',
        'graphics': 'images/objects/activators/green_door_out'
    },

    101: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/machine.png',
        'preview': 'images/preview/machine.png',
        'graphics': 'images/objects/activators/machine'
    },

    102: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/pink_door_in.png',
        'preview': 'images/preview/pink_door_in.png',
        'graphics': 'images/objects/activators/pink_door_in'
    },

    103: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/pink_door_out.png',
        'preview': 'images/preview/pink_door_out.png',
        'graphics': 'images/objects/activators/pink_door_out'
    },

    104: {
        'style': 'activator',
        'type': 'object',
        'menu': 'activator',
        'menu_surf': 'images/menu/sf_bed.png',
        'preview': 'images/preview/sf_bed.png',
        'graphics': 'images/objects/activators/sf_bed'
    },

    105: {
        'style': 'loading',
        'type': None,
        'menu': 'loading',
        'menu_surf': 'images/menu/load.png',
        'preview': None,
        'graphics': None
    },

    106: {
        'style': 'saving',
        'type': None,
        'menu': 'saving',
        'menu_surf': 'images/menu/save.png',
        'preview': None,
        'graphics': None
    },

    107: {
        'style': 'level_save',
        'type': None,
        'menu': 'level_save',
        'menu_surf': 'images/menu/levelsave.png',
        'preview': None,
        'graphics': None
    },

    108: {
        'style': 'none',
        'type': None,
        'menu': 'none',
        'menu_surf': 'images/menu/none.png',
        'preview': None,
        'graphics': None
    },


}
