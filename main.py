import numpy as np
from src.engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon


# Вхідні базові дані
SQUARE_POINTS = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
], dtype=float)

FIGURE_KEY = "square"


# Допоміжні функції

def rot_matrix(deg: float):
    a = np.radians(deg)
    return np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a),  np.cos(a), 0],
        [0, 0, 1]
    ], dtype=float)

def trans_matrix(tx: float, ty: float):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)

def scale_matrix(sx: float, sy: float):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)

def pivot_matrix(px: float, py: float, M: np.ndarray):
    """
    Трансформація M відносно pivot:
    T(px,py) * M * T(-px,-py)
    """
    return trans_matrix(px, py) @ M @ trans_matrix(-px, -py)

def apply_matrix(points: np.ndarray, M: np.ndarray):
    return points @ M.T

def print_points(title: str, pts: np.ndarray):
    print(f"\n{title}")
    for i, p in enumerate(pts):
        print(f"P{i}: ({p[0]:.6f}, {p[1]:.6f})")

def print_matrix(title: str, M: np.ndarray):
    print(f"\n{title}")
    print(np.array_str(M, precision=6, suppress_small=True))

def polygon_xy_from_points(points: np.ndarray):
    return [(p[0], p[1]) for p in points]

def bounds_for_points(*point_sets, margin=1.0):
    all_pts = np.vstack(point_sets)
    xmin = np.min(all_pts[:, 0]) - margin
    ymin = np.min(all_pts[:, 1]) - margin
    xmax = np.max(all_pts[:, 0]) + margin
    ymax = np.max(all_pts[:, 1]) + margin
    return (xmin, ymin, xmax, ymax)


# Візуалізація
class TaskScene(Scene):
    def __init__(self, initial_pts, final_pts, title="Task", pivot=None, **kwargs):
        super().__init__(**kwargs)

        poly_initial = Polygon()
        poly_final = Polygon()

        self["initial"] = poly_initial
        self["final"] = poly_final

        poly_initial.set_geometry(*sum(([x, y] for x, y in polygon_xy_from_points(initial_pts)), []))
        poly_final.set_geometry(*sum(([x, y] for x, y in polygon_xy_from_points(final_pts)), []))

        poly_initial["color"] = "blue"
        poly_initial["line_style"] = "--"
        poly_initial["vertices_show"] = True
        poly_initial["vertex_color"] = "blue"

        poly_final["color"] = "red"
        poly_final["line_style"] = "-"
        poly_final["vertices_show"] = True
        poly_final["vertex_color"] = "red"

        if pivot is not None:
            self["final"].pivot(*pivot)
            self["final"].show_pivot()

def show_result(initial_pts, final_pts, title="Task", pivot=None):
    rect = bounds_for_points(initial_pts, final_pts, margin=1.0)
    scene = TaskScene(
        initial_pts=initial_pts[:, :2],
        final_pts=final_pts[:, :2],
        title=title,
        pivot=pivot,
        image_size=(7, 7),
        coordinate_rect=rect,
        grid_show=True,
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-."
    )
    scene.show()



def task_1():
    print("1")
    pts0 = SQUARE_POINTS.copy()

    R = rot_matrix(30)
    pts1 = apply_matrix(pts0, R)

    T = trans_matrix(2, 3)
    pts2 = apply_matrix(pts1, T)

    M = T @ R

    print_points("Початкові вершини:", pts0)
    print_matrix("Матриця повороту R:", R)
    print_points("Після повороту:", pts1)
    print_matrix("Матриця перенесення T:", T)
    print_points("Після перенесення:", pts2)
    print_matrix("Загальна матриця M = T * R:", M)

    show_result(pts0, pts2, title="Task 1")

def task_2():
    print("2")
    pts0 = SQUARE_POINTS.copy()

    S = scale_matrix(2, 1)
    pts1 = apply_matrix(pts0, S)

    R = rot_matrix(45)
    pts2 = apply_matrix(pts1, R)

    M = R @ S

    print_points("Початкові вершини:", pts0)
    print_matrix("Матриця розтягу S:", S)
    print_points("Після розтягу:", pts1)
    print_matrix("Матриця повороту R:", R)
    print_points("Після повороту:", pts2)
    print_matrix("Загальна матриця M = R @ S:", M)

    show_result(pts0, pts2, title="Task 2")

