const dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];
const bloquesBase = [
  "06:45-08:15",
  "08:15-09:45",
  "09:45-11:15",
  "11:15-12:45",
  "12:45-14:15",
  "14:15-15:45",
  "15:45-17:15",
  "17:15-18:45",
  "18:45-20:15",
  "20:15-21:45",
];

const colores = [
  "#fde2e4",
  "#dbeafe",
  "#dcfce7",
  "#fef3c7",
  "#ede9fe",
  "#fbcfe8",
];

function colorMateria(materiaId) {
  return colores[materiaId % colores.length];
}

function ordenarBloques(a, b) {
  const indiceA = bloquesBase.indexOf(a);
  const indiceB = bloquesBase.indexOf(b);

  if (indiceA !== -1 || indiceB !== -1) {
    if (indiceA === -1) return 1;
    if (indiceB === -1) return -1;
    return indiceA - indiceB;
  }

  return a.localeCompare(b);
}

function obtenerBloques(horarios) {
  const bloques = new Set(bloquesBase);
  horarios.forEach((horario) => bloques.add(horario.bloque));
  return [...bloques].sort(ordenarBloques);
}

export default function ScheduleGrid({ horarios }) {
  const bloques = obtenerBloques(horarios);
  const mapa = new Map();

  horarios.forEach((horario) => {
    const clave = `${horario.dia}|${horario.bloque}`;
    if (!mapa.has(clave)) {
      mapa.set(clave, []);
    }
    mapa.get(clave).push(horario);
  });

  return (
    <div className="grid-card">
      <div className="schedule-grid-scroll">
        <div className="schedule-grid">
          <div className="schedule-corner" />
          {dias.map((dia) => (
            <div key={dia} className="schedule-header">{dia.slice(0, 2).toUpperCase()}</div>
          ))}

          {bloques.map((bloque) => (
            <div key={bloque} className="schedule-row">
              <div className="schedule-time">{bloque}</div>
              {dias.map((dia) => {
                const eventos = mapa.get(`${dia}|${bloque}`) || [];
                return (
                  <div key={`${dia}-${bloque}`} className="schedule-cell">
                    {eventos.map((horario, indice) => (
                      <div
                        key={`${horario.materia_id}-${horario.docente_id}-${horario.aula_id}-${indice}`}
                        className="schedule-event"
                        style={{ backgroundColor: colorMateria(horario.materia_id) }}
                      >
                        <strong>{horario.materia}</strong>
                        <span>{horario.docente}</span>
                        <span>{horario.aula}</span>
                      </div>
                    ))}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
