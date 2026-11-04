import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { RefreshCw } from "lucide-react";
import StatusBadge from "../../components/statusBadge/statusBadge";
import EmptyState from "../../components/emptyState/emptyState";
import OccurrenceCard from "../../components/occurrenceCard/occurrenceCard";
import Pagination from "../../components/pagination/pagination";
import { useMonitoring } from "../../contexts/monitoringContext";
import { useApiQuery } from "../../hooks/useApiQuery";
import { readingEvent } from "../../services/telemetry";
import api from "../../services/api";

const PAGE_SIZE = 30;
export default function History() {
  const { allEvents, allMachines, demoMode } = useMonitoring();
  const [machineFilter, setMachineFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [viewMode, setViewMode] = useState("cards");
  const [page, setPage] = useState(1);
  const [snapshot, setSnapshot] = useState(() => new Date().toISOString());
  const params = {
    page,
    limit: PAGE_SIZE,
    end: snapshot,
    ...(machineFilter ? { machine_id: machineFilter } : {}),
  };
  const query = useApiQuery(
    demoMode ? null : `fleet-history:${new URLSearchParams(params)}`,
    (signal) => api.getFleetHistory(params, { signal }),
    60000,
  );
  const byId = useMemo(
    () => new Map(allMachines.map((machine) => [machine.backendId, machine])),
    [allMachines],
  );
  const events = useMemo(
    () =>
      demoMode
        ? allEvents
        : (query.data?.items || []).map((reading) => {
            const machine = byId.get(reading.machine_id) || {
              id: reading.machine_id,
              name: "Máquina",
            };
            return readingEvent(reading, machine);
          }),
    [demoMode, allEvents, query.data, byId],
  );
  const total = demoMode ? events.length : query.data?.total || 0;
  const pageEvents = demoMode
    ? events.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)
    : events;
  const filtered = pageEvents.filter(
    (event) => !statusFilter || event.status === statusFilter,
  );
  const refresh = () => {
    setSnapshot(new Date().toISOString());
    setPage(1);
  };

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold">Histórico de Leituras</h1>
          <p className="mt-1 text-sm text-text-muted">
            Histórico paginado do banco. Cada leitura registra os estados
            observados da CNC.
          </p>
        </div>
        <button type="button" className="btn-secondary" onClick={refresh}>
          <RefreshCw size={16} />
          Atualizar histórico
        </button>
      </div>
      <div className="panel grid gap-4 p-4 sm:grid-cols-2">
        <label className="space-y-2 text-sm text-text-secondary">
          <span>Máquina CNC</span>
          <select
            className="input-field"
            value={machineFilter}
            onChange={(event) => {
              setMachineFilter(event.target.value);
              setPage(1);
            }}
          >
            <option value="">Todas as máquinas</option>
            {allMachines.map((machine) => (
              <option key={machine.id} value={machine.backendId}>
                {machine.id} — {machine.name}
              </option>
            ))}
          </select>
        </label>
        <label className="space-y-2 text-sm text-text-secondary">
          <span>Estado nesta página</span>
          <select
            className="input-field"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="">Todos os estados</option>
            {[
              "OPERANDO",
              "PARADA",
              "ALARME",
              "EMERGENCIA",
              "MANUTENCAO",
              "DESLIGADA",
            ].map((status) => (
              <option key={status}>{status}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div
          role="group"
          aria-label="Visualização do histórico"
          className="flex gap-2"
        >
          <button
            type="button"
            className="btn-secondary"
            aria-pressed={viewMode === "cards"}
            onClick={() => setViewMode("cards")}
          >
            Cards Detalhados
          </button>
          <button
            type="button"
            className="btn-secondary"
            aria-pressed={viewMode === "table"}
            onClick={() => setViewMode("table")}
          >
            Tabela Compacta
          </button>
        </div>
        <p className="text-xs text-text-muted">
          Consulta até {new Date(snapshot).toLocaleString("pt-BR")}
        </p>
      </div>
      {query.error && (
        <p role="alert" className="panel p-4 text-sm text-amber-500">
          Não foi possível atualizar o histórico. {query.error}
        </p>
      )}
      {query.loading ? (
        <p role="status">Carregando histórico…</p>
      ) : filtered.length === 0 ? (
        <EmptyState
          title="Nenhuma leitura encontrada"
          description={
            statusFilter
              ? "Nenhuma leitura desta página corresponde ao estado selecionado."
              : "Não há leituras disponíveis para a consulta."
          }
        />
      ) : viewMode === "cards" ? (
        <div className="machine-grid">
          {filtered.map((event) => (
            <OccurrenceCard
              key={event.id}
              event={event}
              machine={allMachines.find(
                (machine) => machine.id === event.machineId,
              )}
            />
          ))}
        </div>
      ) : (
        <div
          className="panel overflow-x-auto"
          tabIndex={0}
          aria-label="Tabela de leituras; role horizontalmente para ver todas as colunas"
        >
          <table className="history-table">
            <caption className="sr-only">Leituras de telemetria</caption>
            <thead>
              <tr>
                <th>Data e hora</th>
                <th>Máquina</th>
                <th>Estado</th>
                <th>Detalhes</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((event) => (
                <tr key={event.id}>
                  <td>
                    <time dateTime={event.occurredAt}>
                      {new Date(event.occurredAt).toLocaleString("pt-BR")}
                    </time>
                  </td>
                  <td>{event.machineId}</td>
                  <td>
                    <StatusBadge status={event.status} size="sm" />
                  </td>
                  <td>
                    <Link
                      className="text-accent underline"
                      to={`/maquinas/${encodeURIComponent(event.machineId)}`}
                    >
                      Ver máquina
                    </Link>
                    <p className="mt-1 max-w-64 whitespace-normal text-xs text-text-muted">
                      {event.signalOutputs
                        ?.slice(0, 2)
                        .map((output) => output.title)
                        .join(" · ")}
                    </p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <Pagination
        page={page}
        total={total}
        pageSize={PAGE_SIZE}
        loading={query.loading}
        onChange={setPage}
      />
    </div>
  );
}
