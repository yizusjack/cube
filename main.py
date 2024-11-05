import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# https://pythonprogramming.net/coloring-pyopengl-surfaces-python-opengl

vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# maps how to connected vertices
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

# rgb in float 0-1 values
colors = (
    (1,0,0), #r
    (0,1,0), #g
    (0,0,1), #b
    (0,1,0), #g
    (1,1,1), #wh
    (0,1,1), #cy
    (1,0,0), #r
    (0,1,0), #g
    (0,0,1), #b
    (1,0,0), #r
    (1,1,1), #wh
    (0,1,1), #cy
)

# surfaces are groups of vertices
# indexes to the vertices list
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

def Cube():

    # render colored surfaces as quads
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    # render lines between vertices
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (1280, 720)
    # DOUBLEBUF is a type of buffering where there are
    # two buffers to comply with monitor refresh rates
    # OPENGL says we will be doing opengl calls
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # fov, aspect ratio, nearz, farz clipping planes
    # "nearz and farz values are supposed to be positive
    #  because they are in relation to your perspective,
    #  not in relation to your actual location within the
    #  3D environment."
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # move perspective by x, y, z (-5 to be back from cube)
    glTranslatef(0.0,0.0, -5)

    glRotatef(25, 2, 1, 0)
    left = 0
    right = 0
    up = 0
    down = 0
    rotate_down = 0
    rotate_up = 0
    rotate_left = 0
    rotate_right = 0
    rotate_clockwise = 0
    rotate_counter_clockwise = 0
    # game loop
    while True:
        # pygame events

        if left:
            right, down, up = 0, 0, 0
            glTranslatef(-0.1,0,0)
        if right:
            left, down, up = 0, 0, 0
            glTranslatef(0.1,0,0)
        if up:
            left, down, right = 0, 0, 0
            glTranslatef(0,.1,0)
        if down:
            left, up, right = 0, 0, 0
            glTranslatef(0,-.1,0)
        if rotate_down:
            left, down, right = 0, 0, 0
            glRotatef(5, 1, 0, 0)
        if rotate_up:
            left, down, right = 0, 0, 0
            glRotatef(5, -1, 0, 0)
        if rotate_left:
            glRotatef(5, 0, 1, 0)
        if rotate_right:
            glRotatef(5, 0, -1, 0)
        if rotate_clockwise:
            glRotatef(5, 0, 0, 1)
        if rotate_counter_clockwise:
            glRotatef(5, 0, 0, -1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                # move in X axis
                if event.key == pygame.K_LEFT:
                    left = 1
                if event.key == pygame.K_RIGHT:
                    right = 1

                # move in Y axis
                if event.key == pygame.K_UP:
                    up = 1
                if event.key == pygame.K_DOWN:
                    down = 1

                # Rotate up (around X-axis)
                if event.key == pygame.K_w:
                    rotate_up = 1
                # Rotate down (around X-axis)
                if event.key == pygame.K_s:
                    rotate_down = 1
                # Rotate left (around y-axis)
                if event.key == pygame.K_a:
                    rotate_left = 1
                # Rotate right (around y-axis)
                if event.key == pygame.K_d:
                    rotate_right = 1
                # Rotate clockwise (around z-axis)
                if event.key == pygame.K_z:
                    rotate_clockwise = 1
                # Rotate clockwise (around z-axis)
                if event.key == pygame.K_x:
                    rotate_counter_clockwise = 1
            if event.type == pygame.KEYUP:
                left = 0
                right = 0
                up = 0
                down = 0
                rotate_down = 0
                rotate_up = 0
                rotate_left = 0
                rotate_right = 0
                rotate_clockwise = 0
                rotate_counter_clockwise = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                # move in Z axis
                if event.button == 4:
                    glTranslatef(0,0,.1)

                if event.button == 5:
                    glTranslatef(0,0,-.1)

        # rotate current matrix by, x,y,z (w?) (radians?)
        #glRotatef(1, 3, 1, 1)
        # clear buffers
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # render cube lines
        Cube()
        # update display
        pygame.display.flip()
        # update loop sleep
        pygame.time.wait(10)

main()