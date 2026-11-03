import { lazy } from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import RouteBoundary from "./components/routeBoundary/routeBoundary";
const PasswordHelp = lazy(() => import("./pages/passwordHelp/passwordHelp"));
const Landing = lazy(() => import("./pages/landing/landing"));
const Login = lazy(() => import("./pages/login/login"));
const Register = lazy(() => import("./pages/register/register"));
const CompanySelection = lazy(
  () => import("./pages/companySelection/companySelection"),
);

const DashboardLayout = lazy(
  () => import("./layouts/dashboardLayout/dashboardLayout"),
);
const Dashboard = lazy(() => import("./pages/dashboard/dashboard"));
const Machines = lazy(() => import("./pages/machines/machines"));
const MachineDetails = lazy(
  () => import("./pages/machineDetails/machineDetails"),
);
const Alerts = lazy(() => import("./pages/alerts/alerts"));
const History = lazy(() => import("./pages/history/history"));
const Clients = lazy(() => import("./pages/clients/clients"));
const Units = lazy(() => import("./pages/units/units"));
const Devices = lazy(() => import("./pages/devices/devices"));
const Settings = lazy(() => import("./pages/settings/settings"));
const Admin = lazy(() => import("./pages/admin/admin"));
const AdminAccess = lazy(() => import("./pages/admin/adminAccess"));

const TVLayout = lazy(() => import("./layouts/tvLayout/tvLayout"));
const TVDashboard = lazy(() => import("./pages/tvDashboard/tvDashboard"));
import { MonitoringProvider } from "./contexts/monitoringContext";

export default function App() {
  return (
    <MonitoringProvider>
      <RouteBoundary>
        <Routes>
          {/* Fluxo de acesso */}
          <Route path="/" element={<Navigate to="/inicio" replace />} />
          <Route path="/recuperar-senha" element={<PasswordHelp />} />
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
            <Route
              path="/admin"
              element={
                <AdminAccess>
                  <Admin />
                </AdminAccess>
              }
            />
          </Route>

          {/* Modo TV */}
          <Route element={<TVLayout />}>
            <Route path="/tv" element={<TVDashboard />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </RouteBoundary>
    </MonitoringProvider>
  );
}
