import { useEffect, useState } from "react";
import { Newspaper, ExternalLink, RefreshCw, AlertCircle } from "lucide-react";
import { getMarketNews } from "../services/api";

const CATEGORY_LABELS = {
  general: "Genel",
  forex:   "Döviz",
  crypto:  "Kripto",
  merger:  "Birleşmeler",
};

function timeAgo(unixTimestamp) {
  if (!unixTimestamp) return "";
  const diff = Math.floor((Date.now() / 1000) - unixTimestamp);
  if (diff < 60)   return `${diff} sn önce`;
  if (diff < 3600) return `${Math.floor(diff / 60)} dk önce`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} sa önce`;
  return `${Math.floor(diff / 86400)} gün önce`;
}

function NewsCard({ article }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group bg-white rounded-2xl border border-slate-200 p-5 flex flex-col gap-3 shadow-sm hover:shadow-md hover:border-finsim-primary transition-all"
    >
      <div className="flex items-start justify-between gap-2">
        <span className="text-xs font-semibold text-finsim-primary bg-blue-50 px-2 py-0.5 rounded-full">
          {article.source ?? "Kaynak"}
        </span>
        <span className="text-xs text-slate-400 shrink-0">{timeAgo(article.datetime)}</span>
      </div>

      <p className="text-sm font-semibold text-slate-800 leading-snug group-hover:text-finsim-primary transition-colors line-clamp-3">
        {article.headline}
      </p>

      {article.summary && (
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-3">
          {article.summary}
        </p>
      )}

      <div className="flex items-center gap-1 text-xs text-finsim-primary font-medium mt-auto">
        <span>Devamını oku</span>
        <ExternalLink className="w-3 h-3" />
      </div>
    </a>
  );
}

export default function NewsMock() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [category, setCategory] = useState("general");

  useEffect(() => {
    setLoading(true);
    setError(null);
    getMarketNews(category)
      .then((res) => setArticles(res.articles ?? []))
      .catch(() => setError("Haberler yüklenirken bir hata oluştu."))
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <div className="p-10 max-w-5xl mx-auto">
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Piyasa Haberleri</h1>
          <p className="text-slate-500 mt-1">Piyasaları etkileyen en son gelişmeleri takip edin.</p>
        </div>

        <div className="flex gap-2 flex-wrap">
          {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setCategory(key)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                category === key
                  ? "bg-finsim-primary text-white shadow-sm"
                  : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-8">
        {loading && (
          <div className="flex items-center justify-center gap-2 text-slate-400 py-20">
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span>Haberler yükleniyor…</span>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center gap-2 text-red-400 py-20">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {!loading && !error && articles.length === 0 && (
          <div className="flex items-center justify-center gap-2 text-slate-400 py-20">
            <Newspaper className="w-5 h-5" />
            <span>Bu kategoride haber bulunamadı.</span>
          </div>
        )}

        {!loading && !error && articles.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {articles.slice(0, 12).map((article, idx) => (
              <NewsCard key={idx} article={article} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
