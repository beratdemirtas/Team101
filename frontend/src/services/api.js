const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Sokratik mentora mesaj gönderir.
 * @param {string} message - Kullanıcının yazdığı metin
 * @returns {Promise<string>} Mentorun cevabı
 */
export async function sendChatMessage(message) {
  const response = await fetch(`${BASE_URL}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error(`Sunucu hatası: ${response.status}`);
  }

  const data = await response.json();
  return data.reply;
}