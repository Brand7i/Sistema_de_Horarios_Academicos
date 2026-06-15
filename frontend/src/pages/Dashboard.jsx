import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
  const [resumen, setResumen] = useState({
    docentes: 0,
    materias: 0,
    aulas: 0,
    grupos: 0,
    horarios: 0,
    semestres: 0,
  });
  const [horariosPorSemestre, setHorariosPorSemestre] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/docentes/"),
      api.get("/materias/"),
      api.get("/aulas/"),
      api.get("/grupos/"),
      api.get("/horarios/"),
    ])
      .then(([docentes, materias, aulas, grupos, horarios]) => {
        const conteoSemestres = horarios.data.reduce((acc, item) => {
          acc[item.semestre] = (acc[item.semestre] || 0) + 1;
          return acc;
        }, {});

        setResumen({
          docentes: docentes.data.length,
          materias: materias.data.length,
          aulas: aulas.data.length,
          grupos: grupos.data.length,
          horarios: horarios.data.length,
          semestres: Object.keys(conteoSemestres).length,
        });

        setHorariosPorSemestre(
          Object.entries(conteoSemestres)
            .sort((a, b) => Number(a[0]) - Number(b[0]))
            .map(([semestre, total]) => ({ semestre, total }))
        );
      })
      .finally(() => setCargando(false));
  }, []);

  const semestreMasCargado = horariosPorSemestre.reduce(
    (mejor, actual) => (actual.total > mejor.total ? actual : mejor),
    { semestre: "-", total: 0 }
  );

  return (
    <section>
      <div className="dashboard-hero">
        <div className="dashboard-hero-copy">
          <span className="dashboard-badge">Panel general</span>
          <h1>Sistema de Horarios Academicos Automaticos</h1>
          <p className="subtitulo">
            Genera, revisa y compara horarios academicos por nivel, docente y materia.
          </p>
        </div>

        <div className="dashboard-highlight">
          <strong>{cargando ? "..." : resumen.horarios}</strong>
          <span>bloques horarios registrados</span>
          <p>
            Cada bloque representa una clase en un dia y hora especificos.
          </p>
        </div>
      </div>

      <div className="cards dashboard-cards">
        <div className="card stat-card">
          <small>Docentes</small>
          <span>{resumen.docentes}</span>
          <p>Disponibles para generar horarios.</p>
        </div>
        <div className="card stat-card">
          <small>Materias</small>
          <span>{resumen.materias}</span>
          <p>Asignaturas cargadas en el sistema.</p>
        </div>
        <div className="card stat-card">
          <small>Aulas</small>
          <span>{resumen.aulas}</span>
          <p>Espacios que pueden usarse sin choque.</p>
        </div>
        <div className="card stat-card">
          <small>Grupos</small>
          <span>{resumen.grupos}</span>
          <p>Opciones de grupo por materia y nivel.</p>
        </div>
        <div className="card stat-card stat-card-accent">
          <small>Semestres activos</small>
          <span>{resumen.semestres}</span>
          <p>Niveles con horarios disponibles para generar.</p>
        </div>
      </div>

      <div className="dashboard-panels">
        <div className="info-box">
          <h3>Resumen actual</h3>
          <p>
            {cargando
              ? "Cargando resumen general..."
              : "El sistema ya cuenta con docentes, materias, aulas, grupos y horarios listos para generar alternativas."}
          </p>
        </div>

        <div className="info-box dashboard-mini-panel">
          <h3>Semestre con mas carga</h3>
          <strong>Semestre {semestreMasCargado.semestre}</strong>
          <p>{semestreMasCargado.total} bloques horarios registrados.</p>
        </div>
      </div>

      <div className="info-box">
        <h3>Distribucion por semestre</h3>
        {horariosPorSemestre.length === 0 ? (
          <p>No hay horarios cargados para mostrar.</p>
        ) : (
          <div className="semester-grid">
            {horariosPorSemestre.map((item) => (
              <div key={item.semestre} className="semester-card">
                <strong>Semestre {item.semestre}</strong>
                <span>{item.total} bloques horarios</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
