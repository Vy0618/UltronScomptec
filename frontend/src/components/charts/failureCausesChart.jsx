import { useId, useMemo } from "react";
import { ChartPie } from "lucide-react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { summarizeFailureCauses } from "../../services/failureCauses";

const percentage = (value) => `${value.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`;
const occurrences = (count) => `${count.toLocaleString("pt-BR")} ${count === 1 ? "ocorrência" : "ocorrências"}`;

function CauseTooltip({ active, payload }) {
  const cause = payload?.[0]?.payload;
  if (!active || !cause) return null;
  return (
    <div className="rounded-xl border border-base-border bg-base-surface p-3 text-xs shadow-xl">
      <p className="font-semibold text-text-primary">{cause.label}</p>
      <p className="mt-1 text-text-secondary">
        {occurrences(cause.count)} · {percentage(cause.percentage)}
      </p>
    </div>
  );
}

export default function FailureCausesChart({ machines, hours, loading, demoMode, error }) {
  const headingId = useId();
  const result = useMemo(() => summarizeFailureCauses(machines, hours), [machines, hours]);
  return (
    <section aria-labelledby={headingId} className="space-y-4 border-t border-base-border/70 pt-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 id={headingId} className="flex items-center gap-2 text-sm font-bold text-text-primary">
            <ChartPie size={16} className="text-accent" />
            Principais causas de falhas
          </h3>
          <p className="mt-1 text-xs text-text-muted">Novos acionamentos dos parâmetros da IHM nas últimas {hours}h.</p>
        </div>
        {result.total > 0 && (
          <span className="rounded-full border border-base-border bg-base-surface/60 px-3 py-1.5 text-xs font-semibold text-text-primary">
            {occurrences(result.total)}
          </span>
        )}
      </div>
      {error && <p role="status" className="text-xs text-amber-600">Atualização indisponível. Exibindo o último histórico de causas disponível.</p>}
      {result.total > 0 ? (
        <div className="grid min-w-0 items-center gap-4 sm:grid-cols-2">
          <div
            role="img"
            aria-label={`Causas de falhas: ${result.data.map((cause) => `${cause.label}, ${occurrences(cause.count)}, ${percentage(cause.percentage)}`).join("; ")}.`}
            className="h-64 w-full min-w-0"
          >
            <ResponsiveContainer width="100%" height="100%">
              <PieChart accessibilityLayer>
                <Pie
                  data={result.data}
                  dataKey="count"
                  nameKey="label"
                  cx="50%"
                  cy="50%"
                  outerRadius="85%"
                  startAngle={90}
                  endAngle={-270}
                  stroke="rgb(var(--base-card))"
                  strokeWidth={2}
                  isAnimationActive={false}
                >
                  {result.data.map((cause) => <Cell key={cause.key} fill={cause.color} />)}
                </Pie>
                <Tooltip content={<CauseTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <ul aria-label="Legenda das causas de falhas" className="min-w-0 space-y-2">
            {result.data.map((cause) => (
              <li key={cause.key} className="flex items-center gap-3 rounded-lg border border-base-border/70 bg-base-surface/40 p-3 text-xs">
                <span aria-hidden="true" className="h-3 w-3 shrink-0 rounded-full" style={{ backgroundColor: cause.color }} />
                <div className="min-w-0 flex-1">
                  <p className="break-words font-semibold text-text-primary">{cause.label}</p>
                  <p className="mt-1 text-text-muted">{occurrences(cause.count)}</p>
                </div>
                <span className="shrink-0 font-mono font-bold text-text-primary">{percentage(cause.percentage)}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div role="status" className="flex min-h-44 flex-col items-center justify-center gap-3 rounded-xl border border-base-border/70 bg-base-bg/30 p-6 text-center text-sm text-text-muted">
          <ChartPie size={28} className="text-text-dim" />
          <p>{loading ? "Carregando causas de falhas…" : !result.available ? demoMode ? "Sem histórico de causas no modo de demonstração." : "Aguardando histórico das causas de falhas." : result.samples ? "Nenhum novo acionamento de falha registrado no período." : "Aguardando leituras no período selecionado."}</p>
        </div>
      )}
      <p className="text-[11px] leading-relaxed text-text-muted">
        Cada novo acionamento conta uma ocorrência por causa. Leituras repetidas não aumentam a contagem.
        {" "}Causas simultâneas são contabilizadas separadamente. Após uma lacuna de comunicação, um sinal acionado inicia uma nova ocorrência observada.
      </p>
    </section>
  );
}
