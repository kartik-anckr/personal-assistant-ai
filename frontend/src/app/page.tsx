"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your AI assistant powered by Google Gemini. I can help with math calculations, weather information, and general conversations. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue.trim(),
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage.text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          isUser: false,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, aiMessage]);
      } else {
        throw new Error(data.response || "Unknown error occurred");
      }
    } catch (err) {
      console.error("Error sending message:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to send message. Please make sure the backend is running on localhost:8000"
      );

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error. Please make sure the backend server is running and try again.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700 px-6 py-4 shadow-sm">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
            🎭 LangGraph AI Assistant
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Powered by Google Gemini 1.5 Flash • Math • Weather • General Chat
          </p>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-4xl mx-auto px-6 py-4">
          <div className="h-full overflow-y-auto space-y-4 scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-600">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-3 ${
                  message.isUser ? "flex-row-reverse space-x-reverse" : ""
                }`}
              >
                {/* Avatar */}
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                    message.isUser
                      ? "bg-blue-500 text-white"
                      : "bg-gradient-to-br from-purple-500 to-pink-500 text-white"
                  }`}
                >
                  {message.isUser ? "You" : "🤖"}
                </div>

                {/* Message Bubble */}
                <div
                  className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-2xl ${
                    message.isUser
                      ? "bg-blue-500 text-white ml-auto"
                      : "bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-100 shadow-sm border border-slate-200 dark:border-slate-600"
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.text}
                  </p>
                  <p
                    className={`text-xs mt-2 ${
                      message.isUser
                        ? "text-blue-100"
                        : "text-slate-500 dark:text-slate-400"
                    }`}
                  >
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm font-semibold text-white">
                  🤖
                </div>
                <div className="bg-white dark:bg-slate-700 px-4 py-3 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-600">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="max-w-4xl mx-auto px-6">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-3 mb-4">
            <p className="text-red-800 dark:text-red-200 text-sm">⚠️ {error}</p>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-t border-slate-200 dark:border-slate-700 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message... (Try: 'Add 15 and 25' or 'Weather in Tokyo')"
                disabled={isLoading}
                className="w-full px-4 py-3 pr-12 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-slate-500 dark:placeholder-slate-400 text-slate-800 dark:text-slate-100 disabled:opacity-50 disabled:cursor-not-allowed"
                rows={1}
                style={{ minHeight: "48px", maxHeight: "120px" }}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 dark:disabled:bg-slate-600 text-white rounded-xl font-medium transition-colors duration-200 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M2 21L23 12L2 3V10L17 12L2 14V21Z"
                    fill="currentColor"
                  />
                </svg>
              )}
            </button>
          </div>

          {/* Quick Examples */}
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 dark:text-slate-400">
              Try:
            </span>
            {["Add 15 and 25", "Weather in Tokyo", "Hello there!"].map(
              (example) => (
                <button
                  key={example}
                  onClick={() => setInputValue(example)}
                  className="text-xs px-3 py-1 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-600 dark:text-slate-300 rounded-full transition-colors duration-200"
                >
                  {example}
                </button>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
