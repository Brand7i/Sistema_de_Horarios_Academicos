const ordenDias = {
  Lunes: 1,
  Martes: 2,
  Miércoles: 3,
  Jueves: 4,
  Viernes: 5,
};

export default function TablaHorario({ horarios }) {
  const datos = [...horarios].sort((a, b) => {
    if (a.semestre !== b.semestre) return a.semestre - b.semestre;
    if (ordenDias[a.dia] !== ordenDias[b.dia]) return ordenDias[a.dia] - ordenDias[b.dia];
    return a.bloque.localeCompare(b.bloque);
  });

  return (
    <div className="table-card">
      <table>
        <thead>
          <tr>
            <th>Semestre</th>
            <th>Grupo</th>
            <th>Día</th>
            <th>Bloque</th>
            <th>Materia</th>
            <th>Docente</th>
            <th>Aula</th>
            <th>Tipo</th>
          </tr>
        </thead>
        <tbody>
          {datos.map((h, index) => (
            <tr key={index}>
              <td>{h.semestre}</td>
              <td>{h.grupo}</td>
              <td>{h.dia}</td>
              <td>{h.bloque}</td>
              <td>{h.sigla} - {h.materia}</td>
              <td>{h.docente}</td>
              <td>{h.aula}</td>
              <td>{h.tipo}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
