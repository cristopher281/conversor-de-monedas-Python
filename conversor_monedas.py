import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Monedas")
        self.root.geometry("500x650")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)
        
        # Colores para el diseño minimalista
        self.primary_color = "#4a6bff"
        self.secondary_color = "#ffd900"
        self.accent_color = "#657997"
        self.text_color = "#333333"
        self.error_color = "#ff6b6b"
        
        # Cargar tasas de cambio
        self.exchange_rates = {}
        self.last_update = None
        self.load_currencies()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar valores predeterminados
        self.from_currency.set("USD")
        self.to_currency.set("EUR")
        self.amount_var.set("786.47")
        self.convert_currency()
    
    def load_currencies(self):
        """Cargar tasas de cambio fijas, incluyendo monedas centroamericanas"""
        self.currencies = [
            'USD',  # Dólar estadounidense
            'EUR',  # Euro
            'GBP',  # Libra esterlina
            'JPY',  # Yen japonés
            'CNY',  # Yuan chino
            'INR',  # Rupia india
            'BRL',  # Real brasileño
            'MXN',  # Peso mexicano
            'CAD',  # Dólar canadiense
            'AUD',  # Dólar australiano
            'CHF',  # Franco suizo
            'KRW',  # Won surcoreano
            'RUB',  # Rublo ruso
            'ZAR',  # Rand sudafricano
            'TRY',  # Lira turca
            'SGD',  # Dólar singapurense
            'NZD',  # Dólar neozelandés
            'SEK',  # Corona sueca
            'NOK',  # Corona noruega
            'DKK',  # Corona danesa
            'PLN',  # Zloty polaco
            'THB',  # Baht tailandés
            'IDR',  # Rupia indonesia
            'HKD',  # Dólar de Hong Kong
            'SAR',  # Rial saudí
            'AED',  # Dirham de EAU
            'ARS',  # Peso argentino
            'CLP',  # Peso chileno
            'COP',  # Peso colombiano
            'EGP',  # Libra egipcia
            # Monedas centroamericanas
            'GTQ',  # Quetzal guatemalteco
            'HNL',  # Lempira hondureño
            'NIO',  # Córdoba nicaragüense
            'CRC',  # Colón costarricense
            'PAB',  # Balboa panameño
            'BZD',  # Dólar beliceño
            'SVC',  # Colón salvadoreño
            'DOP',  # Peso dominicano
        ]
        self.exchange_rates = {
            'USD': 1.0,
            'EUR': 0.93,
            'GBP': 0.79,
            'JPY': 147.89,
            'CNY': 7.24,
            'INR': 83.11,
            'BRL': 4.97,
            'MXN': 17.25,
            'CAD': 1.36,
            'AUD': 1.52,
            'CHF': 0.89,
            'KRW': 1325.43,
            'RUB': 94.76,
            'ZAR': 18.91,
            'TRY': 27.32,
            'SGD': 1.35,
            'NZD': 1.65,
            'SEK': 10.78,
            'NOK': 10.63,
            'DKK': 6.95,
            'PLN': 3.95,
            'THB': 36.25,
            'IDR': 16250.0,
            'HKD': 7.85,
            'SAR': 3.75,
            'AED': 3.67,
            'ARS': 900.0,
            'CLP': 930.0,
            'COP': 4100.0,
            'EGP': 47.0,
            # Tasas aproximadas de monedas centroamericanas (por 1 USD)
            'GTQ': 7.75,   # Quetzal guatemalteco
            'HNL': 24.70,  # Lempira hondureño
            'NIO': 36.50,  # Córdoba nicaragüense
            'CRC': 520.0,  # Colón costarricense
            'PAB': 1.0,    # Balboa panameño (paridad con USD)
            'BZD': 2.0,    # Dólar beliceño
            'SVC': 8.75,   # Colón salvadoreño (referencial, ya no circula)
            'DOP': 58.0    # Peso dominicano
        }
        self.last_update = None
    
    def create_widgets(self):
        # Marco principal con scroll
        container = tk.Frame(self.root, bg="#f0f2f5")
        container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container, bg="#f0f2f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        main_frame = tk.Frame(canvas, bg="#f0f2f5", padx=20, pady=20)
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        main_frame.bind("<Configure>", on_configure)
        
        # Encabezado
        header_frame = tk.Frame(main_frame, bg=self.primary_color, padx=20, pady=15)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame, 
            text="Conversor de Monedas", 
            font=("Arial", 20, "bold"), 
            fg="white", 
            bg=self.primary_color
        ).pack()
        
        tk.Label(
            header_frame, 
            text="Tasas de cambio en tiempo real", 
            font=("Arial", 10), 
            fg="white", 
            bg=self.primary_color
        ).pack(pady=(5, 0))
        
        # Entrada de cantidad
        amount_frame = tk.Frame(main_frame, bg=self.secondary_color, padx=15, pady=15)
        amount_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            amount_frame, 
            text="Cantidad:", 
            font=("Arial", 10), 
            fg=self.text_color, 
            bg=self.secondary_color
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(
            amount_frame, 
            textvariable=self.amount_var, 
            font=("Arial", 14), 
            width=20
        )
        amount_entry.grid(row=1, column=0, sticky="ew")
        amount_entry.bind("<KeyRelease>", lambda e: self.convert_currency())
        
        # Selectores de moneda
        currency_frame = tk.Frame(main_frame, bg=self.secondary_color, padx=15, pady=15)
        currency_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Marco para moneda origen y destino
        from_to_frame = tk.Frame(currency_frame, bg=self.secondary_color)
        from_to_frame.pack(fill=tk.X)
        
        # Moneda origen
        from_frame = tk.Frame(from_to_frame, bg=self.secondary_color)
        from_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            from_frame, 
            text="De:", 
            font=("Arial", 10), 
            fg=self.text_color, 
            bg=self.secondary_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.from_currency = tk.StringVar()
        from_combobox = ttk.Combobox(
            from_frame, 
            textvariable=self.from_currency, 
            values=self.currencies, 
            font=("Arial", 11), 
            state="readonly",
            width=12
        )
        from_combobox.pack(fill=tk.X)
        from_combobox.bind("<<ComboboxSelected>>", lambda e: self.convert_currency())
        
        # Botón de intercambio
        swap_frame = tk.Frame(from_to_frame, bg=self.secondary_color, padx=10)
        swap_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        swap_btn = tk.Button(
            swap_frame, 
            text="↔", 
            font=("Arial", 14, "bold"), 
            bg=self.primary_color, 
            fg="white", 
            bd=0,
            command=self.swap_currencies,
            width=3,
            height=1
        )
        swap_btn.pack(pady=15)
        
        # Moneda destino
        to_frame = tk.Frame(from_to_frame, bg=self.secondary_color)
        to_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            to_frame, 
            text="A:", 
            font=("Arial", 10), 
            fg=self.text_color, 
            bg=self.secondary_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.to_currency = tk.StringVar()
        to_combobox = ttk.Combobox(
            to_frame, 
            textvariable=self.to_currency, 
            values=self.currencies, 
            font=("Arial", 11), 
            state="readonly",
            width=12
        )
        to_combobox.pack(fill=tk.X)
        to_combobox.bind("<<ComboboxSelected>>", lambda e: self.convert_currency())
        
        # Resultado
        result_frame = tk.Frame(main_frame, bg=self.accent_color, padx=15, pady=15)
        result_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            result_frame, 
            text="Total", 
            font=("Arial", 10), 
            fg="#777777", 
            bg=self.accent_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.result_var = tk.StringVar()
        self.result_var.set("0.00")
        self.result_label = tk.Label(
            result_frame, 
            textvariable=self.result_var, 
            font=("Arial", 24, "bold"), 
            fg=self.primary_color, 
            bg=self.accent_color
        )
        self.result_label.pack(anchor="w")
        
        self.rate_var = tk.StringVar()
        self.rate_var.set("Tasa de cambio: 1 USD = 0.89 EUR")
        tk.Label(
            result_frame, 
            textvariable=self.rate_var, 
            font=("Arial", 9), 
            fg="#777777", 
            bg=self.accent_color
        ).pack(anchor="w", pady=(5, 0))
        
        # Teclado numérico
        keypad_frame = tk.Frame(main_frame, bg=self.secondary_color, padx=15, pady=15)
        keypad_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear botones del teclado
        buttons = [
            '7', '8', '9', 'C',
            '4', '5', '6', '.',
            '1', '2', '3', '00',
            '0', '='
        ]
        
        row, col = 0, 0
        for btn in buttons:
            if btn == '=':
                btn_frame = tk.Frame(keypad_frame, bg=self.secondary_color)
                btn_frame.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=4, pady=4)
                tk.Button(
                    btn_frame, 
                    text=btn, 
                    font=("Arial", 16, "bold"), 
                    bg=self.primary_color, 
                    fg="white",
                    activebackground="#3a4dcc",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    command=lambda b=btn: self.on_keypad_click(b),
                    height=2,
                    width=8
                ).pack(fill=tk.BOTH, expand=True)
                col += 2
            elif btn == '0':
                btn_frame = tk.Frame(keypad_frame, bg=self.secondary_color)
                btn_frame.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=4, pady=4)
                tk.Button(
                    btn_frame, 
                    text=btn, 
                    font=("Arial", 16), 
                    bg=self.accent_color,
                    activebackground="#e0e4ea",
                    relief="flat",
                    bd=0,
                    command=lambda b=btn: self.on_keypad_click(b),
                    height=2
                ).pack(fill=tk.BOTH, expand=True)
                col += 2
            else:
                btn_frame = tk.Frame(keypad_frame, bg=self.secondary_color)
                btn_frame.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
                bg_color = self.accent_color
                fg_color = self.text_color
                if btn == 'C':
                    bg_color = self.error_color
                    fg_color = "white"
                tk.Button(
                    btn_frame, 
                    text=btn, 
                    font=("Arial", 16), 
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#e0e4ea" if btn != 'C' else "#d9534f",
                    activeforeground=fg_color,
                    relief="flat",
                    bd=0,
                    command=lambda b=btn: self.on_keypad_click(b),
                    height=2,
                    width=5
                ).pack(fill=tk.BOTH, expand=True)
                col += 1
            
            if col >= 4:
                col = 0
                row += 1
        
        # Configurar pesos de las columnas
        for i in range(4):
            keypad_frame.columnconfigure(i, weight=1)
        
        # Pie de página siempre visible
        footer_frame = tk.Frame(main_frame, bg=self.accent_color, padx=10, pady=8)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        update_time = self.last_update.strftime("%d/%m/%Y %H:%M") if self.last_update else "N/A"
        tk.Label(
            footer_frame, 
            text=f"Tasas actualizadas: {update_time} | Fuente: ExchangeRate-API",
            font=("Arial", 8), 
            fg="#777777", 
            bg=self.accent_color
        ).pack()
    
    def on_keypad_click(self, key):
        current = self.amount_var.get()
        
        if key == 'C':
            self.amount_var.set("")
        elif key == '=':
            self.convert_currency()
        elif key == '.':
            if '.' not in current:
                self.amount_var.set(current + '.')
        elif key == '00':
            self.amount_var.set(current + '00')
        else:
            if current == "0":
                self.amount_var.set(key)
            else:
                self.amount_var.set(current + key)
        
        if key != '=':
            self.convert_currency()
    
    def swap_currencies(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)
        self.convert_currency()
    
    def animate_result(self, old_value, new_value, currency, steps=10, delay=30):
        try:
            old = float(old_value.replace(',', '').split()[0])
            new = float(new_value.replace(',', '').split()[0])
        except Exception:
            self.result_var.set(f"{new_value} {currency}")
            return
        diff = (new - old) / steps
        def step(i=1, value=old):
            if i > steps:
                self.result_var.set(f"{new_value} {currency}")
                return
            value += diff
            self.result_var.set(f"{value:,.2f} {currency}")
            self.root.after(delay, lambda: step(i+1, value))
        step()

    def animate_label_bg(self, label, color1, color2, steps=10, delay=20):
        # Transición de color de fondo para el label de resultado
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        def step(i=1):
            if i > steps:
                label.config(bg=color2)
                return
            ratio = i / steps
            rgb = tuple(int(rgb1[j] + (rgb2[j] - rgb1[j]) * ratio) for j in range(3))
            label.config(bg=rgb_to_hex(rgb))
            self.root.after(delay, lambda: step(i+1))
        step()

    def convert_currency(self):
        try:
            amount = float(self.amount_var.get() or 0)
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            if from_curr == to_curr:
                result = amount
                rate = 1.0
            else:
                rate_from = self.exchange_rates.get(from_curr, 1.0)
                rate_to = self.exchange_rates.get(to_curr, 1.0)
                amount_in_usd = amount / rate_from
                result = amount_in_usd * rate_to
                rate = rate_to / rate_from
            formatted_result = "{:,.2f}".format(result)
            # Animación de resultado
            old_value = self.result_var.get()
            self.animate_result(old_value, formatted_result, to_curr)
            formatted_rate = "{:,.4f}".format(rate)
            self.rate_var.set(f"Tasa de cambio: 1 {from_curr} = {formatted_rate} {to_curr}")
            # Animación de fondo del resultado
            if hasattr(self, 'result_label'):
                self.animate_label_bg(self.result_label, self.accent_color, '#d6eaff')
        except ValueError:
            self.result_var.set("0.00")
            self.rate_var.set("Tasa de cambio: 1 USD = 0.89 EUR")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la conversión: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()