def task_3():
    print("3")
    pts0 = SQUARE_POINTS.copy()

    R = rot_matrix(90)
    pts1 = apply_matrix(pts0, R)

    T = trans_matrix(2, 3)
    pts2 = apply_matrix(pts1, T)

    M = T @ R

    print_points("Початкові вершини:", pts0)
    print_matrix("Матриця повороту R:", R)
    print_points("Після повороту:", pts1)
    print_matrix("Матриця перенесення T:", T)
    print_points("Після перенесення:", pts2)
    print_matrix("Загальна матриця M = T @ R:", M)

    show_result(pts0, pts2, title="Task 3")

def task_4():
    print("4")
    pts0 = SQUARE_POINTS.copy()

    S = scale_matrix(1, 3)
    pts1 = apply_matrix(pts0, S)

    R = rot_matrix(60)
    pts2 = apply_matrix(pts1, R)

    M = R @ S

    print_points("Початкові вершини:", pts0)
    print_matrix("Матриця розтягу S:", S)
    print_points("Після розтягу:", pts1)
    print_matrix("Матриця повороту R:", R)
    print_points("Після повороту:", pts2)
    print_matrix("Загальна матриця M = R @ S:", M)

    show_result(pts0, pts2, title="Task 4")

def task_5():
    print("5")
    pts0 = SQUARE_POINTS.copy()

    T = trans_matrix(1, -1)
    pts1 = apply_matrix(pts0, T)

    S = scale_matrix(2, 2)
    pts2 = apply_matrix(pts1, S)

    M = S @ T

    print_points("Початкові вершини:", pts0)
    print_matrix("Матриця перенесення T:", T)
    print_points("Після перенесення:", pts1)
    print_matrix("Матриця масштабування S:", S)
    print_points("Після масштабування:", pts2)
    print_matrix("Загальна матриця M = S @ T:", M)

    show_result(pts0, pts2, title="Task 5")

def task_6():
    print("6")
    pts0 = SQUARE_POINTS.copy()

    # Варіант 1: Розтяг -> Поворот -> Переміщення
    S = scale_matrix(1, 3)   # припускаю: по осі у у 3 рази
    R = rot_matrix(60)
    T = trans_matrix(2, 3)

    M1 = T @ R @ S
    pts1 = apply_matrix(pts0, M1)

    # Варіант 2: Переміщення -> Розтяг -> Поворот
    M2 = R @ S @ T
    pts2 = apply_matrix(pts0, M2)

    print_points("Початкові вершини:", pts0)

    print_matrix("S:", S)
    print_matrix("R:", R)
    print_matrix("T:", T)

    print_matrix("M1 = T @ R @ S:", M1)
    print_points("Фінальні координати для S -> R -> T:", pts1)

    print_matrix("M2 = R @ S @ T:", M2)
    print_points("Фінальні координати для T -> S -> R:", pts2)

    show_result(pts0, pts2, title="Task 6 - order 2")
    show_result(pts0, pts1, title="Task 6 - order 1")

def task_7():
    print("7")
    pts0 = SQUARE_POINTS.copy()
    pivots = [(0.5, 0.5), (0, 1), (1, 1), (2, 2)]
    R = rot_matrix(60)

    for idx, pivot in enumerate(pivots, start=1):
        px, py = pivot
        M = pivot_matrix(px, py, R)
        pts = apply_matrix(pts0, M)

        print(f"\n--- Pivot {idx}: {pivot} ---")
        print_matrix("Матриця трансформації:", M)
        print_points("Нові координати:", pts)

    choice = int(input("\nЯкий pivot показати (1-4)? ").strip())
    pivot = pivots[choice - 1]
    M = pivot_matrix(pivot[0], pivot[1], R)
    pts = apply_matrix(pts0, M)
    show_result(pts0, pts, title=f"Task 7 pivot {pivot}", pivot=pivot)

def task_8():
    print("8")
    pts0 = SQUARE_POINTS.copy()
    pivots = [(0.5, 0.5), (0, 1), (1, 1), (2, 2)]
    S = scale_matrix(2, 3)

    for idx, pivot in enumerate(pivots, start=1):
        px, py = pivot
        M = pivot_matrix(px, py, S)
        pts = apply_matrix(pts0, M)

        print(f"\n--- Pivot {idx}: {pivot} ---")
        print_matrix("Матриця трансформації:", M)
        print_points("Нові координати:", pts)

    choice = int(input("\nЯкий pivot показати (1-4)? ").strip())
    pivot = pivots[choice - 1]
    M = pivot_matrix(pivot[0], pivot[1], S)
    pts = apply_matrix(pts0, M)
    show_result(pts0, pts, title=f"Task 8 pivot {pivot}", pivot=pivot)

