## 背景资源占位与回退
## 说明：当前项目缺少部分背景图，为避免运行期报错，统一回退到默认背景

init -2:
    ## 默认背景
    image bg default = "bg/default_bg.jpg"

    ## 通用场景占位
    image bg room = "bg/bg1.png"
    image bg snowfield = "bg/bg2.png"
    image bg rolinda_house = "bg/bg3.png"
    image bg yedina_clinic = "bg/bg4.png"
    image bg andrea_house = "bg/bg5.png"
    image bg town_square = "bg/bg6.png"
    image bg night = "bg/bg7.png"
    image bg badebiete_house = "bg/bg8.png"
    image bg trial_hall = "bg/bg9.png"
    image bg church = "bg/bg10.png"
    image bg distorted = "bg/bg11.png"
    image bg teaparty = "bg/bg12.png"

    ## 纯黑背景
    image bg black = Solid("#000")
