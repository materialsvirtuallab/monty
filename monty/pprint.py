"""
Pretty printing functions.
"""

import sys
from io import StringIO
from json import JSONEncoder, loads


def pprint_table(table, out=sys.stdout, rstrip=False):
    """
    Prints out a table of data, padded for alignment
    Each row must have the same number of columns.

    Args:
        table: The table to print. A list of lists.
        out: Output stream (file-like object)
        rstrip: if True, trailing withespaces are removed from the entries.
    """

    def max_width_col(table, col_idx):
        """
        Get the maximum width of the given column index
        """
        return max(len(row[col_idx]) for row in table)

    if rstrip:
        for row_idx, row in enumerate(table):
            table[row_idx] = [c.rstrip() for c in row]

    col_paddings = []
    ncols = len(table[0])
    for i in range(ncols):
        col_paddings.append(max_width_col(table, i))

    for row in table:
        # left col
        out.write(row[0].ljust(col_paddings[0] + 1))
        # rest of the cols
        for i in range(1, len(row)):
            col = row[i].rjust(col_paddings[i] + 2)
            out.write(col)
        out.write("\n")


def draw_tree(node, child_iter=lambda n: n.children, text_str=lambda n: str(n)):
    """
    Args:
        node: the root of the tree to be drawn,
        child_iter: function that when called with a node, returns an iterable
            over all its children
        text_str: turns a node into the text to be displayed in the tree.

    The default implementations of these two arguments retrieve the children
    by accessing node.children and simply use str(node) to convert a node to a
    string. The resulting tree is drawn into a buffer and returned as a string.

    Based on https://pypi.python.org/pypi/asciitree/
    """
    return _draw_tree(node, "", child_iter, text_str)


def _draw_tree(node, prefix, child_iter, text_str):
    buf = StringIO()

    children = list(child_iter(node))

    # check if root node
    if prefix:
        buf.write(prefix[:-3])
        buf.write("  +--")
    buf.write(text_str(node))
    buf.write("\n")

    for index, child in enumerate(children):
        if index + 1 == len(children):
            sub_prefix = prefix + "   "
        else:
            sub_prefix = prefix + "  |"

        buf.write(_draw_tree(child, sub_prefix, child_iter, text_str))

    return buf.getvalue()


class DisplayEcoder(JSONEncoder):
    """
    Help convert dicts and objects to a format that can be displayed in notebooks
    """

    def default(self, o):
        """
        Try diffent ways of converting the present object for displaying
        """
        try:
            return o.as_dict()
        except Exception:
            pass

        try:
            return o.__dict__
        except Exception:
            pass

        try:
            return str(o)
        except Exception:
            pass

        return None


def pprint_json(data):
    """
    Display a tree-like object in a jupyter notebook.
    Allows for collapsable interactive interaction with data.

    Args:
        data: a dictionary or object

    Based on:
    https://gist.github.com/jmmshn/d37d5a1be80a6da11f901675f195ca22

    """
    from IPython.display import JSON, display  # pylint: disable=C0415

    display(JSON(loads(DisplayEcoder().encode(data))))
