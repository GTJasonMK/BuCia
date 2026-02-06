# Repository: BuCia
# 用途：一键将嘴/眼序列帧离线预处理（alpha bleed / unmatte / feather），输出到游戏目录。
#       为了更贴近游戏内最终效果：这里保持原分辨率（仅裁剪半身，不缩放），
#       后续在 bake_character_composites.py 中“先拼接再缩放（LANCZOS）”到 0.45。
#
# 运行方式（PowerShell）：
#   在仓库根目录执行：
#     powershell -ExecutionPolicy Bypass -File tools/process_anime_all.ps1
#
# 前置条件：
# - Windows 已安装 Python（可用 `python` 命令）。
# - 已安装 Pillow：`pip install Pillow`
#
# 注意：
# - 读取：asset/anime（源序列帧）。
# - 输出：game/images/anime（全画布序列帧 + 边缘处理）。

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

# ----------------------------
# 可调参数（与 GUI 一致）
# ----------------------------
$Bleed = 1
$Feather = 0.6
$BaseThreshold = 16

# unmatte（去光晕）参数：一般保持默认即可
$UnmatteMaxAlpha = 220
$UnmatteMinAlpha = 8
$UnmatteStrength = 1.0

# 并发进程数：0=自动（Windows 上过高可能会占满 CPU）
$Workers = 0

Write-Host "[1/4] 同步角色立绘：asset/charcater2 -> game/images/characters"

$CharacterMap = @{
  "1.png"   = "andrea.png"
  "2.png"   = "tsibela.png"
  "2.1.png" = "tsibela2.png"
  "3.png"   = "telina.png"
  "4.png"   = "molorava.png"
  "5.png"   = "badebiete.png"
  "6.png"   = "hafu.png"
  "7.png"   = "bolai.png"
  "8.png"   = "ileina.png"
  "9.png"   = "rolinda.png"
  "10.png"  = "yedina.png"
}

foreach ($entry in $CharacterMap.GetEnumerator()) {
  $src = Join-Path $RepoRoot ("asset/charcater2/" + $entry.Key)
  $dst = Join-Path $RepoRoot ("game/images/characters/" + $entry.Value)
  if (-not (Test-Path $src)) { throw "缺少角色立绘：$src" }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
  Copy-Item -Force $src $dst
}

Write-Host "[2/4] 检查 Python/Pillow"
& python -c "import PIL; print('Pillow', PIL.__version__)" | Out-Host

Write-Host "[3/4] 处理序列帧：asset/anime -> game/images/anime"
& python tools/alpha_bleed_feather.py `
  --in "asset/anime" `
  --out "game/images/anime" `
  --base-map "tools/alpha_bleed_map.json" `
  --crop "0,0,2813,2500" `
  --scale 1.0 `
  --bleed $Bleed `
  --feather $Feather `
  --base-threshold $BaseThreshold `
  --unmatte-max-alpha $UnmatteMaxAlpha `
  --unmatte-min-alpha $UnmatteMinAlpha `
  --unmatte-strength $UnmatteStrength `
  --workers $Workers

Write-Host "[4/4] 烘焙组合帧：game/images/anime -> game/images/characters_baked"
& python tools/bake_character_composites.py `
  --anime-dir "game/images/anime" `
  --base-map "tools/alpha_bleed_map.json" `
  --out-dir "game/images/characters_baked" `
  --crop "0,0,2813,2500" `
  --scale 0.45

Write-Host "完成：已更新 game/images/anime 与 game/images/characters_baked（asset/anime 保持为源文件）。"
