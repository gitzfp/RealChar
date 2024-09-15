import { createContext, useContext, useEffect, useState } from "react";

const backendUrl = "http://localhost:8000";

const ChatContext = createContext();
import { useAppStore } from '@/zustand/store';

export const ChatProvider = ({ children }) => {
  const chat = async (message) => {
    setLoading(true);
    const data = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
    const resp = (await data.json()).messages;
    setMessages((messages) => [...messages, ...resp]);
    setLoading(false);
  };
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState();
  const [loading, setLoading] = useState(false);
  const [cameraZoomed, setCameraZoomed] = useState(true);
  const { chatContent } = useAppStore();

  const onMessagePlayed = () => {
    setMessages((messages) => messages.slice(1));
  };

    useEffect(() => {
      if(chatContent?.length > 0 && chatContent[chatContent.length - 1].from === 'user'){
         chat(chatContent[chatContent.length - 1].content)
      }
      console.log('收到了聊天消息：',chatContent)
    }, [chatContent])

    useEffect(() => {
      if (messages.length > 0) {
        setMessage(messages[0]);
      } else {
        setMessage(null);
      }
  }, [messages]);

  return (
    <ChatContext.Provider
      value={{
        chat,
        message,
        onMessagePlayed,
        loading,
        cameraZoomed,
        setCameraZoomed,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};