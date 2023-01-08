from io import StringIO
import re

import pandas as pd
import pytest

from haytex import Report as Report


@pytest.fixture
def list_of_ten_figs():
    """
    List of fake paths to figures
    """
    figs = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j"
            ]
    return figs


@pytest.fixture
def table_to_test():
    """
    Pandas dataframe used to test report add_table function
    """
    table_text = """A,B,C,D,E,F,G,H,I,J
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,
    ,,,,,,,,,"""
    return pd.read_csv(StringIO(table_text))


def test_init():
    """
    Tests whether the report class initialises properly

    """
    tests = list()

    report = Report(
        title="Test Report",
        subtitle="This is a test report",
        author="Test"
            )
    # Are there 11 lines when initialising the class?
    t_eleven_lines = len(report.report_text) == 11
    tests.append(t_eleven_lines)
    print(f"Right number of lines: {t_eleven_lines}")
    # Is the title right?
    t_right_title = r"\title{Test Report\\ \large This is a test report}" \
        in report.report_text
    tests.append(t_right_title)
    print(f"Right title: {t_right_title}")
    # Is the author right?
    t_right_author = r"\author{Test}" in report.report_text
    tests.append(t_right_author)
    print(f"Right author: {t_right_author}")

    assert all(tests)


def test_add_all_section_types():
    """
    Tests whether sections are added properly

    """
    tests = list()

    report = Report()
    report.add_part("P1")
    report.add_chapter("C1")
    report.add_section("S1")
    report.add_subsection("sS1")
    report.add_subsubsection("ssS1")
    report.add_subsubsection("ssS2")
    report.add_subsubsection("ssS3")
    report.add_chapter("C2")
    report.add_section("S2")
    report.add_section("S3")
    report.add_subsection("sS2")
    report.add_subsection("sS3")
    report.add_part("P2")
    report.add_chapter("C3")
    report.add_chapter("C4")
    report.add_section("S4")
    report.add_subsection("sS4")
    report.add_subsubsection("ssS4")

    # Are there 29 lines?
    t_lines = len(report.report_text) == 29
    tests.append(t_lines)
    print(f"Right number of lines: {t_lines}")
    # Are the right number of different sections in there?
    t_parts = all([f"\\part{{P{i}}}" in report.report_text
                   for i in range(1, 3)])
    tests.append(t_parts)
    print(f"Right number of parts: {t_parts}")
    t_chaps = all([f"\\chapter{{C{i}}}" in report.report_text
                   for i in range(1, 5)])
    tests.append(t_chaps)
    print(f"Right number of chapters: {t_chaps}")
    t_secs = all([f"\\section{{S{i}}}" in report.report_text
                  for i in range(1, 5)])
    tests.append(t_secs)
    print(f"Right number of sections: {t_secs}")
    t_subsecs = all([f"\\subsection{{sS{i}}}" in report.report_text
                     for i in range(1, 5)])
    tests.append(t_subsecs)
    print(f"Right number of subsections: {t_subsecs}")
    t_subsubsecs = all([f"\\subsubsection{{ssS{i}}}" in report.report_text
                        for i in range(1, 5)])
    tests.append(t_subsubsecs)
    print(f"Right number of subsections: {t_subsubsecs}")

    assert all(tests)


