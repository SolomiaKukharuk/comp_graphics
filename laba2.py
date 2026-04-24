import numpy as np

from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.engine.model.SimplePolygon import SimplePolygon
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import vertex

# ============================================================
#  Допоміжні функції для математики
# ============================================================

def T(tx, ty, tz):
    return Mat4x4.translation(tx, ty, tz)


def S(sx, sy=None, sz=None):
    if sy is None and sz is None:
        return Mat4x4.scale(sx)
    return Mat4x4.scale(sx, sy, sz)


def Rx(deg):
    return Mat4x4.rotation_x(np.radians(deg))


def Ry(deg):
    return Mat4x4.rotation_y(np.radians(deg))


def Rz(deg):
    return Mat4x4.rotation_z(np.radians(deg))


def R_axis(axis, deg):
    """Обертання навколо довільної осі через формулу Родрігеса."""
    axis = np.array(axis, dtype=float)
    norm = np.linalg.norm(axis)
    if norm == 0:
        raise ValueError("Вісь обертання не може бути нульовим вектором")
    x, y, z = axis / norm
    a = np.radians(deg)
    c = np.cos(a)
    s = np.sin(a)
    C = 1 - c

    m = np.array([
        [c + x*x*C,     x*y*C - z*s, x*z*C + y*s, 0],
        [y*x*C + z*s,   c + y*y*C,   y*z*C - x*s, 0],
        [z*x*C - y*s,   z*y*C + x*s, c + z*z*C,   0],
        [0,             0,           0,           1],
    ], dtype=float)
    return Mat4x4(m)


def euler_xyz(ax, ay, az):
    # У Mat4x4 для XYZ реалізовано Rx * Ry * Rz
    return Mat4x4.rotation_euler(np.radians(ax), np.radians(ay), np.radians(az), configuration=Mat4x4.XYZ)


def euler_zyx(az, ay, ax):
    # У Mat4x4 для ZYX реалізовано Rz * Ry * Rx
    return Mat4x4.rotation_euler(np.radians(az), np.radians(ay), np.radians(ax), configuration=Mat4x4.ZYX)


def around_pivot(M, pivot):
    px, py, pz = pivot
    return T(px, py, pz) * M * T(-px, -py, -pz)


def apply_matrix(points, M):
    result = []
    for p in points:
        v = vertex(p[0], p[1], p[2])
        tv = M * v
        result.append([tv.x, tv.y, tv.z])
    return np.array(result, dtype=float)


def print_matrix(title, M):
    print(f"\n{title}:")
    print(M)


def print_points(title, points):
    print(f"\n{title}:")
    for i, p in enumerate(points):
        print(f"P{i}: ({p[0]:.4f}, {p[1]:.4f}, {p[2]:.4f})")


def print_step(name, points, M):
    print_matrix(f"Матриця: {name}", M)
    new_points = apply_matrix(points, M)
    print_points(f"Після трансформації: {name}", new_points)
    return new_points


# ============================================================
#  Об'єкти
# ============================================================

CUBE_POINTS = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
], dtype=float)

TETRA_POINTS = np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
], dtype=float)

TRIANGLE_POINTS = np.array([
    [1, 2, 3], [4, 5, 6], [7, 8, 9]
], dtype=float)

RECTANGLE_POINTS = np.array([
    [1, 2, 0], [4, 2, 0], [4, 5, 0], [1, 5, 0]
], dtype=float)


# ============================================================
#  Побудова фігур у GraphicEngine3D
# ============================================================

def cube_model(color="cyan", edge_color="blue", alpha=0.25, line_style="-"):
    return Cube(alpha=alpha, color=color, edge_color=edge_color, line_style=line_style)


def tetra_faces(color="cyan", edge_color="blue", alpha=0.25, line_style="-"):
    pts = TETRA_POINTS.tolist()
    faces = [
        [pts[0], pts[1], pts[2]],
        [pts[0], pts[1], pts[3]],
        [pts[0], pts[2], pts[3]],
        [pts[1], pts[2], pts[3]],
    ]
    return [SimplePolygon(*face, color=color, edgecolor=edge_color, alpha=alpha, line_style=line_style) for face in faces]


