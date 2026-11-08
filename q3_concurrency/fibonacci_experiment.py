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


def validate_results(results, expected_results):
    """Check whether the calculated results match the expected values."""
    if results != expected_results:
        raise ValueError(
            f"Incorrect Fibonacci results. "
            f"Expected {expected_results}, got {results}."
        )


def run_sequential(positions, expected_results, rounds=10):
    """Measure the total calculation time for each sequential round."""
    timings = []

    print("\n=== Fibonacci Computation (Without Multithreading) ===")

    for round_number in range(1, rounds + 1):
        start_time = perf_counter_ns()

        results = []
        for n in positions:
            results.append(fibonacci(n))

        end_time = perf_counter_ns()

        elapsed_time = end_time - start_time
        timings.append(elapsed_time)

        validate_results(results, expected_results)

        result_text = ", ".join(
            f"Fib({n})={result}" for n, result in zip(positions, results)
        )
        print(f"Round {round_number:2}: {result_text} | T = {elapsed_time:,} ns")

    average_time = sum(timings) / len(timings)

    print(f"Average T (Without Multithreading): {average_time:,.2f} ns")

    return timings


def fibonacci_worker(n, index, results, start_times, end_times):
    """Calculate one Fibonacci number and record its timing."""
    start_times[index] = perf_counter_ns()

    result = fibonacci(n)

    end_times[index] = perf_counter_ns()
    results[index] = result


def run_multithreaded(positions, expected_results, rounds=10):
    """Measure the time from the earliest worker start to the latest finish."""
    timings = []

    print("\n=== Fibonacci Computation (With Multithreading) ===")

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

        validate_results(results, expected_results)

        result_text = ", ".join(
            f"Fib({n})={result}" for n, result in zip(positions, results)
        )
        print(f"Round {round_number:2}: {result_text} | T = {elapsed_time:,} ns")

    average_time = sum(timings) / len(timings)

    print(f"Average T (With Multithreading): {average_time:,.2f} ns")

    return timings


def display_comparison(sequential_timings, multithreaded_timings):
    """Compare average times as a percentage of the sequential baseline."""
    sequential_average = (
        sum(sequential_timings) / len(sequential_timings)
    )
    multithreaded_average = (
        sum(multithreaded_timings) / len(multithreaded_timings)
    )

    if sequential_average <= 0:
        print("\nObservation: Percentage change cannot be calculated "
              "because the sequential average is zero.")
        return

    percentage_change = (
        (multithreaded_average - sequential_average) / sequential_average * 100
    )

    if percentage_change > 0:
        print("\nObservation: Multithreading increased the average completion "
              f"time by approximately {percentage_change:.1f}%.")
    elif percentage_change < 0:
        print("\nObservation: Multithreading reduced the average completion "
              f"time by approximately {abs(percentage_change):.1f}%.")
    else:
        print("\nObservation: Both methods had the same average completion time.")


def main():
    positions = [35, 38, 40]
    expected_results = [9227465, 39088169, 102334155]

    multithreaded_timings = run_multithreaded(
        positions, expected_results
    )

    sequential_timings = run_sequential(
        positions, expected_results
    )

    print("\nAll rounds produced the expected Fibonacci results.")

    display_comparison(
        sequential_timings, multithreaded_timings
    )


if __name__ == "__main__":
    main()