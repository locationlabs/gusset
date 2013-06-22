"""
Pretty table generation.
"""
from itertools import cycle
from string import capwords
from fabric.colors import red, green, blue, magenta, white, yellow


class ColorRow(dict):
    """
    Ordered collection of column values.
    """
    def __init__(self, table, **kwargs):
        super(ColorRow, self).__init__(self)
        self.table = table
        for column in self.table.columns:
            self[column] = kwargs.get(column)

    def __str__(self):
        """
        Generate a formatted and colored string for this row.
        """
        def format_cell(color, item):
            column, value = item
            width = self.table.column_widths[column]
            return color(" {0}".format(value).ljust(1 + width))

        # get items in column order
        items = [(column, self[column]) for column in self.table.columns]
        # format cells with color and length
        colors_and_items = zip(cycle(self.table.colors), items)
        cells = [format_cell(color, item) for color, item in colors_and_items]
        return " ".join(cells)


class ColorTable(object):
    """
    Simple row/column table.
    """
    DEFAULT_COLORS = [red, green, blue, magenta, white, yellow]

    def __init__(self, *columns, **kwargs):
        """
        Create a table with fixed columns.

        :param columns: *args style list of column names
        :param kwargs: additional options, including `sort_key` and `colors`
        """
        self.columns = columns
        self.sort_key = kwargs.get("sort_key")
        self.colors = kwargs.get("colors", ColorTable.DEFAULT_COLORS)
        header_cells = dict([(column, capwords(column)) for column in self.columns])
        self.header = ColorRow(self, **header_cells)
        # initialize column widths based on header
        self.column_widths = dict([(column, len(self.header[column])) for column in self.columns])
        self.rows = []

    @property
    def separator(self):
        """
        Generate a separator row using current column widths.
        """
        cells = dict([(column, "-" * self.column_widths[column]) for column in self.columns])
        return ColorRow(self, **cells)

    def add(self, **kwargs):
        row = ColorRow(self, **kwargs)

        # update column widths
        for column in self.columns:
            self.column_widths[column] = max(self.column_widths[column], len(row[column]))

        self.rows.append(row)

    def __str__(self):
        """
        Generate a colored table.
        """
        rows = sorted(self.rows, key=self.sort_key) if self.sort_key else self.rows
        return "\n".join(map(str, [self.header, self.separator] + rows))


if __name__ == '__main__':
    table = ColorTable("first", "last", sort_key=lambda row: (row["last"], row["first"]))
    table.add(first="George", last="Washington")
    table.add(first="John", last="Adams")
    table.add(first="Thomas", last="Jefferson")
    print table
