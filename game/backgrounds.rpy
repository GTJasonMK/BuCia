## 背景资源占位与回退
## 说明：当前项目缺少部分背景图，为避免运行期报错，统一回退到默认背景

init -2:
    ## 默认背景
    image bg default = "bg/default_bg.jpg"

    ## 通用场景占位
    image bg room = "bg/default_bg.jpg"
    image bg snowfield = "bg/default_bg.jpg"
    image bg rolinda_house = "bg/default_bg.jpg"
    image bg yedina_clinic = "bg/default_bg.jpg"
    image bg andrea_house = "bg/default_bg.jpg"
    image bg town_square = "bg/default_bg.jpg"
    image bg night = "bg/default_bg.jpg"
    image bg badebiete_house = "bg/default_bg.jpg"
    image bg trial_hall = "bg/default_bg.jpg"
    image bg church = "bg/default_bg.jpg"
    image bg distorted = "bg/default_bg.jpg"
    image bg teaparty = "bg/default_bg.jpg"

    ## 纯黑背景
    image bg black = Solid("#000")
