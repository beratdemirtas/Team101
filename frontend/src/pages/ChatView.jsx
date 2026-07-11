
import { useState, useRef, useEffect } from "react";
import { Send, Info } from "lucide-react";
import { sendChatMessage } from "../services/api";
import MessageBubble from "../components/MessageBubble";
import TypingIndicator from "../components/TypingIndicator";

const formatTime = (date) =>
  date.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });

const WELCOME_MESSAGE = {
  role: "assistant",
  content:
    "Merhaba! Ben FinSim eğitim asistanınızım. Finansal kavramlar, borsa terimleri veya yatırım stratejileri hakkında sorularınızı yanıtlamak için buradayım.\n\nSize nasıl yardımcı olabilirim?",
  timestamp: formatTime(new Date()),
};

export default function ChatView() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const scrollRef = useRef(null);

  // Otomatik en alta kaydırma
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isLoading]);

  const handleSend = async () => {
    const trimmed = inputText.trim();
    if (!trimmed || isLoading) return;

    const userMessage = {
      role: "user",
      content: trimmed,
      timestamp: formatTime(new Date()),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsLoading(true);

    try {
      const reply = await sendChatMessage(trimmed);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: reply,
          timestamp: formatTime(new Date()),
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Üzgünüm, şu anda sunucuya ulaşamıyorum. Lütfen kısa süre sonra tekrar deneyin.",
          timestamp: formatTime(new Date()),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Başlık */}
      <header className="px-10 pt-8 pb-4 shrink-0">
        <h1 className="text-3xl font-bold text-slate-900">Finans Chatbotu</h1>
        <p className="text-slate-500 mt-1">
          Borsa ve finans konularında öğretici destek alın.
        </p>
      </header>

      {/* Mesaj Alanı */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto chat-scroll px-10 py-6"
      >
        <div className="max-w-4xl mx-auto">
          {messages.map((msg, idx) => (
            <MessageBubble
              key={idx}
              role={msg.role}
              content={msg.content}
              timestamp={msg.timestamp}
            />
          ))}
          {isLoading && <TypingIndicator />}
        </div>
      </div>

      {/* Input Bölümü */}
      <div className="px-10 pb-6 pt-3 bg-finsim-bg shrink-0">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                placeholder="Borsayla ilgili bir soru sorun..."
                className="w-full px-5 py-4 pr-4 rounded-full border border-slate-200 bg-white text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-finsim-primary focus:border-transparent shadow-sm disabled:opacity-60"
              />
            </div>
            <button
              onClick={handleSend}
              disabled={!inputText.trim() || isLoading}
              className="w-12 h-12 rounded-full bg-finsim-primary hover:bg-finsim-primaryDark disabled:bg-slate-300 flex items-center justify-center transition-colors shadow-md shrink-0"
              aria-label="Gönder"
            >
              <Send className="w-5 h-5 text-white" />
            </button>
          </div>

          <div className="flex items-center justify-center gap-1.5 mt-3 text-xs text-slate-500">
            <Info className="w-3.5 h-3.5" />
            <span>Yatırım tavsiyesi vermez, eğitici bilgi sunar.</span>
          </div>
        </div>
      </div>
    </div>
  );
}
