import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Aulas() {
  const [aulas, setAulas] = useState([]);

  const cargar = () => api.get("/aulas/").then((res) => setAulas(res.data));

  useEffect(() => {
    cargar();
  }, []);

  return (
    <section>
      <h1>Aulas</h1>
      <p className="subtitulo">
        Aulas detectadas desde el horario importado. Aqui solo se consultan sus capacidades y tipo de uso.
      </p>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Aula</th><th>Capacidad</th><th>Tipo</th></tr>
          </thead>
          <tbody>
            {aulas.map((a) => (
              <tr key={a.id}>
                <td>{a.nombre}</td>
                <td>{a.capacidad}</td>
                <td>{a.tipo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
