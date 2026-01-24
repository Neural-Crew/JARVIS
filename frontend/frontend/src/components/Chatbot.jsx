import { useState } from 'react';
import { useImmer } from 'use-immer';
import api from '@/api';
import { parseTextStream } from '@/utils';
import ChatMessages from '@/components/ChatMessages';
import ChatInput from '@/components/ChatInput';

function Chatbot() {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    const history = [
      ...messages.map(({ role, content }) => ({ role, content })),
      { role: 'user', content: trimmedMessage }
    ];

    setMessages(draft => [...draft,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', sources: [], loading: true }
    ]);
    setNewMessage('');

    try {
      const stream = await api.sendChatMessage(history);
      for await (const textChunk of parseTextStream(stream)) {
        setMessages(draft => {
          draft[draft.length - 1].content += textChunk;
        });
      }
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
      });
    } catch (err) {
      console.log(err);
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    }
  }

  return (
    <div className='relative grow flex flex-col gap-6 pt-6'>
      {messages.length === 0 && (
        <div className='mt-3 font-urbanist text-main-text text-xl font-light space-y-2'>
          <p>👋 Bonjour!</p>
          <p>Je suis votre assistant virtuel pour toute question à propos de l'environnement, je suis alimenté par l'API d'ECOWATCH.</p>
          <p>N'hésitez pas à me poser vos questions.</p>
        </div>
      )}
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
      />
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;
