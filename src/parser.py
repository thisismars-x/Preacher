'''
serialize and load a wireframe object
input:  filepath
output: []vertices, []edges
'''

def decode(file_path: str):
    '''
    example [resources/diamond.obj]

    ---------------------------------
    # diamond.obj

    g Object001

    v 0.000000E+00 0.000000E+00 78.0000
    v 45.0000 45.0000 0.000000E+00
    v 45.0000 -45.0000 0.000000E+00
    v -45.0000 -45.0000 0.000000E+00
    v -45.0000 45.0000 0.000000E+00
    v 0.000000E+00 0.000000E+00 -78.0000

    f     1 2 3
    f     1 3 4
    f     1 4 5
    f     1 5 2
    f     6 5 4
    f     6 4 3
    f     6 3 2
    f     6 2 1
    f     6 1 5

    ---------------------------------
    
    '''
    vertices = []
    edges = set()

    try:
        with open(file_path, 'r') as file:

            for line in file:
                parts = line.strip().split()
                if not parts or parts[0] == '#':
                    continue

                if parts[0] == 'v': 
                    #register a triplet in floating point
                    vertex = list(map(float, parts[1:4]))  
                    vertices.append(vertex)

                elif parts[0] == 'f': 
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]  

                    for i in range(len(face)):
                        edges.add((face[i], face[(i + 1) % len(face)])) 

    except FileNotFoundError:
        print("File does not exist.\n Quitting now")
        return None, None
    
    except Exception as e:
        print(f"Error: {e}")
        return None, None

    return vertices, list(edges)