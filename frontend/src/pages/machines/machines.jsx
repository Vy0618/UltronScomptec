import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, TriangleAlert, X, Factory } from "lucide-react";
import MachineCard from "../../components/machineCard/machineCard";
import EmptyState from "../../components/emptyState/emptyState";
import LoadingState from "../../components/loadingState/loadingState";
import { useMachines } from "../../hooks/useMachines";
import { useMonitoring } from "../../contexts/monitoringContext";
import { isActiveProblem } from "../../utils/problems";
import Pagination from "../../components/pagination/pagination";

const QUICK_FILTERS = [
  ["ALL", "Todas", "total"],
  ["OPERANDO", "Operando", "operating"],
  ["PARADA", "Paradas", "stopped"],
  ["ALARME", "Alarmes", "alarms"],
  ["EMERGENCIA", "Emergências", "emergencies"],
  ["SEM_COMUNICACAO", "Offline", "offline"],
];

export default function Machines() {
  const { machines, loading, error } = useMachines();
  const { scopeSummary, selectedScope, companies, units } = useMonitoring();
  const [searchParams, setSearchParams] = useSearchParams();

  const [query, setQuery] = useState(searchParams.get("busca") || "");
  const [requestedPage, setPage] = useState(1);
  const requestedSearch = searchParams.get("busca") || "";
  useEffect(() => {
    setQuery(requestedSearch);
    setPage(1);
  }, [requestedSearch]);
  const statusFilter = searchParams.get("status") || "ALL";
  const onlyProblems = searchParams.get("problemas") === "1";
  const sectorId = searchParams.get("setor");
  const unitId = searchParams.get("unidade");

  const updateParams = (changes) => {
    setPage(1);
    const next = new URLSearchParams(searchParams);
    Object.entries(changes).forEach(([key, value]) =>
      value ? next.set(key, value) : next.delete(key),
    );
    setSearchParams(next);
  };

  const filtered = useMemo(
    () =>
      machines
        .filter(
          (machine) =>
            (machine.name.toLowerCase().includes(query.toLowerCase()) ||
              machine.id.toLowerCase().includes(query.toLowerCase())) &&
            (statusFilter === "ALL" ||
              machine.status === statusFilter ||
              (statusFilter === "SEM_COMUNICACAO" &&
                machine.status === "DADOS_DESATUALIZADOS")) &&
            (!onlyProblems || isActiveProblem(machine.status)) &&
            (!sectorId || machine.sectorId === sectorId) &&
            (!unitId || machine.unitId === unitId),
        )
        .sort((a, b) =>
          statusFilter === "PARADA"
            ? new Date(a.stateSince).getTime() -
              new Date(b.stateSince).getTime()
            : 0,
        ),
    [machines, query, statusFilter, onlyProblems, sectorId, unitId],
  );
  const page = Math.min(
    requestedPage,
    Math.max(1, Math.ceil(filtered.length / 24)),
  );

  return (
    <div className="space-y-6 animate-fadeUp">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-text-primary">
            Máquinas CNC
          </h1>
          <p className="text-xs text-text-muted">
            {scopeSummary.total} equipamentos conectados no contexto
            selecionado.
          </p>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="panel p-3.5 sm:p-4 space-y-3">
        <div className="flex flex-col gap-2.5 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted"
            />
            <input
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setPage(1);
              }}
              aria-label="Buscar máquinas"
              placeholder="Buscar por ID, modelo ou CNC..."
              className="input-field pl-9 text-xs w-full"
            />
            {query && (
              <button
                onClick={() => setQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary"
              >
                <X size={14} />
              </button>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() =>
                updateParams({
                  problemas: onlyProblems ? null : "1",
                  status: null,
                })
              }
              className={`inline-flex w-full sm:w-auto justify-center items-center gap-1.5 rounded-lg border px-3 py-2 text-xs font-semibold transition-all ${
                onlyProblems
                  ? "border-amber-500/40 bg-amber-500/15 text-amber-400 shadow-sm"
                  : "border-base-border bg-base-card/80 text-text-secondary hover:border-base-borderLight hover:text-text-primary"
              }`}
            >
              <TriangleAlert
                size={14}
                className={onlyProblems ? "text-amber-400" : "text-text-muted"}
              />
              <span>Somente Problemas</span>
            </button>
          </div>
        </div>

        {/* Quick status tabs (horizontally scrollable on mobile) */}
        <div className="flex items-center gap-1.5 border-t border-base-border/70 pt-3 overflow-x-auto pb-1 sm:pb-0 sm:flex-wrap">
          {QUICK_FILTERS.map(([value, label, key]) => {
            const active = statusFilter === value && !onlyProblems;
            const count = scopeSummary[key] ?? 0;

            return (
              <button
                key={value}
                onClick={() =>
                  updateParams({
                    status: value === "ALL" ? null : value,
                    problemas: null,
                  })
                }
                className={`flex shrink-0 items-center gap-1.5 sm:gap-2 rounded-lg border px-2.5 sm:px-3 py-1.5 text-xs font-medium transition-all ${
                  active
                    ? "border-accent/40 bg-accent-soft text-accent shadow-glowGreenSm font-semibold"
                    : "border-base-border/70 bg-base-card/60 text-text-secondary hover:border-base-borderLight hover:bg-base-card hover:text-text-primary"
                }`}
              >
                <span>{label}</span>
                <span
                  className={`data-mono rounded px-1.5 py-0.2 text-[10px] font-bold ${
                    active
                      ? "bg-accent/20 text-accent"
                      : "bg-base-surface text-text-muted"
                  }`}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Sector filter banner if applied */}
      {(sectorId || unitId) && (
        <div className="flex items-center justify-between rounded-xl border border-accent/30 bg-accent-soft px-4 py-2.5 text-xs text-accent">
          <div className="flex items-center gap-2">
            <Factory size={15} />
            <span>Filtro ativo por estrutura fabril/setor selecionado</span>
          </div>
          <button
            onClick={() => updateParams({ setor: null, unidade: null })}
            className="inline-flex items-center gap-1 font-semibold hover:underline"
          >
            <X size={13} /> Limpar filtro de setor
          </button>
        </div>
      )}

      {/* Machine Grid */}
      {loading ? (
        <LoadingState />
      ) : error && machines.length === 0 ? (
        <EmptyState
          title="Não foi possível consultar as máquinas"
          description={error}
        />
      ) : filtered.length === 0 ? (
        <EmptyState
          title="Nenhuma máquina encontrada"
          description="Nenhuma máquina CNC corresponde aos filtros ou busca aplicados."
        />
      ) : (
        <div className="machine-grid">
          {filtered.slice((page - 1) * 24, page * 24).map((machine) => (
            <MachineCard
              key={machine.id}
              machine={machine}
              contextLabel={
                selectedScope.type === "global"
                  ? [
                      companies.find((item) => item.id === machine.companyId)
                        ?.name,
                      units.find((item) => item.id === machine.unitId)?.name,
                    ]
                      .filter(Boolean)
                      .join(" · ")
                  : ""
              }
            />
          ))}
        </div>
      )}
      {filtered.length > 24 && (
        <Pagination
          page={page}
          total={filtered.length}
          pageSize={24}
          onChange={setPage}
        />
      )}
    </div>
  );
}
