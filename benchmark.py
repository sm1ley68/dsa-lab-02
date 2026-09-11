"""
Золотой уровень. Сравнение производительности связного списка и массива.

Два эксперимента:
  1. prepend      — вставка в начало: SinglyLinkedList.prepend O(1) vs DynamicArray.insert(0) O(n);
  2. get(n // 2)  — доступ к среднему элементу: SinglyLinkedList.get O(n) vs DynamicArray.get O(1).

Запуск:
    python3 benchmark.py              # полный прогон (~30 секунд)
    python3 benchmark.py --quick      # быстрый прогон на малых размерах
    python3 benchmark.py --no-show    # только сохранить графики, не открывать окна

Графики сохраняются в каталог results/.
"""

import argparse
import math
import os
import time

import matplotlib

from dynamic_array import DynamicArray
from singly_linked_list import SinglyLinkedList

SIZES = [1000, 5000, 10000, 20000, 50000, 100000]
QUICK_SIZES = [1000, 2000, 4000, 8000, 16000]
RESULTS_DIR = "results"


def _timeit(action, min_total=0.05, max_runs=50):
    """Возвращает лучшее время одного прогона action.

    Прогоны повторяются, пока суммарно не наберётся min_total секунд (но не более
    max_runs раз). Это выравнивает условия для быстрых и медленных замеров: короткая
    операция успевает «прогреться», а длинная измеряется один раз и не тормозит скрипт.
    Берём минимум, а не среднее: помехи от планировщика ОС могут только замедлить
    прогон, поэтому самый быстрый результат ближе всего к чистому времени работы кода.
    """
    best = float("inf")
    total = 0.0
    runs = 0
    while runs < max_runs and (runs == 0 or total < min_total):
        start = time.perf_counter()
        action()
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
        total += elapsed
        runs += 1
    return best


def experiment_prepend(sizes):
    """Сравнение prepend: связный список vs массив."""
    list_times = []
    array_times = []

    print("Эксперимент 1: prepend (вставка в начало), n операций подряд")
    print("Подождите, это может занять 1–2 минуты...")
    print(f"  {'n':>7} | {'список, с':>12} | {'массив, с':>12} | {'массив медленнее в':>20}")
    print("  " + "-" * 60)

    for n in sizes:
        # Связный список: каждая вставка переставляет одну ссылку — O(1).
        def prepend_list(n=n):
            sll = SinglyLinkedList()
            for i in range(n):
                sll.prepend(i)

        # Массив: каждая вставка сдвигает весь хвост вправо — O(n).
        def prepend_array(n=n):
            arr = DynamicArray()
            for i in range(n):
                arr.insert(0, i)

        list_times.append(_timeit(prepend_list))
        array_times.append(_timeit(prepend_array))

        ratio = array_times[-1] / list_times[-1]
        print(f"  {n:>7d} | {list_times[-1]:>12.4f} | {array_times[-1]:>12.4f} | {ratio:>19.1f}x")

    _plot(
        sizes,
        [
            (list_times, "o-", "SinglyLinkedList.prepend (O(1))"),
            (array_times, "s-", "DynamicArray.insert(0) (O(n))"),
        ],
        ylabel="Время на n вставок (секунды)",
        title="Сравнение prepend: связный список vs массив",
        filename="prepend.png",
    )
    return list_times, array_times


def experiment_get_middle(sizes, repeats=2000):
    """Сравнение get(n//2): связный список vs массив."""
    list_times = []
    array_times = []

    print(f"\nЭксперимент 2: get(n//2) (доступ к среднему элементу), {repeats} обращений")
    print(f"  {'n':>7} | {'список, с':>12} | {'массив, с':>12} | {'список медленнее в':>20}")
    print("  " + "-" * 60)

    for n in sizes:
        # Подготовка данных
        sll = SinglyLinkedList()
        arr = DynamicArray()
        for i in range(n):
            sll.prepend(i)
            arr.append(i)
        mid = n // 2

        # Связный список: до середины приходится дойти по ссылкам — O(n).
        def get_list():
            for _ in range(repeats):
                sll.get(mid)

        # Массив: адрес элемента считается арифметикой по индексу — O(1).
        def get_array():
            for _ in range(repeats):
                arr.get(mid)

        list_times.append(_timeit(get_list))
        array_times.append(_timeit(get_array))

        ratio = list_times[-1] / array_times[-1]
        print(f"  {n:>7d} | {list_times[-1]:>12.6f} | {array_times[-1]:>12.6f} | {ratio:>19.1f}x")

    _plot(
        sizes,
        [
            (list_times, "o-", "SinglyLinkedList.get(n//2) (O(n))"),
            (array_times, "s-", "DynamicArray.get(n//2) (O(1))"),
        ],
        ylabel=f"Время на {repeats} обращений (секунды)",
        title="Сравнение доступа по индексу: связный список vs массив",
        filename="get_middle.png",
    )
    return list_times, array_times


def _plot(sizes, series, ylabel, title, filename):
    """Строит и сохраняет график: линейная шкала и логарифмическая рядом.

    Логарифмический масштаб нужен, чтобы быстрая кривая не сливалась с осью:
    там прямая с наклоном k означает зависимость t ~ n^k.
    """
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, log in zip(axes, (False, True)):
        for times, style, label in series:
            ax.plot(sizes, times, style, label=label, linewidth=2)
        ax.set_xlabel("Количество элементов (n)", fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.4)
        ax.legend()
        if log:
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_title("Логарифмический масштаб", fontsize=11)
        else:
            ax.set_title("Линейный масштаб", fontsize=11)
    fig.suptitle(title, fontsize=14)
    fig.tight_layout()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    fig.savefig(path, dpi=120)
    print(f"  График сохранён: {path}")


