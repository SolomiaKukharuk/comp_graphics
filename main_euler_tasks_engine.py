import numpy as np

from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.math.Mat4x4 import Mat4x4


CUBE_POINTS = np.array([
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 1, 1],
    [0, 1, 1, 1],
], dtype=float)


def deg(value):
    return np.radians(value)


def apply_matrix(points, M):
    data = M.data if isinstance(M, Mat4x4) else np.array(M, dtype=float)
    return (data @ points.T).T


def mat_np(M):
    return M.data if isinstance(M, Mat4x4) else np.array(M, dtype=float)


def print_matrix(title, M):
    print(f"\n{title}:")
    print(np.array_str(mat_np(M), precision=6, suppress_small=True))


def print_points(title, pts):
    print(f"\n{title}:")
    for i, p in enumerate(pts):
        print(f"P{i}: ({p[0]: .6f}, {p[1]: .6f}, {p[2]: .6f})")


def print_step_calculation(points, matrices, names):
    current = points.copy()
    total = Mat4x4.identity()

    print_points("Початкові координати", current)

    for M, name in zip(matrices, names):
        print_matrix(f"Матриця етапу: {name}", M)
        current = apply_matrix(current, M)
        total = M * total
        print_points(f"Координати після етапу: {name}", current)

    print_matrix("Загальна матриця", total)
    print_points("Фінальні координати", current)

    return total, current


def euler_xyz(ax, ay, az):
    return Mat4x4.rotation_euler(deg(ax), deg(ay), deg(az), Mat4x4.XYZ)


def euler_zyx(az, ay, ax):
    return Mat4x4.rotation_euler(deg(az), deg(ay), deg(ax), Mat4x4.ZYX)


def get_bounds(points_list, margin=1.5):
    all_pts = np.vstack([pts[:, :3] for pts in points_list])
    mins = all_pts.min(axis=0) - margin
    maxs = all_pts.max(axis=0) + margin
    center = (mins + maxs) / 2
    span = max(maxs - mins)
    if span <= 0:
        span = 2
    half = span / 2
    mins = center - half
    maxs = center + half

    return (mins[0], mins[1], mins[2], maxs[0], maxs[1], maxs[2])


def show_two_cubes(M_final, title="Euler task"):
    final_pts = apply_matrix(CUBE_POINTS, M_final)
    rect = get_bounds([CUBE_POINTS, final_pts])

    scene = Scene(
        coordinate_rect=rect,
        axis_color="grey",
        axis_line_style="-."
    )

    initial_cube = Cube(alpha=0.15, color="cyan", edge_color="blue", line_style="--", line_width=1.0)
    final_cube = Cube(alpha=0.45, color="orange", edge_color="red", line_style="-", line_width=1.5)
    final_cube.transformation = M_final

    initial_cube.show_local_frame()
    final_cube.show_local_frame()

    scene["initial_cube"] = initial_cube
    scene["final_cube"] = final_cube
    scene.show()


def show_many_cubes(matrices, title="Euler interpolation"):
    point_sets = [CUBE_POINTS]
    for M in matrices:
        point_sets.append(apply_matrix(CUBE_POINTS, M))

    rect = get_bounds(point_sets)

    scene = Scene(
        coordinate_rect=rect,
        axis_color="grey",
        axis_line_style="-."
    )

    start_cube = Cube(alpha=0.12, color="cyan", edge_color="blue", line_style="--", line_width=0.8)
    scene["cube_start"] = start_cube

    for i, M in enumerate(matrices):
        cube = Cube(alpha=0.18, color="orange", edge_color="red", line_style="-", line_width=0.8)
        cube.transformation = M
        scene[f"cube_{i}"] = cube

    scene.show()



def task_1():
    print("Розтяг, обертання Euler XYZ і зсув")

    S = Mat4x4.scale(2, 0.5, 1)
    R = euler_xyz(30, 45, 60)
    T = Mat4x4.translation(-3, 2, 5)

    M, _ = print_step_calculation(
        CUBE_POINTS,
        [S, R, T],
        ["розтяг S = scale(2, 0.5, 1)", "обертання Euler XYZ(30,45,60)", "переміщення T(-3,2,5)"]
    )

    show_two_cubes(M, "Euler task 1")



