import math
import numpy as np
import matplotlib as plt

points = open("E:/PythonScripts/Project TAS/noisefilteredPoints.txt","r", encoding='utf-8-sig')
lines = points.readlines()
points.close()
xlist = []
ylist = []
for line in lines:
    columns = line.split(" ")
    if len(line.strip())>0:
        x = round(float(columns[0].strip()),4)
        y = round(float(columns[1].strip()),4)
        xlist.append(x)
        ylist.append(y)

#print(xlist,ylist)
a1 = round(math.sqrt(xlist[0]**2+ylist[0]**2),4)
a2 = round(math.sqrt(xlist[1]**2+ylist[1]**2),4)
a3 = round(math.sqrt(xlist[2]**2+ylist[2]**2),4)

b1 = round(math.sqrt((400-xlist[0])**2+ylist[0]**2),4)
b2 = round(math.sqrt((400-xlist[1])**2+ylist[1]**2),4)
b3 = round(math.sqrt((400-xlist[2])**2+ylist[2]**2),4)

#print(a1,a2,a3)
#print(b1,b2,b3)

points2 = open("E:/PythonScripts/Project TAS/NoisefilteredData.txt","r", encoding='utf-8-sig')
lines2 = points2.readlines()
points2.close()
xlistOG = []
ylistOG = []
for line2 in lines2:
    columns2 = line2.split(" ")
    if len(line2.strip())>0:
        xOG = round(float(columns2[0].strip()),4)
        yOG = round(float(columns2[1].strip()),4)
        xlistOG.append(xOG)
        ylistOG.append(yOG)
#print(xlistOG,ylistOG)

xlistRaw = []
ylistRaw = []
for i in range(0,3):
    x = xlistOG[i]
    xlistRaw.append(x)
    y = ylistOG[i]
    ylistRaw.append(y)
print(xlistRaw)
print(ylistRaw)
xscatter = []
yscatter = []
totsmallest = 1
totsmallest2 = 1
totsmallest3 = 1
totsmallest4 = 1
for k in range(-2000,0):
    for l in range(-2000,2000):
        #print(i,j)
        i = k
        j = l
        da1 = round(math.sqrt((i-xlistOG[0])**2+(ylistOG[0]-j)**2),4)
        da2 = round(math.sqrt((i-xlistOG[1])**2+(ylistOG[1]-j)**2),4)
        da3 = round(math.sqrt((i-xlistOG[2])**2+(ylistOG[2]-j)**2),4)
        #print(abs(da1-a1),abs(da2-a2),abs(da3-a3))
        if abs(da1-a1)<2 and abs(da2-a2)<2 and abs(da3-a3)<2:
            tot = math.sqrt(abs(da1-a1)**2+abs(da2-a2)**2+abs(da3-a3)**2)
            if tot<totsmallest:
                totsmallest = tot
                xsmallest = i
                ysmallest = j
                #print("a point with coordinates x=",i,"and y=",j,"is close to the leading edge")

print("Leading edge step 1 done...(",xsmallest,ysmallest,")")
u = (xsmallest-100)*10
b = (xsmallest+100)*10
uy = (ysmallest-100)*10
by = (xsmallest+100)*10
for k2 in range(int(u),int(b)):
    for l2 in range(int(uy),int(by)):
        #print(i,j)
        i = k2/10
        j = l2/10
        da1 = round(math.sqrt((i-xlistOG[0])**2+(ylistOG[0]-j)**2),4)
        da2 = round(math.sqrt((i-xlistOG[1])**2+(ylistOG[1]-j)**2),4)
        da3 = round(math.sqrt((i-xlistOG[2])**2+(ylistOG[2]-j)**2),4)
        #print(abs(da1-a1),abs(da2-a2),abs(da3-a3))
        if abs(da1-a1)<2 and abs(da2-a2)<2 and abs(da3-a3)<2:
            tot = math.sqrt(abs(da1-a1)**2+abs(da2-a2)**2+abs(da3-a3)**2)
            if tot<totsmallest2:
                totsmallest2 = tot
                xsmallest2 = i
                ysmallest2 = j
                print("a point with coordinates x=",i,"and y=",j,"is close to the leading edge")

print("Leading edge step 2 done...(",xsmallest2,ysmallest2,")")

u = (xsmallest2-10)*100
b = (xsmallest2+10)*100
uy = (ysmallest2-10)*100
by = (xsmallest2+10)*100

for k in range(u,b):
    for l in range(uy,by):
        #print(i,j)
        i = k/100
        j = l/100
        da1 = round(math.sqrt((i-xlistOG[0])**2+(ylistOG[0]-j)**2),4)
        da2 = round(math.sqrt((i-xlistOG[1])**2+(ylistOG[1]-j)**2),4)
        da3 = round(math.sqrt((i-xlistOG[2])**2+(ylistOG[2]-j)**2),4)
        #print(abs(da1-a1),abs(da2-a2),abs(da3-a3))
        if abs(da1-a1)<1 and abs(da2-a2)<1 and abs(da3-a3)<1:
            tot = math.sqrt(abs(da1-a1)**2+abs(da2-a2)**2+abs(da3-a3)**2)
            if tot<totsmallest3:
                totsmallest3 = tot
                xsmallest3 = i
                ysmallest3 = j

print("Leading edge step 3 done...")
for k in range((xsmallest3-0.5)*1000,(xsmallest3+0.5)*1000):
    for l in range((ysmallest3-0.5)*1000,(xsmallest3+0.5)*1000):
        #print(i,j)
        i = k/1000
        j = l/1000
        da1 = round(math.sqrt((i-xlistOG[0])**2+(ylistOG[0]-j)**2),4)
        da2 = round(math.sqrt((i-xlistOG[1])**2+(ylistOG[1]-j)**2),4)
        da3 = round(math.sqrt((i-xlistOG[2])**2+(ylistOG[2]-j)**2),4)
        #print(abs(da1-a1),abs(da2-a2),abs(da3-a3))
        if abs(da1-a1)<0.05 and abs(da2-a2)<0.05 and abs(da3-a3)<0.05:
            tot = math.sqrt(abs(da1-a1)**2+abs(da2-a2)**2+abs(da3-a3)**2)
            if tot<totsmallest4:
                totsmallest4 = tot
                xsmallest4 = i
                ysmallest4 = j

print("leading edge has error: ",totsmallest, "at x = ",xsmallest4,",y = ",ysmallest4)
totsmallestT = 1
for k in range(-468000,-465000):
    for l in range(610000,613000):
        #print(i,j)
        i = k/1000
        j = l/1000
        db1 = round(math.sqrt((xlistOG[0]-i)**2+(j-ylistOG[0])**2),4)
        db2 = round(math.sqrt((xlistOG[1]-i)**2+(j-ylistOG[1])**2),4)
        db3 = round(math.sqrt((xlistOG[2]-i)**2+(j-ylistOG[2])**2),4)
        #print(abs(da1-a1),abs(da2-a2),abs(da3-a3))
        if abs(db1-b1)<0.05 and abs(db2-b2)<0.05 and abs(db3-b3)<0.05:
            totT = math.sqrt(abs(db1-b1)**2+abs(db2-b2)**2+abs(db3-b3)**2)
            if totT<totsmallestT:
                totsmallestT = totT
                xsmallestT = i
                ysmallestT = j
                #print("a point with coordinates x=",i,"and y=",j,"is close to the trailing edge")

print("trailing edge has error: ",totsmallestT, "at x = ",xsmallestT,",y = ",ysmallestT)

            




