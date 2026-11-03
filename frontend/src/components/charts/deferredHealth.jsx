import { lazy, Suspense, useEffect, useRef, useState } from "react";

const FleetHealth = lazy(() => import("./fleetHealth"));
export default function DeferredHealth(props) {
  const root = useRef(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    if (!window.IntersectionObserver) {
      setVisible(true);
      return undefined;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: "150px" },
    );
    observer.observe(root.current);
    return () => observer.disconnect();
  }, []);
  const placeholder = (
    <div
      className="flex min-h-64 items-center justify-center text-sm text-text-muted"
      role="status"
    >
      Preparando gráfico…
    </div>
  );
  return (
    <div ref={root} className="min-h-64">
      {visible ? (
        <Suspense fallback={placeholder}>
          <FleetHealth {...props} />
        </Suspense>
      ) : (
        <div className="flex min-h-64 items-center justify-center">
          <button
            type="button"
            className="btn-secondary"
            onClick={() => setVisible(true)}
          >
            Carregar gráfico de saúde
          </button>
        </div>
      )}
    </div>
  );
}
