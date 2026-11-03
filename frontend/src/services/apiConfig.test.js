import test from "node:test";
import assert from "node:assert/strict";
import { resolveApiBase } from "./apiConfig.js";

test("mobile and web use the current origin; desktop resolves a local or configured server", () => {
  assert.equal(resolveApiBase(undefined, "https:"), "/api");
  assert.equal(resolveApiBase(" /api/ ", "http:"), "/api");
  assert.equal(
    resolveApiBase(undefined, "scomptec:"),
    "http://127.0.0.1:8000/api",
  );
  assert.equal(resolveApiBase("/api", "file:"), "http://127.0.0.1:8000/api");
  assert.equal(
    resolveApiBase("https://server.example/api/", "scomptec:"),
    "https://server.example/api",
  );
});
