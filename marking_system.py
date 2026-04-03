# School Marking System
import json

def calculate_grade(marks):
    if marks >= 90: return "A+"
    elif marks >= 80: return "A"
    elif marks >= 70: return "B"
    elif marks >= 60: return "C"
    elif marks >= 33: return "Pass"
    else: return "Fail"

def main():
    print("--- School Marking System ---")
    students = []
    
    while True:
        name = input("\nStudent ka naam likho (ya 'exit' likho band karne ke liye): ")
        if name.lower() == 'exit':
            break
            
        try:
            marks = float(input(f"{name} ke marks dalo (0-100): "))
            if 0 <= marks <= 100:
                grade = calculate_grade(marks)
                students.append({"name": name, "marks": marks, "grade": grade})
                print(f"Result: {grade}")
            else:
                print("Error: Marks 0 se 100 ke beech hone chahiye!")
        except ValueError:
            print("Error: Sirf numbers dalo!")

    # Final Result Table
    print("\n--- Final Marksheet ---")
    print("Name\t\tMarks\tGrade")
    for s in students:
        print(f"{s['name']}\t\t{s['marks']}\t{s['grade']}")

if __name__ == "__main__":
    main()