# MCS Fbx Demo

## 项目介绍

用于测试网易FBX动画接口



## 原理介绍

在初始化的时候，注册动画混合`idle_walk`

然后同时循环播放两个动画：`idle` 和 `walk`

然后根据当前状态是站立还是行走，不断地设置混合的数值，就能达到动画混合效果

```python
    def init_anim(self):
        # 注册动画混合
        self.register_anim_param('idle', 'walk', 'idle_walk')
        # 同时循环播放两个动画
        self.play_anim('idle', True, True)
        self.play_anim('walk', True, True)

    def Update(self):
        ...
        self.set_anim_param('idle_walk', self.blend_value)
    	...
        # 改变混合值
        if self.state == 'walk':
            if self.blend_value >= 1:
                self.blend_value = 1
                return
            self.blend_value += 0.1
        if self.state == 'idle':
            if self.blend_value <= 0:
                self.blend_value = 0
                return
            self.blend_value -= 0.1
```

