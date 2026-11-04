import {
  OUTPUT_LEVELS,
  signalOutputsFor,
  signalOutputsStale,
} from "../../services/signalOutputs";

export default function SignalOutputList({
  outputs = [],
  stale = false,
  limit = Infinity,
  compact = false,
}) {
  if (!outputs.length) return null;
  return (
    <ul aria-label="Interpretações dos sinais" className="space-y-2">
      {outputs.slice(0, limit).map((output) => {
        const config = OUTPUT_LEVELS[output.level] || OUTPUT_LEVELS.info;
        return (
          <li
            key={output.code}
            data-output-code={output.code}
            className={`rounded-lg border p-3 text-xs ${stale ? OUTPUT_LEVELS.info.tone : config.tone}`}
          >
            <div className="flex flex-wrap items-start justify-between gap-2">
              <strong className="min-w-0 break-words">{output.title}</strong>
              <span className="text-[11px]">
                {stale ? "Última leitura" : config.label}
              </span>
            </div>
            {!compact && (
              <p className="mt-1 leading-relaxed text-text-secondary">
                {output.message}
              </p>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export function SignalOutputSummary({ machine }) {
  const output = signalOutputsFor(machine)[0];
  if (!output) return null;
  const stale = signalOutputsStale(machine);
  const config = OUTPUT_LEVELS[output.level] || OUTPUT_LEVELS.info;
  return (
    <p
      data-output-code={output.code}
      className={`mt-3 rounded-lg border p-2 text-xs ${stale ? OUTPUT_LEVELS.info.tone : config.tone}`}
    >
      {stale ? "Última interpretação: " : ""}
      {output.title}
    </p>
  );
}
