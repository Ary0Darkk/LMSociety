import { useEffect, useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bot, Loader2 } from "lucide-react";

// 1. Define strict types
interface Message { 
  role: 'agent'; // This is a literal type
  text: string; 
}

interface Agent { 
  id: string; 
  name: string; 
  status: 'idle' | 'thinking'; 
  messages: Message[]; 
}

export default function LLMSociety() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws/society");

    ws.current.onmessage = (event) => {
      const payload = JSON.parse(event.data);

      if (payload.type === "INIT_SOCIETY") {
        setAgents(payload.data.map((a: any) => ({ ...a, messages: [] })));
      } 
      
      if (payload.type === "UPDATE_STATUS" || payload.type === "NEW_MESSAGE") {
        setAgents((prev: Agent[]) => prev.map((agent): Agent => {
          if (agent.id === payload.id) {
            // 2. Explicitly cast the new message to match the Message interface
            const newMessage: Message | null = payload.text 
              ? { role: 'agent' as const, text: payload.text } 
              : null;

            return { 
              ...agent, 
              status: payload.status, 
              messages: newMessage ? [...agent.messages, newMessage] : agent.messages 
            };
          }
          return agent;
        }));
      }
    };

    return () => ws.current?.close();
  }, []);

  return (
    <div className="p-8 bg-slate-950 min-h-screen text-white">
      <header className="mb-10">
        <h1 className="text-4xl font-black mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          LLM SOCIETY DEBATE
        </h1>
        <div className="flex items-center gap-2 text-slate-400 font-mono text-sm">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          Connected to Orchestrator
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <Card key={agent.id} className="bg-slate-900 border-slate-800 border-2 shadow-xl overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between border-b border-slate-800 bg-slate-800/30 pb-4">
              <CardTitle className="text-lg flex items-center gap-2">
                <Bot className="text-blue-400" size={20}/>
                {agent.name}
              </CardTitle>
              <Badge className={agent.status === 'thinking' ? "bg-blue-600 animate-pulse" : "bg-slate-700"}>
                {agent.status === 'thinking' && <Loader2 size={12} className="mr-2 animate-spin" />}
                {agent.status.toUpperCase()}
              </Badge>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-72 p-4">
                {agent.messages.length === 0 && (
                  <div className="text-slate-600 text-xs text-center mt-20 italic">Waiting for agent to speak...</div>
                )}
                {agent.messages.map((m, i) => (
                  <div key={i} className="mb-4 bg-slate-800/50 p-3 rounded-lg border border-slate-700 text-sm text-slate-300 animate-in fade-in slide-in-from-bottom-2">
                    {m.text}
                  </div>
                ))}
              </ScrollArea>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}