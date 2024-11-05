import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


# Define your cube vertices, edges, colors, and surfaces here as before
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

# Cube rendering function
def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# Screw motion function
def screw_motion(start, end, rotation_axis, rotation_angle, steps):
    position = np.array(start)
    direction = np.array(end) - position #creates the vector
    step_translation = direction / steps  # Small translation per frame
    step_rotation = rotation_angle / steps  # Small rotation angle per frame
    return step_translation, rotation_axis, step_rotation


def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) #camera settings
    glTranslatef(0.0, 0.0, -5)

    # Starting and ending points for screw motion
    start_pos = np.array([0.0, 0.0, -5.0])
    end_pos = np.array([-10.0, -10.0, -5.0])
    rotation_axis = [1, 1, 1]  # Rotate around y-axis
    rotation_angle = 90  # Total rotation angle in degrees
    steps = 1000  # Total number of steps for the motion

    # Get step-wise translation and rotation
    step_translation, rotation_axis, step_rotation = screw_motion(
        start_pos, end_pos, rotation_axis, rotation_angle, steps
    )

    for _ in range(steps):
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply translation
        glTranslatef(*step_translation) #Makes the move in distance

        # Apply rotation
        glRotatef(step_rotation, *rotation_axis) #makes the move rotationg

        # Render the cube
        Cube()

        # Update the display and control the frame rate
        pygame.display.flip()
        pygame.time.wait(10)

        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


main()