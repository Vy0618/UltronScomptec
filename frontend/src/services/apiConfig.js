export function resolveApiBase(configured, protocol) {
  const value = configured?.trim().replace(/\/+$/, "");
  if (["file:", "scomptec:"].includes(protocol)) {
    return value && !value.startsWith("/")
      ? value
      : `http://127.0.0.1:8000${value || "/api"}`;
  }
  return value || "/api";
}
