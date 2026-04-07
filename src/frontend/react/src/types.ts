export interface Agent {
  name: string
  persona: string
}

export interface DebateMessage {
  id: number
  debate_id: number
  agent_name: string
  content: string
  internal_monologue: string | null
  withheld_info: string | null
  subtext: string | null
  timestamp: string
}

export interface DebateConfig {
  topic: string
  agents: Agent[]
  model: string
}

export const AVAILABLE_MODELS = [
  { id: "Gemini", label: "Gemini", description: "Google's flagship model" },
  { id: "DeepSeek", label: "DeepSeek", description: "Deep reasoning model" },
  { id: "GPT-OSS", label: "GPT-OSS", description: "Open-source GPT variant" },
  { id: "MiniMax", label: "MiniMax", description: "Fast & lightweight" },
] as const

export const DEFAULT_AGENTS: Agent[] = [
  { name: "Philosopher", persona: "A deep thinker focused on ethics, history, and social dynamics." },
  { name: "Engineer", persona: "A pragmatic builder focused on technical feasibility and implementation." },
  { name: "Government", persona: "A regulator focused on public safety, policy, and legal frameworks." },
  { name: "Citizen", persona: "An everyday person concerned with practical impact on daily life." },
]

export const AGENT_COLORS: Record<string, string> = {
  Philosopher: "violet",
  Engineer: "cyan",
  Government: "amber",
  Citizen: "emerald",
}

export function getAgentColor(name: string, index: number): string {
  if (AGENT_COLORS[name]) return AGENT_COLORS[name]
  const fallback = ["rose", "orange", "sky", "lime", "fuchsia", "teal"]
  return fallback[index % fallback.length]
}

export type AgentStatus = "idle" | "thinking" | "listening" | "done"

export function deriveAgentStatus(
  agentName: string,
  speakingAgent: string | null,
  isRunningRound: boolean,
  hasMessages: boolean,
  doneAgents: ReadonlySet<string>
): AgentStatus {
  if (speakingAgent === agentName) return "thinking"
  if (isRunningRound || speakingAgent !== null) {
    if (doneAgents.has(agentName)) return "done"
    return "listening"
  }
  if (hasMessages) return "done"
  return "idle"
}

export const STATUS_CONFIG: Record<AgentStatus, { label: string; dotClass: string; badgeClass: string; animation: string }> = {
  idle: {
    label: "Idle",
    dotClass: "bg-white/30",
    badgeClass: "bg-white/5 text-white/30 border-white/10",
    animation: "",
  },
  thinking: {
    label: "Thinking…",
    dotClass: "bg-amber-400",
    badgeClass: "bg-amber-400/10 text-amber-400 border-amber-400/20",
    animation: "animate-status-pulse",
  },
  listening: {
    label: "Listening",
    dotClass: "bg-blue-400",
    badgeClass: "bg-blue-400/10 text-blue-400 border-blue-400/20",
    animation: "animate-status-breathe",
  },
  done: {
    label: "Done",
    dotClass: "bg-emerald-400",
    badgeClass: "bg-emerald-400/10 text-emerald-400 border-emerald-400/20",
    animation: "",
  },
}
