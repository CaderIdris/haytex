import pandas as pd
import pytest

from haytex.report import Report as Report


@pytest.fixture
def list_of_figs():
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
    t_parts = all([f"P{i}" for i in range(1, 3)])
    tests.append(t_parts)
    print(f"Right number of parts: {t_parts}")
    t_chaps = all([f"C{i}" for i in range(1, 5)])
    tests.append(t_chaps)
    print(f"Right number of chapters: {t_chaps}")
    t_secs = all([f"S{i}" for i in range(1, 5)])
    tests.append(t_secs)
    print(f"Right number of sections: {t_secs}")
    t_subsecs = all([f"sS{i}" for i in range(1, 5)])
    tests.append(t_subsecs)
    print(f"Right number of subsections: {t_subsecs}")
    t_subsubsecs = all([f"ssS{i}" for i in range(1, 5)])
    tests.append(t_subsubsecs)
    print(f"Right number of subsections: {t_subsubsecs}")

    assert all(tests)
