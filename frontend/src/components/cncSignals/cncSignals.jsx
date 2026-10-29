import { observedStates } from "../../services/cncSignals";

export default function CncSignals({ machine }) {
  const stale = machine.dataStale || machine.communicationStatus !== "ONLINE" ||
    ["SEM_COMUNICACAO", "DADOS_DESATUALIZADOS"].includes(machine.status);
  return <section className="panel space-y-4 p-5 lg:col-span-2">
    <div>
      <h2 className="text-sm font-bold text-text-primary">Estados da máquina</h2>
      <p className="mt-1 text-xs text-text-muted">Últimos estados recebidos, independentemente da origem dos dados.</p>
    </div>
    {stale && <p role="status" className="text-xs text-amber-500">Comunicação indisponível ou leitura desatualizada. Os valores exibidos pertencem à última leitura recebida.</p>}
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {observedStates(machine.digitalSignals).map(({ key, label }) => {
        const active = machine.digitalSignals?.[key];
        const known = typeof active === "boolean";
        return <div key={key} className="flex items-center justify-between gap-3 rounded-lg border border-base-border bg-base-card/60 p-3">
          <div>
            <p className="text-xs font-semibold text-text-primary">{label}</p>
          </div>
          <span className={`text-xs font-bold ${known && active ? "text-accent" : "text-text-muted"}`}>
            {known ? active ? "ATIVO" : "INATIVO" : "NÃO INFORMADO"}
          </span>
        </div>;
      })}
    </div>
  </section>;
}
