#Original program by Estuardo del Angel
#Adapted for a wireframe cube and annotated by Douglas Yellow

from turtle import *
from math import *
from time import time
from object_file_codec import decode_obj


"""VARIABLES"""
scale = 0.05 #Arbitrary value to scale the 3D model
screen_size = 700 #Screen width of the Turtle window
bg_brightness = 0 #How bright the background is, with 0 as black and 1 as white
A_start = 90 #Starting rotation angle of the the x-plane (roll) in degrees
B_start = 180 #Starting rotation angle of the the y-plane (pitch) in degrees
C_start = -90 #Starting rotation angle of the the z-plane (yaw) in degrees
A_increase = -2 #Rotation per frame around the x-plane in degrees
B_increase = 3 #Rotation per frame around the y-plane in degrees
C_increase = -3 #Rotation per frame around the z-plane in degrees
thickness = 1 #The line thickness
frame_rate = 60 #The number of frames per second, the maximum is 60 frames per second
light_direction = [1,1,3] #The starting point from which the light beams
viewer_direction = [0,0,1] #The starting point from which the viewer sees
object_information = decode_obj("shuttle")
wireframe = False



"""FUNCTIONS"""
def magnitude(vector):
  return sqrt((vector[0]**2) + (vector[1])**2 + (vector[2]**2))
  
def normalise(vector):
  return [vector[n]/magnitude(vector) for n in range(3)]

def dot_product(vector1,vector2):
  return sum([vector1[n]*vector2[n] for n in range(3)])



"""SETUP"""
screen_dist = scale * screen_size
''' Scales the final result to fit within the bounds and be a visible size.
    Uses 'screen_size' to scale the object to the window size automatically.
    Multiplication by 'scale' is an abitrary amount to fine tune it.'''

#Converts the starting degrees into radians:
A = radians(A_start)
B = radians(B_start)
C = radians(C_start)

#Converts the turning degrees into radians:
A_increase = radians(A_increase)
B_increase = radians(B_increase)
C_increase = radians(C_increase)

tracer(0) #Turns the Turtle animation off and sets the delay to zero for updates, meaning it will only be updated manually
ht() #Hide the Turtle icon
colormode(1.0) #Sets the colours to use the range 0-1 instead of 0-255
pensize(thickness) #Sets the line thickness
bgcolor(bg_brightness,bg_brightness,bg_brightness) #Sets the background between black and white using 'bg_brightness' inputted earlier
pencolor(1, 1, 1) #Sets the pen colour to white as the default
setup(screen_size,screen_size) #Sets the screen geometry to be a square with side length 'screen_size'

#Normalises the inputted light and view direction to be used in equations:
light_direction = normalise(light_direction)
viewer_direction = normalise(viewer_direction)

#Limits 'frame_rate' to below the pre-defined maximum
max_frame_rate = 60
if frame_rate > max_frame_rate:
  frame_rate = max_frame_rate

#Stores each vertex (corner) of a cube with a centre at the origin and an edge length of two in 'vertices' (corners):
vertices = object_information.vertices

#Stores the faces of the 3D model by storing indexes of the vertex list above:
faces = object_information.sides_indices


