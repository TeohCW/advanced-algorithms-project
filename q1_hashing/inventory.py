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

class LinearProbingHashTable:
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


def display_inventory(inventory):
    """Format stored medicines for the pharmacy interface."""
    header = (
        f"{'Slot':<6} | {'ID':<8} | {'Medicine':<24} | "
        f"{'Quantity':>8} | {'Price (RM)':>12}"
    )

    print("\n--- PHARMACY INVENTORY ---")
    print(header)
    print("-" * len(header))

    for index, slot_content in enumerate(inventory.slots):
        if slot_content is None:
            continue

        key, medicine = slot_content

        # Shorten long names so the columns stay aligned.
        name = medicine.name
        if len(name) > 24:
            name = name[:21] + "..."

        ringgit, cents = divmod(medicine.price_cents, 100)
        price = f"{ringgit}.{cents:02d}"

        print(
            f"{index:<6} | {key:<8} | {name:<24} | "
            f"{medicine.quantity:>8} | {price:>12}"
        )

    if inventory.count == 0:
        print("No medicines stored.")

    print("-" * len(header))
    print(f"Total products: {inventory.count}")
    print(f"Capacity: {inventory.capacity}")
    print(f"Load factor: {inventory.count / inventory.capacity:.2f}")


def add_medicine(inventory):
    """Read user input and insert a medicine."""
    print("\n--- ADD MEDICINE ---")

    try:
        product_id = int(input("Product ID: "))
        name = input("Medicine name: ")
        quantity = int(input("Quantity: "))
        price_cents = int(input("Price in cents (e.g. 550 = RM5.50): "))

        # The Medicine constructor validates the supplied values.
        medicine = Medicine(product_id, name, quantity, price_cents)

        # The hash table checks for duplicates and available space.
        index = inventory.insert(product_id, medicine)
        print(f"Medicine added successfully at slot {index}.")

    except ValueError as error:
        print(f"Cannot add medicine: {error}")
    except OverflowError as error:
        print(f"Cannot add medicine: {error}")


def search_medicine(inventory):
    """Search for a medicine using its product ID."""
    print("\n--- SEARCH MEDICINE ---")

    try:
        product_id = int(input("Enter product ID: "))

        if product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

        medicine = inventory.search(product_id)

        if medicine is None:
            print(f"Product {product_id} was not found.")
        else:
            print("Medicine found:")
            print(medicine)

    except ValueError as error:
        print(f"Cannot search: {error}")


def main():
    inventory = LinearProbingHashTable(capacity=11)

    # These IDs deliberately collide to demonstrate linear probing.
    medicines_arr = [
        Medicine(101, "Paracetamol", 50, 550),
        Medicine(112, "Cetirizine", 30, 800),
        Medicine(123, "Vitamin C", 40, 1250),
    ]

    for medicine in medicines_arr:
        inventory.insert(medicine.id, medicine)

    while True:
        print("\n===== PHARMACY INVENTORY SYSTEM =====")
        print("1. Add medicine")
        print("2. Search medicine")
        print("3. Display inventory")
        print("4. Display hash table slots")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_medicine(inventory)
        elif choice == "2":
            search_medicine(inventory)
        elif choice == "3":
            display_inventory(inventory)
        elif choice == "4":
            inventory.display()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please enter 0, 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()