import time
from datetime import timedelta

from simulacion_tp6.main import main

if __name__ == "__main__":
    start_time = time.monotonic()
    main()
    end_time = time.monotonic()
    print(f"Tiempo total: {timedelta(seconds=end_time - start_time)}")
