class Medicine:
    """Represents one medicine product in the pharmacy."""

    def __init__(self, id, name, quantity, price_cents):
        if type(id) is not int or id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Medicine name must not be empty.")

        if type(quantity) is not int or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        if type(price_cents) is not int or price_cents < 0:
            raise ValueError("Price must be a non-negative integer in cents.")

        self.id = id
        self.name = name.strip()
        self.quantity = quantity
        self.price_cents = price_cents

    def __str__(self):
        ringgit, cents = divmod(self.price_cents, 100)   # ringgit = self.price_cents // 100, cents = self.price_cents % 100
        return (
            f"ID: {self.id} | "
            f"Name : {self.name} | "
            f"Quantity: {self.quantity} | "
            f"Price: RM{ringgit}.{cents:02d}"
        )

class LinerProbingHashTable:
    """Stores integer keys and associated values using linear probing."""

    def __init__(self, capacity=11):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.capacity = capacity
        self.slots = [None] * capacity
        self.count = 0

        def hash_function(self, key):
            if type(key) is not int:
                raise TypeError("This hash table requires integer keys.")

            return key % self.capacity

        def insert(self, key, value):
            """Insert a new key-value pair and return its slot index."""
            start_index = self.hash_function(key)

            # Check at most every slot once to avoid an infinite loop.
            for step in range(self.capacity):
                index = (start_index + step) % self.capacity
                slot_content = self.slots[index]

                if slot_content is None:
                    self.slots[index] = (key, value)
                    self.count += 1
                    return index

                if slot_content[0] == key:
                    raise ValueError(f"Key {key} already exists.")

            raise OverflowError("Hash table is full.")

        def search(self, key):
            """Return the associated value, or None if the key is absent."""
            start_index = self.hash_function(key)

            for step in range(self.capacity):
                index = (start_index + step) % self.capacity
                slot_content = self.slots[index]

                # Without deletion, an empty slot ends the search.
                if slot_content is None:
                    return None

                if slot_content[0] == key:
                    return slot_content[1]

            return None

        def display(self):
            """Display the slots so collisions can be inspected."""

            print("\n--- HASH TABLE ---")

            for index, slot_content in enumerate(self.slots):
                if slot_content is None:
                    print(f"Slot {index:2}: EMPTY")
                else:
                    key, value = slot_content
                    print(f"Slot {index:2}: {value}")

            load_factor = self.count / self.capacity
            print(f"\nRecords: {self.count}/{self.capacity}")
            print(f"Load factor: {load_factor:.2f}")
