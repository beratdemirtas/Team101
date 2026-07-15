import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, RefreshCw, AlertCircle } from "lucide-react";
import { getMarketPrice } from "../services/api";

const WATCHLIST = [
  { ticker: "XU100.IS", label: "BIST 100" },
  { ticker: "THYAO.IS", label: "Türk Hava Yolları" },
  { ticker: "GARAN.IS", label: "Garanti Bankası" },
  { ticker: "AAPL",     label: "Apple" },
];

function PriceCard({ ticker, label }) {
  const [data, setData]       = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getMarketPrice(ticker)
      .then(setData)
      .catch(() => setError("Veri alınamadı"))
      .finally(() => setLoading(false));
  }, [ticker]);

  const change = data?.price && data?.previous_close
    ? ((data.price - data.previous_close) / data.previous_close) * 100
    : null;
  const isUp = change !== null && change >= 0;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 flex flex-col gap-2 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">{ticker}</span>
        {!loading && !error && (
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${isUp ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-500"}`}>
            {change !== null ? `${isUp ? "+" : ""}${change.toFixed(2)}%` : "—"}
          </span>
        )}
      </div>

      <p className="font-semibold text-slate-800 text-sm">{label}</p>

      {loading && (
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
          <span>Yükleniyor…</span>
        </div>
      )}
      {error && (
        <div className="flex items-center gap-1.5 text-red-400 text-xs">
          <AlertCircle className="w-3.5 h-3.5" />
          <span>{error}</span>
        </div>
      )}
      {!loading && !error && data && (
        <div className="flex items-center gap-2 mt-1">
          {isUp
            ? <TrendingUp className="w-4 h-4 text-emerald-500" />
            : <TrendingDown className="w-4 h-4 text-red-500" />
          }
          <span className={`text-xl font-bold ${isUp ? "text-emerald-600" : "text-red-500"}`}>
            {data.price != null ? data.price.toFixed(2) : "—"}
          </span>
          <span className="text-xs text-slate-400">{data.currency ?? ""}</span>
        </div>
      )}
    </div>
  );
}

export default function DashboardMock() {
  return (
    <div className="p-10 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900">Merhaba, hoş geldin 👋</h1>
      <p className="text-slate-500 mt-1">Piyasaları keşfetmeye ve öğrenmeye hazır mısın?</p>

      <h2 className="text-lg font-semibold text-slate-700 mt-10 mb-4">Anlık Piyasa Verileri</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {WATCHLIST.map((item) => (
          <PriceCard key={item.ticker} ticker={item.ticker} label={item.label} />
        ))}
      </div>

      <div className="mt-10 p-8 bg-white rounded-2xl border border-slate-200">
        <p className="text-slate-400 text-sm text-center">
          Portföy ve geçmiş grafik verileri — yakında 📈
        </p>
      </div>
    </div>
  );
}
