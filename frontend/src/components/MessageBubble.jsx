
import { Bot, User } from "lucide-react";

export default function MessageBubble({ role, content, timestamp }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} mb-6`}
    >
      {/* Avatar */}
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
          isUser ? "bg-slate-700" : "bg-finsim-primary"
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Baloncuk + üst bilgi */}
      <div className={`flex flex-col max-w-[70%] ${isUser ? "items-end" : "items-start"}`}>
        <span className="text-xs text-slate-500 mb-1 px-1">
          {isUser ? "Siz" : "FinSim Asistan"} • {timestamp}
        </span>
        <div
          className={`px-5 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap shadow-sm ${
            isUser
              ? "bg-finsim-primary text-white rounded-tr-sm"
              : "bg-white text-slate-800 border border-slate-100 rounded-tl-sm"
          }`}
        >
          {content}
        </div>
      </div>
    </div>
  );
}
