"""Small retry helper.

`retry(fn, max_retries=3, exceptions=(Exception,))` calls ``fn()`` until it
returns, attempting at most ``max_retries`` times in total. If every attempt
raises one of ``exceptions``, the last exception is re-raised. Exceptions of
other types propagate immediately (they are not retryable).
"""


def retry(fn, max_retries=3, exceptions=(Exception,)):
    """Call ``fn()`` with retries.

    Attempts the call up to ``max_retries`` times in total. Returns the first
    successful result. If every attempt fails with one of ``exceptions``,
    the last such exception is raised. Non-matching exceptions propagate
    immediately.
    """
    last_exc = None
    for _attempt in range(max_retries):
        try:
            return fn()
        except exceptions as exc:
            last_exc = exc
    raise last_exc