def triangle_faces(color="cyan", edge_color="blue", alpha=0.35, line_style="-"):
    return [SimplePolygon(*TRIANGLE_POINTS.tolist(), color=color, edgecolor=edge_color, alpha=alpha, line_style=line_style)]


def rectangle_faces(color="cyan", edge_color="blue", alpha=0.35, line_style="-"):
    return [SimplePolygon(*RECTANGLE_POINTS.tolist(), color=color, edgecolor=edge_color, alpha=alpha, line_style=line_style)]


def transformed_copies(models, M, pivot=None):
    result = []
    for model in models:
        model.transformation = M
        if pivot is not None:
            model.pivot(*pivot)
            model.show_pivot()
        result.append(model)
    return result


def scene_bounds(*point_sets, margin=1.0):
    all_pts = np.vstack(point_sets)
    mn = all_pts.min(axis=0) - margin
    mx = all_pts.max(axis=0) + margin
    # щоб межі не були нульовими
    for i in range(3):
        if abs(mx[i] - mn[i]) < 1e-6:
            mx[i] += 1
            mn[i] -= 1
    return (mn[0], mn[1], mn[2], mx[0], mx[1], mx[2])


def show_engine_scene(kind, initial_points, final_points, M, title, pivot=None):
    rect = scene_bounds(initial_points, final_points, margin=1.5)
    scene = Scene(
        image_size=(8, 8),
        coordinate_rect=rect,
        title=title,
        grid_show=True,
        axis_show=True,
        axis_color=("red", "green", "blue"),
        axis_line_style="-.",
        axis_show_from_origin=True,
    )

    if kind == "cube":
        init_models = [cube_model(color="cyan", edge_color="blue", alpha=0.15, line_style="--")]
        fin_models = [cube_model(color="orange", edge_color="red", alpha=0.35, line_style="-")]
    elif kind == "tetra":
        init_models = tetra_faces(color="cyan", edge_color="blue", alpha=0.15, line_style="--")
        fin_models = tetra_faces(color="orange", edge_color="red", alpha=0.35, line_style="-")
    elif kind == "triangle":
        init_models = triangle_faces(color="cyan", edge_color="blue", alpha=0.25, line_style="--")
        fin_models = triangle_faces(color="orange", edge_color="red", alpha=0.45, line_style="-")
    elif kind == "rectangle":
        init_models = rectangle_faces(color="cyan", edge_color="blue", alpha=0.25, line_style="--")
        fin_models = rectangle_faces(color="orange", edge_color="red", alpha=0.45, line_style="-")
    else:
        raise ValueError("Невідомий тип фігури")

    for i, model in enumerate(init_models):
        scene[f"initial_{i}"] = model

    for i, model in enumerate(fin_models):
        model.transformation = M
        if pivot is not None:
            model.pivot(*pivot)
            model.show_pivot()
        scene[f"final_{i}"] = model

    scene.show()


def solve_and_show(task_name, kind, points, matrices, names, pivot_for_show=None):
    print(f"\n=== {task_name} ===")
    print_points("Початкові координати", points)

    current = points.copy()
    total = Mat4x4.identity()

    for M, name in zip(matrices, names):
        current = print_step(name, current, M)
        total = M * total

    print_matrix("Загальна матриця", total)
    print_points("Фінальні координати", current)
    show_engine_scene(kind, points, current, total, task_name, pivot=pivot_for_show)


# ============================================================
#  Задачі. Задачі 12 немає за проханням користувача.
# ============================================================

def task_1():
    R = R_axis((1, 1, 0), 45)
    move = T(2, -1, 3)
    solve_and_show("Task 1", "cube", CUBE_POINTS, [R, move], ["обертання 45° навколо осі (1,1,0)", "переміщення (2,-1,3)"])


def task_2():
    sc = S(2, 0.5, 1)
    R = euler_xyz(30, 45, 60)
    move = T(-3, 2, 5)
    solve_and_show("Task 2", "cube", CUBE_POINTS, [sc, R, move], ["розтяг X*2, Y*0.5", "Euler XYZ (30°,45°,60°)", "переміщення (-3,2,5)"])


