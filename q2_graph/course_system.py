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

    def has_path(self, source, destination):
        """Return True if a directed path connects source to destination."""
        if source not in self.adjacency_list:
            raise ValueError("Source vertex does not exist.")

        if destination not in self.adjacency_list:
            raise ValueError("Destination vertex does not exist.")

        stack = [source]
        visited = set()

        while stack:
            current = stack.pop()

            if current == destination:
                return True

            if current in visited:
                continue

            visited.add(current)

            for neighbour in self.adjacency_list[current]:
                if neighbour not in visited:
                    stack.append(neighbour)

        return False

    def removeEdge(self, source, destination):
        """Remove a directed edge if it exists."""
        if source not in self.adjacency_list:
            raise ValueError("Source vertex does not exist.")

        if destination not in self.adjacency_list:
            raise ValueError("Destination vertex does not exist.")

        if destination not in self.adjacency_list[source]:
            return False

        self.adjacency_list[source].remove(destination)
        return True


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


def add_course(course_catalogue, graph):
    """Add a course to both the catalogue and graph."""
    print("\n--- ADD COURSE ---")

    if len(course_catalogue) >= 10:
        print("Cannot add course: the maximum is 10 courses.")
        return

    try:
        code = input("Course code: ").strip().upper()

        if code in course_catalogue:
            print(f"Course '{code}' already exists.")
            return

        name = input("Course name: ")
        credit_hours = int(input("Credit hours: "))
        level = input("Level (core/elective): ")

        # Validate all details before changing either structure.
        course = Course(code, name, credit_hours, level)

        # Create the graph vertex and store its course information.
        graph.addVertex(course.course_code)
        course_catalogue[course.course_code] = course

        print(
            f"Course added successfully: "
            f"{course.course_code} - {course.course_name}"
        )
        print("The new course has no prerequisite connections yet.")

    except ValueError as error:
        print(f"Cannot add course: {error}")


def add_prerequisite(course_catalogue, graph):
    """Add a prerequisite without creating a circular dependency."""
    print("\n--- ADD PREREQUISITE ---")

    course_code = input(
        "Course that requires a prerequisite: "
    ).strip().upper()

    prerequisite_code = input(
        "Course to use as its prerequisite: "
    ).strip().upper()

    if course_code not in course_catalogue:
        print(f"Course '{course_code}' was not found.")
        return

    if prerequisite_code not in course_catalogue:
        print(f"Course '{prerequisite_code}' was not found.")
        return

    if course_code == prerequisite_code:
        print("A course cannot be its own prerequisite.")
        return

    outgoing = graph.listOutgoingAdjacentVertex(prerequisite_code)

    if course_code in outgoing:
        print("This prerequisite connection already exists.")
        return

    # Proposed edge: prerequisite -> course.
    # A path in the opposite direction would complete a cycle.
    if graph.has_path(course_code, prerequisite_code):
        print("Cannot add prerequisite: it would create a cycle.")
        return

    graph.addEdge(prerequisite_code, course_code)

    print(
        f"{prerequisite_code} is now a prerequisite "
        f"of {course_code}."
    )


def remove_prerequisite(course_catalogue, graph):
    """Remove a prerequisite connection after confirmation."""
    print("\n--- REMOVE PREREQUISITE ---")

    course_code = input(
        "Course whose prerequisite you want to remove: "
    ).strip().upper()

    prerequisite_code = input(
        "Prerequisite course to remove: "
    ).strip().upper()

    if course_code not in course_catalogue:
        print(f"Course '{course_code}' was not found.")
        return

    if prerequisite_code not in course_catalogue:
        print(f"Course '{prerequisite_code}' was not found.")
        return

    outgoing = graph.listOutgoingAdjacentVertex(prerequisite_code)

    if course_code not in outgoing:
        print("This prerequisite connection does not exist.")
        return

    confirmation = input(
        f"Remove {prerequisite_code} as a prerequisite "
        f"of {course_code}? Enter y to confirm: "
    ).strip().lower()

    if confirmation != "y":
        print("Removal cancelled.")
        return

    if graph.removeEdge(prerequisite_code, course_code):
        print(
            f"{prerequisite_code} is no longer a prerequisite "
            f"of {course_code}."
        )
    else:
        print("This prerequisite connection does not exist.")


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
        print("5. Add course")
        print("6. Add prerequisite")
        print("7. Remove prerequisite")
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
        elif choice == "5":
            add_course(course_catalogue, graph)
        elif choice == "6":
            add_prerequisite(course_catalogue, graph)
        elif choice == "7":
            remove_prerequisite(course_catalogue, graph)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please enter a number from 0 to 7.")


if __name__ == "__main__":
    main()