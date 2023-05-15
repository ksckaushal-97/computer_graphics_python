import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from classes import *
from PIL import Image
import math
from Shaderfile_class import *

cam = Camera()
WIDTH , HEIGHT = 1280, 720
lastX, lastY = WIDTH/2 , HEIGHT/2
first_mouse = True
left, right, forward, backward, up, down= False, False, False, False, False, False
a = 0
b = 0
dt = 0
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward, up, down
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
            forward = False
    else:
        pass
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
            backward = False
    else:
        pass
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
            left= False
    else:
        pass 
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
            right= False
    else:
        pass
    if key == glfw.KEY_F and action == glfw.PRESS:
        up = True
    elif key == glfw.KEY_F and action == glfw.RELEASE:
            up= False
    else:
        pass 
    if key == glfw.KEY_Z and action == glfw.PRESS:
        down = True
    elif key == glfw.KEY_Z and action == glfw.RELEASE:
            down= False
    else:
        pass
def do_movement(c):
    if left:
        cam.process_keyboard("LEFT", 2*c)
    if right:
        cam.process_keyboard("RIGHT", 2*c)
    if forward:
        cam.process_keyboard("FORWARD", 2*c)
    if backward:
        cam.process_keyboard("BACKWARD",2*c)
    if up:
        cam.process_keyboard("UP", 2*c)
    if down:
        cam.process_keyboard("DOWN", 2*c)


def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height,0.1, 100)
    glUniformMatrix4fv(proj_loc_l, 1, GL_FALSE, projection)
# initializing glfw library
glfw.init()

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)
glfw.set_cursor_pos_callback(window, mouse_look_clb)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_key_callback(window, key_input_clb)
# make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0.5,  0.0, 0.0,  0.0,0.0,1.0,
             0.5, -0.5, 0.5,   1.0, 0.0, 0.0,0.0,1.0,
             0.5,  0.5, 0.5,   1.0, 1.0, 0.0,0.0,1.0,
            -0.5,  0.5, 0.5,   0.0, 1.0, 0.0,0.0,1.0,

            -0.5, -0.5, -0.5,  0.0, 0.0, 0.0,0.0,-1.0,
             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,0.0,-1.0,
             0.5,  0.5, -0.5,  1.0, 1.0, 0.0,0.0,-1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,0.0,-1.0,

             0.5, -0.5, -0.5,   0.0, 0.0, 1.0,0.0,0.0,
             0.5,  0.5, -0.5,  1.0, 0.0,  1.0,0.0,0.0,
             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,0.0,0.0,
             0.5, -0.5,  0.5,   0.0, 1.0, 1.0,0.0,0.0,

            -0.5,  0.5, -0.5,  0.0, 0.0, -1.0,0.0,0.0,
            -0.5, -0.5, -0.5,  1.0, 0.0, -1.0,0.0,0.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, -1.0,0.0,0.0,
            -0.5,  0.5,  0.5,  0.0, 1.0, -1.0,0.0,0.0,

            -0.5, -0.5, -0.5,   0.0, 0.0, 0.0,-1.0,0.0,
             0.5, -0.5, -0.5,   1.0, 0.0, 0.0,-1.0,0.0,
             0.5, -0.5,  0.5,   1.0, 1.0, 0.0,-1.0,0.0,
            -0.5, -0.5,  0.5,   0.0, 1.0, 0.0,-1.0,0.0,

             0.5,  0.5, -0.5,   0.0, 0.0, 0.0,1.0,0.0,
            -0.5,  0.5, -0.5,   1.0, 0.0, 0.0,1.0,0.0,
            -0.5,  0.5,  0.5,   1.0, 1.0, 0.0,1.0,0.0,
             0.5,  0.5,  0.5,   0.0, 1.0,  0.0,1.0,0.0]

#indices = [0,  1,  2,  2,  3,  0,
#           4,  5,  6,  6,  7,  4,
#           8,  9, 10, 10, 11,  8,
#          12, 13, 14, 14, 15, 12,
#          16, 17, 18, 18, 19, 16,
#          20, 21, 22, 22, 23, 20]

indicesX = [0,  1,  2,  2,  3,  0,
           4,  7,  6,  6,  5,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]



vertices = np.array(vertices, dtype=np.float32)
#indices = np.array(indices, dtype=np.uint32)
indicesX = np.array(indicesX, dtype = np.uint32)
shader = shders().create_shader_light()
glUseProgram(shader)
cube = mesh(vertices, indicesX)
lightpos_loc =glGetUniformLocation(shader, "lightPos")
lightcol_loc = glGetUniformLocation(shader, "lightcol")
camerapos_loc = glGetUniformLocation(shader, "cameraPos")
ambient_loc = glGetUniformLocation(shader, "ambient")
glUniform3f(camerapos_loc, cam.camera_pos.x, cam.camera_pos.y, cam.camera_pos.z)
glUniform3f(lightpos_loc, 0.0,6.0,-2.0)
glUniform3f(lightcol_loc, 1.0,1.0,1.0)
glUniform3f(ambient_loc, 0.4,0.4,0.4)
projection = pyrr.matrix44.create_perspective_projection_matrix(60, WIDTH/HEIGHT, 0.1, 100)
model_loc_l = glGetUniformLocation(shader, "model")
proj_loc_l = glGetUniformLocation(shader, "projection")
view_loc_l = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(proj_loc_l, 1, GL_FALSE, projection)
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

# Set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
# Set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# load image
image = Image.open("box.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

glClearColor(0, 0, 0, 1)

#view = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1,0,0])
#view = pyrr.matrix44.create_look_at(pyrr.Vector3([1,0,3]),pyrr.Vector3([0,0,0]),pyrr.Vector3([0,1,0]))
#model = pyrr.matrix44.multiply(rotation, translation)
glEnable(GL_DEPTH_TEST)
glEnable(GL_POLYGON_SMOOTH)  
glEnable(GL_LINE_SMOOTH)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glFrontFace(GL_CCW)
#glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# the main application loop
while not glfw.window_should_close(window):
    a = glfw.get_time()
    dt = a-b
    b = a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc_l, 1, GL_FALSE, view)
    #glUniform3f(camerapos_loc, cam.camera_pos.x, cam.camera_pos.y, cam.camera_pos.z)
    for i in range(0,4):
        for j in range(0,4):
            
            translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([i,3,j]))
            glUniformMatrix4fv(model_loc_l, 1, GL_FALSE, translation)
            cube.draw()     
    
    translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.5,5.0,1.5]))
    glUniformMatrix4fv(model_loc_l, 1, GL_FALSE, translation)
    glUniformMatrix4fv(view_loc_l, 1, GL_FALSE, view)
    cube.draw()
    glfw.swap_buffers(window)
    glfw.poll_events()
    do_movement(dt)
    glUniform3f(camerapos_loc, cam.camera_pos.x, cam.camera_pos.y, cam.camera_pos.z)
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y)
    #glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
    
    
    
# terminate glfw, free up allocated resources
glfw.terminate()