def task_3():
    R1 = Rz(60)
    R2 = R_axis((1, 1, 1), 45)
    move = T(4, -2, 1)
    solve_and_show("Task 3", "cube", CUBE_POINTS, [R1, R2, move], ["обертання Z 60°", "обертання навколо (1,1,1) 45°", "переміщення (4,-2,1)"])


def task_4():
    R = euler_zyx(20, 35, 50)
    move = T(1, 3, -2)
    solve_and_show("Task 4", "cube", CUBE_POINTS, [R, move], ["Euler ZYX (20°,35°,50°)", "переміщення (1,3,-2)"])


def task_5():
    # seed можна змінити або прибрати, якщо треба щоразу випадковий результат
    np.random.seed(5)
    angle = np.random.uniform(10, 90)
    axis = np.random.uniform(-1, 1, 3)
    while np.linalg.norm(axis) < 1e-9:
        axis = np.random.uniform(-1, 1, 3)
    move_vec = np.random.uniform(-5, 5, 3)

    print(f"\nВипадковий кут = {angle:.4f}°")
    print(f"Випадкова вісь = {axis}")
    print(f"Випадковий вектор переміщення = {move_vec}")

    R = R_axis(axis, angle)
    move = T(move_vec[0], move_vec[1], move_vec[2])
    solve_and_show("Task 5", "tetra", TETRA_POINTS, [R, move], ["випадкове обертання", "випадкове переміщення"])


def task_6():
    pivot = (2, 0, 3)
    R = around_pivot(Ry(45), pivot)
    move = T(-1, 2, 4)
    solve_and_show("Task 6", "cube", CUBE_POINTS, [R, move], ["обертання Y 45° навколо pivot (2,0,3)", "переміщення (-1,2,4)"], pivot_for_show=pivot)


def task_7():
    pivot = (1, 2, 3)
    sc = around_pivot(S(1, 1, 3), pivot)
    R = around_pivot(Rz(30), pivot)
    solve_and_show("Task 7", "cube", CUBE_POINTS, [sc, R], ["розтяг Z*3 навколо pivot (1,2,3)", "обертання Z 30° навколо pivot (1,2,3)"], pivot_for_show=pivot)


def task_8():
    pivot = (2, 3, 4)
    R = around_pivot(R_axis((1, 1, 1), 90), pivot)
    move = T(0, -3, 2)
    solve_and_show("Task 8", "triangle", TRIANGLE_POINTS, [R, move], ["обертання 90° навколо осі (1,1,1), що проходить через (2,3,4)", "переміщення (0,-3,2)"], pivot_for_show=pivot)


def task_9():
    pivot = (3, 3, 0)
    R1 = around_pivot(Ry(60), pivot)
    R2 = around_pivot(Rx(30), pivot)
    solve_and_show("Task 9", "rectangle", RECTANGLE_POINTS, [R1, R2], ["поворот Y 60° навколо pivot (3,3,0)", "поворот X 30° навколо pivot (3,3,0)"], pivot_for_show=pivot)


def task_10():
    pivot = (1, 1, 1)
    sc = around_pivot(S(2, 1, 1), pivot)
    R = around_pivot(Ry(45), pivot)
    move = T(-3, 4, 2)
    solve_and_show("Task 10", "cube", CUBE_POINTS, [sc, R, move], ["розтяг X*2 навколо pivot (1,1,1)", "обертання Y 45° навколо pivot (1,1,1)", "переміщення (-3,4,2)"], pivot_for_show=pivot)


def task_11():
    print("\n=== Task 11 ===")
    # Зовнішні обертання: навколо світових осей X, Y, Z.
    A = Rz(60) * Ry(45) * Rx(30)

    # Внутрішні обертання множаться справа. Для цієї пари послідовностей
    # результат матрично збігається з A.
    B = Rz(60) * Ry(45) * Rx(30)

    print_matrix("Матриця A: зовнішні обертання X30 -> Y45 -> Z60", A)
    print_matrix("Матриця B: внутрішні обертання, еквівалентна послідовність", B)
    print_matrix("A - B", A - B)

    pts_A = apply_matrix(CUBE_POINTS, A)
    pts_B = apply_matrix(CUBE_POINTS, B)
    print_points("Фінальні координати для A", pts_A)
    print_points("Фінальні координати для B", pts_B)

    show_engine_scene("cube", CUBE_POINTS, pts_A, A, "Task 11")


