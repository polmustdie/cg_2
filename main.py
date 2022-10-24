from math import *
import pygame
ANGLE=pi/24
SCREEN_SIZE = (1024,800)
VECTORS = [(10,32),(20,47)]
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
LIGHT_GRAY=(220,220,220)

SCREEN_VEC1 = (1,0,0)
SCREEN_VEC2 = (0,1,0)

SCALE = 100
CENTER = (SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2)


def vec_length(vec):
    return sqrt(vec[0]**2+vec[1]**2+vec[2]**2)


def vec_norm(vec):
    length = vec_length(vec)
    if length == 0:
        return (0, 0, 0)
    norm = (vec[0]/length, vec[1]/length, vec[2]/length)
    return norm


def cross_product(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0])


def dot_product(v1, v2):
    ret = 0.0
    for i in range(len(v1)):
        ret += v1[i] * v2[i]
    return ret


SCREEN_NORMAL = vec_norm(cross_product(SCREEN_VEC1, SCREEN_VEC2))
print("SCREEN_NORMAL", SCREEN_NORMAL)

VERTICES_CUBE = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1)]

EDGES_CUBE = [(0, 1),  # 0
              (1, 2),  # 1
              (2, 3),  # 2
              (3, 0),  # 3
              (3, 4),  # 4
              (2, 5),  # 5
              (1, 6),  # 6
              (0, 7),  # 7
              (4, 5),  # 8
              (5, 6),  # 9
              (6, 7),  # 10
              (4, 7),  # 11
              ]



FACES_CUBE = [
    # (0,1,2,3),
    (3, 2, 1, 0),
    (2, 5, 8, 4),
    # (8,9,10,11),
    (10, 11, 9 ,8),
    # (10,6,0,7),#3
    (7, 10, 6, 0),
    (1, 6, 9, 5),
    (3, 4, 11, 7),
]

DRAW_CUBE = True
if DRAW_CUBE:
    VERTICES = VERTICES_CUBE
    EDGES = EDGES_CUBE
    FACES = FACES_CUBE


def normal(face):
    edge1 = EDGES[face[0]]
    edge2 = EDGES[face[1]]
    v1_1 = VERTICES[edge1[1]]
    v1_0 = VERTICES[edge1[0]]
    vec1 = (v1_1[0]-v1_0[0], v1_1[1]-v1_0[1])
    v2_1 = VERTICES[edge2[1]]
    v2_0 = VERTICES[edge2[0]]
    vec1 = (v1_1[0]-v1_0[0], v1_1[1]-v1_0[1], v1_1[2]-v1_0[2])
    vec2 = (v2_1[0]-v2_0[0], v2_1[1]-v2_0[1], v2_1[2]-v2_0[2])
    return vec_norm(cross_product(vec1, vec2))


def is_visible(edge_idx): # if normal >= 0 the edge is visible, else invisible
    for face in FACES:
        if edge_idx in face:
            norm = normal(face)
            cp = dot_product(SCREEN_NORMAL, norm)
            if face == (10,6,0,7):
                print(cp, norm, SCREEN_NORMAL)
            if cp >= 0:
                return True
    return False


def filter_edges():
    ret = set() # set of visible edges
    ret2 = set() # set of invisible edges
    for edge_idx in range(len(EDGES)):
        if is_visible(edge_idx):
            ret.add(EDGES[edge_idx])
        else:
            e=EDGES[edge_idx]
            if e not in ret:
                ret2.add(e)
    print(ret)
    print(ret2)
    return list(ret), list(ret2)


def matrix_rotate_x(angle):
    MX = [
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ]
    return MX


def matrix_rotate_y(angle):
    MY = [
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ]
    return MY


def matrix_rotate_z(angle):
    MZ = [
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ]
    return MZ


def rotate(angle, rot):
    m = rot(angle)
    for i in range(len(VERTICES)):
        VERTICES[i] = product(m, VERTICES[i])


def product(m,v): # Matrix product
    result = []
    for row in m:
        ret = 0
        for i in range(0,len(row)):
            xm = row[i]
            xv = v[i]
            ret += xv*xm
        result.append(ret)
    return result


def to_scr(pos):
    x = pos[0]*SCALE + CENTER[0]
    y = pos[1]*SCALE + CENTER[1]
    return(x, y)


def orthogonal(pos): #removing z
    return(pos[0], pos[1])


def draw_wireframe(screen, color, edges):
    for edge in edges:
        a = VERTICES[edge[0]]
        b = VERTICES[edge[1]]
        ortho_a = orthogonal(a)
        screen_ortho_a = to_scr(ortho_a)
        ortho_b = orthogonal(b)
        screen_ortho_b = to_scr(ortho_b)
        pygame.draw.line(screen, color, screen_ortho_a, screen_ortho_b ,5)


def draw_vec_center(screen, color, vec):
    x=vec[0]
    y=vec[1]
    pygame.draw.line(screen, color, CENTER, (SCREEN_SIZE[0]//2+x, SCREEN_SIZE[1]//2-y), 3)
    return


def draw_vert_index(screen, font): # drawing indexes of verices
    for i in range(len(VERTICES)):
        x = to_scr(orthogonal(VERTICES[i]))
        pic = font.render("%d"%i, False, BLACK)
        screen.blit(pic, x)


def draw_normals(screen):
    for face in FACES:
        norm = normal(face)
        e1 = EDGES[face[0]]
        v11 = VERTICES[e1[0]][0]
        v12 = VERTICES[e1[0]][1]
        v13 = VERTICES[e1[0]][2]
        mid = (v11, v12, v13)
        norm = (mid[0]+norm[0],mid[1]+norm[1], mid[2]+norm[2])
        pygame.draw.line(screen, BLACK, to_scr(mid), to_scr(norm), 2)
    return


def main():
    global SCALE
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024,800))
    font = pygame.font.SysFont('Sans', 32)

    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run=False
            elif ev.type == pygame.KEYDOWN:
                sign = 1.
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    sign = -1.
                if ev.key==pygame.K_UP:
                    VECTORS[0]=(VECTORS[0][0],VECTORS[0][1]+10)
                elif ev.key == pygame.K_q:
                    run = False
                elif ev.key == pygame.K_x:
                    rotate(sign*ANGLE, matrix_rotate_x)
                elif ev.key == pygame.K_z:
                    rotate(sign*ANGLE,matrix_rotate_z)
                elif ev.key == pygame.K_y:
                    rotate(sign*ANGLE,matrix_rotate_y)
                elif ev.key == pygame.K_RIGHT:
                    SCALE = SCALE + 50
                elif ev.key == pygame.K_LEFT:
                    SCALE = SCALE - 50

        screen.fill(WHITE)
        edges1, edges2 = filter_edges()
        draw_wireframe(screen, LIGHT_GRAY, edges2)
        draw_wireframe(screen, GREEN, edges1)
        draw_vert_index(screen, font)
        draw_normals(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except ArgumentError as error:
        print(error)
        pygame.quit()

