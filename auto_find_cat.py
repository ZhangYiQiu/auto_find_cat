#! python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import time
import cv2
import numpy as np

VERSION = "0.0.1"
path = './image'
img_type = 1
def pull_screenshot():
    '''截图'''
    os.system('adb shell screencap -p /sdcard/findCat.png')
    subprocess.run(f'adb pull /sdcard/findCat.png {path}', stderr=subprocess.PIPE)
def updateImg():
    pull_screenshot()
    img_rgb = cv2.imread(f'{path}/findCat.png', img_type)
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
    return img, (min_loc[0] + template_size[1] // 2, min_loc[1] +  template_size[0] // 2),(round(min_val,4), round(max_val,4))

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
    
def findBySIFT(img,template,MIN_MATCH_COUNT = 10):
  sift = cv2.xfeatures2d.SIFT_create()
  # find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(template,None)
  kp2, des2 = sift.detectAndCompute(img,None)
  flann = cv2.BFMatcher()
  matches = flann.knnMatch(des1,des2,k=2)

  # store all the good matches as per Lowe's ratio test.
  good = []
  for m,n in matches:
      if m.distance < 0.5*n.distance:
          good.append(m)
  if len(good)>MIN_MATCH_COUNT:
      src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      matchesMask = mask.ravel().tolist()
      template_size = template.shape
      h, w = template_size[0:2]
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts,M)
      
      img2 = cv2.polylines(img,[np.int32(dst)],True,(255,255,255),4, cv2.LINE_AA)
      
      # Finally we draw our inliers (if successfully found the object) or matching keypoints (if failed).
      # draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                         # singlePointColor = None,
                         # matchesMask = matchesMask, # draw only inliers
                         # flags = 2)

      # img3 = cv2.drawMatches(template,kp1,img,kp2,good,None,**draw_params)
      cv2.imwrite(f'{path}/found.png', img2)
      w1,w2,w3,w4 = [i[0]//1 for i in dst] #逆时针
      return True,(w3-w1) / 2 + w1
  else:
      #print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
      return False,[len(good),MIN_MATCH_COUNT]
def findTemplateAndClick2(Template,Template_size):
    img_rgb = updateImg()
    search_data = findBySIFT(img_rgb,Template)
    isMatch = search_data[0]
    if isMatch:
        print(" "*100, end='\r')
        print(f"本次点击座标为：{search_data[1]}")
        click(search_data[1])
        time.sleep(0.1)
        return True,search_data[1]
    else:
        print(f"最佳匹配度：{search_data[1][0]}，要求匹配度：{search_data[1][1]}, 匹配度不足！{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", end='\r')
        time.sleep(0.1)
        return findTemplateAndClick2(Template,Template_size)
def findTemplateAndClick(Template,Template_size):
    img_rgb = updateImg()
    search_data = search(img_rgb,Template,Template_size)
    minMatchLevel, maxMatchLevel = search_data[2]
    matchLevel = minMatchLevel
    if(matchLevel <= 0.01):
        print(" "*100, end='\r')
        print(f"最佳匹配度：{matchLevel}, 本次点击座标为：{search_data[1]}")
        click(search_data[1])
        time.sleep(0.1)
        return True,search_data[1]
    else:
        print(f"最佳匹配度：{matchLevel}, 匹配度不足！{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", end='\r')
        time.sleep(0.1)
        return findTemplateAndClick(Template,Template_size)

def loadTemplate():
    global GetCatCoinTemplate,GetCatCoinTemplate_size
    global GoShopTemplate,GoShopTemplate_size
    global ClickCatTemplate,ClickCatTemplate_size
    global HappyGetCoinTemplate,HappyGetCoinTemplate_size
    #匹配领猫币
    GetCatCoinTemplate = cv2.imread(f'{path}/GetCatCoin.png', img_type)
    #去店铺
    GoShopTemplate = cv2.imread(f'{path}/GoShop.png', img_type)
    #点击得喵币
    ClickCatTemplate = cv2.imread(f'{path}/ClickCat.png', img_type)
    #开心收下
    HappyGetCoinTemplate = cv2.imread(f'{path}/HappyGetCoin.png', img_type)
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
        findTemplateAndClick2(GetCatCoinTemplate,GetCatCoinTemplate_size)
        time.sleep(0.3)
        findTemplateAndClick2(GoShopTemplate,GoShopTemplate_size)
        time.sleep(10.5)
        findTemplateAndClick2(ClickCatTemplate,ClickCatTemplate_size)
        #time.sleep(0.3)
        #findTemplateAndClick(HappyGetCoinTemplate,HappyGetCoinTemplate_size)
        keyEvent(4)
        time.sleep(0.3)
        print(f'已找到{i+1}只猫猫, 还剩{num-i-1}只猫猫！')
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