import numpy as np
from raytracer import Ray
from opticalelement import OpticalElement

class SphericalRefraction(OpticalElement):
    def __init__(self, z, cur, n11, n22, ar):
        OpticalElement.__init__(self)
        self._z0 = z #where the lens is 
        self._aradius = ar #aperture radius
        self._n1 = n11 #refractive index 1
        self._n2 = n22 #refractive index 2
        self._curvature = cur #curvature
        #finding centre for different orientation of curved surface
        if self._curvature > 0:
            self._radius = 1/self._curvature
            self._centre = self._z0 + self._radius
        elif self._curvature < 0:
            self._radius = -1/self._curvature
            self._centre = self._z0 - self._radius
        

    def intercept(self, ray):
        if self._curvature == 0:     #for plane surface refraction
            direc = ray.k()/np.linalg.norm(ray.k()) #unit vector of direction of travel
            #p[2]+lk[2]=z0, l=(z0-p[2])/k[2])
            self.l=np.array(ray.p()+((self._z0-ray.p()[2])/direc[2])*direc)
            return self.l
        else: #for spherical surface 
            poi = ray.p() - np.array([0.0,0.0,self._centre]) #vector from centre of circle to point
            direc = ray.k()/np.linalg.norm(ray.k()) #unit vector of direction of travel
            if (np.dot(poi,direc)**2 - (np.dot(poi,poi) - self._radius**2)) < 0: #check to see if there is real solution
                return None
            else:
                l1 = -1*np.dot(poi,direc) + np.sqrt(np.dot(poi,direc)**2 - (np.dot(poi,poi) - self._radius**2))
                l2 = -1*np.dot(poi,direc) - np.sqrt(np.dot(poi,direc)**2 - (np.dot(poi,poi) - self._radius**2))
                ll=[l1,l2]
            
            #selecting the correct l value and find Q
            if self._curvature>0:
                self.l = np.array(ray.p() + min(ll)*direc)
            elif self._curvature<0:
                self.l = np.array(ray.p() + max(ll)*direc)
            else:
                return None
        
            #checking if the ray hits the lens
            if np.sqrt(self.l[0]**2+self.l[1]**2) <= self._aradius:
                return self.l
            else:
                return None

    def refract(self,ray,surfnorm):
        normal=surfnorm/np.linalg.norm(surfnorm) #surface normal
        dire = ray.k()/np.linalg.norm(ray.k()) #initial direction k1
        theta1=np.arccos(np.dot(normal,dire))
        #theta2=np.arcsin((self._n1/self._n2)*np.sin(theta1))
        if np.sin(theta1) > self._n2/self._n1: #TIR
            return None
        else:
            #snells law (eqn found on wikipedia)
            r = (self._n1/self._n2)
            c = -np.dot(normal,dire)
            k2 = np.array(r*dire + normal*(r*c - np.sqrt(1-(r**2 * (1-c**2)))))
            #print(normal*(r*c - np.sqrt(1-(r**2 * (1-c**2)))))
            #print(c)
            return k2/np.linalg.norm(k2)

    def propagate_ray(self, ray):
        #self.intercept() or self.refract()
        inte=self.intercept(ray)
        
        if inte.all() == None: #see if intercept exists
            raise NotImplementedError()
        else:
            if self._curvature > 0:
                nor=np.array([0.0,0.0,self._centre])-inte
                newdir=self.refract(ray,-nor/np.linalg.norm(nor))
                ray.append(inte,newdir)
            elif self._curvature == 0:
                nor=np.array([0.0,0.0,1.0])
                newdir=self.refract(ray,-nor/np.linalg.norm(nor))
                ray.append(inte,newdir)
            elif self._curvature < 0:
                nor=inte-np.array([0.0,0.0,self._centre])
                newdir=self.refract(ray,-nor/np.linalg.norm(nor))
                ray.append(inte,newdir)
            

        


    


        
        

    








        

