from raytracer import Ray
from opticalelement import OpticalElement
from refracting_surfaces import SphericalRefraction
from outputplane import OutputPlane
import numpy as np
import matplotlib.pyplot as plt
 
#testing py where i test out stuff to see if it works before investigation
r1 = Ray([0.1,0.0,0.0],[0.0,0.0,1.0])
r2 = Ray([5.0,0.0,0.0],[-0.05,0.0,1.0])
r0 = Ray([2.5,0.0,0.0],[0.05,0.0,1.0])

s = SphericalRefraction(100.0,0.03,1.0,1.5,30)
o = OutputPlane(250.0)

s.propagate_ray(r0)
o.propagate_ray(r0)
s.propagate_ray(r1)
o.propagate_ray(r1)
s.propagate_ray(r2)
o.propagate_ray(r2)
#print(r1.vertices())
#print(r1.vertices()[2][0][2])
x0=[r0.vertices()[0][0],r0.vertices()[1][0],r0.vertices()[2][0]]
z0=[r0.vertices()[0][2],r0.vertices()[1][2],r0.vertices()[2][2]]

x1=[r1.vertices()[0][0],r1.vertices()[1][0],r1.vertices()[2][0]]
z1=[r1.vertices()[0][2],r1.vertices()[1][2],r1.vertices()[2][2]]

x2=[r2.vertices()[0][0],r2.vertices()[1][0],r2.vertices()[2][0]]
z2=[r2.vertices()[0][2],r2.vertices()[1][2],r2.vertices()[2][2]]

plt.grid()
plt.title('Example Rays')
plt.xlabel("z (mm)")
plt.ylabel('x (mm)')
plt.plot(z0,x0)
plt.plot(z1,x1)
plt.plot(z2,x2)
plt.show()
#x=mz+c for the straight line ray from lens to outputplane, but find z when x = 0
#point A = (a,b), point B = (c,d) (axis=(z,x)), m=(d-b)/(c-a), focus=(0-b)/m +a
focusestimate=(0-x1[1])/((x1[2]-x1[1])/(z1[2]-z1[1]))+z1[1]
print("Estimated Paraxial Focus= %.7e" %(focusestimate-100))
focusexpected=(1.5*0.03**-1)/(1.5-1.0)
print("Expected Paraxial Focus= %.7e" %(focusexpected))

r3 = Ray([5.0,0.0,0.0],[0.0,0.0,1.0])
o=OutputPlane(focusestimate)
s.propagate_ray(r3)
o.propagate_ray(r3)

x3=[r3.vertices()[0][0],r3.vertices()[1][0],r3.vertices()[2][0]]
z3=[r3.vertices()[0][2],r3.vertices()[1][2],r3.vertices()[2][2]]

r4 = Ray([2.5,0.0,0.0],[0.0,0.0,1.0])
s.propagate_ray(r4)
o.propagate_ray(r4)
x4=[r4.vertices()[0][0],r4.vertices()[1][0],r4.vertices()[2][0]]
z4=[r4.vertices()[0][2],r4.vertices()[1][2],r4.vertices()[2][2]]

r5 = Ray([5.0,0.0,0.0],[-0.05,0.0,1.0])
r6 = Ray([2.5,0.0,0.0],[-0.05,0.0,1.0])
s.propagate_ray(r5)
s.propagate_ray(r6)
o.propagate_ray(r5)
o.propagate_ray(r6)
x5=[r5.vertices()[0][0],r5.vertices()[1][0],r5.vertices()[2][0]]
z5=[r5.vertices()[0][2],r5.vertices()[1][2],r5.vertices()[2][2]]
x6=[r6.vertices()[0][0],r6.vertices()[1][0],r6.vertices()[2][0]]
z6=[r6.vertices()[0][2],r6.vertices()[1][2],r6.vertices()[2][2]]

plt.grid()
plt.title('Simple test cases')
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
plt.plot(z5,x5,color='blue')
plt.plot(z4,x4,color='red')
plt.plot(z6,x6,color='blue')
plt.plot(z3,x3,color='red')
plt.show()

o=OutputPlane(250.0)
r7=Ray([2.0,0.0,0.0],[0.0,0.0,1.0])
r8=Ray([-2.0,0.0,0.0],[0.0,0.0,1.0])
r9=Ray([20.0,0.0,0.0],[0.0,0.0,1.0])
r10=Ray([-20.0,0.0,0.0],[0.0,0.0,1.0])
r11=Ray([29.0,0.0,0.0],[0.0,0.0,1.0])
r12=Ray([-29.0,0.0,0.0],[0.0,0.0,1.0])

