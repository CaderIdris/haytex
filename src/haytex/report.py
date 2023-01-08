__author__ = "Idris Hayward"
__copyright__ = "2023, Idris Hayward"
__credits__ = ["Idris Hayward"]
__license__ = "Lesser General Public License v2.1"
__version__ = "1.0.0"
__maintainer__ = "Idris Hayward"
__email__ = "CaderIdrisGH@outlook.com"
__status__ = "Stable release"

import re
import shutil
from typing import Optional, Union

import numpy as np
import pandas as pd


class Report:
    """
    Generates a LaTeX report with figures and tables and saves it to a
    specified path with an associated style file

    ```

    Attributes
    ----------
    report_text : list[str]
        List of strings. Each string represents a line of the report. These are
        then joined together, separated by a newline character (\\n) to
        generate the report

    Methods
    -------
    add_part(title="")
        Adds a part to the report

    add_chapter(title="")
        Adds a chapter to te report

    add_section(title="")
        Adds a section to the report

    add_subsection(title="")
        Adds a subsection to the report

    add_subsubsection(title="")
        Adds a subsubsection to the report

    clear_page()
        Adds a clearpage function to the report, forcing the report to
        continue on a new page. This is useful after adding in a lot of floats
        (floats include figures and tables).

    add_figure(figs, cols=None, rows=None, caption=None)
        Adds a figure, multiple subfigures or multiple figures of subfigures to
        the report. Max columns and rows can be specified. Subfigures are
        automatically scaled to equal sizes.

    add_table(table, cols=None, rows=None, caption=None)
        Adds a table or multiple tables to the report. Max columns and rows can
        be specified.

    save_tex(path, style_file=None)
        Saves the report to a LaTeX file with an associated style file. If you
        wish to use your own style file, specify a path to it with style_file.
    """
    def __init__(self, title="", subtitle="", author=""):
        """ Constructs the report object

        Parameters
        ----------
        title : str
            Title of the report
            (Default is an empty string)
        subtitle : str
            Subtitle of the report
            (Default is an empty string)
        author : str
            Author of the report
            (Default is an empty string)

        Returns
        -------
            Instance of the report class
        """
        self.report_text = [
            r"\documentclass[12pt]{book}",
            r"\usepackage{Style}",
            r"\usepackage{float}",
            r"\usepackage{graphicx}",
            r"\usepackage{pgf}",
            r"\usepackage{subcaption}",
            f"\\title{{{title}\\\\ \\large {subtitle}}}",
            f"\\author{{{author}}}",
            r"\begin{document}",
            r"\maketitle",
            r"\tableofcontents"
        ]

    def add_part(self, title=""):
        """ Adds a part to the report

        Parameters
        ----------
        title : str, optional
            Title of the part
            (Default is an empty string)

        Returns
        -------
        None
        """
        self.report_text.append(f"\\part{{{title}}}")

    def add_chapter(self, title=""):
        """ Adds a chapter to the report

        Parameters
        ----------
        title : str, optional
            Title of the chapter
            (Default is an empty string)

        Returns
        -------
        None
        """
        self.report_text.append(f"\\chapter{{{title}}}")

    def add_section(self, title=""):
        """ Adds a section to the report

        Parameters
        ----------
        title : str, optional
            Title of the section
            (Default is an empty string)

        Returns
        -------
        None
        """
        self.report_text.append(f"\\section{{{title}}}")

    def add_subsection(self, title=""):
        """ Adds a subsection to the report

        Parameters
        ----------
        title : str, optional
            Title of the subsection
            (Default is an empty string)

        Returns
        -------
        None
        """
        self.report_text.append(f"\\subsection{{{title}}}")

    def add_subsubsection(self, title=""):
        """ Adds a subsubsection to the report

        Parameters
        ----------
        title : str, optional
            Title of the subsubsection
            (Default is an empty string)

        Returns
        -------
        None
        """
        self.report_text.append(f"\\subsubsection{{{title}}}")

    def clear_page(self):
        """ Adds a clearpage call to the report

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.report_text.append(r"\clearpage")

    def add_figure(
            self,
            figs: Union[str, list[str]],
            cols: Optional[int] = None,
            rows: Optional[int] = None,
            caption: Optional[str] = None
            ):
        """ Adds a figure to the report

        Adds either a single figure, a figure of subfigures or multiple
        figures of subfigures to the report.

        Parameters
        ----------
            figs : str | list[str]
                The path to the figure to add to the report, or list of paths
                to subfigures. This path should either be absolute or relative
                to`k the report tex file.
            cols : int, optional
                The maximum number of subfigures in a row
                (default is None)
            rows : int, optional
                The maximum number of subfigure rows in a figure
                (default is None)
            caption : str, optional
                The caption to add at the bottom of the figure. No caption will
                be added if caption is None
                (default is None)

        Returns
        -------
        None
        """
        # Preparation
        if isinstance(figs, str):
            figs = [figs]
        if cols is None:
            cols = len(figs)
        if rows is None:
            rows = 1
        # Split figs into rows
        row_list: list[list[str]] = list()
        row_numbers = int(np.ceil(len(figs) / cols))
        for row in range(row_numbers):
            if ((row + 1) * cols) < len(figs):
                row_list.append(figs[(row*cols):((row+1)*cols)])
            else:
                row_list.append(figs[(row*cols):])
        # Split rows into figures
        fig_list: list[list[list[str]]] = list()
        fig_total = int(np.ceil(len(row_list) / rows))
        for fig in range(fig_total):
            if (((fig + 1) * rows)) < len(row_list):
                fig_list.append(row_list[(fig*rows):((fig+1)*rows)])
            else:
                fig_list.append(row_list[(fig*rows):])

        file_format_regex = re.compile(r".*\.([\w]*)$")
        fig_sizing = np.floor(10 / cols) / 10
        for fig_index, fig_graphs in enumerate(fig_list, start=1):
            self.report_text.extend([
                r"\begin{figure}[H]",
                r"\centering"
                ])
            for row_index, row_graphs in enumerate(fig_graphs, start=1):
                for graph in row_graphs:
                    file_format = file_format_regex.match(graph)
                    if file_format is not None:
                        self.report_text.append(
                                f"\\begin{{subfigure}}{{{fig_sizing}"
                                f"\\textwidth}}",
                                )
                        if file_format.group(1) == 'pgf':
                            self.report_text.append(
                                f"\\resizebox{{\\linewidth}}{{!}}{{\\input"
                                f"{{\"{graph}\"}}}}"
                                )
                        else:
                            self.report_text.append(
                                f"\\includegraphics[width={fig_sizing}"
                                f"\\textwidth]{{{graph}}}"
                                )
                        self.report_text.append(r"\end{subfigure}")
                if row_index != len(fig_graphs):
                    self.report_text.append("")  # Blank line for newline
            if caption is not None:
                if len(fig_list) > 1:
                    self.report_text.append(
                            f"\\caption{{{caption} [{fig_index}]}}"
                            )
                else:
                    self.report_text.append(
                            f"\\caption{{{caption}}}"
                            )
            self.report_text.append(r"\end{figure}")
            if len(fig_list) != fig_index:
                self.report_text.append(r"\clearpage")

    def add_table(self,
                  table: pd.DataFrame,
                  cols: Optional[int] = None,
                  rows: Optional[int] = None,
                  caption: Optional[str] = None
                  ):
        """ Adds a table (or a table split into sections) to the report

        Takes a pandas dataframe, splits it if it's too big and adds it to the
        report. Splits by column first, then row so column splits are grouped
        together.

        Parameters
        ----------
            table : pd.DataFrame
                Table to add to report
            cols : int, optional
                The maximum number of columns in a table before it is split
                (default is None)
            rows : int, optional
                The maximum number of rows in a table before it is split
                (default is None)
            caption : str, optional
                The caption to add at the bottom of the table. No caption will
                be added if caption is None
                (default is None)

        Returns
        -------
        None
        """
        # Preparation
        if cols is None:
            cols = int(table.shape[1])
        if rows is None:
            rows = int(table.shape[0])
        table_list = [table]
        # Split by columns
        if table.shape[1] > cols:
            col_numbers = int(np.ceil(table.shape[1] / cols))
            table_list = list()
            for col in range(col_numbers):
                if ((col + 1) * cols) < table.shape[1]:
                    table_list.append(table.iloc[:, (col*cols):((col+1)*cols)])
                else:
                    table_list.append(table.iloc[:, (col*cols):])
        # Split by rows
        if table.shape[0] > rows:
            temp_list = list()
            row_numbers = int(np.ceil(table.shape[0] / rows))
            for tab in table_list:
                for row in range(row_numbers):
                    if ((row + 1) * rows) < table.shape[0]:
                        temp_list.append(tab.iloc[(row*rows):((row+1)*rows), :])
                    else:
                        temp_list.append(tab.iloc[(row*rows):, :])
                table_list = temp_list
        for index, tabular in enumerate(table_list, start=1):
            self.report_text.extend([
                r"\begin{table}[H]",
                r"\centering",
                *tabular.style.to_latex().split("\n")[:-1]
                ])
            if caption is not None:
                if len(table_list) > 1:
                    self.report_text.append(
                            f"\\caption{{{caption} [{index}]}}"
                            )
                else:
                    self.report_text.append(
                            f"\\caption{{{caption}}}"
                            )
            self.report_text.append(r"\end{table}")
            if index != len(table_list):
                self.report_text.append("")

    def save_tex(self, path: str, style_file: Optional[str] = None):
        """ Saves the tex file and an associated style file

        A report is generated and saves to Report.tex at the specified path.
        A style file is then either generated and saved to the specified path
        or copied from a file specified by the style_file variable.

        Parameters
        ----------
        path : str
            Path to save the report and style file
        style_file : str, optional
            Path to the style file to be saved alongside Report.tex, a new
            style file will be generated if style_file is None.
            (default is None)

        Returns
        -------
        None
        """
        self.report_text.append(r"\end{document}")
        with open(f"{path}/Report.tex", "w+") as tex_file:
            tex_file.write("\n".join(self.report_text))
        if style_file is not None:
            shutil.copy(style_file, f"{path}/Style.sty")
        else:
            style_text = [
                    r"\usepackage{microtype, color}",
                    r"\usepackage{textcomp}",
                    r"\usepackage{fontspec}",
                    r"\usepackage[margin=0.5in]{geometry}"
                    ]
            with open(f"{path}/Style.sty", "w+") as sty_file:
                sty_file.write("\n".join(style_text))
