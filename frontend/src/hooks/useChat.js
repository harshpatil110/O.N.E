import { useState, useCallback } from 'react';
import { sendMessage as apiSendMessage, getChatHistory } from '../api/chat';

export const useChat = (sessionId, onMessageComplete) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const loadHistory = useCallback(async (sid) => {
    try {
      const history = await getChatHistory(sid);
      const historyArray = Array.isArray(history) ? history : history.data || [];
      if (historyArray.length > 0) {
        setMessages(historyArray.map((msg, i) => ({ ...msg, tempId: `hist-${i}` })));
      }
      return historyArray;
    } catch (error) {
      console.error("Failed to load history", error);
      return [];
    }
  }, []);

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || !sessionId) return;

    // Optimistically add the user's message
    const userMessage = { role: 'user', content: text, tempId: Date.now() };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiSendMessage(sessionId, text);
      console.log("🔥 RAW API RESPONSE DATA:", response);
      console.log("🔥 RESPONSE KEYS:", Object.keys(response || {}));
      console.log("🔥 response.reply =", response?.reply, "| type:", typeof response?.reply);
      console.log("🔥 response.response =", response?.response, "| type:", typeof response?.response);
      console.log("🔥 response.text =", response?.text, "| type:", typeof response?.text);
      console.log("🔥 response.content =", response?.content, "| type:", typeof response?.content);
      console.log("🔥 response.message =", response?.message, "| type:", typeof response?.message);
      
      // Robustly extract the text, handling possible structural variations
      const extractedText = response.reply || response.response || response.text || response.content || response.message || "FALLBACK_ERROR: No text key found in response";
      console.log("🔥 EXTRACTED TEXT =", `[${extractedText}]`, "| length:", extractedText.length);

      // Append the agent's reply
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: extractedText, tempId: Date.now() + 1 }
      ]);

      // Notify parent that a full message roundtrip completed
      // This allows ChecklistContext to refresh progress immediately
      if (onMessageComplete) {
        onMessageComplete();
      }
    } catch (error) {
      console.error("Failed to send message", error);
      // Optional: Add a system error message or rollback
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: "**Error:** Failed to deliver message. Please try again.", isError: true, tempId: Date.now() + 1 }
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, onMessageComplete]);

  const appendInitialMessage = useCallback((text) => {
      setMessages((prev) => {
          if (prev.length === 0) {
              return [{ role: 'assistant', content: text, tempId: Date.now() }]
          }
          return prev;
      });
  }, []);

  return { messages, isLoading, sendMessage, appendInitialMessage, loadHistory };
};
