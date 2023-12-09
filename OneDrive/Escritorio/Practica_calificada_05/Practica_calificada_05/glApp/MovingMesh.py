import pygame
from .Graphics_Data import *
from .Uniform import *
from .Transformations import *


class MovingMesh:
    # Constructor de la clase MovingMesh
    def __init__(self, program_id, vertices, vertex_colors, draw_type,
                 translation=pygame.Vector3(0, 0, 0),  # Vector de traslación por defecto
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),  # Rotación por defecto
                 scale=pygame.Vector3(1, 1, 1),  # Escala por defecto
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0))  # Rotación de movimiento por defecto
                 ):
        self.vertices = vertices  # Vertices del objeto
        self.draw_type = draw_type  # Tipo de dibujo
        self.vao_ref = glGenVertexArrays(1)  # Genera un array de vértices
        glBindVertexArray(self.vao_ref)  # Enlaza el array de vértices
        position = Graphics_Data("vec3", self.vertices)  # Crea los datos gráficos para la posición
        position.create_variable(program_id, "position")  # Crea una variable para la posición
        colors = Graphics_Data("vec3", vertex_colors)  # Crea los datos gráficos para los colores
        colors.create_variable(program_id, "vertex_color")  # Crea una variable para los colores
        self.program_id = program_id  # ID del programa
        self.transformation_mat = identity_mat()  # Matriz de transformación inicial
        self.transformation_mat = rotateA(self.transformation_mat, rotation.angle, rotation.axis)  # Aplica la rotación
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)  # Aplica la traslación
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)  # Aplica la escala
        self.transformation = Uniform("mat4", self.transformation_mat)  # Crea un uniforme para la matriz de transformación
        self.transformation.find_variable(program_id, "model_mat")  # Encuentra la variable para la matriz de transformación
        self.move_rotation = move_rotation  # Rotación de movimiento
        self.program_id = program_id  # ID del programa

    def draw(self):
        # Actualizar la matriz de transformación con la rotación de movimiento
        self.transformation_mat = rotateA(self.transformation_mat, self.move_rotation.angle, self.move_rotation.axis)

        # Crear una nueva variable de transformación uniforme
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.program_id, "model_mat")

        # Cargar la nueva transformación uniforme
        self.transformation.load()

        # Enlazar el VAO (Vertex Array Object)
        glBindVertexArray(self.vao_ref)

        # Dibujar los vértices
        glDrawArrays(self.draw_type, 0, len(self.vertices))
