from cs50 import SQL
import csv

db = SQL("sqlite:///calorievision.db")

with open("nutrition_scrappe.csv", "r") as food_data:
    csv_reader = csv.reader(food_data)

    next(csv_reader)

    for row in csv_reader:
        print(row)
        db.execute("INSERT INTO foods(name, restaurant, min_val, max_val, mean_val) VALUES(:name, :restaurant, "
                   ":min_val, :max_val, :mean_val",
                   name=str(row[1]), restaurant=row[2], min_val=row[3], max_val=row[4], mean_val=row[5])
