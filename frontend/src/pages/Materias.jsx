import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Materias() {
  const [materias, setMaterias] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    sigla: "",
    semestre: 1,
    horas_semana: 4,
    tipo: "Teórica",
  });

  const cargar = () => api.get("/materias/").then((res) => setMaterias(res.data));

  useEffect(() => { cargar(); }, []);

  const guardar = async (e) => {
    e.preventDefault();
    await api.post("/materias/", {
      ...form,
      semestre: Number(form.semestre),
      horas_semana: Number(form.horas_semana),
    });
    setForm({ nombre: "", sigla: "", semestre: 1, horas_semana: 4, tipo: "Teórica" });
    cargar();
  };

  return (
    <section>
      <h1>Materias</h1>

      <form className="form" onSubmit={guardar}>
        <input placeholder="Nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
        <input placeholder="Sigla" value={form.sigla} onChange={(e) => setForm({ ...form, sigla: e.target.value })} required />
        <input type="number" placeholder="Semestre" value={form.semestre} onChange={(e) => setForm({ ...form, semestre: e.target.value })} required />
        <input type="number" placeholder="Horas semana" value={form.horas_semana} onChange={(e) => setForm({ ...form, horas_semana: e.target.value })} required />
        <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })}>
          <option>Teórica</option>
          <option>Laboratorio</option>
        </select>
        <button>Guardar materia</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Sigla</th><th>Materia</th><th>Semestre</th><th>Horas</th><th>Tipo</th></tr>
          </thead>
          <tbody>
            {materias.map((m) => (
              <tr key={m.id}>
                <td>{m.sigla}</td>
                <td>{m.nombre}</td>
                <td>{m.semestre}</td>
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
