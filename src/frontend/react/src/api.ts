import axios from "axios"
import type { DebateConfig, DebateMessage } from "./types"

const client = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
})

export async function startDebate(config: DebateConfig): Promise<number> {
  const res = await client.post("/debate/start", config)
  return res.data.debate_id
}

export async function agentSpeak(debateId: number, agentName: string, prompt?: string): Promise<string> {
  const body: Record<string, string> = { agent: agentName }
  if (prompt) body.prompt = prompt
  const res = await client.post(`/debate/${debateId}/speak`, body)
  return res.data.message
}

export async function getMessages(debateId: number): Promise<DebateMessage[]> {
  const res = await client.get(`/debate/${debateId}`)
  return res.data
}
