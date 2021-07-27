from OpenGL.GL import *
uniform_locs = {}

def get_locs(program):
    uniform_locs['model_loc'] = glGetUniformLocation(program, 'model')
    uniform_locs['view_loc'] = glGetUniformLocation(program, 'view')
    uniform_locs['projection_loc'] = glGetUniformLocation(program, 'projection')
    uniform_locs['use_color_loc'] = glGetUniformLocation(program, 'use_color')


def set_use_color(v):
    glUniform1i(uniform_locs['use_color_loc'], v)

def set_model(model):
    glUniformMatrix4fv(uniform_locs['model_loc'], 1, GL_FALSE, model)

def set_view(view):
    glUniformMatrix4fv(uniform_locs['view_loc'], 1, GL_FALSE, view)

def set_projection(projection):
    glUniformMatrix4fv(uniform_locs['projection_loc'], 1, GL_FALSE, projection)
