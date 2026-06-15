import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
  const [resumen, setResumen] = useState({
    docentes: 0,
    materias: 0,
    aulas: 0,
    grupos: 0,
  });

  useEffect(() => {
    Promise.all([
      api.get("/docentes/"),
      api.get("/materias/"),
      api.get("/aulas/"),
      api.get("/grupos/"),
    ]).then(([docentes, materias, aulas, grupos]) => {
      setResumen({
        docentes: docentes.data.length,
        materias: materias.data.length,
        aulas: aulas.data.length,
        grupos: grupos.data.length,
      });
    });
  }, []);

  return (
    <section>
      <h1>Sistema de Horarios Académicos Automáticos</h1>
      <p className="subtitulo">
        Proyecto aplicado a Ingeniería Informática UMSS usando Algoritmos Genéticos.
      </p>

      <div className="cards">
        <div className="card"><span>{resumen.docentes}</span><p>Docentes</p></div>
        <div className="card"><span>{resumen.materias}</span><p>Materias</p></div>
        <div className="card"><span>{resumen.aulas}</span><p>Aulas</p></div>
        <div className="card"><span>{resumen.grupos}</span><p>Grupos</p></div>
      </div>

      <div className="info-box">
        <h3>¿Cómo trabaja el algoritmo?</h3>
        <p>
          Cada horario se representa como un cromosoma. Cada clase es un gen con
          materia, docente, aula, grupo, día y bloque. El algoritmo evalúa conflictos
          y mejora la solución mediante selección, cruce y mutación.
        </p>
      </div>
    </section>
  );
}
