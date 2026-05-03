import numpy as np
from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.engine.model.SimplePolygon import SimplePolygon
from src.math.Mat4x4 import Mat4x4

def q_from_axis_angle(axis, angle_deg):
    axis = np.array(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    a = np.radians(angle_deg)
    return np.array([np.cos(a / 2), *(axis * np.sin(a / 2))], dtype=float)

def q_mul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ], dtype=float)

def q_conj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]], dtype=float)

def q_norm(q):
    return q / np.linalg.norm(q)

def q_rotate_vector(v, q):
    q = q_norm(q)
    p = np.array([0, v[0], v[1], v[2]], dtype=float)
    return q_mul(q_mul(q, p), q_conj(q))[1:]

def q_to_mat4(q):
    q = q_norm(q)
    w, x, y, z = q
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w),     2*(x*z + y*w),     0],
        [2*(x*y + z*w),     1 - 2*(x*x + z*z), 2*(y*z - x*w),     0],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x*x + y*y), 0],
        [0,                 0,                 0,                 1]
    ], dtype=float)

def apply_mat4(points, M):
    return points @ M.T

def print_matrix(name, M):
    print(name)
    print(np.array_str(M, precision=6, suppress_small=True))

def print_points(name, pts):
    print(name)
    for i, p in enumerate(pts):
        print(f"P{i}: ({p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f})")

def cube_points():
    return np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 1]
    ], dtype=float)

def tetra_points():
    return np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1]
    ], dtype=float)

def add_cube(scene, key, color, edge_color, alpha, M=None):
    obj = Cube(alpha=alpha, color=color, edge_color=edge_color)
    if M is not None:
        obj.transformation = Mat4x4(M)
    scene[key] = obj

def add_tetra(scene, prefix, color, edge_color, alpha, M=None):
    vertices = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    faces = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    for i, face in enumerate(faces):
        coords = []
        for idx in face:
            coords.extend(vertices[idx])
        poly = SimplePolygon(*coords, color=color, edgecolor=edge_color, alpha=alpha)
        if M is not None:
            poly.transformation = Mat4x4(M)
        scene[f"{prefix}_{i}"] = poly

def add_vector_triangle(scene, key, v, color, edge_color, alpha, M=None):
    v = np.array(v, dtype=float)
    side = np.array([0, 0.05, 0], dtype=float)
    poly = SimplePolygon(
        0, 0, 0,
        v[0], v[1], v[2],
        v[0] + side[0], v[1] + side[1], v[2] + side[2],
        color=color,
        edgecolor=edge_color,
        alpha=alpha
    )
    if M is not None:
        poly.transformation = Mat4x4(M)
    scene[key] = poly

def show_cube(M, title):
    scene = Scene(
        coordinate_rect=(-3, -3, -3, 4, 4, 4),
        title=title,
        axis_color="grey",
        axis_line_style="-."
    )
    add_cube(scene, "initial", "cyan", "blue", 0.2)
    add_cube(scene, "final", "orange", "red", 0.7, M)
    scene.show()

def show_tetra(M, title):
    scene = Scene(
        coordinate_rect=(-3, -3, -3, 4, 4, 4),
        title=title,
        axis_color="grey",
        axis_line_style="-."
    )
    add_tetra(scene, "initial", "cyan", "blue", 0.2)
    add_tetra(scene, "final", "orange", "red", 0.7, M)
    scene.show()

def show_vector(v, q, title):
    M = q_to_mat4(q)
    scene = Scene(
        coordinate_rect=(-2, -2, -2, 2, 2, 2),
        title=title,
        axis_color="grey",
        axis_line_style="-."
    )
    add_vector_triangle(scene, "initial", v, "cyan", "blue", 0.3)
    add_vector_triangle(scene, "final", v, "orange", "red", 0.8, M)
    scene.show()

def matrix_to_quaternion(R):
    R = np.array(R, dtype=float)
    tr = np.trace(R)
    if tr > 0:
        s = np.sqrt(tr + 1.0) * 2
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s
    return q_norm(np.array([w, x, y, z], dtype=float))

def axis_angle_from_quaternion(q):
    q = q_norm(q)
    w = np.clip(q[0], -1, 1)
    angle = 2 * np.degrees(np.arccos(w))
    s = np.sqrt(1 - w*w)
    if s < 1e-8:
        axis = np.array([1, 0, 0], dtype=float)
    else:
        axis = q[1:] / s
    return axis, angle

def task_0():
    axis = [1, 1, 0]
    angle = 60
    q = q_from_axis_angle(axis, angle)
    M = q_to_mat4(q)
    pts = apply_mat4(cube_points(), M)
    print(q)
    print(np.linalg.norm(q))
    print_matrix("R", M)
    print_points("vertices", pts)
    show_cube(M, "Quaternion task 0")

def task_1():
    v = np.array([1, 0, 0], dtype=float)
    q = q_from_axis_angle([0, 0, 1], 90)
    rotated = q_rotate_vector(v, q)
    M = q_to_mat4(q)
    print(np.array([0, *v]))
    print(q)
    print(rotated)
    print_matrix("R", M)
    show_vector(v, q, "Quaternion task 1")

def task_2():
    q1 = q_from_axis_angle([1, 0, 0], 45)
    q2 = q_from_axis_angle([0, 1, 0], 30)
    q = q_mul(q2, q1)
    axis, angle = axis_angle_from_quaternion(q)
    M = q_to_mat4(q)
    pts = tetra_points()
    final = np.array([[*q_rotate_vector(p[:3], q), 1] for p in pts])
    print(q1)
    print(q2)
    print(q)
    print(axis)
    print(angle)
    print_points("final", final)
    show_tetra(M, "Quaternion task 2")

def task_3():
    yaw = q_from_axis_angle([0, 0, 1], 30)
    pitch = q_from_axis_angle([0, 1, 0], 90)
    roll = q_from_axis_angle([1, 0, 0], 45)
    q = q_mul(yaw, q_mul(pitch, roll))
    M = q_to_mat4(q)
    pts = apply_mat4(cube_points(), M)
    print(yaw)
    print(pitch)
    print(roll)
    print(q)
    print(np.linalg.norm(q))
    print_matrix("R", M)
    print_points("vertices", pts)
    show_cube(M, "Quaternion task 3")

def task_4():
    R = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=float)
    q = matrix_to_quaternion(R)
    M = q_to_mat4(q)
    pts = apply_mat4(cube_points(), M)
    print(q)
    print_matrix("R from q", M)
    print_points("vertices", pts)
    show_cube(M, "Quaternion task 4")

def task_5():
    M = np.eye(4)
    t = M[:3, 3]
    A = M[:3, :3]
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    sz = np.linalg.norm(A[:, 2])
    scales = np.array([sx, sy, sz], dtype=float)
    R = A @ np.linalg.inv(np.diag(scales))
    q = matrix_to_quaternion(R)
    pts = apply_mat4(cube_points(), M)
    print(t)
    print(scales)
    print_matrix("R", R)
    print_matrix("R.T @ R", R.T @ R)
    print(q)
    print_points("vertices", pts)
    show_cube(M, "Quaternion task 5")

TASKS = {
    "0": task_0,
    "1": task_1,
    "2": task_2,
    "3": task_3,
    "4": task_4,
    "5": task_5
}

def main():
    print("0 1 2 3 4 5")
    n = input().strip()
    if n in TASKS:
        TASKS[n]()

if __name__ == "__main__":
    main()
