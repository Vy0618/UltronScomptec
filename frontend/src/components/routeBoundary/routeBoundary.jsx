import { Component, Suspense } from "react";
import { Link, useLocation } from "react-router-dom";

class PageError extends Component {
  state = { failed: false, resetKey: this.props.resetKey };
  static getDerivedStateFromProps(props, state) {
    return props.resetKey !== state.resetKey
      ? { failed: false, resetKey: props.resetKey }
      : null;
  }
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(error) {
    console.error("Falha ao abrir a página", error);
  }
  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <section
        role="alert"
        className="mx-auto my-12 max-w-lg space-y-4 rounded-xl border border-base-border bg-base-surface p-6"
      >
        <h1 className="text-xl font-bold">
          Não foi possível abrir esta página.
        </h1>
        <p className="text-sm text-text-secondary">
          Tente novamente ou retorne ao painel de monitoramento.
        </p>
        <div className="flex flex-wrap gap-3">
          <button
            className="btn-primary"
            onClick={() => window.location.reload()}
          >
            Tentar novamente
          </button>
          <Link className="btn-secondary" to="/dashboard">
            Voltar ao painel
          </Link>
        </div>
      </section>
    );
  }
}

export default function RouteBoundary({ children }) {
  const { pathname } = useLocation();
  return (
    <PageError resetKey={pathname}>
      <Suspense
        fallback={
          <p role="status" className="p-6 text-sm text-text-secondary">
            Carregando página…
          </p>
        }
      >
        {children}
      </Suspense>
    </PageError>
  );
}
