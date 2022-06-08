import numpy as np
from matplotlib import pyplot as plt 
import streamlit as st
from PIL import Image
import math
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


# 画像のupload
upload_file = st.file_uploader("Choose a file", type=['jpg', 'png', 'jpeg'])

def load_image(image_file):
	img = Image.open(image_file)
	return img


if upload_file is not None:
  try:
        # To See details
        file_details = {"filename":upload_file.name, "filetype":upload_file.type,
                        "filesize":upload_file.size}
        st.write(file_details)

        # To View Uploaded Image
        st.image(load_image(upload_file),width=200)
  except:
    pass
        
        
border_number = st.number_input('閾値を入力', value=50)
        
# 平面画像処理
def imgfile2xy(filename):
  threshold=border_number
  img = np.array(Image.open(filename).convert('L').resize((200, 200)))
  img_bool = img > threshold
  x = np.array([])
  y = np.array([])
  for i in range(img_bool.shape[0]):
    for j in range(img_bool.shape[1]):
      if img_bool[i,j]==False:
        x=np.append(x, j)
        y=np.append(y, (img_bool.shape[0]-1)-i)
  
  return np.concatenate([[x], [y]])

if border_number is not None:
  try:
    img = imgfile2xy(upload_file)

    fig, ax = plt.subplots()
    ax.scatter(img[0], img[1], s=1, color="black")
    ax.axis('equal')
    st.pyplot(fig)
  except:
    pass

value = [0, 1, 2, 3, 4, 5]
key = ['拡大・縮小', '回転', '剪断', 'y軸基準鏡映', 'x軸基準鏡映', '平行移動']

opt_dic = dict(zip(key, value))

option = st.multiselect(
    '処理を選択してください(複数選択可)',
    ['拡大・縮小', '回転', '剪断', 'y軸基準鏡映', 'x軸基準鏡映', '平行移動']
)

if option is not None:
  try:
    o_l = [opt_dic[o] for o in option]
    st.write(o_l[0])

    n = 0
    fig = plt.figure()
    ims = []

    number = st.number_input('Insert a number')

    # for i in range(100):
    n = number

    # 拡大縮小
    A0=np.array([
                [1+n/10, 0, 0],
                [0, 1-n/10, 0],
                [0, 0, 1]
    ])

    # 回転
    A1=np.array([
                [math.cos(math.radians(n)), -math.sin(math.radians(n)), 0],
                [math.sin(math.radians(n)), math.cos(math.radians(n)), 0],
                [0, 0, 1]
    ])

    # 剪断
    A2=np.array([
                [1, math.tan(math.radians(n)), 0],
                [0, 1, 0],
                [0, 0, 1]
    ])

    # y軸鏡映
    A3=np.array([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
    ])
        
    # x軸鏡映
    A4=np.array([
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
    ])

        
    # 平行移動
    A5=np.array([
                [1, 0, n],
                [0, 1, 0],
                [0, 0, 1]
    ])

    A_l = [A0, A1, A2, A3, A4, A5]

    U_A_l = [A_l[o] for o in o_l]

    ims = []

    for i in range(len(U_A_l)-1):
        U_A_l[0] = np.dot(U_A_l[0], U_A_l[1])
        del U_A_l[1]

    img_ = np.insert(img, 2, 1, axis=0)
    imgnew = np.dot(U_A_l, img_)
    imgnew = np.squeeze(imgnew)
    imgnew=np.delete(imgnew, 2, axis=0)
    # st.write(imgnew)
    fig, ax = plt.subplots()
    ax.scatter(imgnew[0], imgnew[1], s=1, color="black")
    ax.axis('equal')
    st.pyplot(fig)
  except:
    pass
  # ims.append(fig)

  # fig, ax = plt.subplots()

  # st.write(ims)
  # st.pyplot(ims[55])  
  #ArtistAnimation機能で，imsの中の画像を繋ぎ合わせる．
  # ani = animation.ArtistAnimation(fig, ims, interval = 100)

  # #imagemagickを使って，gif画像を保存
  # ani.save("test.mp4", writer="ffmpeg")