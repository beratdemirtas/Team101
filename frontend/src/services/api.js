const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendChatMessage(message, userId, sessionId = null) {
  const response = await fetch(`${BASE_URL}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, session_id: sessionId, message }),
  });

  if (!response.ok) {
    throw new Error(`Sunucu hatası: ${response.status}`);
  }

  const data = await response.json();
  return { reply: data.reply, sessionId: data.session_id };
}

export async function getMarketPrice(ticker) {
  const response = await fetch(`${BASE_URL}/market/price/${ticker}`);
  if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
  return response.json();
}

export async function getMarketHistory(ticker, start, end) {
  const response = await fetch(
    `${BASE_URL}/market/history/${ticker}?start=${start}&end=${end}`
  );
  if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
  return response.json();
}

export async function getMarketNews(category = "general") {
  const response = await fetch(`${BASE_URL}/news/market?category=${category}`);
  if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
  return response.json();
}

export async function getCompanyNews(symbol, fromDate, toDate) {
  const response = await fetch(
    `${BASE_URL}/news/company/${symbol}?from_date=${fromDate}&to_date=${toDate}`
  );
  if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
  return response.json();
}