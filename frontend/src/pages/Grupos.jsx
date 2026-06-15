import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Grupos() {
  const [grupos, setGrupos] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    semestre: 1,
    cantidad_estudiantes: 40,
  });

  const cargar = () => api.get("/grupos/").then((res) => setGrupos(res.data));

  useEffect(() => { cargar(); }, []);

  const guardar = async (e) => {
    e.preventDefault();
    await api.post("/grupos/", {
      ...form,
      semestre: Number(form.semestre),
      cantidad_estudiantes: Number(form.cantidad_estudiantes),
    });
    setForm({ nombre: "", semestre: 1, cantidad_estudiantes: 40 });
    cargar();
  };

  return (
    <section>
      <h1>Grupos</h1>

      <form className="form" onSubmit={guardar}>
        <input placeholder="Nombre del grupo" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
        <input type="number" placeholder="Semestre" value={form.semestre} onChange={(e) => setForm({ ...form, semestre: e.target.value })} required />
        <input type="number" placeholder="Cantidad de estudiantes" value={form.cantidad_estudiantes} onChange={(e) => setForm({ ...form, cantidad_estudiantes: e.target.value })} required />
        <button>Guardar grupo</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr><th>Grupo</th><th>Semestre</th><th>Estudiantes</th></tr>
          </thead>
          <tbody>
            {grupos.map((g) => (
              <tr key={g.id}>
                <td>{g.nombre}</td>
                <td>{g.semestre}</td>
                <td>{g.cantidad_estudiantes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
