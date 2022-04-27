from raytracer import Ray
from opticalelement import OpticalElement
from refracting_surfaces import SphericalRefraction
from outputplane import OutputPlane
import numpy as np
import matplotlib.pyplot as plt
from beambundle import beam
from scipy import optimize

#task12-13
d = beam(5,[0,0],[0,0])
d.surface(100.0,0.03,1.0,1.5,30).output(200.0).lettherebelight()
plt.figure()
plt.grid()
plt.title('Bundle of rays')
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
d.xzbeamplot('blue')
#beam(4,0.05,-4,g)
plt.xlim(0,220)
#plt.show()
d.spotdiagram('blue')

e=beam(5,[0.05,0],[-4,0])
e.surface(100.0,0.03,1.0,1.5,30).output(200.0).lettherebelight()
plt.figure()
plt.grid()
plt.title('Bundle of rays')
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
e.xzbeamplot('red')
plt.xlim(0,220)
#plt.show()
e.spotdiagram('red')




diameterrange=[1,2,3,4,5,6,7,8,9,10]
'''
def performance2(l):
    rmsvalue1=[] #rms values for convex side facing input
    diffractionimit1=[] #diffraction limit
    for l in diameterrange:
        convexinput = beam(l,0,0)
        convexinput.surface(100.0,0.03,1.0,1.5,30).output(200.0).lettherebelight()
        rmsvalue1.append(convexinput.rms())
        diffractionimit1.append(558e-6*d.focusestimate()/(l))
    return [rmsvalue1,diffractionimit1]


plt.figure()
plt.grid()
plt.title("Performance of single spherical surface")
plt.xlabel("Radius of beam (mm)")
plt.ylabel("RMS (mm)")
plt.plot(diameterrange,performance2(diameterrange)[0],'x',label='Single Spherical Surface',color='blue')
plt.plot(diameterrange,performance2(diameterrange)[1],'.',label='Diffraction Limit',color='blue')
plt.legend(loc='best')
#plt.show()
'''
#task13-14
print("RMS spot radius = %.3e mm" %(d.rms()))
print("Size of Geometrical Focus = %.3e mm^2" %(np.pi*(d.rms())**2))
print("Estimated Focal Point = %.3e" %(d.focusestimate()))

#task15
b = beam(10,[0,0],[0,0])
c = beam(10,[0,0],[0,0])
b.surface(100.0,0.02,1.0,1.5168,10.1).surface(105.0,0.0,1.5168,1.0,10.1).output(b.focusestimate()).lettherebelight()
c.surface(100.0,0.0,1.0,1.5168,10.1).surface(105.0,-0.02,1.5168,1.0,10.1).output(c.focusestimate()).lettherebelight()

plt.figure(figsize=(6,8))
plt.subplot(2,1,1)
plt.grid()
plt.title('Plano-Convex Lens with convex side facing input')
#plt.xlabel('z (mm)')
plt.ylabel('x (mm)')
b.xzbeamplot('blue')
plt.ylim(-6,6)
plt.xlim(0,220)
plt.subplot(2,1,2)
plt.grid()
plt.title('Plano-Convex Lens with plane side facing input')
plt.xlabel('z (mm)')
plt.ylabel('x (mm)')
c.xzbeamplot('red')
plt.ylim(-6,6)
plt.xlim(0,220)
#plt.show()
#b.spotdiagram('blue')
#c.spotdiagram('red')

print("For Plano-Convex Lens with convex side facing input:")
print("- RMS spot radius = %.3e mm" %(b.rms()))
print("- Size of Geometrical Focus = %.3e mm^2" %(np.pi*(b.rms())**2))
print("- Estimated Focal Point = %.3e \n" %(b.focusestimate()-102.5))

print("For Plano-Convex Lens with plane side facing input:")
print("- RMS spot radius = %.3e mm" %(c.rms()))
print("- Size of Geometrical Focus = %.3e mm^2" %(np.pi*(c.rms())**2))
print("- Estimated Focal Point = %.3e" %(c.focusestimate()-102.5))

#rangeradius=[1,2,3,4,5] #range of radius
def performance(l):
    rmsvalue1=[] #rms values for convex side facing input
    rmsvalue2=[] #rms values for plane side facing input
    diffractionimit1=[] #diffraction limit
    diffractionimit2=[]
    for l in diameterrange:
        convexinput = beam(l,[0,0],[0,0])
        planeinput = beam(l,[0,0],[0,0])
        convexinput.surface(100.0,0.02,1.0,1.5168,10.1).surface(105.0,0.0,1.5168,1.0,10.1).output(b.focusestimate()).lettherebelight()
        planeinput.surface(100.0,0.0,1.0,1.5168,10.1).surface(105.0,-0.02,1.5168,1.0,10.1).output(c.focusestimate()).lettherebelight()
        rmsvalue1.append(convexinput.rms())
        rmsvalue2.append(planeinput.rms())
        diffractionimit1.append(558e-6*(b.focusestimate()-102.5)/(l))
        diffractionimit2.append(558e-6*(c.focusestimate()-102.5)/(l))
    return [rmsvalue1,rmsvalue2,diffractionimit1,diffractionimit2]

