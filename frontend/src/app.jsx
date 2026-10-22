import { Routes, Route, Navigate } from "react-router-dom";

import Splash from "./pages/splash/splash";
import Landing from "./pages/landing/landing";
import Login from "./pages/login/login";
import Register from "./pages/register/register";
import CompanySelection from "./pages/companySelection/companySelection";

import DashboardLayout from "./layouts/dashboardLayout/dashboardLayout";
import Dashboard from "./pages/dashboard/dashboard";
import Machines from "./pages/machines/machines";
import MachineDetails from "./pages/machineDetails/machineDetails";
import Alerts from "./pages/alerts/alerts";
import History from "./pages/history/history";
import Clients from "./pages/clients/clients";
import Units from "./pages/units/units";
import Devices from "./pages/devices/devices";
import Settings from "./pages/settings/settings";
import Admin from "./pages/admin/admin";
import AdminAccess from "./pages/admin/adminAccess";

import TVLayout from "./layouts/tvLayout/tvLayout";
import TVDashboard from "./pages/tvDashboard/tvDashboard";
import { MonitoringProvider } from "./contexts/monitoringContext";

export default function App() {
  return (
    <MonitoringProvider>
    <Routes>
      {/* Fluxo de acesso */}
      <Route path="/" element={<Splash />} />
      <Route path="/inicio" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Register />} />
      <Route path="/selecionar-empresa" element={<CompanySelection />} />

      {/* Área interna (dashboard) */}
      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/maquinas" element={<Machines />} />
        <Route path="/maquinas/:id" element={<MachineDetails />} />
        <Route path="/alertas" element={<Alerts />} />
        <Route path="/historico" element={<History />} />
        <Route path="/clientes" element={<Clients />} />
        <Route path="/unidades" element={<Units />} />
        <Route path="/dispositivos" element={<Devices />} />
        <Route path="/configuracoes" element={<Settings />} />
        <Route path="/admin" element={<AdminAccess><Admin /></AdminAccess>} />
      </Route>

      {/* Modo TV */}
      <Route element={<TVLayout />}>
        <Route path="/tv" element={<TVDashboard />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    </MonitoringProvider>
  );
}
