import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):

    A = calculate_ambient(ambient, areflect) 
    D = calculate_diffuse(light, dreflect, normal)
    S = calculate_specular(light, sreflect, view, normal)

    light = [] 
    light.append( A[0] + D[0] + S[0] )
    light.append( A[1] + D[1] + S[1] )
    light.append( A[2] + D[2] + S[2] )

    print light

    return limit_color(light)
    

def calculate_ambient(alight, areflect):
    amb_vals = []
    amb_vals.append( int(alight[0] * areflect[0]) ) 
    amb_vals.append( int(alight[1] * areflect[1]) )
    amb_vals.append( int(alight[2] * areflect[2]) )
    return limit_color(amb_vals) 
        

def calculate_diffuse(light, dreflect, normal):
    diffuse = []
    N = normalize(normal)
    L = normalize(light[LOCATION])
    dot_prod = dot_product(N, L)
    diffuse.append( int( (light[1][0] * dreflect[0]) * dot_prod ) ) 
    diffuse.append( int( (light[1][1] * dreflect[1]) * dot_prod ) )
    diffuse.append( int( (light[1][2] * dreflect[2]) * dot_prod ) )
    print diffuse 
    return limit_color(diffuse) 

def calculate_specular(light, sreflect, view, normal):
    color = []
    color.append( light[1][0] * sreflect[0] )
    color.append( light[1][1] * sreflect[1] )
    color.append( light[1][2] * sreflect[2] )
    
    N = normalize(normal)
    L = normalize(light[LOCATION])
    V = normalize(view)

    if (dot_product(N, L) <= 0):
        return [0,0,0]

    else:
        a = [x*2*dot_product(N, L) for x in N]
        b = [x-y for x,y in zip(a,L)]
        c = [int(x*(dot_product(b,V)**8)) for x in color]

    return limit_color(c) 

def limit_color(color):
    for x in range(len(color)):
        if color[x] <= 0:
            color[x] = 0

        elif (color[x] >= 255):
            color[x] = 255
    return color 

#vector functions
def normalize(vector):
    x = vector[0]**2
    y = vector[1]**2
    z = vector[2]**2

    mag = (x+y+z)**0.5
        
    return ([one/mag for one in vector]) 

def dot_product(a, b):
    return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2]) 


def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