def task_9():
    print("9")
    pts0 = SQUARE_POINTS.copy()
    pivot = (1, 1)

    S_pivot = pivot_matrix(1, 1, scale_matrix(2, 1))
    T = trans_matrix(3, -2)

    # 1) Розтяг відносно pivot -> Переміщення
    M1 = T @ S_pivot
    pts1 = apply_matrix(pts0, M1)

    # 2) Переміщення -> Розтяг відносно pivot
    M2 = S_pivot @ T
    pts2 = apply_matrix(pts0, M2)

    print_matrix("Матриця розтягу відносно pivot:", S_pivot)
    print_matrix("Матриця переміщення T:", T)

    print_matrix("M1 = T @ S_pivot:", M1)
    print_points("Координати для розтяг -> переміщення:", pts1)

    print_matrix("M2 = S_pivot @ T:", M2)
    print_points("Координати для переміщення -> розтяг:", pts2)

    show_result(pts0, pts2, title="Task 9 - order 2", pivot=pivot)
    show_result(pts0, pts1, title="Task 9 - order 1", pivot=pivot)

def task_10():
    print("10")
    pts0 = SQUARE_POINTS.copy()
    pivot = (0.5, 0.5)

    S_pivot = pivot_matrix(pivot[0], pivot[1], scale_matrix(2, 2))
    R_pivot = pivot_matrix(pivot[0], pivot[1], rot_matrix(30))
    T = trans_matrix(1, -1)

    # 1) Масштабування -> Обертання -> Зсув
    M1 = T @ R_pivot @ S_pivot
    pts1 = apply_matrix(pts0, M1)

    # 2) Зсув -> Масштабування -> Обертання
    M2 = R_pivot @ S_pivot @ T
    pts2 = apply_matrix(pts0, M2)

    # 3) Масштабування -> Зсув -> Обертання
    M3 = R_pivot @ T @ S_pivot
    pts3 = apply_matrix(pts0, M3)

    print_matrix("S_pivot:", S_pivot)
    print_matrix("R_pivot:", R_pivot)
    print_matrix("T:", T)

    print_matrix("M1 = T @ R_pivot @ S_pivot:", M1)
    print_points("Координати для S -> R -> T:", pts1)

    print_matrix("M2 = R_pivot @ S_pivot @ T:", M2)
    print_points("Координати для T -> S -> R:", pts2)

    print_matrix("M3 = R_pivot @ T @ S_pivot:", M3)
    print_points("Координати для S -> T -> R:", pts3)


    show_result(pts0, pts2, title="Task 10 - order 2", pivot=pivot)
    show_result(pts0, pts3, title="Task 10 - order 3", pivot=pivot)
    show_result(pts0, pts1, title="Task 10 - order 1", pivot=pivot)


def task_11():
    print("11")

    T = np.array([
        [2.934, -0.416, 2.000],
        [0.624,  1.956, 3.400],
        [0.000,  0.000, 1.000]
    ], dtype=float)

    # вершини прямокутника після трансформації
    global_pts = np.array([
        [2.0, 3.4, 1],
        [4.9, 4.0, 1],
        [4.5, 6.0, 1],
        [1.6, 5.4, 1]
    ], dtype=float)

    T_inv = np.linalg.inv(T)
    local_pts = apply_matrix(global_pts, T_inv)

    print_matrix("Матриця T:", T)
    print_matrix("Обернена матриця T^-1:", T_inv)
    print_points("Глобальні координати:", global_pts)
    print_points("Відновлені локальні координати:", local_pts)

    show_result(local_pts, global_pts, title="Task 11: local vs global")


