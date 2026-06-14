from backend.app.core.config import settings
from backend.app.domain.entities import ScheduleRequest, ScheduleResponse
from backend.app.genetic.engine import GeneticScheduler


class ScheduleService:
    def __init__(self) -> None:
        self.scheduler = GeneticScheduler(
            population_size=settings.population_size,
            generations=settings.generations,
            mutation_rate=settings.mutation_rate,
            elite_size=settings.elite_size,
        )

    def generate_schedule(self, request: ScheduleRequest) -> ScheduleResponse:
        result = self.scheduler.generate(request)
        message = "Horario generado con restricciones base. Ajusta el fitness con tus reglas reales."

        return ScheduleResponse(
            fitness=result.fitness,
            hard_conflicts=result.hard_conflicts,
            soft_penalties=result.soft_penalties,
            assignments=result.assignments,
            message=message,
        )
