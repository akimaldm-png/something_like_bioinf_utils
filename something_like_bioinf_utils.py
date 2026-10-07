from helpers.fastq import (
    is_read_ok,
    prepare_output_path,
    read_one_read,
    write_read,
)


def filter_fastq(
    input_fastq: str,
    output_fastq: str,
    gc_bounds: int | float | tuple = (0, 100),
    length_bounds: int | float | tuple = (0, 2**32),
    quality_threshold: int | float = 0,
) -> None:
    """
    Фильтрует риды FASTQ-файла по GC-составу, длине и среднему качеству.
    Подходящие риды сохраняются в папку filtered.
    Файл обрабатывается по одному риду.

    Аргументы:
    input_fastq: str (путь до входного FASTQ-файла)
    output_fastq: str (имя выходного файла (сохраняется в папку filtered))
    gc_bounds: int/float/tuple (границы GC-состава в процентах,
        по умолчанию (0, 100). Одно число - верхняя граница)
    length_bounds: int/float/tuple (границы длины,
        по умолчанию (0, 2**32). Одно число - верхняя граница)
    quality_threshold: int/float (порог среднего качества (phred33),
        по умолчанию 0. Риды с качеством ниже порога отбрасываются)

    Ничего не возвращает.
    """
    output_path = prepare_output_path(output_fastq)
    with open(input_fastq, "r") as input_file, open(output_path, "w") as output_file:
        while True:
            read = read_one_read(input_file)
            if read is None:
                break
            if is_read_ok(read, gc_bounds, length_bounds, quality_threshold):
                write_read(output_file, read)