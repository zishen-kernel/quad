from OpenGL.GL.shaders import compileProgram, compileShader

def load(shader_type, shader_path):
    f = open(shader_path)
    data = f.read()
    shader = compileShader(data, shader_type)
    return shader