def task_2():
    print("Поворот у системі Euler ZYX")

    R = euler_zyx(20, 35, 50)
    T = Mat4x4.translation(1, 3, -2)

    M, _ = print_step_calculation(
        CUBE_POINTS,
        [R, T],
        ["обертання Euler ZYX(20,35,50)", "переміщення T(1,3,-2)"]
    )

    show_two_cubes(M, "Euler task 2")




def task_3():
    print("Конвенції та послідовність обертань")

    ax, ay, az = 30, 45, 60

    R_xyz = euler_xyz(ax, ay, az)
    R_zyx = euler_zyx(ax, ay, az)

    pts_xyz = apply_matrix(CUBE_POINTS, R_xyz)
    pts_zyx = apply_matrix(CUBE_POINTS, R_zyx)

    print(f"\nВхідні кути: ({ax}°, {ay}°, {az}°)")
    print_matrix("Матриця R_XYZ", R_xyz)
    print_matrix("Матриця R_ZYX", R_zyx)
    print_matrix("Різниця R_XYZ - R_ZYX", Mat4x4(R_xyz.data - R_zyx.data))

    print_points("Координати вершин після XYZ", pts_xyz)
    print_points("Координати вершин після ZYX", pts_zyx)

    print("\nПояснення:")
    print("У 3D обертання некомутативні: зміна порядку множення матриць змінює фінальну орієнтацію.")
    print("Тому однакові кути для XYZ і ZYX не дають однакового положення куба.")

    choice = input("\nЩо показати? 1 - XYZ, 2 - ZYX: ").strip()
    if choice == "2":
        show_two_cubes(R_zyx, "Euler task 3: ZYX")
    else:
        show_two_cubes(R_xyz, "Euler task 3: XYZ")



def task_4():
    print("Математичне виведення Gimbal Lock")

    print("""
Беремо конвенцію XYZ у вигляді:

    R = Rx(alpha) * Ry(beta) * Rz(gamma)

Елементарні матриці:

Rx(alpha) =
[ 1      0           0      ]
[ 0   cos(a)    -sin(a)    ]
[ 0   sin(a)     cos(a)    ]

Ry(beta) =
[ cos(b)   0   sin(b) ]
[   0      1     0    ]
[-sin(b)   0   cos(b) ]

Rz(gamma) =
[ cos(g)   -sin(g)   0 ]
[ sin(g)    cos(g)   0 ]
[   0         0      1 ]

При beta = 90° маємо cos(beta)=0, sin(beta)=1.
Тоді матриця спрощується до:

R =
[       0              0          1 ]
[ sin(alpha+gamma)  cos(alpha+gamma) 0 ]
[-cos(alpha+gamma)  sin(alpha+gamma) 0 ]

Тобто результат залежить не від alpha і gamma окремо,
а тільки від їхньої суми alpha + gamma.
Це означає, що один ступінь вільності втрачено.
""")

    R1 = euler_xyz(30, 90, 45)
    R2 = euler_xyz(40, 90, 35)  # 30+45 = 40+35 = 75

    print_matrix("R1 = XYZ(30, 90, 45)", R1)
    print_matrix("R2 = XYZ(40, 90, 35)", R2)
    print_matrix("R1 - R2", Mat4x4(R1.data - R2.data))

    print("\nОскільки alpha+gamma однакові, матриці збігаються або відрізняються лише похибкою округлення.")
    show_two_cubes(R1, "Euler task 4: Gimbal Lock")



def task_5():
    print("Практичний експеримент 'Втрачена вісь'")

    # Якщо в умові інші числа — зміни тут.
    first = (30, 90, 45)
    second = (40, 90, 35)  # сума першого і третього кута така сама: 75°

    R1 = euler_xyz(*first)
    R2 = euler_xyz(*second)

    pts1 = apply_matrix(CUBE_POINTS, R1)
    pts2 = apply_matrix(CUBE_POINTS, R2)

    print(f"\nПерший набір кутів XYZ: {first}")
    print(f"Другий набір кутів XYZ: {second}")

    print_matrix("R1", R1)
    print_matrix("R2", R2)
    print_matrix("R1 - R2", Mat4x4(R1.data - R2.data))

    print_points("Координати після першого набору", pts1)
    print_points("Координати після другого набору", pts2)

    max_diff = np.max(np.abs(pts1 - pts2))
    print(f"\nМаксимальна різниця координат: {max_diff:.10f}")
    print("Висновок: при beta = 90° різні параметри alpha і gamma можуть давати те саме положення.")

    show_two_cubes(R1, "Euler task 5: lost axis")



