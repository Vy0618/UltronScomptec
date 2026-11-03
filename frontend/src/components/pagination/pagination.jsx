export default function Pagination({
  page,
  total,
  pageSize,
  onChange,
  loading = false,
}) {
  const pages = Math.max(1, Math.ceil(total / pageSize));
  return (
    <nav
      aria-label="Paginação"
      className="flex flex-wrap items-center justify-between gap-3 text-sm"
    >
      <p className="text-text-muted">
        Página {page} de {pages} · {total} registros
      </p>
      <div className="flex gap-2">
        <button
          type="button"
          className="btn-secondary"
          disabled={page <= 1 || loading}
          onClick={() => onChange(page - 1)}
        >
          Anterior
        </button>
        <button
          type="button"
          className="btn-secondary"
          disabled={page >= pages || loading}
          onClick={() => onChange(page + 1)}
        >
          Próxima
        </button>
      </div>
    </nav>
  );
}
