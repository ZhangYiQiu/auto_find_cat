#! python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import cv2

VERSION = "0.0.1"
path = './image'

def pull_screenshot():
    '''截图'''
    os.system('adb shell screencap -p /sdcard/findCat.png')
    os.system(f'adb pull /sdcard/findCat.png {path}')
def updateImg():
    pull_screenshot()
    img_rgb = cv2.imread(f'{path}/findCat.png', 1)
    return img_rgb
def search(img,template,template_size):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    cv2.rectangle(
        img,
        (min_loc[0], min_loc[1]),
        (min_loc[0] + template_size[1], min_loc[1] + template_size[0]),
        (255, 0, 0),
        4)
    cv2.imwrite(f'{path}/found.png', img)
    return img, (min_loc[0] + template_size[1] // 2, min_loc[1] +  template_size[0] // 2),(round(min_val,1), round(max_val,1))

def resizeImg(img,scale=0.5):
    image = img
    w = int(image.shape[1] * scale)
    h = int(image.shape[0] * scale)
    dim = (w, h)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized
def click(location):
    cmd = f'adb shell input tap {location[0]} {location[1]}'
    os.system(cmd)
def keyEvent(key):
    cmd = f'adb shell input keyevent {key}'
    os.system(cmd)
def findTemplateAndClick(Template,Template_size):
    img_rgb = updateImg()
    search_data = search(img_rgb,Template,Template_size)
    matchLevel = search_data[2][0]
    if(matchLevel == 0.0):
        print(f"本次点击座标为：{search_data[1]}")
        click(search_data[1])
        time.sleep(0.3)
        return True,search_data[1]
    else:
        print(f"未找到点击位置！{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        time.sleep(0.3)
        return findTemplateAndClick(Template,Template_size)

def loadTemplate():
    global GetCatCoinTemplate,GetCatCoinTemplate_size
    global GoShopTemplate,GoShopTemplate_size
    global ClickCatTemplate,ClickCatTemplate_size
    global HappyGetCoinTemplate,HappyGetCoinTemplate_size
    #匹配领猫币
    GetCatCoinTemplate = cv2.imread(f'{path}/GetCatCoin.png', 1)
    #去店铺
    GoShopTemplate = cv2.imread(f'{path}/GoShop.png', 1)
    #点击得喵币
    ClickCatTemplate = cv2.imread(f'{path}/ClickCat.png', 1)
    #开心收下
    HappyGetCoinTemplate = cv2.imread(f'{path}/HappyGetCoin.png', 1)
    def isNone(obj):
        return obj is None;
    if  isNone(GetCatCoinTemplate) or \
        isNone(GoShopTemplate) or \
        isNone(ClickCatTemplate) or \
        isNone(HappyGetCoinTemplate):
        raise Exception("未找到模板文件！")
    GetCatCoinTemplate_size = GetCatCoinTemplate.shape
    GoShopTemplate_size = GoShopTemplate.shape
    ClickCatTemplate_size = ClickCatTemplate.shape
    HappyGetCoinTemplate_size = HappyGetCoinTemplate.shape
def loopFind(num):
    for i in range(num):
        findTemplateAndClick(GetCatCoinTemplate,GetCatCoinTemplate_size)
        findTemplateAndClick(GoShopTemplate,GoShopTemplate_size)
        time.sleep(10)
        findTemplateAndClick(ClickCatTemplate,ClickCatTemplate_size)
        findTemplateAndClick(HappyGetCoinTemplate,HappyGetCoinTemplate_size)
        keyEvent(4)
        print(f'已找到{i+1}只猫猫！')
def main():
    this_exe_name='全自动找猫猫程序'
    os.system(f"title {this_exe_name} by 风轻云断")
    try:
        print('加载模板文件...')
        loadTemplate()
        num = input("请输入找猫猫次数：")
        if not num.isdigit():
            raise Exception('输入的不是一个整数，结束运行！')
        loopFind(int(num))
    except Exception as e:
        print(e)
        input('按任意键退出')
        sys.exit(0)
if __name__ =="__main__":
    main()