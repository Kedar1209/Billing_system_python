import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("650x700")

        # Variables
        self.item_name = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.gst_percent = tk.DoubleVar(value=5)

        self.total_amount = 0

        self.create_ui()
        self.create_bill_header()

    # ---------- UI ----------
    def create_ui(self):
        tk.Label(self.root, text="🛒 Billing System",
                 font=("Arial", 20, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Item Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.item_name).grid(row=0, column=1)

        tk.Label(frame, text="Price").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.price).grid(row=1, column=1)

        tk.Label(frame, text="Quantity").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.quantity).grid(row=2, column=1)

        tk.Label(frame, text="GST %").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.gst_percent).grid(row=3, column=1)

        tk.Button(frame, text="Add Item", command=self.add_item,
                  bg="green", fg="white").grid(row=4, columnspan=2, pady=10)

        # Bill Area with Scrollbar
        bill_frame = tk.Frame(self.root)
        bill_frame.pack()

        scrollbar = tk.Scrollbar(bill_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.bill_area = tk.Text(bill_frame, height=18, width=70,
                                 yscrollcommand=scrollbar.set)
        self.bill_area.pack()

        scrollbar.config(command=self.bill_area.yview)

        # Total
        self.total_label = tk.Label(self.root, text="Total: ₹0.00",
                                   font=("Arial", 14, "bold"))
        self.total_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save Bill", command=self.save_bill,
                  bg="blue", fg="white").grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Clear", command=self.clear_bill,
                  bg="red", fg="white").grid(row=0, column=1, padx=10)

    # ---------- BILL HEADER ----------
    def create_bill_header(self):
        self.bill_area.insert(tk.END, "===== SHOP BILL =====\n")
        self.bill_area.insert(tk.END, f"Date: {datetime.now()}\n")
        self.bill_area.insert(tk.END, "-"*50 + "\n")
        self.bill_area.insert(tk.END, "Item\tQty\tPrice\tTotal\n")
        self.bill_area.insert(tk.END, "-"*50 + "\n")

    # ---------- LOGIC ----------
    def add_item(self):
        name = self.item_name.get()
        pr = self.price.get()
        qty = self.quantity.get()
        gst = self.gst_percent.get()

        if not name or pr <= 0 or qty <= 0:
            messagebox.showerror("Error", "Enter valid details")
            return

        subtotal = pr * qty
        gst_amount = subtotal * gst / 100
        total = subtotal + gst_amount

        self.total_amount += total

        self.bill_area.insert(
            tk.END,
            f"{name}\t{qty}\t₹{pr:.2f}\t₹{total:.2f}\n"
        )

        self.total_label.config(text=f"Total: ₹{self.total_amount:.2f}")

        # Reset inputs
        self.item_name.set("")
        self.price.set(0.0)
        self.quantity.set(0)

    def save_bill(self):
        if self.total_amount == 0:
            messagebox.showerror("Error", "No bill to save")
            return

        filename = f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # ✅ FIXED: Added encoding="utf-8"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.bill_area.get("1.0", tk.END))
            f.write("-"*50 + "\n")
            f.write(f"Final Total: ₹{self.total_amount:.2f}")

        messagebox.showinfo("Saved", f"Bill saved as {filename}")

    def clear_bill(self):
        self.bill_area.delete("1.0", tk.END)
        self.total_amount = 0
        self.total_label.config(text="Total: ₹0.00")
        self.create_bill_header()


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingSystem(root)
    root.mainloop()
