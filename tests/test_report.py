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
    tests.append(len(report.report_text) == 11)


    assert all(tests)
