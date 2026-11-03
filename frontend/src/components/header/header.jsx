import { useState, useRef, useEffect } from "react";
import {
  Menu,
  Search,
  Bell,
  ChevronDown,
  Sliders,
  LogOut,
  Sun,
  Moon,
  X,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { clearSession, readSessionUser } from "../../services/adminSession";
import { useMonitoring } from "../../contexts/monitoringContext";
import ContextSwitcher from "../contextSwitcher/contextSwitcher";
import { getStatusConfig } from "../../utils/status";
import { savePreferences, usePreferences } from "../../services/preferences";

const alertKey = (alert) =>
  JSON.stringify([
    alert.id,
    alert.severity,
    alert.occurredAt || alert.stateSince,
  ]);
export default function Header({ onMenuClick }) {
  const navigate = useNavigate();
  const preferences = usePreferences();
  const user = readSessionUser() || { name: "Visitante", email: "" };
  const [panel, setPanel] = useState(null);
  const [search, setSearch] = useState("");
  const [readAlerts, setReadAlerts] = useState(() => new Set());
  const root = useRef(null);
  const searchInput = useRef(null);
  const trigger = useRef(null);
  const { alerts, demoMode, apiConnected, connectionError, loading } =
    useMonitoring();
  const unread = alerts.filter(
    (alert) => !readAlerts.has(alertKey(alert)),
  ).length;
  const markRead = (items) =>
    setReadAlerts(
      (current) => new Set([...current, ...items.map(alertKey)].slice(-500)),
    );
  const toggle = (name, event) => {
    trigger.current = event.currentTarget;
    setPanel((current) => (current === name ? null : name));
  };
  useEffect(() => {
    const click = (event) => {
      if (!root.current?.contains(event.target)) setPanel(null);
    };
    const keyboard = (event) => {
      if (event.key === "Escape") {
        setPanel(null);
        trigger.current?.focus();
      }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        trigger.current = document.getElementById("global-search-trigger");
        setPanel("search");
      }
    };
    document.addEventListener("pointerdown", click);
    document.addEventListener("keydown", keyboard);
    return () => {
      document.removeEventListener("pointerdown", click);
      document.removeEventListener("keydown", keyboard);
    };
  }, []);
  useEffect(() => {
    if (panel === "search") searchInput.current?.focus();
  }, [panel]);
  const submit = (event) => {
    event.preventDefault();
    navigate(
      `/maquinas${search.trim() ? `?busca=${encodeURIComponent(search.trim())}` : ""}`,
    );
    setPanel(null);
  };
  const connectionLabel = demoMode
    ? "DEMONSTRAÇÃO"
    : loading
      ? "CONECTANDO"
      : apiConnected
        ? "CONECTADO"
        : "SEM CONEXÃO";
  return (
    <header
      ref={root}
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) setPanel(null);
      }}
      className="sticky top-0 z-30 flex min-h-16 items-center justify-between gap-2 border-b border-base-border bg-base-surface px-3 py-2 sm:px-6"
    >
      <div className="flex min-w-0 flex-1 items-center gap-2">
        <button
          id="navigation-trigger"
          type="button"
          onClick={onMenuClick}
          aria-label="Abrir menu"
          aria-controls="app-navigation"
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-base-border text-text-secondary lg:hidden"
        >
          <Menu size={20} />
        </button>
        <ContextSwitcher
          open={panel === "context"}
          onToggle={(event) => toggle("context", event)}
          onClose={() => setPanel(null)}
        />
      </div>
      <div className="flex shrink-0 items-center gap-1.5 sm:gap-2">
        <span
          role="status"
          title={connectionError || ""}
          className={`hidden rounded-full border px-3 py-1 text-xs font-semibold xl:block ${apiConnected || demoMode ? "border-accent/20 text-accent" : "border-base-border text-text-muted"}`}
        >
          {connectionLabel}
        </span>
        <button
          type="button"
          onClick={() =>
            savePreferences({
              ...preferences,
              theme: preferences.theme === "light" ? "dark" : "light",
            })
          }
          aria-label={
            preferences.theme === "light"
              ? "Ativar tema escuro"
              : "Ativar tema claro"
          }
          className="hidden h-11 w-11 items-center justify-center rounded-lg border border-base-border text-text-secondary sm:flex"
        >
          {preferences.theme === "light" ? (
            <Moon size={18} />
          ) : (
            <Sun size={18} />
          )}
        </button>
        <button
          type="button"
          id="global-search-trigger"
          onClick={(event) => toggle("search", event)}
          aria-expanded={panel === "search"}
          aria-controls="global-search"
          aria-label="Buscar máquinas"
          title="Buscar máquinas (Ctrl+K)"
          className="flex h-11 w-11 items-center justify-center rounded-lg border border-base-border text-text-secondary"
        >
          <Search size={18} />
        </button>
        <button
          type="button"
          onClick={(event) => toggle("alerts", event)}
          aria-expanded={panel === "alerts"}
          aria-controls="header-alerts"
          aria-label={`Notificações: ${unread} alertas não lidos`}
          className="relative flex h-11 w-11 items-center justify-center rounded-lg border border-base-border text-text-secondary"
        >
          <Bell size={18} />
          {preferences.showBadge && unread > 0 && (
            <span className="absolute -right-1 -top-1 rounded-full bg-accent px-1.5 text-[11px] font-bold text-white">
              {unread > 99 ? "99+" : unread}
            </span>
          )}
        </button>
        <button
          type="button"
          onClick={(event) => toggle("user", event)}
          aria-label="Menu da conta"
          aria-expanded={panel === "user"}
          aria-controls="user-menu"
          className="flex h-11 min-w-11 items-center justify-center gap-2 rounded-lg border border-base-border px-2 text-text-primary"
        >
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/10 text-sm font-bold text-accent">
            {user.name.charAt(0)}
          </span>
          <span className="hidden max-w-36 truncate text-xs font-semibold sm:block">
            {user.name}
          </span>
          <ChevronDown size={12} className="hidden sm:block" />
        </button>
      </div>
      {panel === "search" && (
        <form
          id="global-search"
          role="search"
          onSubmit={submit}
          className="absolute left-3 right-3 top-full mt-2 flex gap-2 rounded-xl border border-base-border bg-base-surface p-3 shadow-panel sm:left-auto sm:w-[min(500px,calc(100vw-2rem))]"
        >
          <label className="sr-only" htmlFor="global-machine-search">
            Buscar máquinas por nome ou código
          </label>
          <input
            id="global-machine-search"
            ref={searchInput}
            className="input-field min-w-0"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Nome ou código da CNC"
          />
          <button className="btn-primary" type="submit">
            Buscar
          </button>
          <button
            className="px-2 text-text-muted"
            type="button"
            aria-label="Fechar busca"
            onClick={() => {
              setPanel(null);
              trigger.current?.focus();
            }}
          >
            <X size={18} />
          </button>
        </form>
      )}
      {panel === "alerts" && (
        <section
          id="header-alerts"
          aria-label="Notificações"
          className="absolute left-3 right-3 top-full mt-2 overflow-hidden rounded-xl border border-base-border bg-base-surface shadow-panel sm:left-auto sm:w-96"
        >
          <div className="flex items-center justify-between gap-3 border-b border-base-border p-3">
            <h2 className="text-sm font-bold">
              {alerts.length} alertas ativos
            </h2>
            {unread > 0 && (
              <button
                type="button"
                onClick={() => markRead(alerts)}
                className="text-xs font-semibold text-accent"
              >
                Marcar como lidos
              </button>
            )}
          </div>
          <ul className="max-h-[50svh] divide-y divide-base-border overflow-y-auto">
            {alerts.slice(0, 50).map((alert) => {
              const config = getStatusConfig(alert.severity);
              const Icon = config.icon;
              return (
                <li key={alertKey(alert)}>
                  <Link
                    to={`/maquinas/${encodeURIComponent(alert.machineId)}`}
                    onClick={() => {
                      markRead([alert]);
                      setPanel(null);
                    }}
                    className={`flex gap-3 p-3 hover:bg-base-cardHover ${preferences.compactAlerts ? "py-2.5" : "py-4"}`}
                  >
                    <Icon
                      size={18}
                      className={`mt-1 shrink-0 ${config.text}`}
                    />
                    <span className="min-w-0">
                      <strong className={`block text-xs ${config.text}`}>
                        {config.label}
                      </strong>
                      <span className="mt-1 block break-words text-sm">
                        {alert.machineId} · {alert.machineName}
                      </span>
                    </span>
                    {!readAlerts.has(alertKey(alert)) && (
                      <span
                        className="ml-auto mt-2 h-2 w-2 shrink-0 rounded-full bg-accent"
                        aria-label="Não lido"
                      />
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
          {!alerts.length && (
            <p className="p-4 text-sm text-text-muted">
              {loading
                ? "Carregando alertas…"
                : connectionError
                  ? "Alertas sem confirmação atual."
                  : "Nenhum alerta ativo."}
            </p>
          )}
          <Link
            to="/alertas"
            onClick={() => setPanel(null)}
            className="block border-t border-base-border p-3 text-center text-sm font-semibold text-accent"
          >
            Ver todos os alertas
          </Link>
        </section>
      )}
      {panel === "user" && (
        <section
          id="user-menu"
          aria-label="Conta"
          className="absolute right-3 top-full mt-2 w-[min(280px,calc(100vw-1.5rem))] space-y-2 rounded-xl border border-base-border bg-base-surface p-3 shadow-panel"
        >
          <p className="break-words text-sm font-semibold">{user.name}</p>
          <p className="break-all text-xs text-text-muted">{user.email}</p>
          <Link
            to="/configuracoes"
            onClick={() => setPanel(null)}
            className="flex min-h-11 items-center gap-2 text-sm text-text-secondary"
          >
            <Sliders size={16} />
            Configurações da conta
          </Link>
          <Link
            to="/login"
            onClick={() => {
              clearSession();
              setPanel(null);
            }}
            className="flex min-h-11 items-center gap-2 text-sm text-rose-400"
          >
            <LogOut size={16} />
            Encerrar sessão
          </Link>
        </section>
      )}
    </header>
  );
}
