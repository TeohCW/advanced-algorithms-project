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


def main():
    graph = DirectedGraph()

    graph.addVertex("CS101")
    graph.addVertex("CS102")
    graph.addVertex("CS201")

    # Prerequisite -> dependent course
    graph.addEdge("CS101", "CS102")
    graph.addEdge("CS102", "CS201")

    print("--- GRAPH STRUCTURE ---")
    print(graph.adjacency_list)

    print("\nPrerequisites of CS102:")
    print(graph.listIncomingAdjacentVertex("CS102"))

    print("\nCourses that CS102 is a prerequisite for:")
    print(graph.listOutgoingAdjacentVertex("CS102"))


if __name__ == "__main__":
    main()