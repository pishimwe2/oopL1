import sys

class Task:
    def __init__(self, title, category, grade, proportion):
        self.title = title
        self.category = category  # "FA" for Formative or "SA" for Summative
        self.grade = grade
        self.proportion = proportion

    def below_threshold(self, min_score=50):
        return self.grade < min_score


class Learner:
    def __init__(self):
        self.tasks = []

    def record_task(self, title, category, grade, proportion):
        self.tasks.append(Task(title, category, grade, proportion))

    def collect_tasks(self):
        print("Input task information. Type 'done' to complete.")
        while True:
            title = input("Task Title (or 'done' to stop): ")
            if title.lower() == "done":
                break

            category = input("Category (FA for Formative, SA for Summative): ").upper()
            while category not in ["FA", "SA"]:
                category = input("Invalid category. Use FA or SA: ").upper()

            grade = float(input("Grade (0-100): "))
            while grade < 0 or grade > 100:
                grade = float(input("Invalid grade. Enter a value between 0 and 100: "))

            proportion = float(input("Proportion (%) FA=60 max, SA=40 max: "))
            while (category == "FA" and proportion > 60) or (category == "SA" and proportion > 40) or proportion < 0:
                proportion = float(input("Invalid proportion. Enter a valid percentage: "))

            self.record_task(title, category, grade, proportion)

    def compute_totals(self):
        totals = {"FA": 0, "SA": 0}
        proportions = {"FA": 0, "SA": 0}

        for task in self.tasks:
            totals[task.category] += task.grade * task.proportion / 100
            proportions[task.category] += task.proportion

        if proportions["FA"] > 60 or proportions["SA"] > 40:
            raise ValueError("Proportions exceed allowed limits: 60% for formative, 40% for summative")

        return totals["FA"], totals["SA"]

    def evaluate_progress(self):
        formative_score, summative_score = self.compute_totals()
        return "Passed" if formative_score >= 30 and summative_score >= 20 else "Failed"

    def find_resubmissions(self):
        candidates = [task for task in self.tasks if task.category == "FA" and task.below_threshold()]
        if not candidates:
            return []
        min_score = min(task.grade for task in candidates)
        return [task for task in candidates if task.grade == min_score]

    def display_transcript(self, sort_order="asc"):
        ordered_tasks = sorted(
            self.tasks,
            key=lambda task: task.grade,
            reverse=(sort_order == "des")
        )

        print(f"\nTranscript Summary ({sort_order.capitalize()} Order):")
        print(f"{'Task':<18} {'Category':<15} {'Grade (%)':<12} {'Proportion (%)':<12}")
        print("-" * 50)
        for task in ordered_tasks:
            print(f"{task.title:<18} {task.category:<15} {task.grade:<12} {task.proportion:<12}")
        print("-" * 50)


def reset_program():
    while True:
        restart = input("\nRestart the program? (yes/no): ").strip().lower()
        if restart == "yes":
            main()
        elif restart == "no":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.")


def main():
    learner = Learner()
    learner.collect_tasks()

    try:
        formative_score, summative_score = learner.compute_totals()
        print(f"\nFormative Total: {formative_score}%, Summative Total: {summative_score}%")
        print("Overall Status:", learner.evaluate_progress())

        resubmission_tasks = learner.find_resubmissions()
        if resubmission_tasks:
            print("\nEligible for resubmission:")
            for task in resubmission_tasks:
                print(f"{task.title} with grade {task.grade}%")
        else:
            print("\nNo tasks eligible for resubmission.")

        sort_order = input("\nEnter transcript order ('asc' for ascending, 'des' for descending): ").lower()
        while sort_order not in ["asc", "des"]:
            sort_order = input("Invalid order. Enter 'asc' or 'des': ").lower()
        learner.display_transcript(sort_order=sort_order)

    except ValueError as error:
        print(f"\nError: {error}")

    reset_program()


if __name__ == "__main__":
    main()
