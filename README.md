<h1 align="center">
	haytex
</h1>

**Contact**: [CaderIdrisGH@outlook.com](mailto:CaderIdrisGH@outlook.com)

![Tests](https://github.com/CaderIdris/haytex/actions/workflows/tests.yml/badge.svg)
 
---

## Table of Contents

1. [Summary](##summary)
1. [Main Features](##main-features)
1. [How to Install](##how-to-install)
1. [Dependencies](##dependencies)
1. [Example Usage](##example-usage)
1. [Acknowledgements](##acknowledgements)

---

## Summary

haytex is a module used to generate simple LaTeX reports using Python.
This can be useful when you need to generate a pdf report after performing data analyses.

---

## Main Features

- Split the report up using all logical structure divisions from parts to subsubsections
- Add a figure, containing one or multiple subfigures. The number of rows and columns of subfigures in a figure can be specified
- Add a pandas dataframe as a table. The table can be split into chunks of a specified number of rows and columns
- Use the provided very basic style file or specify your own to use

---

## How to install

**pip**

```bash
pip install git+https://github.com/CaderIdris/haytex@{release_tag}
```

**conda**
```bash
conda install git pip
pip install git+https://github.com/CaderIdris/haytex@{release_tag} 
```

The release tags can be found in the sidebar

---

## Dependencies

Please see [requirements.txt](./requirements.txt) and [requirements_dev.txt](./requirements_dev.txt) for the standard and development dependencies respectively.

---

## Example Usage

```python3
from haytex import Report
import pandas as pd

report = Report(title="Example Report", subtitle="This is an example report", author="You")

report.add_chapter("You can add figures to these?")
report.add_section("Heres a single figure")
report.add_figure("figures/a.png", caption="A single figure")
report.add_subsection("Wait, pgf figures too?")
report.add_figure("figures/a.pgf", caption="A single figure, in pgf format")
report.add_section("Here's multiple figures")
list_of_figs = [
	"figures/b.png",
	"figures/c.png",
	"figures/d.png",
	"figures/e.png"
]
report.add_figure(list_of_figs, caption="A 2x2 grid of subfigures")
report.clear_page()  # Starts a new page while flushing all pending floats
report.add_section("Wow, tables too?")
table = pd.read_csv("example.csv")
report.add_table(table, caption="A latex table created from a dataframe")
report.save_tex(path="report/", style_file="settings/Style.sty")
```

---

## Acknowledgements

Many thanks to James Murphy at [Mcoding](https://mcoding.io) who's excellent tutorial [Automated Testing in Python](https://www.youtube.com/watch?v=DhUpxWjOhME) and [associated repository](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject) helped a lot when structuring this package
