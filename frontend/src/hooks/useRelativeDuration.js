import { useSyncExternalStore } from "react";
import { formatDuration } from "../utils/time";

let now = Date.now();
let timer;
const listeners = new Set();
const tick = () => {
  now = Date.now();
  listeners.forEach((listener) => listener());
};
function visibility() {
  clearInterval(timer);
  if (!document.hidden) {
    tick();
    timer = setInterval(tick, 1000);
  }
}
function subscribe(listener) {
  listeners.add(listener);
  if (listeners.size === 1) {
    document.addEventListener("visibilitychange", visibility);
    visibility();
  }
  return () => {
    listeners.delete(listener);
    if (!listeners.size) {
      clearInterval(timer);
      document.removeEventListener("visibilitychange", visibility);
    }
  };
}
export function useClock() {
  return useSyncExternalStore(
    subscribe,
    () => now,
    () => now,
  );
}
export function useRelativeDuration(stateSince, showSeconds = true) {
  const current = useClock();
  const parsed = Date.parse(stateSince);
  const seconds = Number.isFinite(parsed)
    ? Math.max(0, Math.floor((current - parsed) / 1000))
    : null;
  return {
    seconds,
    formatted: seconds == null ? "—" : formatDuration(seconds, { showSeconds }),
  };
}
