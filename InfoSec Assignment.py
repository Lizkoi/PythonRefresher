# Days in Seconds
def days_to_seconds(days):
    return days * 24 * 60 * 60

days = int(input("Enter the number of days: "))
sec = days_to_seconds(days)
print(f"The number of seconds in {days} day(s) is {sec} seconds.")


# Volume of a Sphere
def sphere_volume(radius):
    return (4 / 3) * 3.14 * (radius ** 3)

radius = float(input("Enter the radius of the sphere: "))
vol = sphere_volume(radius)
print(f"The volume of the sphere with radius {radius} is {vol:.4f}.")


# Area and Perimeter of a Square
def square_area(side):
    return side ** 2

def square_perimeter(side):
    return side * 4

side = float(input("Enter the side length of the square: "))
area = square_area(side)
perimeter = square_perimeter(side)
print(f"The area of the square with side length {side} is {area:.2f}.")
print(f"The perimeter of the square with side length {side} is {perimeter:.2f}.")


# Character Case Check
def check_case(char):
    if len(char) != 1:
        print("Please enter only a single character.")
        return
    if char.isupper():
        print("The character is uppercase.")
    elif char.islower():
        print("The character is lowercase.")
    else:
        print("The character is neither uppercase nor lowercase (possibly a number or symbol).")

user_char = input("Enter a character: ").strip()
check_case(user_char)


# Pseudocode Implementation
def update_X_until_Y(X, Y, add_value, sub_value, min_Y):
    while True:
        X += (add_value / Y)
        Y -= sub_value
        if Y <= min_Y:
            print(f"The value of X when Y reaches {min_Y} or below is {X:.2f}")
            break

X = float(input("Set the initial value of X: "))
Y = float(input("Set the initial value of Y: "))
add_value = float(input("Set the value to be added to X: "))
sub_value = float(input("Set the value to be subtracted from Y: "))
min_Y = float(input("Set the minimum Y value to stop at: "))
update_X_until_Y(X, Y, add_value, sub_value, min_Y)


# Average of User-Input Values
def calculate_average(values):
    return sum(values) / len(values) bn 

values = []
print("Enter 5 numeric values:")
while len(values) < 5:
    try:
        num = float(input(f"Enter number {len(values) + 1}: "))
        values.append(num)
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

print("You have entered the following numbers:")
print(values)
average = calculate_average(values)
print(f"The average of the values is {average:.2f}.")