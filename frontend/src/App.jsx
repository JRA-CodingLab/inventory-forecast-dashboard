import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import TopBar from "./components/TopBar";
import LoginDialog from "./components/LoginDialog";
import Landing from "./pages/Landing";
import Overview from "./pages/Overview";
import "./App.css";

export default function App() {
  const [showLogin, setShowLogin] = useState(false);

  return (
    <div className="min-h-screen flex flex-col">
      <TopBar onLoginClick={() => setShowLogin(true)} />

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/dashboard" element={<Overview />} />
        </Routes>
      </main>

      {showLogin && <LoginDialog onClose={() => setShowLogin(false)} />}
    </div>
  );
}
