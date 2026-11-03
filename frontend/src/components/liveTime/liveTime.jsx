import { useClock, useRelativeDuration } from "../../hooks/useRelativeDuration";
import { formatRelativeTime } from "../../utils/time";

export function Duration({ since }) {
  return useRelativeDuration(since).formatted;
}
export function RelativeTime({ date, short = false }) {
  const now = useClock();
  if (!Number.isFinite(Date.parse(date))) return "Sem registro";
  const label = formatRelativeTime(date, now);
  return short ? label.replace("há ", "") : label;
}