def growth_exponent(sizes, times):
    """Оценивает показатель степени k в зависимости t ~ n^k.

    Считается по соседним точкам: k = log(t2 / t1) / log(n2 / n1), затем усредняется.
    Ориентиры: k ≈ 0 — время не зависит от n (O(1)), k ≈ 1 — линейный рост,
    k ≈ 2 — квадратичный.
    """
    exponents = []
    for i in range(1, len(sizes)):
        if times[i - 1] <= 0 or times[i] <= 0:
            continue
        exponents.append(math.log(times[i] / times[i - 1]) / math.log(sizes[i] / sizes[i - 1]))
    return sum(exponents) / len(exponents) if exponents else float("nan")


def _verdict(measured, expected, tolerance=0.35):
    """Сходится ли измеренный показатель степени с теоретическим."""
    return "совпадает с теорией" if abs(measured - expected) <= tolerance else (
        "расходится с теорией — стоит перепроверить замер"
    )


def conclusions(sizes, prepend_result, get_result):
    """Печатает выводы по замерам."""
    sll_prepend, arr_prepend = prepend_result
    sll_get, arr_get = get_result
    n_max = sizes[-1]

    k_sll_prepend = growth_exponent(sizes, sll_prepend)
    k_arr_prepend = growth_exponent(sizes, arr_prepend)
    k_sll_get = growth_exponent(sizes, sll_get)
    k_arr_get = growth_exponent(sizes, arr_get)

    print("\n" + "=" * 70)
    print("ВЫВОДЫ")
    print("=" * 70)

    print("\n1. Вставка в начало (prepend)")
    print(f"   При n = {n_max} список быстрее массива в {arr_prepend[-1] / sll_prepend[-1]:.0f} раз,")
    print("   и разрыв растёт вместе с n — то есть дело не в константе, а в асимптотике.")
    print(f"   Список: суммарное время n вставок растёт как n^{k_sll_prepend:.2f}; ожидалось n^1,")
    print(f"   потому что одна вставка — O(1). {_verdict(k_sll_prepend, 1).capitalize()}.")
    print("   Механизм: создаётся узел, его next смотрит на старый head, head переставляется")
    print("   на новый узел. Остальные узлы не трогаются вообще, сколько бы их ни было.")
    print(f"   Массив: суммарное время растёт как n^{k_arr_prepend:.2f}; ожидалось n^2,")
    print(f"   потому что одна вставка — O(n). {_verdict(k_arr_prepend, 2).capitalize()}.")
    print("   Механизм: элементы лежат непрерывным блоком, поэтому перед записью в нулевую")
    print("   ячейку весь хвост сдвигается на одну позицию вправо: 1 + 2 + ... + n ≈ n²/2.")

    print("\n2. Доступ к среднему элементу get(n//2)")
    print(f"   При n = {n_max} массив быстрее списка в {sll_get[-1] / arr_get[-1]:.0f} раз.")
    print(f"   Массив: время растёт как n^{k_arr_get:.2f}; ожидалось n^0, то есть постоянное время.")
    print(f"   {_verdict(k_arr_get, 0).capitalize()}.")
    print("   Механизм: адрес элемента вычисляется арифметикой по индексу за одно действие.")
    print(f"   Список: время растёт как n^{k_sll_get:.2f}; ожидалось n^1. {_verdict(k_sll_get, 1).capitalize()}.")
    print("   Механизм: узлы разбросаны по памяти, произвольного доступа нет — до середины")
    print("   приходится честно пройти n/2 ссылок.")

    print("\n3. Общий вывод")
    print("   Ни одна структура не лучше другой «вообще» — они меняют одно на другое.")
    print("   Связный список платит доступом по индексу за дешёвые вставки и удаления;")
    print("   массив платит вставками в начало за мгновенный доступ по индексу и за")
    print("   компактность в памяти (у списка на каждый элемент есть ещё и ссылка).")
    print("   Выбор структуры определяется тем, какая операция в задаче самая частая:")
    print("   часто вставляем и удаляем в начале или по ссылке — список;")
    print("   часто читаем по индексу и обходим подряд — массив.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="быстрый прогон на малых размерах")
    parser.add_argument("--no-show", action="store_true",
                        help="не открывать окна с графиками, только сохранить PNG")
    parser.add_argument("--repeats", type=int, default=2000,
                        help="число обращений в эксперименте get(n//2)")
    args = parser.parse_args()

    # С --no-show принудительно берём файловый бэкенд: окна не открываются, графики
    # только сохраняются. Иначе бэкенд выбирает сам matplotlib — GUI, если он доступен,
    # и Agg при запуске без дисплея.
    if args.no_show:
        matplotlib.use("Agg")

    sizes = QUICK_SIZES if args.quick else SIZES

    prepend_result = experiment_prepend(sizes)
    get_result = experiment_get_middle(sizes, repeats=args.repeats)
    conclusions(sizes, prepend_result, get_result)

    if not args.no_show:
        import matplotlib.pyplot as plt

        if matplotlib.get_backend().lower() == "agg":
            print(f"\nGUI-бэкенд недоступен, графики только сохранены в {RESULTS_DIR}/.")
        else:
            plt.show()


if __name__ == "__main__":
    main()