def test_singlefig():
    """Tests what happens when a single figure is added in string format

    Asserts the following:
        Expected number of blank lines present. Blank lines indicate a new row
        in the figure (0)

        Expected number of figures present. If more figures are present than
        rowsplit, the figure is split in to 2 (1)

        Expected number of subfigures present. Should always be 10. (1)

        Expected number of images imported (1)

        Expected number of captions present. Should equal number of figures
        or 0 if no caption given. Captions should be unique (e.q Fig A, Fig B)
        (1)

        Expected number of clearpages. Clearpage should separate two figures.
        (0)

        Expected number of centering calls. Every figure should begin with a
        centering call.
        (1)
    """

    tests = list()

    report = Report()
    report.add_figure("a.pgf", caption="Test")
    report_text = report.report_text
    # Check that there are no blank lines
    blank_lines = sum([len(i) == 0 for i in report_text])
    t_blank_lines = blank_lines == 0
    tests.append(t_blank_lines)
    print(f"Right number of blank lines: {t_blank_lines}")
    # Check number of figs present
    begin_end_fig_regex = re.compile(r"\\begin\{figure\}|\\end\{figure\}")
    figs_present = sum([bool(re.match(begin_end_fig_regex, i))
                        for i in report_text])
    t_figs_present = figs_present == 2
    tests.append(t_figs_present)
    print(f"Right number of figs: {t_figs_present}")
    # Check number of subfigs present
    begin_end_subfig_regex = re.compile(
            r"\\begin\{subfigure\}|\\end\{subfigure\}"
            )
    subfigs_present = sum([bool(re.match(begin_end_subfig_regex, i))
                           for i in report_text])
    t_subfigs_present = subfigs_present == 2
    tests.append(t_subfigs_present)
    print(f"Right number of subfigs: {t_subfigs_present}")
    # Check number of pictures imported
    import_regex = re.compile(r"\\input\{.*\}")
    import_present = sum([bool(re.search(import_regex, i))
                          for i in report_text])
    t_import_present = import_present == 1
    tests.append(t_import_present)
    print(f"Right number of imports: {t_import_present}")
    # Expected number of captions
    cap_regex = re.compile(r"\\caption\{Test\}")
    captions_present = [i for i in report_text if re.match(cap_regex, i)]
    u_caps_present = len(set(captions_present))  # Cast to set to remove dupes
    t_caps_present = u_caps_present == 1
    tests.append(t_caps_present)
    print(f"Right number of captions: {t_caps_present}")
    # Check for clearpages
    clear_pages = sum([i == r"\clearpage" for i in report_text])
    t_clear_pages = clear_pages == 0
    tests.append(t_clear_pages)
    print(f"Right number of clear pages: {t_clear_pages}")
    # Check for centering calls
    centering_calls = sum([i == r"\centering" for i in report_text])
    t_centering_calls = centering_calls == 1
    tests.append(t_centering_calls)
    print(f"Right number of clear pages: {t_centering_calls}")
    assert all(tests)


@pytest.mark.parametrize(
        "cols,rows,caption,fileformat,"
        "ex_blanklines,ex_figs,ex_sfigs,ex_captions,ex_clearpages",
        [
            (None, None, None, ".png", 0, 1, 10, 0, 0),
            (None, None, "Test", ".png", 0, 1, 10, 1, 0),
            (2, 5, "Test", ".png", 4, 1, 10, 1, 0),
            (2, 3, "Test", ".png", 3, 2, 10, 2, 1),
            (1, 1, "Test", ".png", 0, 10, 10, 10, 9),
            (None, None, None, ".pgf", 0, 1, 10, 0, 0),
            (None, None, "Test", ".pgf", 0, 1, 10, 1, 0),
            (2, 5, "Test", ".pgf", 4, 1, 10, 1, 0),
            (2, 3, "Test", ".pgf", 3, 2, 10, 2, 1),
            (1, 1, "Test", ".pgf", 0, 10, 10, 10, 9),
            ]
        )
def test_multifig(
        list_of_ten_figs,
        cols,
        rows,
        caption,
        fileformat,
        ex_blanklines,
        ex_figs,
        ex_sfigs,
        ex_captions,
        ex_clearpages,
        ):
    """ Tests adding multiple figures to a plot

    Asserts the following:
        Expected number of blank lines present. Blank lines indicate a new row
        in the figure

        Expected number of figures present. If more figures are present than
        rowsplit, the figure is split in to 2

        Expected number of subfigures present. Should always be 10.

        Expected number of images imported

        Expected number of captions present. Should equal number of figures
        or 0 if no caption given. Captions should be unique (e.q Fig A, Fig B)

        Expected number of clearpages. Clearpage should separate two figures.

        Expected number of centering calls. Every figure should begin with a
        centering call.
    """

    figs = [f"{name}{fileformat}" for name in list_of_ten_figs]

    tests = list()

    report = Report()
    report.add_figure(figs, cols=cols, rows=rows, caption=caption)
    report_text = report.report_text
    # Check for blank lines
    blank_lines = sum([len(i) == 0 for i in report_text])
    t_blank_lines = blank_lines == ex_blanklines
    tests.append(t_blank_lines)
    print(f"Right number of blank lines: {t_blank_lines}")
    # Check number of figs present
    begin_end_fig_regex = re.compile(r"\\begin\{figure\}|\\end\{figure\}")
    figs_present = sum([bool(re.match(begin_end_fig_regex, i))
                        for i in report_text])
    t_figs_present = figs_present == 2 * ex_figs
    tests.append(t_figs_present)
    print(f"Right number of figs: {t_figs_present}")
    # Check number of subfigs present
    begin_end_subfig_regex = re.compile(
            r"\\begin\{subfigure\}|\\end\{subfigure\}"
            )
    subfigs_present = sum([bool(re.match(begin_end_subfig_regex, i))
                           for i in report_text])
    t_subfigs_present = subfigs_present == 2 * ex_sfigs
    tests.append(t_subfigs_present)
    print(f"Right number of subfigs: {t_subfigs_present}")
    # Check number of pictures imported
    if fileformat == ".pgf":
        import_regex = re.compile(r"\\input\{.*\}")
    else:
        import_regex = re.compile(r"\\includegraphics\[.*\]\{.*\}")
    import_present = sum([bool(re.search(import_regex, i))
                          for i in report_text])
    t_import_present = import_present == ex_sfigs
    tests.append(t_import_present)
    print(f"Right number of imports: {t_import_present}")
    # Expected number of captions
    cap_regex = re.compile(r"\\caption\{.*\}")
    captions_present = [i for i in report_text if re.match(cap_regex, i)]
    u_caps_present = len(set(captions_present))  # Cast to set to remove dupes
    t_caps_present = u_caps_present == ex_captions
    tests.append(t_caps_present)
    print(f"Right number of captions: {t_caps_present}")
    # Check for clearpages
    clear_pages = sum([i == r"\clearpage" for i in report_text])
    t_clear_pages = clear_pages == ex_clearpages
    tests.append(t_clear_pages)
    print(f"Right number of clear pages: {t_clear_pages}")
    # Check for centering calls
    centering_calls = sum([i == r"\centering" for i in report_text])
    t_centering_calls = centering_calls == ex_figs
    tests.append(t_centering_calls)
    print(f"Right number of clear pages: {t_centering_calls}")
    assert all(tests)


