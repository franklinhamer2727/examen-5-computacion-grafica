import pygame
from .Graphics_Data import *
from .Uniform import *
from .Transformations import *

class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type,
                 translation=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1)
                 ):
        self.vertices = vertices  # Almacena los vértices del objeto
        self.draw_type = draw_type  # Almacena el tipo de dibujo
        self.vao_ref = glGenVertexArrays(1)  # Genera un array de vértices
        glBindVertexArray(self.vao_ref)  # Enlaza el array de vértices
        position = Graphics_Data("vec3", self.vertices)  # Crea los datos gráficos para la posición
        position.create_variable(program_id, "position")  # Crea una variable para la posición
        colors = Graphics_Data("vec3", vertex_colors)  # Crea los datos gráficos para los colores
        colors.create_variable(program_id, "vertex_color")  # Crea una variable para los colores
        self.transformation_mat = identity_mat()  # Crea una matriz de transformación inicial como la matriz identidad
        self.transformation_mat = rotateA(self.transformation_mat, rotation.angle, rotation.axis)  # Aplica una rotación a la matriz de transformación
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)  # Aplica una traslación a la matriz de transformación
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)  # Aplica una escala a la matriz de transformación
        self.transformation = Uniform("mat4", self.transformation_mat)  # Crea un uniforme para la matriz de transformación
        self.transformation.find_variable(program_id, "model_mat")  # Encuentra la variable correspondiente a la matriz de transformación en el programa de shaders

    def draw(self):
        self.transformation.load()  # Carga la matriz de transformación en el programa de shaders
        glBindVertexArray(self.vao_ref)  # Enlaza el array de vértices
        glDrawArrays(self.draw_type, 0, len(self.vertices))  # Dibuja los vértices del objeto según el tipo de dibujo especificado
