from time import perf_counter_ns
from threading import Thread

def fibonacci(n):
    """Return the Fibonacci number at position n."""
    if type(n) is not int or n < 0:
        raise ValueError("Position must be a non-negative integer.")

    current = 0
    next_number = 1

    for step in range(n):
        current, next_number = next_number, current + next_number

    return current


def run_sequential(positions, rounds=10):
    """Measure the total calculation time for each sequential round."""
    timings = []

    print("\n--- SEQUENTIAL EXECUTION ---")

    for round_number in range(1, rounds + 1):
        start_time = perf_counter_ns()

        results = []
        for n in positions:
            results.append(fibonacci(n))

        end_time = perf_counter_ns()

        elapsed_time = end_time - start_time
        timings.append(elapsed_time)

        print(f"Round {round_number:2}: {elapsed_time:,} ns")

    average_time = sum(timings) / len(timings)

    print(f"\nResults: {results}")
    print(f"Average time: {average_time:,.2f} ns")

    return timings


def fibonacci_worker(n, index, results, start_times, end_times):
    """Calculate one Fibonacci number and record its timing."""
    start_times[index] = perf_counter_ns()

    result = fibonacci(n)

    end_times[index] = perf_counter_ns()
    results[index] = result


def run_multithreaded(positions, rounds=10):
    """Measure the time from the earliest worker start to the latest finish."""
    timings = []

    print("\n--- MULTITHREADED EXECUTION ---")

    for round_number in range(1, rounds + 1):
        results = [None] * len(positions)
        start_times = [None] * len(positions)
        end_times = [None] * len(positions)
        threads = []

        for index, n in enumerate(positions):
            thread = Thread(
                target=fibonacci_worker,
                args=(n, index, results, start_times, end_times)
            )
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        elapsed_time = max(end_times) - min(start_times)
        timings.append(elapsed_time)

        print(f"Round {round_number:2}: {elapsed_time:,} ns")

    average_time = sum(timings) / len(timings)

    print(f"\nResults: {results}")
    print(f"Average time: {average_time:,.2f} ns")

    return timings


def main():
    positions = [35, 38, 40]

    print("--- FIBONACCI RESULTS ---")

    for n in positions:
        result = fibonacci(n)
        print(f"F({n}) = {result}")

    run_sequential(positions)
    run_multithreaded(positions)


if __name__ == "__main__":
    main()