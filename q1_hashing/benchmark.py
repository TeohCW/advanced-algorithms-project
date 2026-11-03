from random import Random
from time import perf_counter_ns
from statistics import mean

from inventory import Medicine, LinearProbingHashTable


def linear_search(medicines, product_id):
    """Search the array one record at a time."""
    for medicine in medicines:
        if medicine.id == product_id:
            return medicine

    return None


def measure_searches(search_function, search_ids):
    """Measure the total time for a batch of searches."""
    start = perf_counter_ns()

    for product_id in search_ids:
        search_function(product_id)

    end = perf_counter_ns()
    return end - start


def compare_searches(medicines, inventory, search_ids, rounds):
    """Check correctness, then time both methods over several rounds."""

    def array_search(product_id):
        return linear_search(medicines, product_id)

    def hash_search(product_id):
        return inventory.search(product_id)

    # Verify correctness and warm up both methods before timing.
    for product_id in search_ids:
        array_result = array_search(product_id)
        hash_result = hash_search(product_id)

        if array_result is not hash_result:
            raise AssertionError(
                f"Search results disagree for ID {product_id}."
            )

    array_times = []
    hash_times = []

    print(
        f"{'Round':<8} | {'Array batch (ns)':>18} | "
        f"{'Hash batch (ns)':>18}"
    )
    print("-" * 50)

    for round_number in range(1, rounds + 1):
        # Alternate order so one method is not always measured first.
        if round_number % 2 == 1:
            array_time = measure_searches(array_search, search_ids)
            hash_time = measure_searches(hash_search, search_ids)
        else:
            hash_time = measure_searches(hash_search, search_ids)
            array_time = measure_searches(array_search, search_ids)

        array_times.append(array_time)
        hash_times.append(hash_time)

        print(
            f"{round_number:<8} | {array_time:>18,} | "
            f"{hash_time:>18,}"
        )

    average_array = mean(array_times)
    average_hash = mean(hash_times)
    searches_per_round = len(search_ids)

    print("\nAverage batch time:")
    print(f"Array:      {average_array:,.0f} ns")
    print(f"Hash table: {average_hash:,.0f} ns")

    print("\nAverage time per search:")
    print(f"Array:      {average_array / searches_per_round:,.2f} ns")
    print(f"Hash table: {average_hash / searches_per_round:,.2f} ns")

    if average_hash > 0:
        ratio = average_array / average_hash
        print(f"\nArray time / hash-table time: {ratio:.2f}")
        print("Above 1 means the hash table was faster.")


def run_experiment(record_count, rounds=10, searches_per_round=200):
    """Create identical datasets and compare successful/missing searches."""
    rng = Random(42)

    # Unique, reproducible IDs with varied hash positions.
    product_ids = rng.sample(
        range(1, record_count * 100 + 1),
        record_count
    )

    medicines = [
        Medicine(product_id, f"Medicine {product_id}", 10, 500)
        for product_id in product_ids
    ]

    # Keep the load factor below 0.5.
    capacity = record_count * 2 + 1
    inventory = LinearProbingHashTable(capacity=capacity)

    for medicine in medicines:
        inventory.insert(medicine.id, medicine)

    # Existing IDs: some can repeat across the batch.
    successful_ids = [
        rng.choice(product_ids)
        for _ in range(searches_per_round)
    ]

    # IDs outside the generated range are guaranteed to be absent.
    missing_ids = [
        rng.randrange(
            record_count * 100 + 1,
            record_count * 200 + 1
        )
        for _ in range(searches_per_round)
    ]

    print("\n" + "=" * 65)
    print(f"RECORDS: {record_count}")
    print(f"Table capacity: {capacity}")
    print(f"Load factor: {inventory.count / capacity:.3f}")
    print(f"Rounds: {rounds}")
    print(f"Searches per round per method: {searches_per_round}")
    print("=" * 65)

    print("\nSUCCESSFUL SEARCHES")
    compare_searches(medicines, inventory, successful_ids, rounds)

    print("\nUNSUCCESSFUL SEARCHES")
    compare_searches(medicines, inventory, missing_ids, rounds)


def main():
    for record_count in [100, 1000, 5000]:
        run_experiment(record_count)


if __name__ == "__main__":
    main()