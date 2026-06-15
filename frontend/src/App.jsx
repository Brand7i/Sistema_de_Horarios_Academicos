import { useState } from "react";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Docentes from "./pages/Docentes";
import Materias from "./pages/Materias";
import Aulas from "./pages/Aulas";
import Grupos from "./pages/Grupos";
import GenerarHorario from "./pages/GenerarHorario";

export default function App() {
  const [vista, setVista] = useState("dashboard");

  const renderVista = () => {
    if (vista === "docentes") return <Docentes />;
    if (vista === "materias") return <Materias />;
    if (vista === "aulas") return <Aulas />;
    if (vista === "grupos") return <Grupos />;
    if (vista === "generar") return <GenerarHorario />;
    return <Dashboard />;
  };

  return (
    <div className="layout">
      <Navbar vista={vista} setVista={setVista} />
      <main>{renderVista()}</main>
    </div>
  );
}
