import glfw
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import numpy as np
import pyrr
import math
class shders:
    def create_shader_light(self) :
        self.vertex_src = """
        # version 440
        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec2 a_texture;
        layout(location = 2) in vec3 aNormal;
        uniform mat4 model;  
        uniform mat4 projection;
        uniform mat4 view;
        out vec2 v_texture;
        out vec3 fragPos;
        out vec3 Normal;
        void main()
        {
        fragPos = vec3(model* vec4(a_position, 1.0));
        Normal = mat3(transpose(inverse(model))) * aNormal;
        gl_Position = projection*view*model* vec4(a_position, 1.0);
        v_texture = a_texture;
        }
        """
        self.fragment_src = """
        # version 440
        in vec2 v_texture;
        in vec3 Normal;
        in vec3 fragPos;
        out vec4 FragColor;
        uniform vec3 lightPos;
        uniform vec3 lightcol;
        uniform sampler2D s_texture;
        uniform vec3 cameraPos;
        uniform vec3 ambient;
        void main()
        {
            vec3 lightDir = normalize(lightPos - fragPos);
            //vec3 ncam_pos = normalize(cameraPos);
            vec3 viewdir = normalize(cameraPos-fragPos);
            vec3 norm = normalize(Normal);
            vec3 reflectedDir = reflect(-lightDir, norm);
        
            vec3 lightlevel = vec3(0.0);
            lightlevel = lightlevel+ambient;

            lightlevel += lightcol*max(0.0, dot(norm, lightDir));

            lightlevel += lightcol * pow(max(dot(viewdir, reflectedDir), 0.0), 32);
            FragColor = vec4(lightlevel, 1.0) * texture(s_texture, v_texture); 
        }
        """
        return (compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER)))
    