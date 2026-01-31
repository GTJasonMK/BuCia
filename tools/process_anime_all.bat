@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

REM Repository: BuCia
REM Purpose: Preprocess frame PNGs (alpha bleed/unmatte/feather), then bake composites.
REM Note   : Keep this file ASCII-only to avoid cmd.exe UTF-8 parsing issues.

set "REPO_ROOT=%~dp0.."
pushd "%REPO_ROOT%" || exit /b 1

set "BLEED=1"
set "FEATHER=0.6"
set "BASE_THRESHOLD=16"
set "UNMATTE_MAX_ALPHA=220"
set "UNMATTE_MIN_ALPHA=8"
set "UNMATTE_STRENGTH=1.0"
set "WORKERS=0"
REM Keep original resolution here (crop only). Bake will do "compose first, then scale (LANCZOS)" to 0.45.
set "SCALE=1.0"
set "CROP=0,0,2813,2500"

echo [1/4] Sync character sprites: asset\charcater2 ^> game\images\characters
if not exist "game\images\characters" mkdir "game\images\characters"
copy /y "asset\charcater2\1.png"   "game\images\characters\andrea.png"    >nul
copy /y "asset\charcater2\2.png"   "game\images\characters\tsibela.png"   >nul
copy /y "asset\charcater2\2.1.png" "game\images\characters\tsibela2.png"  >nul
copy /y "asset\charcater2\3.png"   "game\images\characters\telina.png"    >nul
copy /y "asset\charcater2\4.png"   "game\images\characters\molorava.png"  >nul
copy /y "asset\charcater2\5.png"   "game\images\characters\badebiete.png" >nul
copy /y "asset\charcater2\6.png"   "game\images\characters\hafu.png"      >nul
copy /y "asset\charcater2\7.png"   "game\images\characters\bolai.png"     >nul
copy /y "asset\charcater2\8.png"   "game\images\characters\ileina.png"    >nul
copy /y "asset\charcater2\9.png"   "game\images\characters\rolinda.png"   >nul
copy /y "asset\charcater2\10.png"  "game\images\characters\yedina.png"    >nul

echo [2/4] Check Pillow
python -c "import PIL; print('Pillow', PIL.__version__)" 1>nul 2>nul
if errorlevel 1 (echo Pillow is missing or python is not available. Please run: pip install Pillow & popd & exit /b 1)

echo [3/4] Process frames: asset\anime ^> game\images\anime
python "%~dp0alpha_bleed_feather.py" --in "asset\anime" --out "game\images\anime" --base-map "tools\alpha_bleed_map.json" --crop "%CROP%" --scale %SCALE% --bleed %BLEED% --feather %FEATHER% --base-threshold %BASE_THRESHOLD% --unmatte-max-alpha %UNMATTE_MAX_ALPHA% --unmatte-min-alpha %UNMATTE_MIN_ALPHA% --unmatte-strength %UNMATTE_STRENGTH% --workers %WORKERS%
if errorlevel 1 (echo Processing failed. See output above. & popd & exit /b 1)

echo [4/4] Bake composites: game\images\anime ^> game\images\characters_baked
python "%~dp0bake_character_composites.py" --anime-dir "game\images\anime" --base-map "tools\alpha_bleed_map.json" --out-dir "game\images\characters_baked" --crop "%CROP%" --scale 0.45
if errorlevel 1 (echo Baking failed. See output above. & popd & exit /b 1)

echo Done: game\images\anime and game\images\characters_baked updated.
popd
exit /b 0
