# coding=utf-8
AnimCfg = {
    'player_base': {  # 模型名字
        # 'shoot': {  # 动画名字
        #     'loop': True,  # 是否循环
        #     'layer': 1,  # 优先级
        #     'mask': ['leg.l', 'leg.r'],  # 是否屏蔽骨骼
        # },
        'idle': {
            'loop': True,
            'layer': 3,
            'mask': [],
        },
        'walk': {
            'loop': True,
            'layer': 2,
            'mask': [],
        },
        'jump': {
            'loop': True,
            'layer': 0,
            'mask': [],
        }
    },
    'lazer_gun': {
        'shoot': {
            'loop': True,
            'layer': 1,
            'mask': []
        }
    }
}

mapping = {
    'idle': ['walk', 'jump'],
    'walk': ['idle', 'jump'],
    'jump': ['idle', 'walk']
}
