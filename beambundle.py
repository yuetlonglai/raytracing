from raytracer import Ray
from opticalelement import OpticalElement
from refracting_surfaces import SphericalRefraction
from outputplane import OutputPlane
import numpy as np
import matplotlib.pyplot as plt

class beam(OpticalElement): #class for generating a beam of light through lens system
    def __init__(self,diameter,direction=[0.0,0.0],displacement=[0.0,0.0]):
        self._points=[Ray([0.0+displacement[0],0.0+displacement[1],0.0],[direction[0],direction[1],1.0])]
        self._surfaces = []
        self._endplane=[]
        self._x=[]
        self._y=[]
        self._z=[]
        self._pointsonz0x=[]
        self._pointsonz0y=[]
        self._pointsonfocusx=[]
        self._pointsonfocusy=[]
        self._outputz=200.0
        for i in range(1,diameter+1): #for every radius at initial points for rays
            for j in range(6*i): #initial points for rays at radius
                p = Ray([(i/2)*np.cos(2*np.pi*j/(6*i))+displacement[0],(i/2)*np.sin(2*np.pi*j/(6*i))+displacement[1],0.0],[direction[0],direction[1],1.0])
                self._points.append(p)
        
    def surface(self, z, cur, n11, n22, ar): #define refracting surface
        s = SphericalRefraction(z, cur, n11, n22, ar)
        self._surfaces.append(s)
        return self

    def output(self,e): #define output plane
        self._outputz = e #where the output plane is
        o = OutputPlane(e)
        self._endplane.append(o)
        return self

    def lettherebelight(self): #propagate all light rays
        for i in range(len(self._points)): #propagate every initial points
            for j in range(len(self._surfaces)):
                self._surfaces[j].propagate_ray(self._points[i]) #append a list of surfaces
            self._endplane[0].propagate_ray(self._points[i])
            
            x=[]
            y=[]
            z=[]
            for k in range(len(self._points[i].vertices())): #make list of x y z coordinates of points
                x.append(self._points[i].vertices()[k][0]) 
                y.append(self._points[i].vertices()[k][1])
                z.append(self._points[i].vertices()[k][2])
                
            self._x.append(x)
            self._y.append(y)
            self._z.append(z)
            
            #spot coordinates for spot diagram
            self._pointsonz0x.append(self._points[i].vertices()[0][0])
            self._pointsonz0y.append(self._points[i].vertices()[0][1])
            self._pointsonfocusx.append(self._points[i].vertices()[-1][0])
            self._pointsonfocusy.append(self._points[i].vertices()[-1][1])
        
    
    def xzbeamplot(self,colour): #plot beam of light rays on xz plane
        for i in range(len(self._x)):
            plt.plot(self._z[i],self._x[i],'-',color=colour)
            #plt.plot(self._z[i],self._x[i],'x',color='black') #plotting intercepts

    def yzbeamplot(self,colour): #plot beam of light rays on yz plane
        for i in range(len(self._y)):
            plt.plot(self._z[i],self._y[i],'-',color=colour)
            #plt.plot(self._z[i],self._y[i],'x',color='black') #plotting intercepts

    def spotdiagram(self,colour): #plot spot diagram
        plt.figure(figsize=(9,4))
        plt.suptitle('Spot Diagrams')
        plt.subplot(1,2,1)
        plt.grid()
        plt.title('$z=0$')
        plt.xlabel('x (mm)')
        plt.ylabel('y (mm)')
        plt.plot(self._pointsonz0x,self._pointsonz0y,'.',color=colour)
        plt.subplot(1,2,2)
        plt.grid()
        plt.title('focus')
        plt.xlabel('x (mm)')
        #plt.ylabel('y')
        plt.plot(self._pointsonfocusx,self._pointsonfocusy,'.',color=colour)
        plt.show()

    def rms(self): #find root mean square radius
        squaresum=0
        for k in range(len(self._pointsonfocusx)):
            squaresum += self._pointsonfocusx[k]**2 + self._pointsonfocusy[k]**2
        return np.sqrt(squaresum/len(self._pointsonfocusx))

    def focusestimate(self): #find the estimate of the location of the paraxial focal point on the z axis using a ray close to optical axis
        para = Ray([0.1,0.0,0.0],[0.0,0.0,1.0])
        for j in range(len(self._surfaces)):
            self._surfaces[j].propagate_ray(para)
        OutputPlane(self._outputz + 100).propagate_ray(para)
        #x=mz+c for the straight line ray from lens to outputplane, but find z when x = 0
        #point A = (a,b), point B = (c,d) (axis=(z,x)), m=(d-b)/(c-a)
        a=para.vertices()[-2][2]
        b=para.vertices()[-2][0]
        c=para.vertices()[-1][2]
        d=para.vertices()[-1][0]
        m=(d-b)/(c-a)
        return ((0-b)/m) +a
