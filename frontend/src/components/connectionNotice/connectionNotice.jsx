import { useMonitoring } from "../../contexts/monitoringContext";

export default function ConnectionNotice() {
  const { demoMode, loading, connectionError, dataWarning, lastSync } = useMonitoring();
  if (demoMode || (!loading && !connectionError && !dataWarning)) return null;
  return <div role="status" className="m-3 rounded-lg border border-amber-500/40 bg-amber-500/10 p-3 text-sm text-amber-300">
    {loading ? "Conectando ao servidor de monitoramento…" : connectionError ? "Sem conexão com o backend. Tentando reconectar automaticamente." : dataWarning}
    {connectionError && <span className="block text-xs">{connectionError}</span>}
    {connectionError && lastSync && <span className="block text-xs">Última atualização confirmada: {lastSync.toLocaleString("pt-BR")}. As leituras exibidas estão desatualizadas; os alertas conhecidos foram preservados.</span>}
  </div>;
}
