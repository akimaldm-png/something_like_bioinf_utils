import os
from typing import TextIO


def make_bounds(bounds: int | float | tuple) -> tuple:
    """
    Приводит границы фильтра к виду (нижняя, верхняя).

    Аргументы:
    bounds: int/float (верхняя граница (нижняя считается равной 0))
            tuple (нижняя, верхняя)

    Возвращает кортеж (нижняя, верхняя).
    """
    if isinstance(bounds, (int, float)): # проверяем тип введенного значения
        return (0, bounds)
    return bounds


def is_length_ok(sequence: str, length_bounds: int | float | tuple) -> bool:
    """
    Проверяет, попадает ли длина последовательности в заданные границы
    (границы включаются).

    Аргументы:
    sequence: str (нуклеотидная последовательность)
    length_bounds: int/float/tuple (верхняя граница или (нижняя, верхняя))

    Возвращает True, если длина в границах, иначе False.
    """
    lower, upper = make_bounds(length_bounds)
    return lower <= len(sequence) <= upper


def calculate_gc_content(sequence: str) -> float:
    """
    Считает GC-состав последовательности в процентах.

    Аргументы:
    sequence: str (нуклеотидная последовательность)

    Возвращает float - процент G и C (от 0 до 100).
    Для пустой последовательности возвращает 0.
    """
    if len(sequence) == 0:
        return 0.0
    sequence_upper = sequence.upper()
    gc_count = sequence_upper.count("G") + sequence_upper.count("C")
    return gc_count / len(sequence) * 100


def is_gc_ok(sequence: str, gc_bounds: int | float | tuple) -> bool:
    """
    Проверяет, попадает ли GC-состав последовательности в заданные границы
    (границы включаются).

    Аргументы:
    sequence: str (нуклеотидная последовательность)
    gc_bounds: int/float/tuple (верхняя граница или (нижняя, верхняя), в процентах)

    Возвращает True, если GC-состав в границах, иначе False.
    """
    lower, upper = make_bounds(gc_bounds)
    return lower <= calculate_gc_content(sequence) <= upper


def calculate_mean_quality(quality: str) -> float:
    """
    Считает среднее качество рида по строке качества (шкала phred33).

    Аргументы:
    quality: str (строка качества из FASTQ)

    Возвращает float среднее качество по всем нуклеотидам.
    Для пустой строки возвращает 0.
    """
    if len(quality) == 0:
        return 0.0
    total = 0
    for symbol in quality:
        total = total + ord(symbol) - 33
    return total / len(quality)


def is_quality_ok(quality: str, quality_threshold: int | float) -> bool:
    """
    Проверяет, что среднее качество рида не ниже порога.

    Аргументы:
    quality: str (строка качества из FASTQ (phred33))
    quality_threshold: int/float (пороговое значение среднего качества)

    Возвращает True, если среднее качество >= порога, иначе False.
    """
    return calculate_mean_quality(quality) >= quality_threshold


def read_one_read(fastq_file: TextIO) -> tuple | None:
    """
    Читает один рид (4 строки) из открытого FASTQ-файла.

    Аргументы:
    fastq_file: TextIO (FASTQ-файл, открытый на чтение)

    Возвращает кортеж (заголовок, последовательность, разделитель, качество)
    или None, если файл закончился.
    """
    header = fastq_file.readline().strip()
    if header == "":
        return None
    sequence = fastq_file.readline().strip()
    separator = fastq_file.readline().strip()
    quality = fastq_file.readline().strip()
    return header, sequence, separator, quality