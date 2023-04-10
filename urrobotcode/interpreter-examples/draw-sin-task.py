import numpy as np
import matplotlib.pyplot as plt

#sin그래프 그리기
x = np.linspace(0, 2*np.pi, 50)
z = np.sin(x) / 10

#sin그래프 확인
plt.plot(x, z)
plt.show()

#ur로봇용 좌표값으로 변경
a = np.arange(-.350, .350, 0.014)
b = z + (.406850164907)

#commands.txt에 넣을 양식으로 만들기
for n1, n2 in zip(a, b):
    print("movej(p[", n1 ,  ", -.474135937785, ", n2 , ", -.002413342538, 2.223964959773, -2.216468912013],a=1,v=1.05,t=0,r=0)", sep='', end='\n')


#Terminal에서 실행 코드 : python sendInterpreterFromFile.py 192.168.213.79 commands.txt -v