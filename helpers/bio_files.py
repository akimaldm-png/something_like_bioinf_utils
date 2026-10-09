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


def get_description_end(columns_line: str) -> int:
    """
    Находит, где заканчивается столбец Description в таблице BLAST:
    позиция, с которой начинается слово Scientific в строке шапки.

    Аргументы:
    columns_line: str - (первая строка шапки таблицы со словом Scientific)

    Возвращает int (номер позиции, где начинается столбец Scientific Name)
    """
    return columns_line.index("Scientific")


def extract_description(table_line: str, description_end: int) -> str:
    """
    Вырезает из строки таблицы BLAST значение столбца Description.

    Аргументы:
    table_line: str (строка таблицы с совпадением)
    description_end: int (позиция, где заканчивается столбец Description)

    Возвращает str - описание белка без пробелов по краям.
    """
    return table_line[:description_end].strip()


def write_lines(output_file: str, lines: list[str]) -> None:
    """
    Записывает строки в файл, каждую с новой строки.

    Аргументы:
    output_file: str (путь до выходного файла)
    lines: list[str] (строки для записи)

    Ничего не возвращает.
    """
    with open(output_file, "w") as file:
        for line in lines:
            file.write(line + "\n")