# build.py
import PyInstaller.__main__
import os
import shutil

# 清理之前的构建文件
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# PyInstaller 配置
args = [
    'src/TeaPicK/application.py',  # 主程序入口
    '--name=TeaPicK',              # 可执行文件名
    '--onefile',                   # 打包成单个文件
    '--console',                   # 显示控制台窗口
    # '--windowed',                # 不显示控制台窗口（如果是GUI）
    '--add-data', 'src/TeaPicK/config;config',  # 包含配置文件
    '--hidden-import=configparser',
    '--hidden-import=json',
    '--hidden-import=os',
    '--hidden-import=sys',
    '--hidden-import=colorlog',
    '--hidden-import=selenium',
    '--hidden-import=webdriver_manager',
    '--collect-all=selenium',
    '--collect-all=webdriver_manager',
    '--clean',                     # 清理临时文件
]

# 运行打包
PyInstaller.__main__.run(args)

print("打包完成！可执行文件在 dist/ 目录下")

# 复制配置文件到 dist 目录（可选）
config_src = 'src/TeaPicK/config'
config_dst = 'dist/config'
if os.path.exists(config_src):
    if os.path.exists(config_dst):
        shutil.rmtree(config_dst)
    shutil.copytree(config_src, config_dst)
    print("配置文件已复制到 dist/config/")
