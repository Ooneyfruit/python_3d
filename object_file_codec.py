def decode_obj(file_name):
    from os import getcwd, chdir
    
    class decode:
        def v(self, vertex):
            self.vertices.append([float(val) for val in vertex])
            
        def vn(self,vertex_normal):
            self.vertex_normals.append([float(val) for val in vertex_normal])
        
        def f(self,face):
            if "/" in face[0]:
              indices = [[int(val)-1 for val in face[n].split("/")] for n in range(3)]
              self.faces.append(indices)
              self.sides_indices.append([indices[n][0] for n in range(3)])
            else:
              self.sides_indices.append([int(val)-1 for val in face])
            
        function_names = dir()[2:]
        dispatcher = dict()
        for function in function_names:
          dispatcher[function] = eval(function)
        
        def __dir__(self):
          return self.dispatcher
        
        def __init__(self):
          self.vertices = list()
          self.vertex_normals = list()
          self.faces = list()
          self.sides_indices = list()
          
    decode_object = decode()
    dispatcher = decode_object.__dir__()
    
    path_name = getcwd() + "/Object_Files"
    chdir(path_name)
    print(path_name)
    obj_file_pointer = open(file_name + ".obj", "r")
    for line in obj_file_pointer:
        current_line = line
        current_split = current_line.strip("\n").split()
        try:
          dispatcher[current_split[0]](decode_object, current_split[1:])
        except (KeyError, IndexError) as KeyIndexError:
          continue
          
    return decode_object

def test():       
  test = decode_obj("lanky.obj")
  print(test.vertices[:6])
  print(test.vertex_normals[:6])
  print(test.faces[:6])
  print(test.sides_indices[:6])
  
#test()