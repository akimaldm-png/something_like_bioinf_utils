import os
from typing import TextIO


def make_oneline_output_path(input_fasta: str) -> str:
    """
    Составляет имя выходного файла по имени входного, добавляя к имени _oneline.

    Аргументы:
    input_fasta: str (путь до входного FASTA-файла)

    Возвращает str (путь к выходному файлу)
    """
    base, extension = os.path.splitext(input_fasta)
    return base + "_oneline" + extension


def write_fasta_record(output_file: TextIO, header: str, sequence: str) -> None:
    """
    Записывает одну FASTA-запись (заголовок и последовательность в одну строку).

    Аргументы:
    output_file: TextIO (файл, открытый на запись)
    header: str (заголовок записи (строка, начинающаяся с >))
    sequence: str (последовательность целиком)

    Ничего не возвращает.
    """
    output_file.write(header + "\n")
    output_file.write(sequence + "\n")