def task_13():
    print("\n=== Task 13 ===")
    M = Mat4x4.identity()
    pts0 = TETRA_POINTS.copy()
    print_points("Початкові координати", pts0)

    # Внутрішні трансформації множимо справа: M = M * Mi
    R1 = Rx(45)
    M = M * R1
    pts1 = apply_matrix(pts0, M)
    print_matrix("Крок 1: локальне обертання X 45°", M)
    print_points("Після кроку 1", pts1)

    # Переміщення вздовж оновленої локальної Y: локальне T справа
    move_local_y = T(0, 2, 0)
    M = M * move_local_y
    pts2 = apply_matrix(pts0, M)
    print_matrix("Крок 2: локальне переміщення вздовж Y на 2", M)
    print_points("Після кроку 2", pts2)

    R2 = Rz(30)
    M = M * R2
    pts3 = apply_matrix(pts0, M)
    print_matrix("Крок 3: локальне обертання Z 30°", M)
    print_points("Після кроку 3", pts3)

    show_engine_scene("tetra", pts0, pts3, M, "Task 13")


def decompose_scale_angle_axis(M):
    A = M.data[:3, :3]
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    sz = np.linalg.norm(A[:, 2])
    R = A @ np.linalg.inv(np.diag([sx, sy, sz]))

    value = (np.trace(R) - 1) / 2
    value = np.clip(value, -1, 1)
    angle = np.degrees(np.arccos(value))

    if abs(np.sin(np.radians(angle))) < 1e-8:
        axis = np.array([0, 1, 0], dtype=float)
    else:
        axis = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1],
        ]) / (2 * np.sin(np.radians(angle)))

    return (sx, sy, sz), angle, axis


def task_15():
    print("\n=== Task 15 ===")
    pivot = (1, 1, 1)

    sc = around_pivot(S(2, 2, 2), pivot)
    R_local = Ry(90)
    move = T(-3, 4, 2)

    # Масштабування навколо pivot, потім внутрішнє обертання справа, потім зовнішнє переміщення зліва.
    M = move * sc * R_local
    pts = apply_matrix(CUBE_POINTS, M)

    print_matrix("Масштабування навколо pivot", sc)
    print_matrix("Внутрішнє обертання Y 90°", R_local)
    print_matrix("Зовнішнє переміщення", move)
    print_matrix("Фінальна матриця", M)
    print_points("Фінальні координати", pts)

    scale_values, angle, axis = decompose_scale_angle_axis(M)
    print("\nДекомпозиція фінальної матриці:")
    print(f"scale = ({scale_values[0]:.4f}, {scale_values[1]:.4f}, {scale_values[2]:.4f})")
    print(f"angle = {angle:.4f}°")
    print(f"axis = ({axis[0]:.4f}, {axis[1]:.4f}, {axis[2]:.4f})")

    show_engine_scene("cube", CUBE_POINTS, pts, M, "Task 15", pivot=pivot)


TASKS = {
    "1": task_1,
    "2": task_2,
    "3": task_3,
    "4": task_4,
    "5": task_5,
    "6": task_6,
    "7": task_7,
    "8": task_8,
    "9": task_9,
    "10": task_10,
    "11": task_11,
    "13": task_13,
    "15": task_15,
}


def main():
    print("Оберіть задачу:")
    print("1 2 3 4 5 6 7 8 9 10 11 13 15")
    print("Задачу 12 пропущено, бо в умові немає фінальної матриці.")
    number = input("Введіть номер: ").strip()
    if number in TASKS:
        TASKS[number]()
    else:
        print("Такої задачі немає в меню.")


if __name__ == "__main__":
    main()
