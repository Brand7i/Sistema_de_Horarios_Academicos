const ordenDias = {
  Lunes: 1,
  Martes: 2,
  Miercoles: 3,
  "Miércoles": 3,
  Jueves: 4,
  Viernes: 5,
  Sabado: 6,
  "Sábado": 6,
};

const niveles = {
  1: "A",
  2: "B",
  3: "C",
  4: "D",
  5: "E",
  6: "F",
  7: "G",
  8: "H",
  9: "I",
};

function ordenarHorarios(a, b) {
  if (a.semestre !== b.semestre) return a.semestre - b.semestre;
  if (a.sigla !== b.sigla) return a.sigla.localeCompare(b.sigla);
  if (a.grupo !== b.grupo) return a.grupo.localeCompare(b.grupo);
  if (a.docente !== b.docente) return a.docente.localeCompare(b.docente);
  if ((ordenDias[a.dia] || 99) !== (ordenDias[b.dia] || 99)) {
    return (ordenDias[a.dia] || 99) - (ordenDias[b.dia] || 99);
  }
  return a.bloque.localeCompare(b.bloque);
}

function agruparHorarios(horarios) {
  const grupos = [];
  const mapa = new Map();

  [...horarios].sort(ordenarHorarios).forEach((horario) => {
    const clave = `${horario.semestre}|${horario.sigla}|${horario.materia}`;
    if (!mapa.has(clave)) {
      const grupo = {
        clave,
        semestre: horario.semestre,
        nivel: niveles[horario.semestre] || String(horario.semestre),
        sigla: horario.sigla,
        materia: horario.materia,
        filas: [],
      };
      mapa.set(clave, grupo);
      grupos.push(grupo);
    }

    mapa.get(clave).filas.push(horario);
  });

  return grupos;
}

export default function TablaHorario({ horarios }) {
  const grupos = agruparHorarios(horarios);

  return (
    <div className="table-card">
      {grupos.length === 0 ? (
        <p>No hay horarios para mostrar con los filtros actuales.</p>
      ) : (
        <div className="pdf-table">
          <div className="pdf-table-header">
            <span>Nivel</span>
            <span>Materia</span>
            <span>Grupo</span>
            <span>Tipo</span>
            <span>Docente</span>
            <span>Dia</span>
            <span>Hora</span>
            <span>Aula</span>
          </div>

          {grupos.map((grupo) => (
            <div key={grupo.clave} className="pdf-subject-block">
              {grupo.filas.map((horario, indice) => (
                <div
                  key={`${grupo.clave}-${horario.grupo}-${horario.docente}-${horario.dia}-${horario.bloque}-${indice}`}
                  className="pdf-table-row"
                >
                  <span className="pdf-cell pdf-cell-level">
                    {indice === 0 ? grupo.nivel : ""}
                  </span>
                  <span className="pdf-cell pdf-cell-materia">
                    {indice === 0 ? `${grupo.sigla} ${grupo.materia}` : ""}
                  </span>
                  <span className="pdf-cell">{horario.grupo}</span>
                  <span className="pdf-cell">{horario.tipo}</span>
                  <span className="pdf-cell pdf-cell-docente">{horario.docente}</span>
                  <span className="pdf-cell pdf-cell-dia">{horario.dia}</span>
                  <span className="pdf-cell pdf-cell-hora">{horario.bloque}</span>
                  <span className="pdf-cell">{horario.aula}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