plt.figure()
plt.grid()
plt.title("Performance of the plano-convex lens")
plt.xlabel("Diameter of beam (mm)")
plt.ylabel("RMS (mm)")
plt.plot(diameterrange,performance(diameterrange)[0],'x',label='Plano-Convex Lens with convex side facing input (Lens 1)',color='blue')
plt.plot(diameterrange,performance(diameterrange)[1],'x',label='Plano-Convex Lens with plane side facing input (Lens 2)',color='red')
plt.plot(diameterrange,performance(diameterrange)[2],'.',label='Diffraction Limit for Lens 1',color='blue')
plt.plot(diameterrange,performance(diameterrange)[3],'.',label='Diffraction Limit for Lens 2',color='red')
plt.legend(loc='best')
#plt.show()

#lens optimization
def lensoptimise(cur):
    opbeam = beam(10,[0,0],[0,0])
    opbeam.surface(100.0,cur[0],1.0,1.5168,10.1).surface(105.0,cur[1],1.5168,1.0,10.1).output(202.5).lettherebelight()
    return opbeam.rms()

minimum=optimize.fmin_tnc(lensoptimise,np.array([0.001,-0.001]),bounds=[(-0.1,0.1),(-0.1,0.1)],approx_grad=True)
print("- The optimised values of curvatures are: %.3e mm^-1, %.3e mm^-1" %(minimum[0][0],minimum[0][1]))
#print("- The focus point is at %.3e mm from origin" %(lensmaker(1.5168,minimum[0][0],minimum[0][1],5)))
print("- The corresponding rms value = %.3e mm" %(lensoptimise([minimum[0][0],minimum[0][1]])))

'''
#see how initial guess changes optimisation
guesslist=np.linspace(0.001,0.01,50)
curvaturelist=[]
rmslist=[]
for bou in guesslist:
    minimum=optimize.fmin_tnc(lensoptimise,np.array([bou,-bou]),bounds=[(-0.1,0.1),(-0.1,0.1)],approx_grad=True)
    curvaturelist.append([minimum[0][0],minimum[0][1]])
    rmslist.append(lensoptimise([minimum[0][0],minimum[0][1]]))

#print(rmslist)
plt.figure()
plt.plot(guesslist,rmslist)
plt.show()
'''





#trying to plot contour map
def contourmap(curve1,curve2):
    curvaturevalues=[]
    rmsvalues=[]
    for i in curve1:
        rmsvaluesrow=[]
        c=[]
        for j in curve2:
            opbeam1 = beam(5,[0,0],[0,0])
            opbeam1.surface(100.0,i,1.0,1.5168,100).surface(105.0,j,1.5168,1.0,100).output(202.5).lettherebelight()
            rmsvaluesrow.append(opbeam1.rms())
            c.append([i,j])
        rmsvalues.append(rmsvaluesrow)
        curvaturevalues.append(c)
    return rmsvalues, curvaturevalues

curvatures1=np.linspace(0.0045,0.0145,30)
curvatures2=-curvatures1
x,y=np.meshgrid(curvatures1,curvatures2)
z=contourmap(curvatures1,curvatures2)[0]
zz=contourmap(curvatures1,curvatures2)[1]

#find the minimas
minimas=[]
for g in range(len(z)):
    for counter, h in enumerate(z[g]):
        if h == min(z[g]):
            minimas.append(zz[g][counter])
minimax=[]
minimay=[]
for s in range(len(minimas)):
    minimax.append(minimas[s][0])
    minimay.append(minimas[s][1])
#print(minimas)

#contour and minima plots

plt.figure()
plt.xlabel('curvature 1 ($mm^{-1}$)')
plt.ylabel('curvature 2 ($mm^{-1}$)')
plt.contourf(x,y,z,500)
#plt.plot(minimax,minimay,'x',color='black')
#plt.plot(minimax,minimay,'-',color='white')
plt.colorbar().set_label('RMS (mm)')
plt.show()

plt.figure()
plt.xlabel('curvature 1 ($mm^{-1}$)')
plt.ylabel('curvature 2 ($mm^{-1}$)')
plt.contour(x,y,z,levels=(0.0075,0.01,0.03,0.05,0.07,0.1))
#plt.plot(minimax,minimay,'x',color='black')
#plt.plot(minimax,minimay,'-',color='white')
plt.colorbar().set_label('RMS (mm)')
plt.show()



'''
#plotting the beam through optimzed lens
optimisedbeam=beam(10,[0,0],[0,0])
optimisedbeam.surface(100.0,minimum[0][0],1.0,1.5168,10.1).surface(105.0,minimum[0][1],1.5168,1.0,10.1).output(202.5).lettherebelight()
plt.figure()
plt.grid()
plt.title("Optimized lens")
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
optimisedbeam.xzbeamplot('green')
plt.show()
#optimisedbeam.spotdiagram('green')
'''