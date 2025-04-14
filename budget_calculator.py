import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class BudgetCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Budget Calculator")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=('Arial', 10))
        self.style.configure("Header.TLabel", font=('Arial', 14, 'bold'))
        self.style.configure("Subheader.TLabel", font=('Arial', 12))
        self.style.configure("TEntry", padding=5)
        
        # Initialize data storage
        self.income_sources = []
        self.expense_categories = []
        self.savings_goals = []
        self.monthly_data = {}
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.income_tab = ttk.Frame(self.notebook)
        self.expenses_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        self.savings_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.income_tab, text="Income")
        self.notebook.add(self.expenses_tab, text="Expenses")
        self.notebook.add(self.analysis_tab, text="Analysis")
        self.notebook.add(self.savings_tab, text="Savings")
        
        # Initialize tabs
        self.setup_income_tab()
        self.setup_expenses_tab()
        self.setup_analysis_tab()
        self.setup_savings_tab()
        
        # Load existing data if available
        self.load_data()
    
    def setup_income_tab(self):
        # Income sources frame
        income_frame = ttk.LabelFrame(self.income_tab, text="Income Sources", padding="10")
        income_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add income source
        add_income_frame = ttk.Frame(income_frame)
        add_income_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_income_frame, text="Source:").pack(side=tk.LEFT, padx=5)
        self.income_source_entry = ttk.Entry(add_income_frame, width=20)
        self.income_source_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_income_frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.income_amount_entry = ttk.Entry(add_income_frame, width=10)
        self.income_amount_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_income_frame, text="Add Income", 
                  command=self.add_income_source).pack(side=tk.LEFT, padx=5)
        
        # Income sources list
        self.income_tree = ttk.Treeview(income_frame, columns=("Source", "Amount"), 
                                      show="headings", height=5)
        self.income_tree.heading("Source", text="Source")
        self.income_tree.heading("Amount", text="Amount")
        self.income_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Monthly total
        self.monthly_total_label = ttk.Label(income_frame, text="Monthly Total: $0.00",
                                           style="Header.TLabel")
        self.monthly_total_label.pack(pady=5)
    
    def setup_expenses_tab(self):
        # Expenses frame
        expenses_frame = ttk.LabelFrame(self.expenses_tab, text="Expense Categories", 
                                      padding="10")
        expenses_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add expense category
        add_expense_frame = ttk.Frame(expenses_frame)
        add_expense_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_expense_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.expense_category_entry = ttk.Entry(add_expense_frame, width=20)
        self.expense_category_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_expense_frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.expense_amount_entry = ttk.Entry(add_expense_frame, width=10)
        self.expense_amount_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_expense_frame, text="Add Expense", 
                  command=self.add_expense_category).pack(side=tk.LEFT, padx=5)
        
        # Expense categories list
        self.expense_tree = ttk.Treeview(expenses_frame, columns=("Category", "Amount"), 
                                       show="headings", height=5)
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Monthly expenses total
        self.expenses_total_label = ttk.Label(expenses_frame, 
                                            text="Monthly Expenses Total: $0.00",
                                            style="Header.TLabel")
        self.expenses_total_label.pack(pady=5)
    
    def setup_analysis_tab(self):
        # Analysis frame
        analysis_frame = ttk.Frame(self.analysis_tab, padding="10")
        analysis_frame.pack(fill=tk.BOTH, expand=True)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(analysis_frame, text="Budget Summary", padding="10")
        summary_frame.pack(fill=tk.X, pady=5)
        
        # Summary labels
        self.net_income_label = ttk.Label(summary_frame, text="Net Monthly Income: $0.00",
                                        style="Subheader.TLabel")
        self.net_income_label.pack(pady=2)
        
        self.savings_potential_label = ttk.Label(summary_frame, 
                                               text="Potential Monthly Savings: $0.00",
                                               style="Subheader.TLabel")
        self.savings_potential_label.pack(pady=2)
        
        # Recommendations frame
        recommendations_frame = ttk.LabelFrame(analysis_frame, text="Recommendations", 
                                            padding="10")
        recommendations_frame.pack(fill=tk.X, pady=5)
        
        self.recommendations_text = tk.Text(recommendations_frame, height=5, wrap=tk.WORD)
        self.recommendations_text.pack(fill=tk.X, pady=5)
        
        # Chart frame
        chart_frame = ttk.LabelFrame(analysis_frame, text="Expense Distribution", 
                                   padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.figure = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Update analysis button
        ttk.Button(analysis_frame, text="Update Analysis", 
                  command=self.update_analysis).pack(pady=5)
    
    def setup_savings_tab(self):
        # Savings goals frame
        savings_frame = ttk.LabelFrame(self.savings_tab, text="Savings Goals", 
                                     padding="10")
        savings_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add savings goal
        add_savings_frame = ttk.Frame(savings_frame)
        add_savings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_savings_frame, text="Goal:").pack(side=tk.LEFT, padx=5)
        self.savings_goal_entry = ttk.Entry(add_savings_frame, width=20)
        self.savings_goal_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_savings_frame, text="Target Amount:").pack(side=tk.LEFT, padx=5)
        self.savings_target_entry = ttk.Entry(add_savings_frame, width=10)
        self.savings_target_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_savings_frame, text="Monthly Contribution:").pack(side=tk.LEFT, 
                                                                     padx=5)
        self.savings_contribution_entry = ttk.Entry(add_savings_frame, width=10)
        self.savings_contribution_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_savings_frame, text="Add Goal", 
                  command=self.add_savings_goal).pack(side=tk.LEFT, padx=5)
        
        # Savings goals list
        self.savings_tree = ttk.Treeview(savings_frame, 
                                       columns=("Goal", "Target", "Monthly", "Progress"),
                                       show="headings", height=5)
        self.savings_tree.heading("Goal", text="Goal")
        self.savings_tree.heading("Target", text="Target Amount")
        self.savings_tree.heading("Monthly", text="Monthly Contribution")
        self.savings_tree.heading("Progress", text="Progress")
        self.savings_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Total savings
        self.total_savings_label = ttk.Label(savings_frame, 
                                           text="Total Monthly Savings: $0.00",
                                           style="Header.TLabel")
        self.total_savings_label.pack(pady=5)
    
    def add_income_source(self):
        source = self.income_source_entry.get().strip()
        amount = self.income_amount_entry.get().strip()
        
        if not source or not amount:
            messagebox.showerror("Error", "Please enter both source and amount")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return
        
        self.income_sources.append({"source": source, "amount": amount})
        self.income_tree.insert("", "end", values=(source, f"${amount:,.2f}"))
        self.update_totals()
        
        # Clear entries
        self.income_source_entry.delete(0, tk.END)
        self.income_amount_entry.delete(0, tk.END)
    
    def add_expense_category(self):
        category = self.expense_category_entry.get().strip()
        amount = self.expense_amount_entry.get().strip()
        
        if not category or not amount:
            messagebox.showerror("Error", "Please enter both category and amount")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return
        
        self.expense_categories.append({"category": category, "amount": amount})
        self.expense_tree.insert("", "end", values=(category, f"${amount:,.2f}"))
        self.update_totals()
        
        # Clear entries
        self.expense_category_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
    
    def add_savings_goal(self):
        goal = self.savings_goal_entry.get().strip()
        target = self.savings_target_entry.get().strip()
        contribution = self.savings_contribution_entry.get().strip()
        
        if not goal or not target or not contribution:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            target = float(target)
            contribution = float(contribution)
            if target <= 0 or contribution <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive amounts")
            return
        
        self.savings_goals.append({
            "goal": goal,
            "target": target,
            "monthly": contribution,
            "progress": 0
        })
        
        self.savings_tree.insert("", "end", values=(
            goal,
            f"${target:,.2f}",
            f"${contribution:,.2f}",
            "0%"
        ))
        
        self.update_totals()
        
        # Clear entries
        self.savings_goal_entry.delete(0, tk.END)
        self.savings_target_entry.delete(0, tk.END)
        self.savings_contribution_entry.delete(0, tk.END)
    
    def update_totals(self):
        # Calculate income total
        income_total = sum(item["amount"] for item in self.income_sources)
        self.monthly_total_label.config(text=f"Monthly Total: ${income_total:,.2f}")
        
        # Calculate expenses total
        expenses_total = sum(item["amount"] for item in self.expense_categories)
        self.expenses_total_label.config(text=f"Monthly Expenses Total: ${expenses_total:,.2f}")
        
        # Calculate savings total
        savings_total = sum(item["monthly"] for item in self.savings_goals)
        self.total_savings_label.config(text=f"Total Monthly Savings: ${savings_total:,.2f}")
        
        # Update analysis
        self.update_analysis()
    
    def update_analysis(self):
        # Calculate net income
        income_total = sum(item["amount"] for item in self.income_sources)
        expenses_total = sum(item["amount"] for item in self.expense_categories)
        savings_total = sum(item["monthly"] for item in self.savings_goals)
        
        net_income = income_total - expenses_total - savings_total
        self.net_income_label.config(text=f"Net Monthly Income: ${net_income:,.2f}")
        
        # Calculate savings potential
        savings_potential = net_income
        self.savings_potential_label.config(
            text=f"Potential Monthly Savings: ${savings_potential:,.2f}"
        )
        
        # Generate recommendations
        recommendations = []
        
        if net_income < 0:
            recommendations.append("⚠️ Warning: Your expenses exceed your income!")
            recommendations.append("Consider reducing expenses or increasing income.")
        
        if expenses_total > income_total * 0.5:
            recommendations.append("Your expenses are high relative to your income.")
            recommendations.append("Consider reviewing and reducing non-essential expenses.")
        
        if savings_total < income_total * 0.2:
            recommendations.append("Your savings rate is below the recommended 20%.")
            recommendations.append("Consider increasing your monthly savings contributions.")
        
        if not recommendations:
            recommendations.append("Your budget looks healthy!")
            recommendations.append("Keep up the good financial habits.")
        
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, "\n".join(recommendations))
        
        # Update chart
        self.update_chart()
    
    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not self.expense_categories:
            ax.text(0.5, 0.5, "No expense data available", 
                   ha='center', va='center')
        else:
            categories = [item["category"] for item in self.expense_categories]
            amounts = [item["amount"] for item in self.expense_categories]
            
            # Create pie chart
            ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                  startangle=90)
            ax.axis('equal')
            ax.set_title('Expense Distribution')
        
        self.canvas.draw()
    
    def save_data(self):
        data = {
            "income_sources": self.income_sources,
            "expense_categories": self.expense_categories,
            "savings_goals": self.savings_goals,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("budget_data.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        try:
            if os.path.exists("budget_data.json"):
                with open("budget_data.json", "r") as f:
                    data = json.load(f)
                    
                    self.income_sources = data.get("income_sources", [])
                    self.expense_categories = data.get("expense_categories", [])
                    self.savings_goals = data.get("savings_goals", [])
                    
                    # Populate income tree
                    for item in self.income_sources:
                        self.income_tree.insert("", "end", 
                                             values=(item["source"], 
                                                   f"${item['amount']:,.2f}"))
                    
                    # Populate expense tree
                    for item in self.expense_categories:
                        self.expense_tree.insert("", "end", 
                                              values=(item["category"], 
                                                    f"${item['amount']:,.2f}"))
                    
                    # Populate savings tree
                    for item in self.savings_goals:
                        progress = (item["progress"] / item["target"]) * 100
                        self.savings_tree.insert("", "end", 
                                              values=(item["goal"],
                                                    f"${item['target']:,.2f}",
                                                    f"${item['monthly']:,.2f}",
                                                    f"{progress:.1f}%"))
                    
                    self.update_totals()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetCalculator(root)
    
    # Save data when closing
    def on_closing():
        app.save_data()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop() 