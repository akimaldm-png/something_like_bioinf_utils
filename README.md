# something_like_bioinf_utils

Небольшой пакет утилит для работы с биоинформатическими файлами: FASTQ, FASTA и текстовыми отчётами BLAST. Написан на Python, без сторонних библиотек.

## Возможности

- `filter_fastq` — фильтрация ридов FASTQ по GC-составу, длине и среднему качеству (phred33). Файл обрабатывается построчно, без загрузки в память целиком.
- `convert_multiline_fasta_to_oneline` — перевод FASTA, где последовательности разбиты на несколько строк, в формат «одна последовательность — одна строка».
- `parse_blast_output` — извлечение описания лучшего совпадения для каждого запроса из txt-отчёта BLAST.

## Установка

Необходим Python 3.10 или новее. Сторонние библиотеки не требуются.

```bash
git clone https://github.com/akimaldm-png/something_like_bioinf_utils.git
cd something_like_bioinf_utils
```

## Использование

Функции импортируются из главного скрипта:

```python
from something_like_bioinf_utils import (
    filter_fastq,
    convert_multiline_fasta_to_oneline,
    parse_blast_output,
)
```

### filter_fastq

```python
filter_fastq(
    input_fastq="reads.fastq",
    output_fastq="good_reads.fastq",
    gc_bounds=(20, 80),
    length_bounds=(50, 300),
    quality_threshold=30,
)
```

Отфильтрованные риды сохраняются в папку `filtered/` (если папки нет, она создаётся автоматически).

| Аргумент | По умолчанию | Описание |
|---|---|---|
| `gc_bounds` | `(0, 100)` | Интервал GC-состава в процентах. Одно число — верхняя граница |
| `length_bounds` | `(0, 2**32)` | Интервал длины рида. Одно число — верхняя граница |
| `quality_threshold` | `0` | Минимальное среднее качество рида (phred33) |

Все границы включаются в интервал.

### convert_multiline_fasta_to_oneline

```python
convert_multiline_fasta_to_oneline("sequences.fasta", "sequences_oneline.fasta")
```

Аргумент `output_fasta` необязателен: если его не указать, результат сохранится рядом со входным файлом с суффиксом `_oneline`.

### parse_blast_output

```python
parse_blast_output("blast_results.txt", "best_hits.txt")
```

Для каждого запроса берётся описание первого (лучшего) совпадения. Уникальные описания сохраняются в файл по одному на строку, по алфавиту.

## Структура проекта

```
something_like_bioinf_utils/
├── something_like_bioinf_utils.py   # основные утилиты
├── helpers/
│   ├── fastq.py        # вспомогательные функции (filter_fastq)
│   └── bio_files.py    # вспомогательные функции (FASTA и BLAST)
└── README.md
```

## Автор

Александра Акименкова — [GitHub](https://github.com/akimaldm-png)