"""
Legacy NumPy Sales Analysis Script
===================================
This file preserves the original foundational proof-of-concept script
demonstrating basic NumPy array operations, statistics, and initial Matplotlib plots.
"""

import numpy as np
import matplotlib.pyplot as plt

# Sales Data (5 Employees x 3 Months: Jan, Feb, Mar)
sales = np.array([
    [1200, 1500, 1800],
    [2000, 2200, 2500],
    [1700, 1900, 2100],
    [2500, 2600, 2800],
    [3000, 3200, 3500]
])

print("Sales Data")
print(sales)

# Shape
print("\nShape :", sales.shape)

# Size
print("Size :", sales.size)

# Dimensions
print("Dimensions :", sales.ndim)

# Data Type
print("Data Type :", sales.dtype)


# Total Sales
print("\nTotal Sales :", np.sum(sales))

# Average Sales
print("Average Sales :", np.mean(sales))

# Maximum Sales
print("Maximum Sales :", np.max(sales))

# Minimum Sales
print("Minimum Sales :", np.min(sales))

# Median Sales
print("Median Sales :", np.median(sales))

# Standard Deviation
print("Standard Deviation :", np.std(sales))


# ---------------- Employee Wise Total Sales ---------------- #

print("\n========== Employee Wise Total Sales ==========")
employee_sales = np.sum(sales, axis=1)
print(employee_sales)

# ---------------- Month Wise Total Sales ---------------- #

print("\n========== Month Wise Total Sales ==========")
month_sales = np.sum(sales, axis=0)
print(month_sales)

# ---------------- Best Employee ---------------- #

best_employee = np.argmax(employee_sales)

print("\nBest Employee : Employee", best_employee + 1)
print("Sales :", employee_sales[best_employee])

# ---------------- Best Month ---------------- #

months = ["January", "February", "March"]

best_month = np.argmax(month_sales)

print("\nBest Month :", months[best_month])
print("Sales :", month_sales[best_month])


# ---------------- RESHAPE ---------------- #

print("\n========== Reshape ==========")

reshape_array = sales.reshape(3, 5)

print(reshape_array)

# ---------------- FLATTEN ---------------- #

print("\n========== Flatten ==========")

flat = sales.flatten()

print(flat)

# ---------------- SLICING ---------------- #

print("\n========== First Two Employees ==========")

print(sales[:2])

print("\n========== January Sales ==========")

print(sales[:, 0])

# ---------------- INDEXING ---------------- #

print("\n========== Employee 3 March Sales ==========")

print(sales[2, 2])


# Employee Names
employees = [
    "Emp 1",
    "Emp 2",
    "Emp 3",
    "Emp 4",
    "Emp 5"
]

# Employee Total Sales
employee_sales = np.sum(sales, axis=1)

# Bar Chart
plt.figure(figsize=(8, 5))
plt.bar(employees, employee_sales)
plt.title("Employee Wise Total Sales")
plt.xlabel("Employees")
plt.ylabel("Total Sales")
plt.grid()
plt.show()


months = [
    "January",
    "February",
    "March"
]

month_sales = np.sum(sales, axis=0)

plt.figure(figsize=(8, 5))
plt.plot(months, month_sales, marker="o")
plt.title("Month Wise Sales")
plt.xlabel("Months")
plt.ylabel("Sales")
plt.grid()
plt.show()
