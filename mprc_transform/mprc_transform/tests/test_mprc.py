"""pytest test suite — wraps verify.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from mprc.verify import TESTS

@pytest.mark.parametrize("fn,desc", TESTS, ids=[d for _, d in TESTS])
def test_mprc(fn, desc):
    assert fn(), desc
