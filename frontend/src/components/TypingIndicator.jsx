
import { Bot } from "lucide-react";

export default function TypingIndicator() {
  return (
    <div className="flex gap-3 mb-6">
      <div className="w-10 h-10 rounded-full bg-finsim-primary flex items-center justify-center shrink-0">
        <Bot className="w-5 h-5 text-white" />
      </div>
      <div className="flex flex-col items-start">
        <span className="text-xs text-slate-500 mb-1 px-1">
          FinSim Asistan
        </span>
        <div className="bg-white border border-slate-100 shadow-sm rounded-2xl rounded-tl-sm px-5 py-4 flex items-center gap-2">
          <span className="text-sm text-slate-500 mr-1">Mentor düşünüyor</span>
          <span className="w-2 h-2 bg-finsim-primary rounded-full animate-bounce-dot" style={{ animationDelay: "0s" }} />
          <span className="w-2 h-2 bg-finsim-primary rounded-full animate-bounce-dot" style={{ animationDelay: "0.15s" }} />
          <span className="w-2 h-2 bg-finsim-primary rounded-full animate-bounce-dot" style={{ animationDelay: "0.3s" }} />
        </div>
      </div>
    </div>
  );
}
