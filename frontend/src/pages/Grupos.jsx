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

export default function Grupos() {
  const [grupos, setGrupos] = useState([]);

  const cargar = () => api.get("/grupos/").then((res) => setGrupos(res.data));

  useEffect(() => {
    cargar();
  }, []);

  return (
    <section>
      <h1>Grupos</h1>
      <p className="subtitulo">
        Grupos ya cargados desde la base importada. Esta vista queda para revisar el nivel y la cantidad de estudiantes.
      </p>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Grupo</th><th>Nivel</th><th>Estudiantes</th></tr>
          </thead>
          <tbody>
            {grupos.map((g) => (
              <tr key={g.id}>
                <td>{g.nombre}</td>
                <td>{niveles[g.semestre] || `Semestre ${g.semestre}`}</td>
                <td>{g.cantidad_estudiantes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
