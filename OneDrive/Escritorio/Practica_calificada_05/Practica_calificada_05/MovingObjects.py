from glApp.PyOGApp import *  # Importa la clase PyOGApp del módulo glApp
from glApp.Utils import *  # Importa las utilidades del módulo glApp
from glApp.Square import *  # Importa la clase Square del módulo glApp
from glApp.Triangle import *  # Importa la clase Triangle del módulo glApp
from glApp.Axes import *  # Importa la clase Axes del módulo glApp
from glApp.Cube import *  # Importa la clase Cube del módulo glApp
from glApp.LoadMesh import *  # Importa la clase LoadMesh del módulo glApp
from glApp.MovingCube import *  # Importa la clase MovingCube del módulo glApp

# Shader de vértices
vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
void main()
{
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position,1);
    color = vertex_color;
}
'''

# Shader de fragmentos
fragment_shader = r'''
#version 330 core
in vec3 color;
out vec4 frag_color;
void main()
{
    frag_color = vec4(color, 1);
}
'''


# Clase MovingObjects que hereda de PyOGApp
class MovingObjects(PyOGApp):

    def __init__(self):
        super().__init__(20, 30, 1400, 800)  # Llama al constructor de la clase padre
        self.axes = None
        self.moving_cube = None
        self.moving_fig1 = None
        self.moving_happy = None
        self.moving_fig2 = None
        # self.moving_fig3 = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)  # Crea el programa de shaders
        self.axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))  # Crea una instancia de la clase Axes
        # self.moving_cube = MovingCube(self.program_id, location = pygame.Vector3(2, 1, 2),
        #                             move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        # cargamos los obj

        happy = LoadMesh("models/feliz_navidad_bloque.obj", self.program_id)  # Carga el modelo feliz_navidad_bloque.obj
        fig1 = LoadMesh("models/corona.obj", self.program_id)  # Carga el modelo corona.obj

        self.moving_happy = MovingMesh(self.program_id, vertices=happy.vertices,
                                       vertex_colors=happy.colors, draw_type=GL_TRIANGLES,
                                       translation=pygame.Vector3(0, 0, 0),
                                       scale=pygame.Vector3(0.05, 0.05,
                                                            0.05))  # Crea una instancia de MovingMesh para el modelo feliz_navidad_bloque.obj

        nro = len(happy.colors)
        yellow = [0.937254, 0.721568, 0.062745]
        colors1 = yellow * nro

        self.moving_fig1 = MovingMesh(self.program_id, vertices=fig1.vertices,
                                      vertex_colors=colors1, draw_type=GL_TRIANGLES,
                                      translation=pygame.Vector3(0, 2.5, 0),
                                      scale=pygame.Vector3(0.09, 0.09, 0.09),
                                      move_rotation=Rotation(1, pygame.Vector3(0, 1,
                                                                               0)))  # Crea una instancia de MovingMesh para el modelo corona.obj

        self.camera = Camera(self.program_id, self.screen_width,
                             self.screen_height)  # Crea una instancia de la clase Camera
        glEnable(GL_DEPTH_TEST)  # Habilita la prueba de profundidad

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpia el búfer de color y el búfer de profundidad
        glUseProgram(self.program_id)  # Usa el programa de shaders
        self.camera.update()  # Actualiza la cámara
        self.axes.draw()  # Dibuja los ejes

        self.moving_happy.draw()  # Dibuja el modelo feliz_navidad_bloque.obj
        self.moving_fig1.draw()  # Dibuja el modelo corona.obj


# Crea una instancia de la clase MovingObjects y ejecuta el bucle principal
MovingObjects().mainloop()
