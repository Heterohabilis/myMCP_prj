import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatSidebar from './ChatSidebar';
import ChatInput from './ChatInput';
import ChatMessages, { Message } from './ChatMessages';
import { useToast } from '@/hooks/use-toast';

const Chat = () => {
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // ✅ 新增：调用后端 API 的异步函数
  const fetchAIResponse = async (prompt: string): Promise<string> => {
    try {
      const res = await fetch('http://localhost:8000/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      return data.output || '[Empty response]';
    } catch (error) {
      toast({
        title: '请求失败',
        description: '后端服务无法访问或返回异常',
        variant: 'destructive',
      });
      return '[Error fetching response]';
    }
  };

  // ✅ 替换原来的 handleSendMessage
  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: uuidv4(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    const response = await fetchAIResponse(content);

    const assistantMessage: Message = {
      id: uuidv4(),
      content: response,
      role: 'assistant',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  return (
    <div className="flex h-screen bg-background">
      <ChatSidebar />
      <div className="flex-1 flex flex-col ml-20">
        <div className="flex-1 overflow-y-auto">
          <ChatMessages messages={messages} isLoading={isLoading} />
        </div>
        <ChatInput 
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default Chat;
