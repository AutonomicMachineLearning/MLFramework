from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.models import Sequential

#4. 모델 구성하기
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(24, 24, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))

# json 형태로 모델 정보 출력 및 txt파일로 저장
json = model.to_json()
print("json : ", json)
fw = open('sample.txt', 'w')
fw.write(json)
fw.close()

# 모델 아키텍처 보기
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

%matplotlib inline

SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))