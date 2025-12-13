# Make a Car class with properties and behaviors

class Car:
    def __init__(self, make, model, year, color, fuel_level=100):
        self.make = make           # Manufacturer
        self.model = model         # Model name
        self.year = year           # Manufacturing year
        self.color = color         # Car color
        self.fuel_level = fuel_level  # Fuel percentage (0-100)
        self.engine_on = False     # Engine status

    def start_engine(self):
        if self.engine_on:
            print("Engine is already on.")
        elif self.fuel_level <= 0:
            print("Cannot start engine. Fuel tank is empty.")
        else:
            self.engine_on = True
            print("Engine started.")

    def stop_engine(self):
        if not self.engine_on:
            print("Engine is already off.")
        else:
            self.engine_on = False
            print("Engine stopped.")

    def drive(self, distance):
        if not self.engine_on:
            print("Start the engine first.")
            return
        fuel_needed = distance * 0.5  # Assume 0.5% fuel per km (example)
        if fuel_needed > self.fuel_level:
            print("Not enough fuel to drive that distance.")
            return
        self.fuel_level -= fuel_needed
        print(f"Driven {distance} km. Fuel left: {self.fuel_level:.2f}%")

    def refuel(self, amount):
        if amount <= 0:
            print("Enter a positive amount to refuel.")
            return
        self.fuel_level = min(100, self.fuel_level + amount)
        print(f"Refueled {amount}%. Current fuel level: {self.fuel_level:.2f}%")

    def display_status(self):
        print(f"{self.year} {self.color} {self.make} {self.model}")
        print(f"Engine On: {self.engine_on}")
        print(f"Fuel Level: {self.fuel_level:.2f}%")


# Example usage
car1 = Car("Toyota", "Corolla", 2022, "Red")
car1.display_status()
car1.start_engine()
car1.drive(50)
car1.refuel(30)
car1.drive(150)
car1.stop_engine()
car1.display_status()
