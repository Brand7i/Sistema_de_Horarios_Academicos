import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Aulas() {
  const [aulas, setAulas] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    capacidad: 40,
    tipo: "Teórica",
  });

  const cargar = () => api.get("/aulas/").then((res) => setAulas(res.data));

  useEffect(() => { cargar(); }, []);

  const guardar = async (e) => {
    e.preventDefault();
    await api.post("/aulas/", {
      ...form,
      capacidad: Number(form.capacidad),
    });
    setForm({ nombre: "", capacidad: 40, tipo: "Teórica" });
    cargar();
  };

  return (
    <section>
      <h1>Aulas</h1>

      <form className="form" onSubmit={guardar}>
        <input placeholder="Nombre del aula" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
        <input type="number" placeholder="Capacidad" value={form.capacidad} onChange={(e) => setForm({ ...form, capacidad: e.target.value })} required />
        <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })}>
          <option>Teórica</option>
          <option>Laboratorio</option>
        </select>
        <button>Guardar aula</button>
      </form>

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
