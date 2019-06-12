# 教你用 Python 自动找猫猫

## 依赖
使用python3编写
需要opencv-contrib-python，需卸载opencv-python，opencv-python缺少部分功能。
还需要numpy
```
pip uninstall opencv-python
pip install opencv-contrib-python==3.4.2.* -i https://mirrors.aliyun.com/pypi/simple/
pip install numpy -i https://mirrors.aliyun.com/pypi/simple/
```
## 准备
1. 安装[adb驱动](https://adb.clockworkmod.com/)
2. 安装 ADB 后，请在环境变量里将 adb 的安装路径保存到 PATH 变量里，确保 adb 命令可以被识别到
3. 使用数据线连接设备到电脑
4. 在命令行执行`adb devices`显示如下表明设备已连接
    ```
    List of devices attached
    xxxxxxxx    device
    ```
    - 部分新机型可能需要再另外勾上允许模拟点击权限
    - 小米设备除了 USB 调试，还要打开底下的 USB 调试（安全）
    - USB 可能要设置成 MTP 模式
### 操作步骤

1. 安卓手机打开 USB 调试，设置 > 开发者选项 > USB 调试
2. 电脑与手机 USB 线连接，确保执行 `adb devices` 可以找到设备 ID
3. 打开淘宝，点击右上角，进入到合猫猫主页
![](./resource/image/home.png)
4. 执行`python auto_find_cat.py`开始自动找猫猫