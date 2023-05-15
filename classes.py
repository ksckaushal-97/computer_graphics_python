import glfw
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import numpy as np
import pyrr
import math

    

class mesh:
    def __init__(self, vertices, indices):
        self.indices = indices
        self.vao =glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        self.ebo =glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self):
        glBindVertexArray(self.vao)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

class Camera:
    def __init__(self):
        self.camera_pos = pyrr.Vector3([0.0,3.0,6.0])
        self.camera_front = pyrr.Vector3([0.0,0.0,-1.0])
        self.camera_up = pyrr.Vector3([0.0,1.0,0.0])
        self.camera_right = pyrr.Vector3([1.0,0.0,0.0])
        self.cond = True
        self.mouse_sensitivity = 0.5
        self.jaw = -45
        self.pitch =0
    def get_view_matrix(self):
        return (pyrr.matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up))

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch = True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = pyrr.Vector3([0.0,0.0,0.0])
        front.x = math.cos(math.radians(self.jaw))* math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z =  math.sin(math.radians(self.jaw))* math.cos(math.radians(self.pitch))

        self.camera_front = pyrr.vector.normalize(front)
        self.camera_right = pyrr.vector.normalize(pyrr.vector3.cross(self.camera_front, pyrr.Vector3([0.0,1.0,0.0])))
        self.camera_up = pyrr.vector.normalize(pyrr.vector3.cross(self.camera_right, self.camera_front)) 

    def process_keyboard(self, direction, velocity):
        cond = True               
        if self.camera_pos.x >= -1.0 and self.camera_pos.x <= 4.0:
            if self.camera_pos.y >= 2.0 and self.camera_pos.y <= 4.0:
                if self.camera_pos.z >= -1.0 and self.camera_pos.z <= 4.0:
                    cond = False

        if cond:
            if direction == "FORWARD":
                self.camera_pos += (self.camera_front * velocity)
            if direction == "BACKWARD":
                self.camera_pos -= (self.camera_front * velocity)
            if direction == "LEFT":
                self.camera_pos -= (self.camera_right * velocity)
            if direction == "RIGHT":
                self.camera_pos += (self.camera_right * velocity)
            if direction == "UP":
                self.camera_pos += (self.camera_up * velocity)
            if direction == "DOWN":
                self.camera_pos -= (self.camera_up * velocity)
        else:
            if direction == "FORWARD":
                if self.camera_pos.z > 3.6 and self.camera_pos.z <=4.0:
                    mul = pyrr.Vector3([self.camera_front[0],self.camera_front[1],0.0])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.x < -0.55 and self.camera_pos.x >= -1.0:
                    mul = pyrr.Vector3([0.0,self.camera_front[1],self.camera_front[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.z < -0.5 and self.camera_pos.z >= -1:
                    mul = pyrr.Vector3([self.camera_front[0],self.camera_front[1],0.0])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.x > 3.5 and self.camera_pos.x <=4.0:
                    mul = pyrr.Vector3([0.0,self.camera_front[1],self.camera_front[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.y >= 2.0 and  self.camera_pos.y <= 2.5:
                    mul = pyrr.Vector3([self.camera_front[0],0.0,self.camera_front[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.y >= 3.5 and self.camera_pos.y <= 4.0:
                    mul = pyrr.Vector3([self.camera_front[0],0.0,self.camera_front[2]])
                    self.camera_pos += (mul * velocity)
                else:
                    pass

            if direction == "BACKWARD":
                if self.camera_pos.z > 3.6 and self.camera_pos.z <=4.0:
                    mul = pyrr.Vector3([self.camera_front[0],self.camera_front[1],0.0])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.x < -0.55 and self.camera_pos.x >= -1.0:
                    mul = pyrr.Vector3([0.0,self.camera_front[1],self.camera_front[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.z < -0.5 and self.camera_pos.z >= -1:
                    mul = pyrr.Vector3([self.camera_front[0],self.camera_front[1],0.0])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.x > 3.5 and self.camera_pos.x <=4.0:
                    mul = pyrr.Vector3([0.0,self.camera_front[1],self.camera_front[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.y >= 2.0 and  self.camera_pos.y <= 2.5:
                    mul = pyrr.Vector3([self.camera_front[0],0.0,self.camera_front[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.y >= 3.5 and self.camera_pos.y <= 4.0:
                    mul = pyrr.Vector3([self.camera_front[0],0.0,self.camera_front[2]])
                    self.camera_pos -= (mul * velocity)
                else:
                    pass 
            if direction == "LEFT":
                if self.camera_pos.z > 3.6 and self.camera_pos.z <=4.0:
                    mul = pyrr.Vector3([self.camera_right[0],self.camera_right[1],0.0])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.x < -0.55 and self.camera_pos.x >= -1.0:
                    mul = pyrr.Vector3([0.0,self.camera_right[1],self.camera_right[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.z < -0.5 and self.camera_pos.z >= -1:
                    mul = pyrr.Vector3([self.camera_right[0],self.camera_right[1],0.0])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.x > 3.5 and self.camera_pos.x <=4.0:
                    mul = pyrr.Vector3([0.0,self.camera_right[1],self.camera_right[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.y >= 2.0 and  self.camera_pos.y <= 2.5:
                    mul = pyrr.Vector3([self.camera_right[0],0.0,self.camera_right[2]])
                    self.camera_pos -= (mul * velocity)
                elif self.camera_pos.y >= 3.5 and self.camera_pos.y <= 4.0:
                    mul = pyrr.Vector3([self.camera_right[0],0.0,self.camera_right[2]])
                    self.camera_pos -= (mul * velocity)
                else:
                    pass 
            if direction == "RIGHT":
                if self.camera_pos.z > 3.6 and self.camera_pos.z <=4.0:
                    mul = pyrr.Vector3([self.camera_right[0],self.camera_right[1],0.0])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.x < -0.55 and self.camera_pos.x >= -1.0:
                    mul = pyrr.Vector3([0.0,self.camera_right[1],self.camera_right[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.z < -0.5 and self.camera_pos.z >= -1:
                    mul = pyrr.Vector3([self.camera_right[0],self.camera_right[1],0.0])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.x > 3.5 and self.camera_pos.x <=4.0:
                    mul = pyrr.Vector3([0.0,self.camera_right[1],self.camera_right[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.y >= 2.0 and  self.camera_pos.y <= 2.5:
                    mul = pyrr.Vector3([self.camera_right[0],0.0,self.camera_right[2]])
                    self.camera_pos += (mul * velocity)
                elif self.camera_pos.y >= 3.5 and self.camera_pos.y <= 4.0:
                    mul = pyrr.Vector3([self.camera_right[0],0.0,self.camera_right[2]])
                    self.camera_pos += (mul * velocity)
                else:
                    pass 
            if direction == "UP":
                self.camera_pos -= (self.camera_up * velocity)
            if direction == "DOWN":
                self.camera_pos -= (self.camera_up * velocity)

        

        
        