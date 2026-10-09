from helpers.bio_files import (
    extract_description,
    get_description_end,
    make_oneline_output_path, 
    write_fasta_record,
    write_lines,
)


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


def convert_multiline_fasta_to_oneline(
    input_fasta: str,
    output_fasta: str | None = None,
) -> None:
    """
    Переводит FASTA-файл, в котором последовательности разбиты на несколько строк,
    в формат, где каждая последовательность записана одной строкой.
    Файл обрабатывается построчно, в памяти хранится одна запись.

    Аргументы:
    input_fasta: str (путь до входного FASTA-файла)
    output_fasta: str | None (путь до выходного файла, если не указан,
        файл сохраняется рядом со входным с _oneline)

    Ничего не возвращает.
    """
    if output_fasta is None:
        output_fasta = make_oneline_output_path(input_fasta)

    with open(input_fasta, "r") as input_file, open(output_fasta, "w") as output_file:
        header = None
        sequence = ""
        for line in input_file:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    write_fasta_record(output_file, header, sequence)
                header = line
                sequence = ""
            else:
                sequence = sequence + line
        if header is not None:
            write_fasta_record(output_file, header, sequence)


def parse_blast_output(input_file: str, output_file: str) -> None:
    """
    Читает текстовый отчёт BLAST и для каждого запроса (Query) берёт описание
    лучшего совпадения - первую строку столбца Description.
    Уникальные описания сохраняет в файл, по одному на строку,
    отсортированными по алфавиту.

    Аргументы:
    input_file: str (путь до txt-файла с результатами BLAST)
    output_file: str (путь до выходного файла)

    Ничего не возвращает.
    """
    descriptions = set()
    with open(input_file, "r") as blast_file:
        for line in blast_file:
            if line.startswith("Sequences producing significant alignments:"):
                columns_line = blast_file.readline()
                blast_file.readline()
                first_hit_line = blast_file.readline()
                description_end = get_description_end(columns_line)
                descriptions.add(extract_description(first_hit_line, description_end))
    write_lines(output_file, sorted(descriptions, key=str.lower))