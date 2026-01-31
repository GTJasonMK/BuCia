## 背景资源占位与回退
## 说明：当前项目缺少部分背景图，为避免运行期报错，统一回退到默认背景

init -1:
    ## 默认背景（使用fit确保完整显示）
    image bg default = Transform("bg/default_bg.jpg", fit="contain", xysize=(config.screen_width, config.screen_height))

    ## 通用场景占位（使用fit确保完整显示）
    image bg room = Transform("bg/bg1.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg snowfield = Transform("bg/bg2.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg rolinda_house = Transform("bg/bg3.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg yedina_clinic = Transform("bg/bg4.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg andrea_house = Transform("bg/bg5.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg town_square = Transform("bg/bg6.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg night = Transform("bg/bg7.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg badebiete_house = Transform("bg/bg8.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg trial_hall = Transform("bg/bg9.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg church = Transform("bg/bg10.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg distorted = Transform("bg/bg11.png", fit="contain", xysize=(config.screen_width, config.screen_height))
    image bg teaparty = Transform("bg/bg12.png", fit="contain", xysize=(config.screen_width, config.screen_height))

    ## 纯黑背景
    image bg black = Solid("#000")
