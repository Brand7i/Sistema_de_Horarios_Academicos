import { useEffect, useState } from "react";
import { api } from "../services/api";
import TablaHorario from "../components/TablaHorario";

export default function GenerarHorario() {
  const [horarios, setHorarios] = useState([]);
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);

  const cargarHorario = () => {
    api.get("/horarios/").then((res) => setHorarios(res.data));
  };

  useEffect(() => { cargarHorario(); }, []);

  const generar = async () => {
    setCargando(true);
    setResultado(null);

    try {
      const res = await api.post("/horarios/generar");
      setResultado(res.data);
      cargarHorario();
    } catch (error) {
      alert(error.response?.data?.detail || "Error al generar horario");
    } finally {
      setCargando(false);
    }
  };

  return (
    <section>
      <h1>Generar horario</h1>
      <p className="subtitulo">
        El sistema aplicará selección, cruce y mutación para buscar el mejor horario posible.
      </p>

      <button className="primary" onClick={generar} disabled={cargando}>
        {cargando ? "Generando..." : "Generar horario con AG"}
      </button>

      {resultado && (
        <div className="resultado">
          <h3>Resultado del algoritmo</h3>
          <p><strong>Fitness:</strong> {resultado.fitness}</p>
          <p><strong>Total de clases:</strong> {resultado.total_clases}</p>
          <p><strong>Conflictos detectados:</strong> {resultado.conflictos.length}</p>

          {resultado.conflictos.length > 0 && (
            <ul>
              {resultado.conflictos.map((c, index) => <li key={index}>{c}</li>)}
            </ul>
          )}
        </div>
      )}

      <h2>Horario generado</h2>
      <TablaHorario horarios={horarios} />
    </section>
  );
}
