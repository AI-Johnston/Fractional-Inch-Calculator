import tkinter as tk
from tkinter import ttk
from fractions import Fraction

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Fractional Inch Calculator")

        # Input 1
        self.feet_label = ttk.Label(master, text="Feet:")
        self.feet_label.grid(row=0, column=0, padx=5, pady=5)
        self.feet_entry = ttk.Entry(master, width=10)
        self.feet_entry.grid(row=0, column=1, padx=5, pady=5)

        self.inches_label = ttk.Label(master, text="Inches:")
        self.inches_label.grid(row=1, column=0, padx=5, pady=5)
        self.inches_entry = ttk.Entry(master, width=10)
        self.inches_entry.grid(row=1, column=1, padx=5, pady=5)

        self.fraction_label = ttk.Label(master, text="Fraction (e.g., 1/2):")
        self.fraction_label.grid(row=2, column=0, padx=5, pady=5)
        self.fraction_entry = ttk.Entry(master, width=10)
        self.fraction_entry.grid(row=2, column=1, padx=5, pady=5)

        # Input 2
        self.feet_label2 = ttk.Label(master, text="Feet:")
        self.feet_label2.grid(row=0, column=2, padx=5, pady=5)
        self.feet_entry2 = ttk.Entry(master, width=10)
        self.feet_entry2.grid(row=0, column=3, padx=5, pady=5)

        self.inches_label2 = ttk.Label(master, text="Inches:")
        self.inches_label2.grid(row=1, column=2, padx=5, pady=5)
        self.inches_entry2 = ttk.Entry(master, width=10)
        self.inches_entry2.grid(row=1, column=3, padx=5, pady=5)

        self.fraction_label2 = ttk.Label(master, text="Fraction (e.g., 1/2):")
        self.fraction_label2.grid(row=2, column=2, padx=5, pady=5)
        self.fraction_entry2 = ttk.Entry(master, width=10)
        self.fraction_entry2.grid(row=2, column=3, padx=5, pady=5)

        # Buttons
        self.add_button = ttk.Button(master, text="Add", command=lambda: self.calculate("add"))
        self.add_button.grid(row=3, column=0, padx=5, pady=5)

        self.subtract_button = ttk.Button(master, text="Subtract", command=lambda: self.calculate("subtract"))
        self.subtract_button.grid(row=3, column=1, padx=5, pady=5)

        self.multiply_button = ttk.Button(master, text="Multiply", command=lambda: self.calculate("multiply"))
        self.multiply_button.grid(row=3, column=2, padx=5, pady=5)

        self.divide_button = ttk.Button(master, text="Divide", command=lambda: self.calculate("divide"))
        self.divide_button.grid(row=3, column=3, padx=5, pady=5)

        self.clear_button = ttk.Button(master, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=4, column=1, padx=5, pady=5)

        # Result
        self.result_label = ttk.Label(master, text="Result:")
        self.result_label.grid(row=5, column=0, padx=5, pady=5)
        self.result_value = ttk.Label(master, text="")
        self.result_value.grid(row=5, column=1, padx=5, pady=5)

        # Number Pad
        self.number_pad_frame = ttk.Frame(master)
        self.number_pad_frame.grid(row=0, column=4, rowspan=3, padx=5, pady=5)

        self.current_entry = None  # To keep track of which entry is currently selected

        # Create number buttons
        numbers = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '/', '.'
        ]
        row_val = 0
        col_val = 0
        for button_text in numbers:
            ttk.Button(self.number_pad_frame, text=button_text, width=4,
                       command=lambda text=button_text: self.insert_text(text)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

        # Set focus to an entry field when clicked
        self.feet_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.feet_entry))
        self.inches_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.inches_entry))
        self.fraction_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.fraction_entry))
        self.feet_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.feet_entry2))
        self.inches_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.inches_entry2))
        self.fraction_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.fraction_entry2))

    def set_current_entry(self, entry):
        """Sets the currently selected entry field."""
        self.current_entry = entry


    def insert_text(self, text):
        """Inserts text into the currently selected entry field."""
        if self.current_entry:
            self.current_entry.insert(tk.END, text)


    def _get_value(self, feet_entry, inches_entry, fraction_entry):
        """Helper function to get the total inches from the entries."""
        try:
            feet = int(feet_entry.get() or 0)
            inches = int(inches_entry.get() or 0)
            fraction_str = fraction_entry.get() or "0/1"
            fraction = Fraction(fraction_str)
            return (feet * 12) + inches + float(fraction)  # Convert Fraction to float for calculations
        except ValueError:
            self.result_value.config(text="Invalid input")
            return None
        except ZeroDivisionError:
            self.result_value.config(text="Invalid fraction")
            return None

    def _format_result(self, total_inches):
         """Helper function to format the result back into feet, inches, and fraction."""
         feet = int(total_inches // 12)
         remaining_inches = total_inches % 12
         inches = int(remaining_inches // 1)  # Get the whole number of inches
         fractional_inches = remaining_inches - inches

         # Find the closest common fraction (1/2, 1/4, 1/8, 1/16)
         fractions = [Fraction(0, 1), Fraction(1, 16), Fraction(1, 8), Fraction(1, 4), Fraction(3, 8), Fraction(1, 2), Fraction(5, 8), Fraction(3, 4), Fraction(7, 8), Fraction(15, 16)]
         closest_fraction = min(fractions, key=lambda frac: abs(float(frac) - fractional_inches))


         return f"{feet} ft, {inches} in, {closest_fraction}"


    def calculate(self, operation):
        value1 = self._get_value(self.feet_entry, self.inches_entry, self.fraction_entry)
        value2 = self._get_value(self.feet_entry2, self.inches_entry2, self.fraction_entry2)

        if value1 is not None and value2 is not None:
            try:
                if operation == "add":
                    total_inches = value1 + value2
                elif operation == "subtract":
                    total_inches = value1 - value2
                elif operation == "multiply":
                    total_inches = value1 * value2
                elif operation == "divide":
                    if value2 == 0:
                        self.result_value.config(text="Cannot divide by zero")
                        return
                    total_inches = value1 / value2
                else:
                    self.result_value.config(text="Invalid operation")
                    return

                self.result_value.config(text=self._format_result(total_inches))

            except Exception as e:
                self.result_value.config(text=f"Error: {e}")


    def clear_fields(self):
        self.feet_entry.delete(0, tk.END)
        self.inches_entry.delete(0, tk.END)
        self.fraction_entry.delete(0, tk.END)
        self.feet_entry2.delete(0, tk.END)
        self.inches_entry2.delete(0, tk.END)
        self.fraction_entry2.delete(0, tk.END)
        self.result_value.config(text="")

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()