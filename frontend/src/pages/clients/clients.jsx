import ClientCard from "../../components/clientCard/clientCard";

import { useMonitoring } from "../../contexts/monitoringContext";
import EmptyState from "../../components/emptyState/emptyState";

export default function Clients() {
  const { companies } = useMonitoring();

  return (
    <div className="space-y-6 animate-fadeUp">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-2xl font-extrabold tracking-tight text-text-primary">
              Clientes Industriais
            </h1>
            <span className="rounded-full bg-accent-soft border border-accent/30 px-2.5 py-0.5 text-[10px] font-bold text-accent">
              {companies.length} EMPRESAS CONECTADAS
            </span>
          </div>
          <p className="mt-1 text-xs text-text-muted">
            Gestão de contas corporativas, plantas industriais e situação
            operacional de cada cliente.
          </p>
        </div>
      </div>

      {/* Grid of Clients */}
      {companies.length === 0 && (
        <EmptyState
          title="Gestão de clientes indisponível"
          description="Esta instalação monitora máquinas diretamente. Acesse Máquinas CNC para acompanhar os equipamentos cadastrados."
        />
      )}
      <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        {companies.map((company) => (
          <ClientCard key={company.id} company={company} />
        ))}
      </div>
    </div>
  );
}
