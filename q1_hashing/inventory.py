class Medicine:

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
