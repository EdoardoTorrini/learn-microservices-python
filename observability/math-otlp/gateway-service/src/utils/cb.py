from circuitbreaker import circuit, CircuitBreakerError
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from functools import wraps


def resilient(failure_threshold=3, recovery_timeout=5, retry_attempts=3, retry_wait=1, timeout=None, fallback=None):
    def decorator(func):
        # Circuit breaker
        protected_func = circuit(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=Exception
        )(func)

        # Automatic retry
        retry_func = retry(
            stop=stop_after_attempt(retry_attempts),
            wait=wait_fixed(retry_wait),
            reraise=True
        )(protected_func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if timeout:
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(retry_func, *args, **kwargs)
                        return future.result(timeout=timeout)
                else:
                    return retry_func(*args, **kwargs)
            except (RetryError, CircuitBreakerError, Exception, FuturesTimeout) as e:
                # if isinstance(e, FuturesTimeout):
                #     print(f"Timeout superato: {timeout}s")
                # else:
                #     print(f"Errore definitivo: {e}")
                if fallback:
                    return fallback(*args, **kwargs)
                return None
        return wrapper
    return decorator
