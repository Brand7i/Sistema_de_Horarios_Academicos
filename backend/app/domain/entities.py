from pydantic import BaseModel, Field


class Teacher(BaseModel):
    id: str
    name: str


class Room(BaseModel):
    id: str
    name: str
    capacity: int


class StudentGroup(BaseModel):
    id: str
    name: str
    size: int


class TimeSlot(BaseModel):
    id: str
    day: str
    start_time: str
    end_time: str


class Course(BaseModel):
    id: str
    name: str
    teacher_id: str
    student_group_id: str
    sessions_per_week: int = Field(ge=1)
    expected_students: int = Field(ge=1)


class ClassInstance(BaseModel):
    id: str
    course_id: str
    teacher_id: str
    student_group_id: str
    expected_students: int


class Assignment(BaseModel):
    class_instance_id: str
    course_id: str
    teacher_id: str
    student_group_id: str
    room_id: str
    time_slot_id: str


class ScheduleRequest(BaseModel):
    teachers: list[Teacher]
    rooms: list[Room]
    student_groups: list[StudentGroup]
    time_slots: list[TimeSlot]
    courses: list[Course]


class ScheduleResponse(BaseModel):
    fitness: int
    hard_conflicts: int
    soft_penalties: int
    assignments: list[Assignment]
    message: str
