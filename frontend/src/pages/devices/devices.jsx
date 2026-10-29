import { useEffect, useState } from "react";
import api from "../../services/api";

export default function Devices() {
  const [devices, setDevices] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    api.getDevices().then(items => { if (active) setDevices(items); })
      .catch(reason => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);
  return <div className="space-y-5">
    <h1 className="text-2xl font-bold">Coletores opcionais</h1>
    <p className="text-sm text-text-muted">Adaptadores de aquisição cadastrados. O monitoramento das máquinas funciona sem esses cadastros.</p>
    {loading && <p role="status">Consultando coletores…</p>}
    {error && <p role="alert" className="text-amber-500">{error}</p>}
    {!loading && !error && devices.length === 0 && <p>Nenhum coletor cadastrado. Envie eventos com o ID da máquina e seus estados.</p>}
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {devices.map(device => <section key={device.id} className="panel space-y-2 p-5">
        <h2 className="font-bold">{device.name}</h2>
        <p className="text-xs text-text-muted">ID: {device.id}</p>
        <p className="text-xs text-text-muted">Máquina: {device.cnc_id}</p>
      </section>)}
    </div>
  </div>;
}
