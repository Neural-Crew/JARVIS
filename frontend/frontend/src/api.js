const BASE_URL = import.meta.env.VITE_API_URL;

async function sendChatMessage(messages) {
  const res = await fetch(BASE_URL + '/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages })
  });
  if (!res.ok) {
    let data = null;
    try {
      data = await res.json();
    } catch {
      data = await res.text();
    }
    return Promise.reject({ status: res.status, data });
  }
  return res.body;
}

export default {
  sendChatMessage
};
