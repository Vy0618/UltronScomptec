import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  selectSignalOutputMachines,
  OUTPUT_LEVELS,
} from "../../services/signalOutputs";
import SignalOutputList from "./signalOutputList";
import Pagination from "../pagination/pagination";
import StatusBadge from "../statusBadge/statusBadge";
import { formatDateTime } from "../../utils/time";

const PAGE_SIZE = 6;
export default function FleetSignalOutputs({ machines, loading, error }) {
  const [machineId, setMachineId] = useState("");
  const [level, setLevel] = useState("");
  const [page, setPage] = useState(1);
  const selected = machines.some((machine) => machine.id === machineId)
    ? machineId
    : "";
  const rows = useMemo(
    () => selectSignalOutputMachines(machines, selected, level),
    [machines, selected, level],
  );
  const currentPage = Math.min(
    page,
    Math.max(1, Math.ceil(rows.length / PAGE_SIZE)),
  );
  return (
    <section
      aria-labelledby="signal-outputs-title"
      className="panel space-y-4 p-4 sm:p-5"
    >
      <div>
        <h2
          id="signal-outputs-title"
          className="text-base font-extrabold text-text-primary"
        >
          Interações entre sinais
        </h2>
        <p className="mt-1 text-xs text-text-muted">
          Resultados das combinações recebidas. A interpretação acompanha cada
          leitura, sem substituir o estado da máquina.
        </p>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="space-y-1 text-sm text-text-secondary">
          <span>Máquina das interações</span>
          <select
            className="input-field"
            value={selected}
            onChange={(event) => {
              setMachineId(event.target.value);
              setPage(1);
            }}
          >
            <option value="">Todas as máquinas</option>
            {machines.map((machine) => (
              <option key={machine.id} value={machine.id}>
                {machine.id} — {machine.name}
              </option>
            ))}
          </select>
        </label>
        <label className="space-y-1 text-sm text-text-secondary">
          <span>Nível das interações</span>
          <select
            className="input-field"
            value={level}
            onChange={(event) => {
              setLevel(event.target.value);
              setPage(1);
            }}
          >
            <option value="">Todos os níveis</option>
            {Object.entries(OUTPUT_LEVELS).map(([value, config]) => (
              <option key={value} value={value}>
                {config.label}
              </option>
            ))}
          </select>
        </label>
      </div>
      {error && (
        <p role="status" className="text-xs text-amber-600">
          Sem confirmação atual da API. As interpretações disponíveis pertencem
          à última leitura conhecida.
        </p>
      )}
      {!rows.length ? (
        <p role="status" className="py-4 text-sm text-text-muted">
          {loading
            ? "Carregando interpretações…"
            : selected || level
              ? "Nenhuma interpretação corresponde aos filtros."
              : "Aguardando interpretações dos sinais pela API."}
        </p>
      ) : (
        <div className="grid min-w-0 gap-4 lg:grid-cols-2">
          {rows
            .slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE)
            .map(({ machine, outputs, stale }) => (
              <article
                key={machine.id}
                className="min-w-0 space-y-3 rounded-xl border border-base-border p-3"
              >
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <Link
                    to={`/maquinas/${encodeURIComponent(machine.id)}`}
                    className="min-w-0 break-words text-sm font-bold text-accent"
                  >
                    {machine.id} · {machine.name}
                  </Link>
                  <StatusBadge status={machine.status} size="sm" />
                </div>
                {stale && (
                  <p className="text-xs text-amber-600">
                    Últimas interpretações conhecidas; aguardando leitura atual.
                  </p>
                )}
                <SignalOutputList outputs={outputs} stale={stale} limit={2} />
                <p className="text-xs text-text-muted">
                  Leitura: {formatDateTime(machine.telemetryTimestamp)}
                </p>
                <Link
                  className="inline-block text-xs font-semibold text-accent underline"
                  to={`/maquinas/${encodeURIComponent(machine.id)}`}
                >
                  {outputs.length > 2
                    ? `Ver as ${outputs.length} interpretações nos detalhes`
                    : "Ver sinais e detalhes"}
                </Link>
              </article>
            ))}
        </div>
      )}
      {rows.length > PAGE_SIZE && (
        <Pagination
          page={currentPage}
          total={rows.length}
          pageSize={PAGE_SIZE}
          onChange={setPage}
        />
      )}
    </section>
  );
}