def task_12():
    print("12")

    T = np.array([
        [0.866, 0.5,   4.0],
        [0.5,   0.866, 3.0],
        [0.0,   0.0,   1.0]
    ], dtype=float)

    pts0 = SQUARE_POINTS.copy()
    pts1 = apply_matrix(pts0, T)

    A = T[:2, :2]
    c1 = A[:, 0]
    c2 = A[:, 1]
    dot = np.dot(c1, c2)

    print_matrix("Матриця T:", T)
    print("\nСпроба розкладу на TRS:")
    print(f"translation = ({T[0,2]}, {T[1,2]})")
    print(f"dot(column1, column2) = {dot:.6f}")

    if abs(dot) > 1e-6:
        print("\nВисновок:")
        print("Чистий розклад на scale + rotation + translation неможливий.")
        print("Причина: стовпці лінійної частини не ортогональні, отже матриця містить shear")
        print("або не є чистою TRS-матрицею.")
    else:
        print("\nСтовпці ортогональні, розклад можливий.")

    print_points("Початковий квадрат:", pts0)
    print_points("Трансформований квадрат:", pts1)

    show_result(pts0, pts1, title="Task 12")


def task_13():
    print("13")

    T = np.array([
        [1.414, -2.121, 1.0],
        [1.414,  2.121, 1.0],
        [0.0,    0.0,   1.0]
    ], dtype=float)

    pts0 = SQUARE_POINTS.copy()
    pts1 = apply_matrix(pts0, T)

    A = T[:2, :2]

    # масштаби як довжини стовпців
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])

    # кут з першого стовпця
    theta = np.degrees(np.arctan2(A[1, 0], A[0, 0]))

    tx = T[0, 2]
    ty = T[1, 2]

    R = rot_matrix(theta)
    S = scale_matrix(sx, sy)
    Ttrans = trans_matrix(tx, ty)

    T_rebuilt = Ttrans @ R @ S

    print_matrix("Матриця T:", T)
    print(f"\nsx = {sx:.6f}")
    print(f"sy = {sy:.6f}")
    print(f"theta = {theta:.6f} градусів")
    print(f"translation = ({tx:.6f}, {ty:.6f})")

    print_matrix("R:", R)
    print_matrix("S:", S)
    print_matrix("T_translation:", Ttrans)
    print_matrix("Відновлена матриця T_rebuilt = T_translation @ R @ S:", T_rebuilt)

    print_points("Початковий квадрат:", pts0)
    print_points("Фінальний квадрат:", pts1)

    show_result(pts0, pts1, title="Task 13")


def task_14():
    print("14")

    T = np.array([
        [1.732, -1.000,  5.0],
        [1.000,  1.732, -3.0],
        [0.000,  0.000,  1.0]
    ], dtype=float)

    pivot = (1.0, 1.0)
    pts0 = SQUARE_POINTS.copy()
    pts1 = apply_matrix(pts0, T)

    A = T[:2, :2]

    # лінійна частина
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    theta = np.degrees(np.arctan2(A[1, 0], A[0, 0]))

    # матриця scale+rotation
    RS = rot_matrix(theta) @ scale_matrix(sx, sy)

    # перенос
    px, py = pivot
    pivot_shift = np.array([
        [1, 0, px],
        [0, 1, py],
        [0, 0, 1]
    ]) @ RS @ np.array([
        [1, 0, -px],
        [0, 1, -py],
        [0, 0, 1]
    ])

    # окремий додатковий перенос
    extra_tx = T[0, 2] - pivot_shift[0, 2]
    extra_ty = T[1, 2] - pivot_shift[1, 2]

    T_extra = trans_matrix(extra_tx, extra_ty)
    T_rebuilt = T_extra @ pivot_shift

    print_matrix("Матриця T:", T)
    print(f"\npivot = {pivot}")
    print(f"sx = {sx:.6f}")
    print(f"sy = {sy:.6f}")
    print(f"theta = {theta:.6f} градусів")

    print_matrix("RS = R @ S:", RS)
    print_matrix("Матриця трансформації навколо pivot:", pivot_shift)

    print(f"\nДодатковий перенос: ({extra_tx:.6f}, {extra_ty:.6f})")
    print_matrix("T_extra:", T_extra)
    print_matrix("Відновлена матриця T_rebuilt = T_extra @ pivot_shift:", T_rebuilt)

    print_points("Початковий квадрат:", pts0)
    print_points("Фінальний квадрат:", pts1)

    show_result(pts0, pts1, title="Task 14", pivot=pivot)




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
    "12": task_12,
    "13": task_13,
    "14": task_14,
}

def main():
    print("\nОберіть номер задачі:")
    for i in range(1, 15):
        print(i)

    number = input("\nВведіть номер задачі: ").strip()

    if number in TASKS:
        TASKS[number]()
    else:
        print("Невірний номер задачі.")

if __name__ == "__main__":
    main()