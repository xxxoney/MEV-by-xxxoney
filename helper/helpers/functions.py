from typing import List, Any, Tuple

from helper.helpers.dataclasses import Data


def create_table(header: List[Any], rows: List[Any]) -> str:
    """
    Generates a table from the data.

    Parameters:
    - header [list]: List of header columns.
    - rows [list]: List of rows.

    Returns:
    - str: A rendered table with data.
    """
    num_columns = len(rows[0])
    col_widths = [max(len(str(header[i])), *(len(str(row[i])) for row in rows)) for i in range(num_columns)]

    horizontal_border = '+' + '+'.join(['-' * (width + 2) for width in col_widths]) + '+'
    header_row = '|' + '|'.join([' ' + str(header[i]).ljust(col_widths[i]) + ' ' for i in range(num_columns)]) + '|'

    yield horizontal_border
    yield header_row
    yield horizontal_border

    for row in rows:
        yield '|' + '|'.join([' ' + str(row[i]).ljust(col_widths[i]) + ' ' for i in range(num_columns)]) + '|'
        yield horizontal_border


def run_process(process: Any, arguments: Tuple = None) -> Data:
    """
    Starts the process.

    Parameters:
    - process [any]: Class object.
    - arguments [tuple]: Tuple of arguments for process.

    Returns:
    - List: List of collected files.
    """
    if not arguments:
        return process.run()

    return process(*arguments).run()
