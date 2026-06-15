export default function Navbar({ vista, setVista }) {
  const opciones = [
    ["dashboard", "Dashboard"],
    ["docentes", "Docentes"],
    ["materias", "Materias"],
    ["aulas", "Aulas"],
    ["grupos", "Grupos"],
    ["generar", "Generador de horarios"],
  ];

  return (
    <aside className="sidebar">
      <h2>Generador de horarios</h2>
      <p>Ingenieria Informatica UMSS</p>

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
