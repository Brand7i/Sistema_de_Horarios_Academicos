import random
from dataclasses import dataclass

from backend.app.domain.entities import Assignment, ClassInstance, Room, ScheduleRequest


@dataclass
class CandidateSchedule:
    assignments: list[Assignment]
    fitness: int
    hard_conflicts: int
    soft_penalties: int


class GeneticScheduler:
    def __init__(
        self,
        population_size: int,
        generations: int,
        mutation_rate: float,
        elite_size: int,
    ) -> None:
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size

    def generate(self, request: ScheduleRequest) -> CandidateSchedule:
        class_instances = self._expand_classes(request)
        population = [self._create_candidate(request, class_instances) for _ in range(self.population_size)]

        for _ in range(self.generations):
            population.sort(key=lambda candidate: candidate.fitness, reverse=True)
            next_population = population[: self.elite_size]

            while len(next_population) < self.population_size:
                parent_a = self._tournament_selection(population)
                parent_b = self._tournament_selection(population)
                child = self._crossover(parent_a, parent_b)
                child = self._mutate(child, request)
                next_population.append(self._evaluate(child, request))

            population = next_population

        population.sort(key=lambda candidate: candidate.fitness, reverse=True)
        return population[0]

    def _expand_classes(self, request: ScheduleRequest) -> list[ClassInstance]:
        instances: list[ClassInstance] = []

        for course in request.courses:
            for session_number in range(course.sessions_per_week):
                instances.append(
                    ClassInstance(
                        id=f"{course.id}-s{session_number + 1}",
                        course_id=course.id,
                        teacher_id=course.teacher_id,
                        student_group_id=course.student_group_id,
                        expected_students=course.expected_students,
                    )
                )

        return instances

    def _create_candidate(
        self,
        request: ScheduleRequest,
        class_instances: list[ClassInstance],
    ) -> CandidateSchedule:
        assignments: list[Assignment] = []

        for instance in class_instances:
            room = random.choice(request.rooms)
            time_slot = random.choice(request.time_slots)
            assignments.append(
                Assignment(
                    class_instance_id=instance.id,
                    course_id=instance.course_id,
                    teacher_id=instance.teacher_id,
                    student_group_id=instance.student_group_id,
                    room_id=room.id,
                    time_slot_id=time_slot.id,
                )
            )

        return self._evaluate(
            CandidateSchedule(assignments=assignments, fitness=0, hard_conflicts=0, soft_penalties=0),
            request,
        )

    def _evaluate(self, candidate: CandidateSchedule, request: ScheduleRequest) -> CandidateSchedule:
        hard_conflicts = 0
        soft_penalties = 0
        rooms_by_id = {room.id: room for room in request.rooms}
        teacher_time: set[tuple[str, str]] = set()
        room_time: set[tuple[str, str]] = set()
        group_time: set[tuple[str, str]] = set()

        for assignment in candidate.assignments:
            teacher_key = (assignment.teacher_id, assignment.time_slot_id)
            room_key = (assignment.room_id, assignment.time_slot_id)
            group_key = (assignment.student_group_id, assignment.time_slot_id)

            if teacher_key in teacher_time:
                hard_conflicts += 1
            else:
                teacher_time.add(teacher_key)

            if room_key in room_time:
                hard_conflicts += 1
            else:
                room_time.add(room_key)

            if group_key in group_time:
                hard_conflicts += 1
            else:
                group_time.add(group_key)

            room = rooms_by_id[assignment.room_id]
            if self._expected_students(candidate.assignments, assignment.class_instance_id, request) > room.capacity:
                hard_conflicts += 1

        soft_penalties += self._penalize_repeated_day(candidate.assignments, request)
        fitness = 1000 - (hard_conflicts * 100) - (soft_penalties * 10)

        return CandidateSchedule(
            assignments=candidate.assignments,
            fitness=fitness,
            hard_conflicts=hard_conflicts,
            soft_penalties=soft_penalties,
        )

    def _expected_students(
        self,
        assignments: list[Assignment],
        class_instance_id: str,
        request: ScheduleRequest,
    ) -> int:
        course_by_id = {course.id: course for course in request.courses}
        assignment = next(item for item in assignments if item.class_instance_id == class_instance_id)
        return course_by_id[assignment.course_id].expected_students

    def _penalize_repeated_day(self, assignments: list[Assignment], request: ScheduleRequest) -> int:
        penalties = 0
        slot_by_id = {slot.id: slot for slot in request.time_slots}
        course_days: dict[str, set[str]] = {}

        for assignment in assignments:
            day = slot_by_id[assignment.time_slot_id].day
            course_days.setdefault(assignment.course_id, set())
            if day in course_days[assignment.course_id]:
                penalties += 1
            course_days[assignment.course_id].add(day)

        return penalties

    def _tournament_selection(self, population: list[CandidateSchedule]) -> CandidateSchedule:
        contenders = random.sample(population, k=min(4, len(population)))
        contenders.sort(key=lambda candidate: candidate.fitness, reverse=True)
        return contenders[0]

    def _crossover(self, parent_a: CandidateSchedule, parent_b: CandidateSchedule) -> CandidateSchedule:
        pivot = random.randint(1, len(parent_a.assignments) - 1)
        assignments = parent_a.assignments[:pivot] + parent_b.assignments[pivot:]
        return CandidateSchedule(assignments=assignments, fitness=0, hard_conflicts=0, soft_penalties=0)

    def _mutate(self, candidate: CandidateSchedule, request: ScheduleRequest) -> CandidateSchedule:
        assignments: list[Assignment] = []

        for assignment in candidate.assignments:
            updated = assignment.model_copy()
            if random.random() < self.mutation_rate:
                updated.room_id = random.choice(request.rooms).id
            if random.random() < self.mutation_rate:
                updated.time_slot_id = random.choice(request.time_slots).id
            assignments.append(updated)

        return CandidateSchedule(assignments=assignments, fitness=0, hard_conflicts=0, soft_penalties=0)
