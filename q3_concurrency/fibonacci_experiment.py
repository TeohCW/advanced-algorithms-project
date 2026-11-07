from time import perf_counter_ns

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


def main():
    positions = [35, 38, 40]

    print("--- FIBONACCI RESULTS ---")

    for n in positions:
        result = fibonacci(n)
        print(f"F({n}) = {result}")

    run_sequential(positions)


if __name__ == "__main__":
    main()