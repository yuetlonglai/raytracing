from raytracer import Ray

class OpticalElement:
    def propagate_ray(self,ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()