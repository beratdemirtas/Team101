import { useEffect, useState } from "react";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

const TYPEWRITER_SPEED_MS = 12;

const PROSE_CLASSES =
  "prose prose-sm max-w-none text-slate-800 " +
  "prose-headings:text-slate-900 prose-headings:font-semibold " +
  "prose-strong:text-slate-900 " +
  "prose-code:bg-slate-100 prose-code:px-1 prose-code:rounded " +
  "prose-ul:my-1 prose-ol:my-1 prose-li:my-0 " +
  "prose-p:my-1 prose-p:leading-relaxed";

function TypewriterMarkdown({ text }) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed("");
    if (!text) return;

    let index = 0;
    const interval = setInterval(() => {
      index += 1;
      setDisplayed(text.slice(0, index));
      if (index >= text.length) clearInterval(interval);
    }, TYPEWRITER_SPEED_MS);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className={PROSE_CLASSES}>
      <ReactMarkdown>{displayed}</ReactMarkdown>
    </div>
  );
}

export default function MessageBubble({ role, content, timestamp, animate = false }) {
  const isUser = role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} mb-6`}>
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

      <div className={`flex flex-col max-w-[70%] ${isUser ? "items-end" : "items-start"}`}>
        <span className="text-xs text-slate-500 mb-1 px-1">
          {isUser ? "Siz" : "FinSim Asistan"} • {timestamp}
        </span>
        <div
          className={`px-5 py-3 rounded-2xl text-sm shadow-sm ${
            isUser
              ? "bg-finsim-primary text-white rounded-tr-sm whitespace-pre-wrap leading-relaxed"
              : "bg-white border border-slate-100 rounded-tl-sm"
          }`}
        >
          {isUser ? (
            content
          ) : animate ? (
            <TypewriterMarkdown text={content} />
          ) : (
            <div className={PROSE_CLASSES}>
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
