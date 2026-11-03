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

    DELETED = object()  # Unique marker for a deleted object.

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

    def _find_index(self, key):
        """Return the key's slot index, or None if it is absent."""

        start_index = self.hash_function(key)

        for step in range(self.capacity):
            index = (start_index + step) % self.capacity
            slot_content = self.slots[index]

            if slot_content is None:
                return None

            # Deleted slots must not end the search.
            if slot_content is self.DELETED:
                continue

            if slot_content[0] == key:
                return index

        return None

    def insert(self, key, value):
        """Insert a new key-value pair and return its slot index, reusing a deleted slot when possible"""

        start_index = self.hash_function(key)
        first_deleted = None

        for step in range(self.capacity):
            index = (start_index + step) % self.capacity
            slot_content = self.slots[index]

            if slot_content is self.DELETED:
                if first_deleted is None:
                    first_deleted = index

            elif slot_content is None:
                if first_deleted is not None:
                    index = first_deleted

                self.slots[index] = (key, value)
                self.count += 1
                return index

            elif slot_content[0] == key:
                raise ValueError(f"Key {key} already exists.")

        # No unused slots, but a deleted slot may still be available.
        if first_deleted is not None:
            self.slots[first_deleted] = (key, value)
            self.count += 1
            return first_deleted

        raise OverflowError("Hash table is full.")

    def search(self, key):
        """Return the associated value, or None if absent."""

        index = self._find_index(key)

        if index is None:
            return None

        return self.slots[index][1]

    def update(self, key, value):
        """Replace an existing value without changing its key or slot."""

        index = self._find_index(key)

        if index is None:
            return False

        self.slots[index] = (key, value)
        return True

    def delete(self, key):
        """Mark an existing entry as deleted."""

        index = self._find_index(key)

        if index is None:
            return False

        self.slots[index] = self.DELETED
        self.count -= 1
        return True

    def display(self):
        """Display occupied, empty and deleted slots."""

        print("\n--- HASH TABLE ---")

        for index, slot_content in enumerate(self.slots):
            if slot_content is None:
                print(f"Slot {index:2}: EMPTY")
            elif slot_content is self.DELETED:
                print(f"Slot {index:2}: DELETED")
            else:
                key, value = slot_content
                print(f"Slot {index:2}: {value}")

        print(f"\nRecords: {self.count}/{self.capacity}")
        print(f"Load factor: {self.count / self.capacity:.2f}")


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
        if slot_content is None or slot_content is inventory.DELETED:
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


def edit_medicine(inventory):
    """Edit medicine details while keeping the product ID unchanged."""

    print("\n--- EDIT MEDICINE ---")

    try:
        product_id = int(input("Enter product ID to edit: "))

        if product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

        current = inventory.search(product_id)

        if current is None:
            print(f"Product {product_id} was not found.")
            return

        print(f"Current details: {current}")
        print("Press Enter to keep an existing value.")

        name_input = input(f"Name [{current.name}]: ").strip()
        quantity_input = input(
            f"Quantity [{current.quantity}]: "
        ).strip()
        price_input = input(
            f"Price in cents [{current.price_cents}]: "
        ).strip()

        name = current.name if name_input == "" else name_input
        quantity = (
            current.quantity
            if quantity_input == ""
            else int(quantity_input)
        )
        price_cents = (
            current.price_cents
            if price_input == ""
            else int(price_input)
        )

        # Validate all changes before replacing the stored record.
        updated = Medicine(product_id, name, quantity, price_cents)

        if inventory.update(product_id, updated):
            print("Medicine updated successfully.")
            print(updated)
        else:
            print(f"Product {product_id} was not found.")

    except ValueError as error:
        print(f"Cannot edit medicine: {error}")


def delete_medicine(inventory):
    """Delete a medicine after the user confirms."""

    print("\n--- DELETE MEDICINE ---")

    try:
        product_id = int(input("Enter product ID to delete: "))

        if product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

        medicine = inventory.search(product_id)

        if medicine is None:
            print(f"Product {product_id} was not found.")
            return

        print(medicine)
        confirmation = input(
            "Delete this medicine? Enter y to confirm: "
        ).strip().lower()

        if confirmation != "y":
            print("Deletion cancelled.")
            return

        if inventory.delete(product_id):
            print(f"Product {product_id} deleted successfully.")
        else:
            print(f"Product {product_id} was not found.")

    except ValueError as error:
        print(f"Cannot delete medicine: {error}")


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
        print("5. Edit medicine")
        print("6. Delete medicine")
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
        elif choice == "5":
            edit_medicine(inventory)
        elif choice == "6":
            delete_medicine(inventory)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please enter a number from 0 to 6.")


if __name__ == "__main__":
    main()