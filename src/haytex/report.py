import re
import shutil
from typing import Match, Optional, Union

import numpy as np
import pandas as pd


class Report:
    def __init__(self, title="", subtitle="", author=""):
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
        self.report_text.append(f"\\part{{{title}}}")

    def add_chapter(self, title=""):
        self.report_text.append(f"\\chapter{{{title}}}")

    def add_section(self, title=""):
        self.report_text.append(f"\\section{{{title}}}")

    def add_subsection(self, title=""):
        self.report_text.append(f"\\subsection{{{title}}}")

    def add_subsubsection(self, title=""):
        self.report_text.append(f"\\subsubsection{{{title}}}")

    def clear_page(self):
        self.report_text.append(r"\clearpage")

    def add_figure(
            self,
            figs: Union[str, list[str]],
            cols: Optional[int] = None,
            rows: Optional[int] = None,
            caption: Optional[str] = None
            ):
        """
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
        print(fig_list)
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
                self.report_text.append(f"\\caption{{{caption} [{fig_index}]}}")
            self.report_text.append(r"\end{figure}")
            if len(fig_list) != fig_index:
                self.report_text.append(r"\clearpage")
        print(self.report_text)

    def save_tex(self, path):
        self.report_text.append(r"\end{document}")
        with open(f"{path}/Report.tex", "w+") as tex_file:
            tex_file.write("\n".join(self.report_text))
        shutil.copy("Settings/Style.sty", f"{path}/Style.sty")
