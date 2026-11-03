import { useEffect, useRef, useState } from "react";
import { startPolling } from "../services/telemetry";

// Small, bounded cache for public monitoring reads. Mutations bypass this cache.
const cache = new Map();
export function useApiQuery(key, load, interval = 15000) {
  const loader = useRef({ key, load });
  loader.current = { key, load };
  const [state, setState] = useState({
    key,
    data: cache.get(key)?.data ?? null,
    loading: Boolean(key),
    error: null,
  });
  useEffect(() => {
    if (!key) return undefined;
    const cached = cache.get(key);
    setState({
      key,
      data: cached?.data ?? null,
      loading: !cached || Date.now() - cached.at >= interval,
      error: null,
    });
    let stop;
    const begin = () => {
      stop = startPolling(
        async (cancelled, signal) => {
          if (loader.current.key !== key) return;
          const data = await loader.current.load(signal);
          if (cancelled()) return;
          cache.delete(key);
          cache.set(key, { data, at: Date.now() });
          if (cache.size > 60) cache.delete(cache.keys().next().value);
          setState({ key, data, loading: false, error: null });
        },
        (error) =>
          setState((current) => ({
            ...current,
            loading: false,
            error: error.message || "Consulta indisponível",
          })),
        interval,
      );
    };
    const delay = cached ? Math.max(0, interval - (Date.now() - cached.at)) : 0;
    const timer = delay ? setTimeout(begin, delay) : null;
    if (!delay) begin();
    return () => {
      clearTimeout(timer);
      stop?.();
    };
  }, [key, interval]);
  if (!key) return { data: null, loading: false, error: null };
  return state.key === key
    ? state
    : { data: cache.get(key)?.data ?? null, loading: true, error: null };
}
