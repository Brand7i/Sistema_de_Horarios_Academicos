from backend.app.domain.entities import (
    Course,
    Room,
    ScheduleRequest,
    StudentGroup,
    Teacher,
    TimeSlot,
)


def build_sample_request() -> ScheduleRequest:
    teachers = [
        Teacher(id="t1", name="Ing. Perez"),
        Teacher(id="t2", name="Lic. Rojas"),
        Teacher(id="t3", name="Msc. Flores"),
    ]

    rooms = [
        Room(id="r1", name="Lab A", capacity=35),
        Room(id="r2", name="Lab B", capacity=30),
        Room(id="r3", name="Aula 201", capacity=45),
    ]

    student_groups = [
        StudentGroup(id="g1", name="1er semestre A", size=32),
        StudentGroup(id="g2", name="3er semestre A", size=28),
        StudentGroup(id="g3", name="5to semestre A", size=26),
    ]

    time_slots = [
        TimeSlot(id="ts1", day="Lunes", start_time="08:00", end_time="10:00"),
        TimeSlot(id="ts2", day="Lunes", start_time="10:15", end_time="12:15"),
        TimeSlot(id="ts3", day="Martes", start_time="08:00", end_time="10:00"),
        TimeSlot(id="ts4", day="Martes", start_time="10:15", end_time="12:15"),
        TimeSlot(id="ts5", day="Miercoles", start_time="08:00", end_time="10:00"),
        TimeSlot(id="ts6", day="Jueves", start_time="08:00", end_time="10:00"),
    ]

    courses = [
        Course(
            id="c1",
            name="Programacion I",
            teacher_id="t1",
            student_group_id="g1",
            sessions_per_week=2,
            expected_students=32,
        ),
        Course(
            id="c2",
            name="Matematica Discreta",
            teacher_id="t2",
            student_group_id="g1",
            sessions_per_week=2,
            expected_students=32,
        ),
        Course(
            id="c3",
            name="Base de Datos I",
            teacher_id="t3",
            student_group_id="g2",
            sessions_per_week=2,
            expected_students=28,
        ),
        Course(
            id="c4",
            name="Estructura de Datos",
            teacher_id="t1",
            student_group_id="g2",
            sessions_per_week=2,
            expected_students=28,
        ),
        Course(
            id="c5",
            name="Ingenieria de Software I",
            teacher_id="t3",
            student_group_id="g3",
            sessions_per_week=2,
            expected_students=26,
        ),
    ]

    return ScheduleRequest(
        teachers=teachers,
        rooms=rooms,
        student_groups=student_groups,
        time_slots=time_slots,
        courses=courses,
    )
