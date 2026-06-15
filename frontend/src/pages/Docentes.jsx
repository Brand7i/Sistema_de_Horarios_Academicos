import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Docentes() {
  const [docentes, setDocentes] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    correo: "",
    especialidad: "",
    disponibilidad: "Lunes Martes Miércoles Jueves Viernes",
  });

  const cargar = () => api.get("/docentes/").then((res) => setDocentes(res.data));

  useEffect(() => { cargar(); }, []);

  const guardar = async (e) => {
    e.preventDefault();
    await api.post("/docentes/", form);
    setForm({ nombre: "", correo: "", especialidad: "", disponibilidad: "Lunes Martes Miércoles Jueves Viernes" });
    cargar();
  };

  return (
    <section>
      <h1>Docentes</h1>

      <form className="form" onSubmit={guardar}>
        <input placeholder="Nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
        <input placeholder="Correo" value={form.correo} onChange={(e) => setForm({ ...form, correo: e.target.value })} />
        <input placeholder="Especialidad" value={form.especialidad} onChange={(e) => setForm({ ...form, especialidad: e.target.value })} required />
        <input placeholder="Disponibilidad" value={form.disponibilidad} onChange={(e) => setForm({ ...form, disponibilidad: e.target.value })} required />
        <button>Guardar docente</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Nombre</th><th>Correo</th><th>Especialidad</th><th>Disponibilidad</th></tr>
          </thead>
          <tbody>
            {docentes.map((d) => (
              <tr key={d.id}>
                <td>{d.nombre}</td>
                <td>{d.correo}</td>
                <td>{d.especialidad}</td>
                <td>{d.disponibilidad}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
