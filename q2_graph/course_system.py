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


class DirectedGraph:
    """A reusable unweighted directed graph."""

    def __init__(self):
        self.adjacency_list = {}

    def addVertex(self, vertex):
        """Add a vertex with no outgoing edges."""
        if vertex in self.adjacency_list:
            raise ValueError("Vertex already exists.")

        self.adjacency_list[vertex] = []

    def addEdge(self, source, destination):
        """Add a directed edge from source to destination."""
        if source not in self.adjacency_list:
            raise ValueError("Source vertex does not exist.")

        if destination not in self.adjacency_list:
            raise ValueError("Destination vertex does not exist.")

        if destination in self.adjacency_list[source]:
            raise ValueError("Edge already exists.")

        self.adjacency_list[source].append(destination)

    def listIncomingAdjacentVertex(self, vertex):
        """Return all vertices with an edge pointing to this vertex."""
        if vertex not in self.adjacency_list:
            raise ValueError("Vertex does not exist.")

        incoming = []

        for source, neighbours in self.adjacency_list.items():
            if vertex in neighbours:
                incoming.append(source)

        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        """Return all vertices this vertex points to."""
        if vertex not in self.adjacency_list:
            raise ValueError("Vertex does not exist.")

        return self.adjacency_list[vertex].copy()


def display_course_list(course_catalogue):
    """Display the codes and names of all courses."""
    print("\n--- ALL COURSES ---")

    if not course_catalogue:
        print("No courses available.")
        return

    for course in course_catalogue.values():
        print(f"{course.course_code}: {course.course_name}")


def select_course(course_catalogue):
    """Read a course code and return its object, or None if absent."""
    code = input("Enter course code: ").strip().upper()

    course = course_catalogue.get(code)

    if course is None:
        print(f"Course '{code}' was not found.")

    return course


def display_course_details(course_catalogue):
    """Display full details regardless of core/elective status."""
    print("\n--- COURSE DETAILS ---")
    course = select_course(course_catalogue)

    if course is not None:
        print(course)


def display_prerequisites(course_catalogue, graph):
    """Display the selected course's direct prerequisites."""
    print("\n--- DIRECT PREREQUISITES ---")
    course = select_course(course_catalogue)

    if course is None:
        return

    incoming = graph.listIncomingAdjacentVertex(course.course_code)

    print(f"\nPrerequisites for {course.course_name}:")

    if not incoming:
        print("This course has no direct prerequisites.")
        return

    for code in incoming:
        prerequisite = course_catalogue[code]
        print(f"{code}: {prerequisite.course_name}")


def display_unlocked_courses(course_catalogue, graph):
    """Display courses for which the selected course is a prerequisite."""
    print("\n--- COURSES THIS COURSE UNLOCKS ---")
    course = select_course(course_catalogue)

    if course is None:
        return

    outgoing = graph.listOutgoingAdjacentVertex(course.course_code)

    print(f"\nCourses requiring {course.course_name}:")

    if not outgoing:
        print("This course is not a direct prerequisite for any course.")
        return

    for code in outgoing:
        dependent = course_catalogue[code]
        print(f"{code}: {dependent.course_name}")

    print("Other prerequisites may also need to be completed.")


def main():
    courses = [
        Course("CS101", "Introduction to Programming", 3, "core"),
        Course("CS102", "Object-Oriented Programming", 3, "core"),
        Course("CS103", "Discrete Mathematics", 3, "core"),
        Course("CS201", "Data Structures", 3, "core"),
        Course("CS202", "Advanced Algorithms", 3, "core"),
        Course("CS203", "Web Development", 3, "elective"),
    ]

    course_catalogue = {}
    graph = DirectedGraph()

    for course in courses:
        course_catalogue[course.course_code] = course
        graph.addVertex(course.course_code)

    prerequisites = [
        ("CS101", "CS102"),
        ("CS102", "CS201"),
        ("CS103", "CS201"),
        ("CS201", "CS202"),
        ("CS103", "CS202"),
        ("CS102", "CS203"),
    ]

    for prerequisite, dependent in prerequisites:
        graph.addEdge(prerequisite, dependent)

    while True:
        print("\n===== COURSE PREREQUISITE SYSTEM =====")
        print("1. List all courses")
        print("2. View full course details")
        print("3. View direct prerequisites")
        print("4. View courses unlocked")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            display_course_list(course_catalogue)
        elif choice == "2":
            display_course_details(course_catalogue)
        elif choice == "3":
            display_prerequisites(course_catalogue, graph)
        elif choice == "4":
            display_unlocked_courses(course_catalogue, graph)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please enter a number from 0 to 4.")


if __name__ == "__main__":
    main()