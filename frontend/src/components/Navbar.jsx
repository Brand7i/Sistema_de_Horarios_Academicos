export default function Navbar({ vista, setVista }) {
  const opciones = [
    ["dashboard", "Dashboard"],
    ["docentes", "Docentes"],
    ["materias", "Materias"],
    ["aulas", "Aulas"],
    ["grupos", "Grupos"],
    ["generar", "Generar horario"],
  ];

  return (
    <aside className="sidebar">
      <h2>Horarios AG</h2>
      <p>Ingeniería Informática UMSS</p>

      <nav>
        {opciones.map(([key, label]) => (
          <button
            key={key}
            className={vista === key ? "active" : ""}
            onClick={() => setVista(key)}
          >
            {label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
