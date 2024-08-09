import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os

class ParameterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Parameter Configuration")
        self.geometry("1200x800")

        self.config_file = ""
        self.create_widgets()

    def create_widgets(self):
        # Alias
        ttk.Label(self, text="Alias").grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
        self.alias = ttk.Combobox(self, values=[
            "/T3STER/0/MS401/SLOT5/CH0",
            "/T3STER/0/MS401/SLOT5/CH1",
            "/T3STER/0/MS401/SLOT5/CH2",
            "/T3STER/0/MS401/SLOT5/CH3"
        ])
        self.alias.current(0)  # set default value
        self.alias.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=5)

        # UserAlias
        ttk.Label(self, text="UserAlias").grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
        self.user_alias = ttk.Entry(self)
        self.user_alias.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=5)

        # OutputMode
        ttk.Label(self, text="OutputMode (default)").grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)
        self.output_mode_default = ttk.Entry(self)
        self.output_mode_default.grid(column=1, row=2, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="OutputMode (locked)").grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)
        self.output_mode_locked_var = tk.BooleanVar(value=False)
        self.output_mode_locked = ttk.Checkbutton(self, variable=self.output_mode_locked_var)
        self.output_mode_locked.grid(column=3, row=2, sticky=tk.EW, padx=10, pady=5)

        # SetCurrent
        ttk.Label(self, text="SetCurrent (default)").grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)
        self.set_current_default = ttk.Entry(self)
        self.set_current_default.grid(column=1, row=3, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="SetCurrent (locked)").grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)
        self.set_current_locked_var = tk.BooleanVar(value=False)
        self.set_current_locked = ttk.Checkbutton(self, variable=self.set_current_locked_var)
        self.set_current_locked.grid(column=3, row=3, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="SetCurrent (min)").grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
        self.set_current_min = ttk.Entry(self)
        self.set_current_min.grid(column=1, row=4, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="SetCurrent (max)").grid(column=2, row=4, sticky=tk.W, padx=10, pady=5)
        self.set_current_max = ttk.Entry(self)
        self.set_current_max.grid(column=3, row=4, sticky=tk.EW, padx=10, pady=5)

        # VoltageCorner
        ttk.Label(self, text="VoltageCorner (default)").grid(column=0, row=5, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_default = ttk.Entry(self)
        self.voltage_corner_default.grid(column=1, row=5, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="VoltageCorner (locked)").grid(column=2, row=5, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_locked_var = tk.BooleanVar(value=False)
        self.voltage_corner_locked = ttk.Checkbutton(self, variable=self.voltage_corner_locked_var)
        self.voltage_corner_locked.grid(column=3, row=5, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="VoltageCorner (min)").grid(column=0, row=6, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_min = ttk.Entry(self)
        self.voltage_corner_min.grid(column=1, row=6, sticky=tk.EW, padx=10, pady=5)

        ttk.Label(self, text="VoltageCorner (max)").grid(column=2, row=6, sticky=tk.W, padx=10, pady=5)
        self.voltage_corner_max = ttk.Entry(self)
        self.voltage_corner_max.grid(column=3, row=6, sticky=tk.EW, padx=10, pady=5)

        # Buttons
        submit_btn = ttk.Button(self, text="Submit", command=self.submit)
        submit_btn.grid(column=0, row=7, padx=10, pady=20, columnspan=2)

        save_btn = ttk.Button(self, text="Save Config", command=self.save_config)
        save_btn.grid(column=2, row=7, padx=10, pady=20, columnspan=2)

        load_btn = ttk.Button(self, text="Load Config", command=self.load_config)
        load_btn.grid(column=4, row=7, padx=10, pady=20, columnspan=2)

    def save_config(self):
        config = {
            "Alias": self.alias.get(),
            "UserAlias": self.user_alias.get(),
            "OutputMode": {
                "default": self.output_mode_default.get(),
                "locked": self.output_mode_locked_var.get()
            },
            "SetCurrent": {
                "default": float(self.set_current_default.get()),
                "locked": self.set_current_locked_var.get(),
                "min": float(self.set_current_min.get()),
                "max": float(self.set_current_max.get())
            },
            "VoltageCorner": {
                "default": float(self.voltage_corner_default.get()),
                "locked": self.voltage_corner_locked_var.get(),
                "min": float(self.voltage_corner_min.get()),
                "max": float(self.voltage_corner_max.get())
            }
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            print("Configuration saved to", file_path)

    def load_config(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                config = json.load(f)
            self.apply_config(config)
            print("Configuration loaded from", file_path)

    def apply_config(self, config):
        self.alias.set(config.get("Alias", "/T3STER/0/MS401/SLOT5/CH0"))
        self.user_alias.delete(0, tk.END)
        self.user_alias.insert(0, config.get("UserAlias", ""))
        self.output_mode_default.delete(0, tk.END)
        self.output_mode_default.insert(0, config.get("OutputMode", {}).get("default", "ON"))
        self.output_mode_locked_var.set(config.get("OutputMode", {}).get("locked", False))
        self.set_current_default.delete(0, tk.END)
        self.set_current_default.insert(0, config.get("SetCurrent", {}).get("default", 0.01))
        self.set_current_locked_var.set(config.get("SetCurrent", {}).get("locked", False))
        self.set_current_min.delete(0, tk.END)
        self.set_current_min.insert(0, config.get("SetCurrent", {}).get("min", -0.2))
        self.set_current_max.delete(0, tk.END)
        self.set_current_max.insert(0, config.get("SetCurrent", {}).get("max", 0.2))
        self.voltage_corner_default.delete(0, tk.END)
        self.voltage_corner_default.insert(0, config.get("VoltageCorner", {}).get("default", 10))
        self.voltage_corner_locked_var.set(config.get("VoltageCorner", {}).get("locked", False))
        self.voltage_corner_min.delete(0, tk.END)
        self.voltage_corner_min.insert(0, config.get("VoltageCorner", {}).get("min", -40))
        self.voltage_corner_max.delete(0, tk.END)
        self.voltage_corner_max.insert(0, config.get("VoltageCorner", {}).get("max", 40))

    def submit(self):
        config = {
            "Alias": self.alias.get(),
            "UserAlias": self.user_alias.get(),
            "OutputMode": {
                "default": self.output_mode_default.get(),
                "locked": self.output_mode_locked_var.get()
            },
            "SetCurrent": {
                "default": float(self.set_current_default.get()),
                "locked": self.set_current_locked_var.get(),
                "min": float(self.set_current_min.get()),
                "max": float(self.set_current_max.get())
            },
            "VoltageCorner": {
                "default": float(self.voltage_corner_default.get()),
                "locked": self.voltage_corner_locked_var.get(),
                "min": float(self.voltage_corner_min.get()),
                "max": float(self.voltage_corner_max.get())
            }
        }

        print("Configuration Submitted:")
        print(json.dumps(config, indent=4))


if __name__ == "__main__":
    app = ParameterApp()
    app.mainloop()