"""MAIN LOOP"""
while True:
    time_start = time()
    clear() #Clears the screen of all Turtle drawings
   
    #Stores cosine and sine values of the rotation angles for easy referencing:
    sinA = sin(A)
    cosA = cos(A)
    sinB = sin(B)
    cosB = cos(B)
    sinC = sin(C)
    cosC = cos(C)
    
    #Rotates the coordinates of the vertices within 3D space centred on the origin:
    vertices_rot = list() #Clears the rotated vertices list so it can be updated again
    for vertex in vertices:
    	#print(vertex)
    	x,y,z = vertex #Assigning variable names to coordinates for easy referencing
    	
    	x_rot = (x * cosB*cosC) - (y * cosB*sinC) + (z * sinB)
    	y_rot = ((x * sinA*sinB*cosC) + (x * cosA*sinC)) + ((y * cosA*cosC) - (y * sinA*sinB*sinC)) - (z * sinA*cosB)
    	z_rot = ((x * sinA*sinC) - (x * cosA*sinB*cosC)) + ((y * cosA*sinB*sinC) + (y * sinA*cosC)) + (z * cosA * cosB)
    	
    	vertices_rot.append([x_rot,y_rot,z_rot])
    
    faces_order = list()
    for face in range(len(faces)):
    	vector_points = list()
    	
    	face_vertices = list()
    	#print(len(vertices_rot))
    	for vertex_index in faces[face]:
    		  #print(vertex_index)
    		  face_vertices.append(vertices_rot[vertex_index])
    		
    	#Assigning variable names to chosen rotated vertices for easy referencing:
    	Ax,Ay,Az = face_vertices[0]
    	Bx,By,Bz = face_vertices[1]
    	Cx,Cy,Cz = face_vertices[2]
    	
    	#Calculate dimensions of vectors by subtracting the start points from the end points:
    	vector_AB = vA = [(Bx-Ax), (By-Ay), (Bz-Az)]
    	vector_AC = vB = [(Cx-Ax), (Cy-Ay), (Bz-Az)]
    	
    	#Cross product of vectors AB and AC to make vector N, the normal:
    	normal_vector = [(vA[1]*vB[2])-(vA[2]*vB[1]),(vA[2]*vB[0])-(vA[0]*vB[2]),(vA[0]*vB[1])-(vA[1]*vB[0])]
    	''' In this example, the lowercase letters 'a' and 'b' mean 'vector_AB' and 'vector_AC' respectively.
    	    The normal with dimensions <cx,cy,cz> to the plane ABC can be calculated more easily if point A is the origin.
    	    This is because the cross product of vectors AB and AC with dimensions cx, cy, and cz can be calculated as:
    	    cx = ay(bz) − az(by)
    	    cy = az(bx) − ax(bz)
          cz = ax(by) − ay(bx)'''
          
    	try:
    	  normal_vector_magnitude = magnitude(normal_vector)
    	  observer_luminance = dot_product(normal_vector, viewer_direction)/normal_vector_magnitude #The normal vector dot product the normalised vector of the observer's view, which is at default <0,0,-1>, divided by magnitude of the normal vector
    	except ZeroDivisionError:
    	  observer_luminance = 0
    	
    	if observer_luminance >= 0 or wireframe:
    		#Finds the centroid's z position by calculating the mean of the face's vertices' z positions:
    		z_tot = 0
    		for vertex in face_vertices:
    			z_tot += vertex[2]
    		faces_order.append([face,z_tot/4,normal_vector.copy(), normal_vector_magnitude])
    		
    faces_order.sort(key = lambda a : a[1])
    
    #Displays the rotated points using orthographic projection:
    for face in faces_order: #For each face of the faces stored, where a 'face' in this context being the list of indices of vertices that make up its edges
        filling = False
        if not wireframe:
          try:
            face_luminance = dot_product(face[2], light_direction)/face[3] #The normal vector dot product the normalised vector of the light direction, divided by magnitude of the normal vector
          except ZeroDivisionError:
            face_luminance = 0
          
          if face_luminance < 0:
            face_luminance = 0
          elif face_luminance > 1:
            face_luminance = 1
          
          fillcolor(face_luminance,face_luminance,face_luminance)
          pencolor(face_luminance,face_luminance,face_luminance)
          
        pu() #Turns off the pen to prevent extra lines when starting the cycle of drawing a face over again
        for vertex_index in faces[face[0]]: #For each index of a vertex as specified with the faces list
            #Converts the given face's vertex to a coordinate:
            x_rot = vertices_rot[vertex_index][0]
            y_rot = vertices_rot[vertex_index][1]
            
            #Moves the Turtle to the rotated point, being scaled to fit visibly within the space orthographically:
            goto((screen_dist * x_rot), (screen_dist * y_rot)) #This orthographic projection is not realistic as it does not incorporate a lensing effect like our eyes or cameras do.
            pd() #Pen down only after the first movement, since that is used to move the Turtle to the beginning of the face's vertices (stored in 'temp')
            if not (wireframe or filling):
            	filling = True
            	begin_fill()
        end_fill()

    #Draw everything the pen recorded to the screen
    update()
   
    #Add the step to the rotation of the 3D model
    A += A_increase * (max_frame_rate/frame_rate)
    B += B_increase * (max_frame_rate/frame_rate)
    C += C_increase * (max_frame_rate/frame_rate)
    
    time_delta = 1/(time() -time_start)
    while time_delta > frame_rate:
      time_delta = 1/(time()-time_start)