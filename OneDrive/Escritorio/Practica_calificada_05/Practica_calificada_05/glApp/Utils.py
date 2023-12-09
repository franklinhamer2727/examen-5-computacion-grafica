import numpy as np
from OpenGL.GL import *
import numpy as np

def format_vertices(coordinates, triangles):
    allTriangles = []  # Lista para almacenar todos los triángulos

    for t in range(0, len(triangles), 3):  # Itera sobre los triángulos en grupos de 3
        allTriangles.append(coordinates[triangles[t]])  # Agrega el primer vértice del triángulo a la lista
        allTriangles.append(coordinates[triangles[t+1]])  # Agrega el segundo vértice del triángulo a la lista
        allTriangles.append(coordinates[triangles[t+2]])  # Agrega el tercer vértice del triángulo a la lista
    return np.array(allTriangles, np.float32)  # Convierte la lista de triángulos en un array numpy de tipo float32


def compile_shader(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)  # Crea un objeto shader del tipo especificado
    glShaderSource(shader_id, shader_source)  # Asigna el código fuente al shader
    glCompileShader(shader_id)  # Compila el shader
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)  # Verifica si la compilación fue exitosa
    if not compile_success:  # Si la compilación no fue exitosa
        error_message = glGetShaderInfoLog(shader_id)  # Obtiene el mensaje de error de compilación
        glDeleteShader(shader_id)  # Elimina el shader
        error_message = "\n" + error_message.decode("utf-8")  # Decodifica el mensaje de error
        raise Exception(error_message)  # Lanza una excepción con el mensaje de error
    return shader_id  # Retorna el ID del shader compilado


def create_program(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)  # Compila el shader de vértices
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)  # Compila el shader de fragmentos
    program_id = glCreateProgram()  # Crea un programa de shaders
    glAttachShader(program_id, vertex_shader_id)  # Adjunta el shader de vértices al programa
    glAttachShader(program_id, fragment_shader_id)  # Adjunta el shader de fragmentos al programa
    glLinkProgram(program_id)  # Enlaza el programa de shaders
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)  # Verifica si el enlace fue exitoso
    if not link_success:  # Si el enlace no fue exitoso
        info = glGetShaderInfoLog(program_id)  # Obtiene el mensaje de error de enlace
        raise RuntimeError(info)  # Lanza una excepción con el mensaje de error
    glDeleteShader(vertex_shader_id)  # Elimina el shader de vértices
    glDeleteShader(fragment_shader_id)  # Elimina el shader de fragmentos
    return program_id  # Retorna el ID del programa de shaders
