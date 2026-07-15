import { User, BookOpen, Target, BarChart2, Edit3 } from "lucide-react";

const PROFILE = {
  name: "Demo Kullanıcı",
  email: "demo@finsim.app",
  joinDate: "Temmuz 2026",
  level: "Başlangıç Yatırımcısı",
  xp: 120,
  xpMax: 500,
  riskProfile: "Orta",
  interests: ["Hisse Senetleri", "ETF", "Kişisel Finans", "Risk Yönetimi"],
  stats: [
    { label: "Sohbet Sayısı", value: "12" },
    { label: "Öğrenilen Konu", value: "8" },
    { label: "Sanal Bakiye", value: "₺10.000" },
  ],
};

function StatCard({ label, value }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 text-center shadow-sm">
      <p className="text-2xl font-bold text-finsim-primary">{value}</p>
      <p className="text-xs text-slate-500 mt-1">{label}</p>
    </div>
  );
}

export default function ProfileMock() {
  const xpPercent = Math.min((PROFILE.xp / PROFILE.xpMax) * 100, 100);

  return (
    <div className="p-10 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900">Profil</h1>
      <p className="text-slate-500 mt-1">Hesap bilgileriniz ve öğrenme istatistikleriniz.</p>

      <div className="mt-8 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex items-center gap-6">
        <div className="w-20 h-20 rounded-full bg-finsim-primary flex items-center justify-center shrink-0">
          <User className="w-10 h-10 text-white" />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-xl font-bold text-slate-900 truncate">{PROFILE.name}</h2>
          <p className="text-sm text-slate-500 truncate">{PROFILE.email}</p>
          <p className="text-xs text-slate-400 mt-0.5">Üyelik: {PROFILE.joinDate}</p>
        </div>
        <button className="flex items-center gap-1.5 text-sm text-finsim-primary font-medium hover:underline shrink-0">
          <Edit3 className="w-4 h-4" />
          Düzenle
        </button>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-4">
        {PROFILE.stats.map((s) => (
          <StatCard key={s.label} label={s.label} value={s.value} />
        ))}
      </div>

      <div className="mt-6 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex flex-col gap-5">

        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0">
            <BarChart2 className="w-4 h-4 text-finsim-primary" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <p className="text-sm font-semibold text-slate-800">Seviye</p>
              <span className="text-xs font-medium text-finsim-primary">{PROFILE.level}</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div
                className="bg-finsim-primary h-2 rounded-full transition-all duration-700"
                style={{ width: `${xpPercent}%` }}
              />
            </div>
            <p className="text-xs text-slate-400 mt-1">{PROFILE.xp} / {PROFILE.xpMax} XP</p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center shrink-0">
            <Target className="w-4 h-4 text-amber-500" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800 mb-1">Risk Profili</p>
            <span className="inline-block text-xs font-semibold px-3 py-1 rounded-full bg-amber-50 text-amber-600 border border-amber-200">
              {PROFILE.riskProfile}
            </span>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center shrink-0">
            <BookOpen className="w-4 h-4 text-emerald-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800 mb-2">İlgi Alanları</p>
            <div className="flex flex-wrap gap-2">
              {PROFILE.interests.map((interest) => (
                <span
                  key={interest}
                  className="text-xs px-3 py-1 rounded-full bg-slate-100 text-slate-600 font-medium"
                >
                  {interest}
                </span>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
