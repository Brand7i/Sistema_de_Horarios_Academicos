import { useEffect, useState } from "react";
import { api } from "../services/api";

const ordenDias = {
  Lunes: 1,
  Martes: 2,
  Miercoles: 3,
  "Miércoles": 3,
  Jueves: 4,
  Viernes: 5,
  Sabado: 6,
  "Sábado": 6,
};

function ordenarSlots(a, b) {
  if ((ordenDias[a.dia] || 99) !== (ordenDias[b.dia] || 99)) {
    return (ordenDias[a.dia] || 99) - (ordenDias[b.dia] || 99);
  }
  return a.bloque.localeCompare(b.bloque);
}

function construirResumenDocentes(docentes, horarios) {
  const docentesPorId = new Map(
    docentes.map((docente) => [
      docente.id,
      {
        ...docente,
        materias: new Map(),
      },
    ])
  );

  horarios.forEach((horario) => {
    const docente = docentesPorId.get(horario.docente_id);
    if (!docente) return;

    const claveMateria = `${horario.materia_id}|${horario.grupo_id}`;
    if (!docente.materias.has(claveMateria)) {
      docente.materias.set(claveMateria, {
        materia_id: horario.materia_id,
        sigla: horario.sigla,
        materia: horario.materia,
        grupo: horario.grupo,
        semestre: horario.semestre,
        tipo: horario.tipo,
        slots: [],
      });
    }

    docente.materias.get(claveMateria).slots.push({
      dia: horario.dia,
      bloque: horario.bloque,
      aula: horario.aula,
    });
  });

  return [...docentesPorId.values()]
    .map((docente) => ({
      ...docente,
      materias: [...docente.materias.values()]
        .map((materia) => ({
          ...materia,
          slots: materia.slots.sort(ordenarSlots),
        }))
        .sort((a, b) => {
          if (a.semestre !== b.semestre) return a.semestre - b.semestre;
          if (a.sigla !== b.sigla) return a.sigla.localeCompare(b.sigla);
          return a.grupo.localeCompare(b.grupo);
        }),
    }))
    .sort((a, b) => a.nombre.localeCompare(b.nombre));
}

export default function Docentes() {
  const [docentes, setDocentes] = useState([]);
  const [horariosImportados, setHorariosImportados] = useState([]);

  const cargar = async () => {
    const [docentesRes, horariosRes] = await Promise.all([
      api.get("/docentes/"),
      api.get("/horarios/", { params: { origen: "importado" } }),
    ]);
    setDocentes(docentesRes.data);
    setHorariosImportados(horariosRes.data);
  };

  useEffect(() => {
    cargar();
  }, []);

  const resumenDocentes = construirResumenDocentes(docentes, horariosImportados);

  return (
    <section>
      <h1>Docentes</h1>
      <p className="subtitulo">
        Docentes importados desde el horario base. Aqui se muestran las materias que dicta cada docente y sus bloques reales.
      </p>

      <div className="table-card">
        <div className="docentes-list">
          {resumenDocentes.map((docente) => (
            <article key={docente.id} className="docente-card">
              <div className="docente-header">
                <div>
                  <h3>{docente.nombre}</h3>
                  <p>{docente.correo || "Sin correo registrado"}</p>
                </div>
              </div>

              {docente.materias.length === 0 ? (
                <span className="docente-empty">Este docente no tiene horarios importados asignados.</span>
              ) : (
                <div className="docente-materias">
                  {docente.materias.map((materia) => (
                    <section
                      key={`${docente.id}-${materia.materia_id}-${materia.grupo}`}
                      className="docente-materia-card"
                    >
                      <div className="docente-materia-header">
                        <div>
                          <strong>{materia.sigla} {materia.materia}</strong>
                          <span>Nivel {String.fromCharCode(64 + materia.semestre)} | {materia.grupo} | {materia.tipo}</span>
                        </div>
                      </div>

                      <div className="docente-slots">
                        {materia.slots.map((slot) => (
                          <span
                            key={`${materia.materia_id}-${materia.grupo}-${slot.dia}-${slot.bloque}-${slot.aula}`}
                            className="docente-slot"
                          >
                            {slot.dia} {slot.bloque} | {slot.aula}
                          </span>
                        ))}
                      </div>
                    </section>
                  ))}
                </div>
              )}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
