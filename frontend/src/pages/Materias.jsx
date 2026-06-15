import { useEffect, useState } from "react";
import { api } from "../services/api";

const niveles = {
  1: "Nivel A",
  2: "Nivel B",
  3: "Nivel C",
  4: "Nivel D",
  5: "Nivel E",
  6: "Nivel F",
  7: "Nivel G",
  8: "Nivel H",
  9: "Nivel I",
};

export default function Materias() {
  const [materias, setMaterias] = useState([]);

  const cargar = () => api.get("/materias/").then((res) => setMaterias(res.data));

  useEffect(() => {
    cargar();
  }, []);

  return (
    <section>
      <h1>Materias</h1>
      <p className="subtitulo">
        Materias importadas desde la carga base. Esta seccion queda como consulta del plan academico por nivel.
      </p>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Sigla</th><th>Materia</th><th>Nivel</th><th>Horas</th><th>Tipo</th></tr>
          </thead>
          <tbody>
            {materias.map((m) => (
              <tr key={m.id}>
                <td>{m.sigla}</td>
                <td>{m.nombre}</td>
                <td>{niveles[m.semestre] || `Semestre ${m.semestre}`}</td>
                <td>{m.horas_semana}</td>
                <td>{m.tipo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
