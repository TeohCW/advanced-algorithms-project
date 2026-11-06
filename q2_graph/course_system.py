class Course:
    """Represents a university course."""

    def __init__(self, course_code, course_name, credit_hours, level):
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must not be empty.")

        if not isinstance(course_name, str) or not course_name.strip():
            raise ValueError("Course name must not be empty.")

        if type(credit_hours) is not int or credit_hours <= 0:
            raise ValueError("Credit hours must be a positive integer.")

        if not isinstance(level, str):
            raise ValueError("Level must be core or elective.")

        level = level.strip().lower()

        if level not in ("core", "elective"):
            raise ValueError("Level must be core or elective.")

        self.course_code = course_code.strip().upper()
        self.course_name = course_name.strip()
        self.credit_hours = credit_hours
        self.level = level

    def __str__(self):
        """Return the full course details."""
        return (
            f"Course code: {self.course_code}\n"
            f"Course name: {self.course_name}\n"
            f"Credit hours: {self.credit_hours}\n"
            f"Level: {self.level.title()}"
        )


def main():
    course = Course(
        "cs101",
        "Introduction to Programming",
        3,
        "Core"
    )

    print("--- COURSE DETAILS ---")
    print(course)


if __name__ == "__main__":
    main()