@pytest.mark.parametrize(
        "cols,rows,caption,"
        "ex_blanklines,ex_tables,ex_tabulars,ex_captions",
        [
            (None, None, None, 0, 1, 1, 0),
            (None, None, "Test", 0, 1, 1, 1),
            (2, 5, "Test", 9, 10, 10, 10),
            (2, 3, "Test", 19, 20, 20, 20),
            (1, 1, "Test", 99, 100, 100, 100),
            ]
        )
def test_table(
        table_to_test,
        cols, rows,
        caption,
        ex_blanklines,
        ex_tables,
        ex_tabulars,
        ex_captions
        ):
    """ Tests adding multiple figures to a plot

    Asserts the following:
        Expected number of blank lines present. Blank lines indicate a new
        table

        Expected number of tables present. If more rows or cols are present
        than row or col arg, the table is split

        Expected number of tabulars present

        Expected number of captions present. Should equal number of tables
        or 0 if no caption given. Captions should be unique
        (e.q Table A, Table B)

        Expected number of centering calls. Every figure should begin with a
        centering call.
    """

    tests = list()

    report = Report()
    report.add_table(table_to_test, cols=cols, rows=rows, caption=caption)
    report_text = report.report_text
    # Check for blank lines
    blank_lines = sum([len(i) == 0 for i in report_text])
    t_blank_lines = blank_lines == ex_blanklines
    tests.append(t_blank_lines)
    print(f"Right number of blank lines: {t_blank_lines}")
    # Check number of tables present
    begin_end_table_regex = re.compile(r"\\begin\{table\}|\\end\{table\}")
    tables_present = sum([bool(re.match(begin_end_table_regex, i))
                          for i in report_text])
    t_tables_present = tables_present == 2 * ex_tables
    tests.append(t_tables_present)
    print(f"Right number of tables: {t_tables_present}")
    # Check number of tabulars present
    begin_end_tabular_regex = re.compile(
            r"\\begin\{tabular\}|\\end\{tabular\}"
            )
    tabulars_present = sum([bool(re.match(begin_end_tabular_regex, i))
                           for i in report_text])
    t_tabulars_present = tabulars_present == 2 * ex_tabulars
    tests.append(t_tabulars_present)
    print(f"Right number of tabulars: {t_tabulars_present}")
    # Expected number of captions
    if ex_captions != 1:
        cap_regex = re.compile(r"\\caption\{.*\}")
    else:
        cap_regex = re.compile(r"\\caption\{Test\}")
    captions_present = [i for i in report_text if re.match(cap_regex, i)]
    u_caps_present = len(set(captions_present))  # Cast to set to remove dupes
    t_caps_present = u_caps_present == ex_captions
    tests.append(t_caps_present)
    print(f"Right number of captions: {t_caps_present}")
    # Check for centering calls
    centering_calls = sum([i == r"\centering" for i in report_text])
    t_centering_calls = centering_calls == ex_tables
    tests.append(t_centering_calls)
    print(f"Right number of centering calls: {t_centering_calls}")
    assert all(tests)
