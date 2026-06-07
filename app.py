import customtkinter as ctk
import os
import requests
from dotenv import load_dotenv

load_dotenv()


#Theme and Color Options
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.API_KEY= os.getenv("API_KEY")

        #Window Config
        self.title("Currency Converter")
        self.geometry("400x450")
        self.resizable(False, False)

        #App Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="Currency Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(padx=20, pady=(30, 20))

        # From CURRENCY
        self.from_label=ctk.CTkLabel(
            self,
            text="From Currency",
            font=ctk.CTkFont(size=14))
        self.from_label.pack(anchor="w", padx=40, pady=(10, 2))

        #Currency Options
        self.currency_options = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]
        self.from_currency_dropdown = ctk.CTkComboBox(self, values=self.currency_options, width=320)
        self.from_currency_dropdown.pack(padx=40, pady=(0, 15))
        self.from_currency_dropdown.set("USD") #Default Value

        #To CURRENCY
        self.to_label = ctk.CTkLabel(self, text="To Currency: ", font=ctk.CTkFont(size=14))
        self.to_label.pack(padx=40, pady=(10, 2))

        self.to_currency_dropdown = ctk.CTkComboBox(self, values=self.currency_options, width=320)
        self.to_currency_dropdown.pack(padx=40, pady=(0, 15))
        self.to_currency_dropdown.set("EUR") #Default Value

        # Amount Entry
        self.amount_label= ctk.CTkLabel(self, text="Amount: ", font=ctk.CTkFont(size=14))
        self.amount_label.pack(anchor="w", padx=40, pady=(10, 2))

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Enter amount (e.g. 100)", width=320)
        self.amount_entry.pack(padx=40, pady=(0, 20))

        # Convert Button
        self.convert_button = ctk.CTkButton(
            self,
            text="Convert",
            command=self.convert_currency,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        self.convert_button.pack(padx=40, pady=10, fill="x")


        #Result Label
        self.result_label = ctk.CTkLabel(
            self, 
            text="Result: --",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f538d"
        )
        self.result_label.pack(padx=20, pady=(20, 10))

    def convert_currency(self):
        from_curr = self.from_currency_dropdown.get()
        to_curr = self.to_currency_dropdown.get()
        amount_str = self.amount_entry.get()

        #Amount Validation
        if not amount_str:
            self.result_label.configure(text="Please enter an amount", text_color="red")
            return
        
        try:
            amount = float(amount_str)
        except ValueError:
            self.result_label.configure(text="Invalid amount. Use numbers only.", text_color="red")
            return
        
        #Check for API Key
        if self.API_KEY != os.getenv("API_KEY"):
            self.result_label.configure(text="Error: Update your API Key in the code!", text_color="red")
            return
        
        url = f"https://v6.exchangerate-api.com/v6/{self.API_KEY}/latest/{from_curr}"

        try:
            self.result_label.configure(text="Fetching rates....", text_color="#1f538d")
            self.update_idletasks()

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data.get("result") == "success":
                rates = data.get("conversion_rates", {})

                if to_curr in rates: 
                    exchange_rate = rates[to_curr]
                    converted_amount = amount * exchange_rate

                    self.result_label.configure(
                        text=f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}",
                        text_color="#22c55e"
                    )
                else:
                    self.result_label.configure(text=f"Target currency {to_curr} not found.", text_color="red")
            else:
                error_type = data.get("error-type", "Unknown error")
                self.result_label.configure(text=f"API Error: {error_type}", text_color="red")

        except requests.exceptions.RequestException:
            self.result_label.configure(text="Network Error. Check Internet Connection.", text_color="red")

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()