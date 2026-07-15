
import { useState } from "react";
import Sidebar from "./Sidebar";
import ChatView from "../pages/ChatView";
import DashboardMock from "../pages/DashboardMock";
import SimulationMock from "../pages/SimulationMock";
import NewsMock from "../pages/NewsMock";
import ProfileMock from "../pages/ProfileMock";

export default function Layout() {
  const [activePage, setActivePage] = useState("chatbot");

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":  return <DashboardMock />;
      case "simulation": return <SimulationMock />;
      case "news":       return <NewsMock />;
      case "profile":    return <ProfileMock />;
      case "chatbot":
      default:           return <ChatView />;
    }
  };

  return (
    <div className="flex h-screen bg-finsim-bg overflow-hidden">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="flex-1 overflow-hidden">{renderPage()}</main>
    </div>
  );
}