def task_6():
    print("Інтерполяція в зоні сингулярності")
    A = np.array([0.0, 80.0, 0.0])
    B = np.array([0.0, 100.0, 0.0])

    matrices = []

    print(f"\nПоложення A = {A}")
    print(f"Положення B = {B}")
    print("\n10 кроків Lerp для кутів XYZ:")

    forward0 = np.array([[0, 0, 1, 1]], dtype=float)

    for i, t in enumerate(np.linspace(0, 1, 10)):
        angles = A + t * (B - A)
        R = euler_xyz(angles[0], angles[1], angles[2])
        matrices.append(R)

        forward = apply_matrix(forward0, R)[0, :3]
        print(f"step {i}: t={t:.3f}, angles=({angles[0]:.3f}, {angles[1]:.3f}, {angles[2]:.3f}), forward={forward}")

    print("\nПояснення:")
    print("Лінійна інтерполяція Euler-кутів інтерполює не орієнтацію напряму, а три числові параметри.")
    print("Коли середній кут наближається до 90°, система наближається до сингулярності,")
    print("тому рух може виглядати неприродно або смикано.")

    show_many_cubes(matrices, "Euler task 6: interpolation")


def stable_to_euler_xyz(M):
    """
    Стабільний розклад для конвенції XYZ рушія:
    R = Rx(alpha) * Ry(beta) * Rz(gamma)

    Для цієї конвенції:
        beta = asin(R[0,2])
    При |cos(beta)| ~ 0 маємо Gimbal Lock.
    Тоді примусово ставимо gamma = 0 і знаходимо alpha.
    """
    R = M.data[:3, :3]
    eps = 1e-8

    beta = np.arcsin(np.clip(R[0, 2], -1.0, 1.0))
    cb = np.cos(beta)

    if abs(cb) > eps:
        alpha = np.arctan2(-R[1, 2], R[2, 2])
        gamma = np.arctan2(-R[0, 1], R[0, 0])
        gimbal = False
    else:
        # Сингулярність: один кут фіксуємо, щоб отримати стабільний розв'язок.
        gamma = 0.0
        if beta > 0:
            # при beta = +90° матриця залежить від alpha + gamma
            alpha = np.arctan2(R[1, 0], R[1, 1])
        else:
            # при beta = -90° аналогічний стабілізований варіант
            alpha = np.arctan2(-R[1, 0], R[1, 1])
        gimbal = True

    return np.degrees([alpha, beta, gamma]), gimbal


def task_7():
    print("Декомпозиція та неоднозначність розв'язку")

    R = Mat4x4.rotation_y(deg(90))

    print_matrix("Задана матриця R = Ry(90°)", R)

    angles, gimbal = stable_to_euler_xyz(R)
    print(f"\nСтабільний розклад XYZ: alpha={angles[0]:.6f}, beta={angles[1]:.6f}, gamma={angles[2]:.6f}")
    print(f"Gimbal Lock detected: {gimbal}")

    print("\nПеревірка неоднозначності:")
    examples = [
        (0, 90, 0),
        (30, 90, -30),
        (45, 90, -45),
        (75, 90, -75),
    ]

    base = euler_xyz(*examples[0])
    for ex in examples:
        M = euler_xyz(*ex)
        diff = np.max(np.abs(M.data - base.data))
        print(f"XYZ{ex} -> max difference from XYZ{examples[0]} = {diff:.10f}")

    print("\nВисновок:")
    print("У сингулярності існує нескінченно багато комбінацій кутів, які дають ту саму матрицю.")
    print("Щоб отримати стабільний розв'язок, алгоритм примусово встановлює один кут, тут gamma = 0.")

    show_two_cubes(R, "Euler task 7: decomposition")



TASKS = {
    "1": task_1,
    "2": task_2,
    "3": task_3,
    "4": task_4,
    "5": task_5,
    "6": task_6,
    "7": task_7,
}


def main():
    print("Оберіть номер задачі: 1 2 3 4 5 6 7")
    number = input("Введіть номер задачі: ").strip()

    if number in TASKS:
        TASKS[number]()
    else:
        print("Такої задачі немає. Введіть число від 1 до 7.")


if __name__ == "__main__":
    main()
