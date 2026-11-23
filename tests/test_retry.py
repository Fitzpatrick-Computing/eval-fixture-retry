"""Visible test suite for fixit.retry.

Run from the repository root:  python3 -m pytest -q
"""
import pytest

from fixit import retry


def test_returns_value_on_success():
    calls = []

    def ok():
        calls.append(1)
        return "done"

    assert retry(ok, max_retries=3) == "done"
    assert calls == [1]


def test_non_matching_exception_propagates_immediately():
    calls = []

    def bad():
        calls.append(1)
        raise ValueError("nope")

    with pytest.raises(ValueError):
        retry(bad, max_retries=5, exceptions=(KeyError,))
    # A non-retryable exception must not be retried at all.
    assert calls == [1]


def test_succeeds_after_transient_failure():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise ConnectionError("transient")
        return "recovered"

    # Fails once, then succeeds: with max_retries=3 the helper must return
    # the value from the second attempt.
    assert retry(flaky, max_retries=3, exceptions=(ConnectionError,)) == "recovered"
    assert calls == [1, 1]


def test_attempts_max_retries_times_before_raising():
    calls = []

    def always_fails():
        calls.append(1)
        raise ConnectionError("down")

    with pytest.raises(ConnectionError, match="down"):
        retry(always_fails, max_retries=3, exceptions=(ConnectionError,))
    assert calls == [1, 1, 1]


def test_reraises_last_exception_after_max_retries():
    calls = []

    def always_fails():
        calls.append(len(calls))
        raise ConnectionError(f"attempt {len(calls)}")

    with pytest.raises(ConnectionError, match="attempt 2"):
        retry(always_fails, max_retries=2, exceptions=(ConnectionError,))
    assert calls == [0, 1]
