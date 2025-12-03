import customtkinter as ctk
import tkinter as tk
import math
import numpy as np
from tkinter import messagebox

class ScientificCalculator:
    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("Scientific Calculator")
        self.window.geometry("500x650")
        self.window.resizable(False, False)
        
        # Initialize calculator state
        self.current_input = "0"
        self.operator = ""
        self.previous_value = 0
        self.new_input = True
        self.degree_mode = True  # True for degrees, False for radians
        self.memory = 0
        
        self.create_widgets()
        self.setup_keyboard_bindings()
    
    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Display
        self.display = ctk.CTkEntry(
            main_frame,
            font=ctk.CTkFont(size=28, weight="bold"),
            justify="right",
            height=70
        )
        self.display.pack(pady=10, padx=10, fill="x")
        self.display.insert(0, "0")
        
        # Mode indicator
        mode_frame = ctk.CTkFrame(main_frame, height=30)
        mode_frame.pack(fill="x", padx=10, pady=5)
        
        self.mode_label = ctk.CTkLabel(
            mode_frame, 
            text="DEG", 
            font=ctk.CTkFont(size=12),
            text_color="lightblue"
        )
        self.mode_label.pack(side="left")
        
        self.memory_label = ctk.CTkLabel(
            mode_frame, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color="yellow"
        )
        self.memory_label.pack(side="right")
        
        # Tab view for different function groups
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tabview.add("Basic")
        self.tabview.add("Scientific")
        self.tabview.add("Constants")
        self.tabview.add("Statistics")
        
        self.create_basic_tab()
        self.create_scientific_tab()
        self.create_constants_tab()
        self.create_statistics_tab()
    
    def create_basic_tab(self):
        tab = self.tabview.tab("Basic")
        
        buttons = [
            ['MC', 'MR', 'M+', 'M-', 'MS', 'C'],
            ['±', '%', '√', 'x²', '1/x', 'CE'],
            ['7', '8', '9', '/', 'sin', 'cos'],
            ['4', '5', '6', '*', 'tan', 'log'],
            ['1', '2', '3', '-', 'ln', 'exp'],
            ['0', '.', '=', '+', 'π', 'e']
        ]
        
        self.create_button_grid(tab, buttons)
    
    def create_scientific_tab(self):
        tab = self.tabview.tab("Scientific")
        
        buttons = [
            ['(', ')', 'x^y', 'x!', '10^x', 'e^x'],
            ['sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'sinh', 'cosh', 'tanh'],
            ['asin', 'acos', 'atan', 'asinh', 'acosh', 'atanh'],
            ['mod', 'abs', 'floor', 'ceil', 'round', 'rand'],
            ['DEG/RAD', 'hypot', 'gcd', 'lcm', 'nCr', 'nPr'],
            ['←', 'C', '=', 'π', 'e', 'φ']
        ]
        
        self.create_button_grid(tab, buttons)
    
    def create_constants_tab(self):
        tab = self.tabview.tab("Constants")
        
        buttons = [
            ['π', 'e', 'φ', 'c', 'G', 'h'],
            ['ε0', 'μ0', 'NA', 'k', 'σ', 'R'],
            ['me', 'mp', 'mn', 'α', 'μB', 'μN'],
            ['F', 'KJ', 'RK', 'g', 'atm', 'ly'],
            ['au', 'pc', 'M☉', 'R☉', 'L☉', 'T☉'],
            ['←', 'C', '=', '(', ')', '+']
        ]
        
        self.create_button_grid(tab, buttons)
    
    def create_statistics_tab(self):
        tab = self.tabview.tab("Statistics")
        
        buttons = [
            ['mean', 'median', 'mode', 'std', 'var', 'sum'],
            ['min', 'max', 'range', 'corr', 'reg', 'prob'],
            ['7', '8', '9', 'add', 'clear', 'C'],
            ['4', '5', '6', '(', ')', '='],
            ['1', '2', '3', 'data', 'stats', 'view'],
            ['0', '.', 'del', '+', '-', '*']
        ]
        
        self.create_button_grid(tab, buttons)
        self.data_set = []
    
    def create_button_grid(self, parent, buttons):
        # Configure grid
        for i in range(6):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(6):
            parent.grid_columnconfigure(i, weight=1)
        
        # Create buttons
        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                if not text:
                    continue
                
                # Determine button color
                if text in ['=', 'C', 'CE', '←']:
                    fg_color = ("#FF6B6B", "#FF6B6B")
                elif text in ['+', '-', '*', '/', 'x^y', 'mod']:
                    fg_color = ("#4ECDC4", "#4ECDC4")
                elif text in ['sin', 'cos', 'tan', 'log', 'ln', 'exp']:
                    fg_color = ("#45B7D1", "#45B7D1")
                else:
                    fg_color = None
                
                btn = ctk.CTkButton(
                    parent,
                    text=text,
                    font=ctk.CTkFont(size=14),
                    command=lambda t=text: self.button_click(t),
                    height=40,
                    fg_color=fg_color
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    def setup_keyboard_bindings(self):
        self.window.bind('<Key>', self.key_press)
        self.display.focus_set()
    
    def button_click(self, value):
        # Handle different types of operations
        if value.isdigit() or value == '.':
            self.input_number(value)
        elif value in ['+', '-', '*', '/', 'mod', 'x^y']:
            self.input_operator(value)
        elif value == '=':
            self.calculate()
        elif value in ['C', 'CE']:
            self.clear(value)
        elif value == '←':
            self.backspace()
        elif value == 'DEG/RAD':
            self.toggle_angle_mode()
        elif value in ['MC', 'MR', 'M+', 'M-', 'MS']:
            self.memory_operation(value)
        else:
            self.scientific_function(value)
    
    def input_number(self, value):
        if self.new_input or self.current_input == "0":
            self.current_input = value if value != '.' else "0."
            self.new_input = False
        else:
            if value == '.' and '.' in self.current_input:
                return
            self.current_input += value
        self.update_display()
    
    def input_operator(self, op):
        if self.operator and not self.new_input:
            self.calculate()
        self.operator = op
        self.previous_value = self.get_current_value()
        self.new_input = True
    
    def scientific_function(self, func):
        try:
            value = self.get_current_value()
            result = 0
            
            # Trigonometric functions
            if func == 'sin':
                result = math.sin(math.radians(value) if self.degree_mode else value)
            elif func == 'cos':
                result = math.cos(math.radians(value) if self.degree_mode else value)
            elif func == 'tan':
                result = math.tan(math.radians(value) if self.degree_mode else value)
            elif func == 'sin⁻¹' or func == 'asin':
                result = math.degrees(math.asin(value)) if self.degree_mode else math.asin(value)
            elif func == 'cos⁻¹' or func == 'acos':
                result = math.degrees(math.acos(value)) if self.degree_mode else math.acos(value)
            elif func == 'tan⁻¹' or func == 'atan':
                result = math.degrees(math.atan(value)) if self.degree_mode else math.atan(value)
            
            # Hyperbolic functions
            elif func == 'sinh':
                result = math.sinh(value)
            elif func == 'cosh':
                result = math.cosh(value)
            elif func == 'tanh':
                result = math.tanh(value)
            elif func == 'asinh':
                result = math.asinh(value)
            elif func == 'acosh':
                result = math.acosh(value)
            elif func == 'atanh':
                result = math.atanh(value)
            
            # Logarithmic functions
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'exp':
                result = math.exp(value)
            elif func == '10^x':
                result = 10 ** value
            elif func == 'e^x':
                result = math.exp(value)
            
            # Power functions
            elif func == 'x²':
                result = value ** 2
            elif func == '√':
                result = math.sqrt(value)
            elif func == '1/x':
                result = 1 / value if value != 0 else float('inf')
            elif func == 'x!':
                result = math.factorial(int(value)) if value >= 0 and value == int(value) else math.gamma(value + 1)
            
            # Mathematical functions
            elif func == 'abs':
                result = abs(value)
            elif func == 'floor':
                result = math.floor(value)
            elif func == 'ceil':
                result = math.ceil(value)
            elif func == 'round':
                result = round(value)
            elif func == 'hypot':
                result = math.hypot(self.previous_value, value)
            
            # Constants
            elif func == 'π':
                result = math.pi
            elif func == 'e':
                result = math.e
            elif func == 'φ':
                result = (1 + math.sqrt(5)) / 2  # Golden ratio
            
            # Statistical functions (for data set)
            elif func == 'mean' and self.data_set:
                result = np.mean(self.data_set)
            elif func == 'median' and self.data_set:
                result = np.median(self.data_set)
            elif func == 'std' and self.data_set:
                result = np.std(self.data_set)
            elif func == 'var' and self.data_set:
                result = np.var(self.data_set)
            elif func == 'sum' and self.data_set:
                result = np.sum(self.data_set)
            elif func == 'add':
                self.data_set.append(value)
                self.current_input = f"Added {value}"
                self.new_input = True
                self.update_display()
                return
            
            else:
                # Handle other functions
                result = self.handle_special_functions(func, value)
            
            self.current_input = self.format_result(result)
            self.new_input = True
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error in {func}: {str(e)}")
    
    def handle_special_functions(self, func, value):
        """Handle more complex scientific functions"""
        if func == 'nCr':  # Combination
            n = self.previous_value
            r = value
            return math.comb(int(n), int(r))
        elif func == 'nPr':  # Permutation
            n = self.previous_value
            r = value
            return math.perm(int(n), int(r))
        elif func == 'gcd':
            return math.gcd(int(self.previous_value), int(value))
        elif func == 'lcm':
            return math.lcm(int(self.previous_value), int(value))
        elif func == 'rand':
            return np.random.random()
        else:
            return value
    
    def calculate(self):
        if self.operator:
            try:
                current_value = self.get_current_value()
                
                if self.operator == '+':
                    result = self.previous_value + current_value
                elif self.operator == '-':
                    result = self.previous_value - current_value
                elif self.operator == '*':
                    result = self.previous_value * current_value
                elif self.operator == '/':
                    if current_value == 0:
                        raise ValueError("Division by zero")
                    result = self.previous_value / current_value
                elif self.operator == 'mod':
                    result = self.previous_value % current_value
                elif self.operator == 'x^y':
                    result = self.previous_value ** current_value
                
                self.current_input = self.format_result(result)
                self.operator = ""
                self.new_input = True
                self.update_display()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.clear('C')
    
    def clear(self, clear_type='C'):
        if clear_type == 'CE':
            self.current_input = "0"
        else:  # 'C'
            self.current_input = "0"
            self.operator = ""
            self.previous_value = 0
        self.new_input = True
        self.update_display()
    
    def backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()
    
    def toggle_angle_mode(self):
        self.degree_mode = not self.degree_mode
        self.mode_label.configure(text="DEG" if self.degree_mode else "RAD")
    
    def memory_operation(self, op):
        current_value = self.get_current_value()
        
        if op == 'MC':  # Memory Clear
            self.memory = 0
            self.memory_label.configure(text="")
        elif op == 'MR':  # Memory Recall
            self.current_input = str(self.memory)
            self.new_input = True
            self.update_display()
        elif op == 'M+':  # Memory Add
            self.memory += current_value
        elif op == 'M-':  # Memory Subtract
            self.memory -= current_value
        elif op == 'MS':  # Memory Store
            self.memory = current_value
        
        if self.memory != 0:
            self.memory_label.configure(text="M")
    
    def get_current_value(self):
        try:
            return float(self.current_input)
        except ValueError:
            return 0
    
    def format_result(self, result):
        if result == float('inf') or result == float('-inf'):
            return "Infinity"
        elif math.isnan(result):
            return "Error"
        
        # Format number for display
        if abs(result) > 1e10 or (abs(result) < 1e-5 and result != 0):
            return f"{result:.6e}"
        elif result == int(result):
            return str(int(result))
        else:
            return f"{result:.10g}".rstrip('0').rstrip('.')
    
    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
    
    def key_press(self, event):
        key = event.char
        if key.isdigit() or key == '.':
            self.input_number(key)
        elif key in ['+', '-', '*', '/']:
            self.input_operator(key)
        elif key == '\r' or key == '=':
            self.calculate()
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key == '\x1b':  # Escape
            self.clear('C')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = ScientificCalculator()
    calculator.run()