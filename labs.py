import math

#Define our own complex number class
class myComplex:

    # __init__ is required for a class and specifies what happens when a new object is created
    # in our case, the class holds two float numbers (the real and imaginary part) which are initialised
    # by the arguments passed, or set to 0. if no arguments are passed
    def __init__(self,x=0., y=0.):
        self.re=x
        self.im=y

    # Return the modulus of a complex number
    def R(self):
        return math.sqrt(self.re**2 + self.im**2)
    
    # Return the phase
    def phi(self):
        return math.atan2(self.im, self.re)

    # Or we can set modulus and phase
    def setRphi(self, R, phi):
        self.re = R * math.cos(phi)
        self.im = R * math.sin(phi)
   
    # Overload the "+" operator to add two numbers
    def __add__(self, other):
        return myComplex(self.re + other.re, self.im + other.im)
    
    # Overload the "-" operator to subtract two numbers
    def __sub__(self, other):
        return myComplex(self.re - other.re, self.im - other.im)
    
    # Overload the "*" operator to multiply two numbers
    def __mul__(self, other):
        return myComplex(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)
    
    # Define the complex conjugate
    def conjugate(self):
        return myComplex(self.re, -1 * self.im)
    
    # Overload the "/" operator to divide two numbers
    def __truediv__(self, other):
        numerator = other.conjugate()*self
        denominator = (other*other.conjugate()).re
        return myComplex(numerator.re / denominator, numerator.im / denominator)
    
    # Rotate the phase of a complex number given an argument
    def phase_rotate(self, arg):
        return np.arctan(np.tan(self.phi() + arg))
    
    # Print out complex numbers
    def __repr__(self):
        return '%f + %f i' %(self.re, self.im)


a = myComplex(5.,2.)
b = myComplex(7., 4.)
print(a/b)


