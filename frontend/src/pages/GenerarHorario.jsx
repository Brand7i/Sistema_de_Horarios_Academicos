import { useEffect, useState } from "react";
import { api } from "../services/api";
import ScheduleGrid from "../components/ScheduleGrid";
import TablaHorario from "../components/TablaHorario";

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

function esFisicaGeneralEspecial(materia) {
  return materia?.sigla === "2006063";
}

function esGrupoFisicaTeoria(docente) {
  return docente?.grupo_referencia?.endsWith("-GB");
}

function extraerDocentesSeleccionados(valor) {
  if (Array.isArray(valor)) return valor;
  return valor ? [valor] : [];
}

function construirSeleccionDesdeHorario(horario) {
  const seleccionActual = {};

  for (const bloque of horario || []) {
    if (!seleccionActual[bloque.materia_id]) {
      seleccionActual[bloque.materia_id] = [];
    }
    if (!seleccionActual[bloque.materia_id].includes(bloque.docente_id)) {
      seleccionActual[bloque.materia_id].push(bloque.docente_id);
    }
  }

  return seleccionActual;
}

export default function GenerarHorario() {
  const [semestre, setSemestre] = useState(1);
  const [config, setConfig] = useState(null);
  const [horariosImportados, setHorariosImportados] = useState([]);
  const [horarios, setHorarios] = useState([]);
  const [alternativasAG, setAlternativasAG] = useState([]);
  const [indiceAlternativa, setIndiceAlternativa] = useState(0);
  const [seleccion, setSeleccion] = useState({});
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);

  const limpiarGeneracion = () => {
    setAlternativasAG([]);
    setIndiceAlternativa(0);
    setResultado(null);
  };

  const reiniciarTodo = () => {
    setSeleccion({});
    setHorarios([]);
    limpiarGeneracion();
  };

  const cargarConfiguracion = async (valorSemestre) => {
    const [configRes, importadosRes] = await Promise.all([
      api.get("/horarios/configuracion", { params: { semestre: valorSemestre } }),
      api.get("/horarios/", { params: { origen: "importado", semestre: valorSemestre } }),
    ]);

    setConfig(configRes.data);
    setHorariosImportados(importadosRes.data);
    setHorarios([]);
    setSeleccion({});
    setAlternativasAG([]);
    setIndiceAlternativa(0);
    setResultado(null);
  };

  useEffect(() => {
    cargarConfiguracion(semestre);
  }, [semestre]);

  useEffect(() => {
    if (alternativasAG.length > 0) {
      setHorarios(alternativasAG[indiceAlternativa]?.horario || []);
      return;
    }

    const seleccionIds = new Set(Object.values(seleccion));
    if (seleccionIds.size === 0) {
      setHorarios([]);
      return;
    }

    const preview = horariosImportados.filter((horario) => {
      const docentesSeleccionados = extraerDocentesSeleccionados(seleccion[horario.materia_id]);
      return docentesSeleccionados.includes(horario.docente_id);
    });
    setHorarios(preview);
  }, [alternativasAG, indiceAlternativa, seleccion, horariosImportados]);

  const generar = async (docentesOverride = seleccion) => {
    if (!config) return;

    setCargando(true);
    setResultado(null);

    try {
      const res = await api.post("/horarios/generar", {
        semestre,
        docentes_por_materia: docentesOverride,
      });
      setResultado(res.data);
      setAlternativasAG(res.data.alternativas || []);
      setIndiceAlternativa(0);
      setHorarios((res.data.alternativas && res.data.alternativas[0]?.horario) || []);
    } catch (error) {
      alert(error.response?.data?.detail || "Error al generar horario");
    } finally {
      setCargando(false);
    }
  };

  const totalMaterias = config?.materias.length || 0;
  const totalSeleccionadas = Object.values(seleccion).filter((valor) => extraerDocentesSeleccionados(valor).length > 0).length;
  const puedeGenerar = !!config && !cargando;
  const alternativaActual = alternativasAG[indiceAlternativa] || null;
  const totalAlternativas = alternativasAG.length;
  const mostrandoPreview = totalAlternativas === 0 && totalSeleccionadas > 0;
  const seleccionVisible = totalAlternativas > 0
    ? construirSeleccionDesdeHorario(alternativaActual?.horario || [])
    : seleccion;
  const conflictosActuales = alternativaActual?.conflictos || resultado?.conflictos || [];
  const totalClasesActual = alternativaActual?.horario?.length || resultado?.total_clases || 0;

  const seleccionarDocente = (materia, docente) => {
    limpiarGeneracion();
    setSeleccion((actual) => {
      if (!esFisicaGeneralEspecial(materia)) {
        return {
          ...actual,
          [materia.materia_id]: docente.id,
        };
      }

      const teoria = materia.docentes.find(esGrupoFisicaTeoria);
      const teoriaId = teoria?.id;
      const actuales = extraerDocentesSeleccionados(actual[materia.materia_id]);
      const laboratorioActual = actuales.find((id) => id !== teoriaId);

      if (esGrupoFisicaTeoria(docente)) {
        return {
          ...actual,
          [materia.materia_id]: laboratorioActual ? [docente.id, laboratorioActual] : [docente.id],
        };
      }

      return {
        ...actual,
        [materia.materia_id]: teoriaId ? [teoriaId, docente.id] : [docente.id],
      };
    });
  };

  const generarDesdeCero = () => {
    setSeleccion({});
    setHorarios([]);
    limpiarGeneracion();
    generar({});
  };

  return (
    <section>
      <h1>Generador de horarios</h1>

      <div className="horarios-layout">
        <aside className="selection-panel">
          <div className="selection-controls">
            <select value={semestre} onChange={(e) => setSemestre(Number(e.target.value))}>
              {Object.entries(niveles).map(([valor, texto]) => (
                <option key={valor} value={valor}>{texto}</option>
              ))}
            </select>

            <button onClick={generarDesdeCero} disabled={!puedeGenerar}>
              {cargando ? "Generando..." : "Generar horario con AG"}
            </button>
            <div className="selection-actions">
              <button
                type="button"
                className="secondary"
                onClick={reiniciarTodo}
                disabled={cargando && totalSeleccionadas === 0 && totalAlternativas === 0}
              >
                Reiniciar seleccion
              </button>
            </div>
            <span className="selection-status">
              {totalSeleccionadas} de {totalMaterias} materias con docente fijado manualmente
            </span>
          </div>

          {config && (
            <div className="selection-list">
              <h3>{niveles[semestre]}</h3>
              {config.materias.map((materia) => (
                <div
                  key={materia.materia_id}
                  className={`subject-card ${seleccion[materia.materia_id] ? "" : "subject-card-pending"}`}
                >
                  <div className="subject-header">
                    <strong>{materia.nombre}</strong>
                    <span>{materia.sigla}</span>
                  </div>
                  <div className="subject-meta">
                    <span>{materia.horas_semana} h/semana</span>
                    <span>{materia.tipo}</span>
                  </div>
                  <div className="subject-state">
                    {seleccionVisible[materia.materia_id] ? "Docente usado en esta opcion" : "Seleccion automatica"}
                  </div>
                  <div className="teacher-options">
                    {materia.docentes.map((docente) => (
                      <label
                        key={docente.id}
                        className={`teacher-option ${esFisicaGeneralEspecial(materia) && esGrupoFisicaTeoria(docente) ? "teacher-option-fixed" : ""}`}
                      >
                        <input
                          type={esFisicaGeneralEspecial(materia) && esGrupoFisicaTeoria(docente) ? "checkbox" : "radio"}
                          name={esFisicaGeneralEspecial(materia) && !esGrupoFisicaTeoria(docente)
                            ? `materia-${materia.materia_id}-laboratorio`
                            : `materia-${materia.materia_id}`}
                          checked={extraerDocentesSeleccionados(seleccionVisible[materia.materia_id]).includes(docente.id)}
                          onChange={() => seleccionarDocente(materia, docente)}
                        />
                        <span>
                          {docente.grupo_referencia} {docente.nombre}
                          {esFisicaGeneralEspecial(materia) && esGrupoFisicaTeoria(docente)
                            ? " - teoria fija"
                            : ""}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </aside>

        <div className="schedule-panel">
          {resultado && (
            <div className="resultado">
              <h3>Resultado del algoritmo</h3>
              <p><strong>Total de clases:</strong> {totalClasesActual}</p>
              <p><strong>Materias:</strong> {resultado.parametros.materias}</p>
              <p><strong>Bloques base del importado:</strong> {resultado.parametros.clases_base_importadas}</p>
              <p><strong>Alternativas generadas:</strong> {resultado.parametros.alternativas}</p>
              <p><strong>Conflictos:</strong> {conflictosActuales.length}</p>
              {conflictosActuales.length > 0 && (
                <div className="resultado-conflicts">
                  {conflictosActuales.slice(0, 4).map((conflicto) => (
                    <p key={conflicto}>{conflicto}</p>
                  ))}
                </div>
              )}
            </div>
          )}

          {totalAlternativas > 0 && (
            <div className="alternatives-bar">
              <button
                type="button"
                className="secondary"
                disabled={indiceAlternativa === 0}
                onClick={() => setIndiceAlternativa((actual) => Math.max(0, actual - 1))}
              >
                Anterior
              </button>
              <span>Horario {indiceAlternativa + 1} de {totalAlternativas}</span>
              <button
                type="button"
                className="secondary"
                disabled={indiceAlternativa >= totalAlternativas - 1}
                onClick={() => setIndiceAlternativa((actual) => Math.min(totalAlternativas - 1, actual + 1))}
              >
                Siguiente
              </button>
            </div>
          )}

          {mostrandoPreview && (
            <div className="info-box">
              <strong>Vista previa de seleccion</strong>
              <p>
                La grilla muestra los bloques importados de los docentes que vas marcando. Cuando pulses
                `Generar`, el AG construira alternativas usando esas elecciones como restriccion.
              </p>
            </div>
          )}

          <ScheduleGrid horarios={horarios} />

          <div className="table-section">
            <h3>
              {mostrandoPreview ? "Detalle de la seleccion actual" : "Detalle generado por AG"}
            </h3>
            <TablaHorario horarios={horarios} />
          </div>
        </div>
      </div>
    </section>
  );
}