rlist=[r7,r8,r9,r10,r11,r12]
x7=[]
x8=[]
x9=[]
x10=[]
x11=[]
x12=[]
z7=[]
z8=[]
z9=[]
z10=[]
z11=[]
z12=[]
xlist=[x7,x8,x9,x10,x11,x12]
zlist=[z7,z8,z9,z10,z11,z12]
for i in range(len(rlist)):
    s.propagate_ray(rlist[i])
    o.propagate_ray(rlist[i])
    xlist[i].append(rlist[i].vertices()[0][0])
    xlist[i].append(rlist[i].vertices()[1][0])
    xlist[i].append(rlist[i].vertices()[2][0])
    zlist[i].append(rlist[i].vertices()[0][2])
    zlist[i].append(rlist[i].vertices()[1][2])
    zlist[i].append(rlist[i].vertices()[2][2])

plt.figure()
plt.grid()
plt.title("")
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
plt.plot(z7,x7,color='blue')
plt.plot(z8,x8,color='blue')
plt.plot(z9,x9,color='red')
plt.plot(z10,x10,color='red')
plt.plot(z11,x11,color='green')
plt.plot(z12,x12,color='green')
plt.show()


'''
#to try out how the bundle will work, this is implemented into the beam class in beambundle.py
def rms(listx,listy):
    squaresum=0
    for k in range(len(listx)):
        squaresum += listx[k]**2 + listy[k]**2
    
    return np.sqrt(squaresum/len(listx))

def lensmaker(nrefrac,cur1,cur2,d):
    return ((nrefrac-1)*(cur1-cur2+((nrefrac-1)*d*cur1*cur2)/nrefrac))**(-1)   

pointsonz0x=[]
pointsonz0y=[]
pointsonfocusx=[]
pointsonfocusy=[]

#for single surface 
def beam(a,d,c,colour): #radius,direction,displacement from origin, color of graph)
    for i in range(a+1): #for every radius at initial points for rays
        for j in range(-(3*i+1),3*i+1): #initial points for rays at radius
            rr = Ray([i*np.cos(np.pi*j/(3*i+1))+c,i*np.sin(np.pi*j/(3*i+1))+c,0.0],[d,0.0,1.0])
            ss = SphericalRefraction(100.0,0.03,1.0,1.5,30)
            oo = OutputPlane(200.0)
    
            ss.propagate_ray(rr)
            oo.propagate_ray(rr)
    
            xx=[rr.vertices()[0][0],rr.vertices()[1][0],rr.vertices()[2][0]]
            zz=[rr.vertices()[0][2],rr.vertices()[1][2],rr.vertices()[2][2]]

            pointsonz0x.append(rr.vertices()[0][0])
            pointsonz0y.append(rr.vertices()[0][1])
            pointsonfocusx.append(rr.vertices()[2][0])
            pointsonfocusy.append(rr.vertices()[2][1])

            #plt.plot(zz[1],xx[1],'x',color='black') #to visualise the intercepts
            plt.plot(zz,xx,color=colour) #plot the light ray

 

g='blue'

plt.figure()
plt.grid()
plt.title('Bundle of rays')
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
beam(5,0,0,g)
#beam(4,0.05,-4,g)
plt.ylim(-10,10)
plt.xlim(0,220)
#plt.show()

plt.figure(figsize=(9,4))
plt.suptitle('Spot Diagrams')
plt.subplot(1,2,1)
plt.grid()
plt.title('$z=0$')
plt.xlabel('x')
plt.ylabel('y')
plt.plot(pointsonz0x,pointsonz0y,'.',color=g)
plt.subplot(1,2,2)
plt.grid()
plt.title('focus')
plt.xlabel('x')
#plt.ylabel('y')
plt.plot(pointsonfocusx,pointsonfocusy,'.',color=g)
#plt.show()
print("RMS spot radius = %.3e mm" %(rms(pointsonfocusx,pointsonfocusy)))
print("Size of Geometrical Focus = %.3e mm^2" %(np.pi*rms(pointsonfocusx,pointsonfocusy)**2))

pointsonfocusx1=[]
pointsonfocusy1=[]
#for plano convex lens with plane side facing screen
def beam2(a,d,c,colour): #radius,direction,displacement from origin, color of graph)
    for i in range(a+1): #for every radius at initial points for rays
        for j in range(-(3*i+1),3*i+1): #initial points for rays at radius
            rr = Ray([i*np.cos(np.pi*j/(3*i+1))+c,i*np.sin(np.pi*j/(3*i+1))+c,0.0],[d,0.0,1.0])
            ss1 = SphericalRefraction(100.0,0.02,1.0,1.5168,10.1) #convex surface
            ss2 = SphericalRefraction(105.0,0.0,1.5168,1.0,10.1) #flat surface
            oo = OutputPlane(200.0)


            ss1.propagate_ray(rr)
            ss2.propagate_ray(rr)
            oo.propagate_ray(rr)
    
            xx=[rr.vertices()[0][0],rr.vertices()[1][0],rr.vertices()[2][0],rr.vertices()[3][0]]
            zz=[rr.vertices()[0][2],rr.vertices()[1][2],rr.vertices()[2][2],rr.vertices()[3][2]]
            
            
            pointsonz0x.append(rr.vertices()[0][0])
            pointsonz0y.append(rr.vertices()[0][1])
            
            pointsonfocusx1.append(rr.vertices()[3][0])
            pointsonfocusy1.append(rr.vertices()[3][1])
            
            #plt.plot(zz[1],xx[1],'x',color='black') #to visualise intercept
            #plt.plot(zz[2],xx[2],'x',color='black')
            plt.plot(zz,xx,color=colour) #plot the light ray

pointsonfocusx2=[]
pointsonfocusy2=[]
#for plano convex lens with convex side facing screen
def beam3(a,d,c,colour): #radius,direction,displacement from origin, color of graph)
    for i in range(a+1): #for every radius at initial points for rays
        for j in range(-(3*i+1),3*i+1): #initial points for rays at radius
            rr = Ray([i*np.cos(np.pi*j/(3*i+1))+c,i*np.sin(np.pi*j/(3*i+1))+c,0.0],[d,0.0,1.0])
            ss1 = SphericalRefraction(100.0,0.0,1.0,1.5168,10.1) #convex surface
            ss2 = SphericalRefraction(105.0,-0.02,1.5168,1.0,10.1) #flat surface
            oo = OutputPlane(200.0)


            ss1.propagate_ray(rr)
            ss2.propagate_ray(rr)
            oo.propagate_ray(rr)
    
            xx=[rr.vertices()[0][0],rr.vertices()[1][0],rr.vertices()[2][0],rr.vertices()[3][0]]
            zz=[rr.vertices()[0][2],rr.vertices()[1][2],rr.vertices()[2][2],rr.vertices()[3][2]]
            
            
            pointsonz0x.append(rr.vertices()[0][0])
            pointsonz0y.append(rr.vertices()[0][1])
            
            pointsonfocusx2.append(rr.vertices()[3][0])
            pointsonfocusy2.append(rr.vertices()[3][1])
            
            #plt.plot(zz[1],xx[1],'x',color='black') #to visualise intercept
            #plt.plot(zz[2],xx[2],'x',color='black')
            plt.plot(zz,xx,color=colour) #plot the light ray
            


plt.figure(figsize=(6,8))
plt.subplot(2,1,2)
plt.grid()
plt.title('Plano-Convex Lens with convex side facing screen')
plt.xlabel('z (mm)')
plt.ylabel('x (mm)')
beam3(5,0,0,'red')
plt.ylim(-6,6)
plt.xlim(0,220)
plt.subplot(2,1,1)
plt.grid()
plt.title('Plano-Convex Lens with plane side facing screen')
#plt.xlabel('z (mm)')
plt.ylabel('x (mm)')
beam2(5,0,0,'blue')
plt.ylim(-6,6)
plt.xlim(0,220)
#plt.show()
print("Estimated Paraxial Focus = %.3e" %(lensmaker(1.5168,0.02,0,5)))
print("RMS spot radius for plane side facing screen = %.3e mm" %(rms(pointsonfocusx1,pointsonfocusy1)))
print("Size of Geometrical Focus = %.3e mm^2" %(np.pi*(rms(pointsonfocusx1,pointsonfocusy1)**2)))
print("RMS spot radius for convex side facing screen = %.3e mm" %(rms(pointsonfocusx2,pointsonfocusy2)))
print("Size of Geometrical Focus = %.3e mm^2" %(np.pi*(rms(pointsonfocusx2,pointsonfocusy2)**2)))
'''
