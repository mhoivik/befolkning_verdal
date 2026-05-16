import time

import konfig

START_TIDSPUNKT = time.perf_counter()

def Logg(obj, msg: str) -> None:
    if not konfig.LOGGING:
        return
    tid = time.perf_counter() - START_TIDSPUNKT
    print(f"[{tid:.4g}s] [{obj.__class__.__name__}] {msg}")