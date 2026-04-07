import type { Agent, DebateMessage } from "../types"
import { getAgentColor, deriveAgentStatus } from "../types"
import AgentPanel from "./AgentPanel"

interface DebateViewProps {
  topic: string
  agents: Agent[]
  messages: DebateMessage[]
  round: number
  isRunningRound: boolean
  isAutoRunning: boolean
  speakingAgent: string | null
  doneAgents: ReadonlySet<string>
  onRunRound: () => void
  onAutoRun: () => void
  onStopAutoRun: () => void
  onSpeak: (agentName: string) => void
  onSendMessage: (agentName: string, prompt: string) => void
  onBack: () => void
}

export default function DebateView({
  topic,
  agents,
  messages,
  round,
  isRunningRound,
  isAutoRunning,
  speakingAgent,
  doneAgents,
  onRunRound,
  onAutoRun,
  onStopAutoRun,
  onSpeak,
  onSendMessage,
  onBack,
}: DebateViewProps) {
  function messagesForAgent(agentName: string): DebateMessage[] {
    return messages.filter(
      (m) => m.agent_name === agentName || m.agent_name === `user:${agentName}`
    )
  }

  const cols =
    agents.length <= 2 ? 2 : agents.length <= 4 ? 2 : agents.length <= 6 ? 3 : 4
  const rows = Math.ceil(agents.length / cols)

  return (
    <div className="flex h-screen flex-col bg-[#0f0f14]">
      {/* Top bar */}
      <div className="flex h-12 shrink-0 items-center justify-between border-b border-white/10 bg-white/[0.02] px-4">
        <div className="flex items-center gap-4 min-w-0">
          <button
            onClick={onBack}
            className="shrink-0 cursor-pointer rounded-md px-2.5 py-1 text-xs font-medium text-white/40 transition-colors hover:bg-white/10 hover:text-white/80"
          >
            ← Back
          </button>
          <div className="h-4 w-px bg-white/10" />
          <span className="truncate text-sm font-medium text-white/70">{topic}</span>
        </div>

        <div className="flex items-center gap-3">
          <span className="hidden sm:inline text-xs text-white/30">
            Round {round} · {agents.length} agents · {messages.length} messages
          </span>
          {isAutoRunning ? (
            <button
              onClick={onStopAutoRun}
              className="shrink-0 cursor-pointer rounded-lg bg-red-500/80 hover:bg-red-500 px-4 py-1.5 text-xs font-semibold text-white transition-colors"
            >
              ■ Stop
            </button>
          ) : (
            <>
              <button
                onClick={onAutoRun}
                disabled={isRunningRound}
                className="shrink-0 cursor-pointer rounded-lg bg-gradient-to-r from-emerald-500 to-teal-500 px-4 py-1.5 text-xs font-semibold text-white shadow-lg shadow-emerald-500/20 transition-all duration-200 hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isRunningRound ? "Running..." : "▶ Auto-Run"}
              </button>
              <button
                onClick={onRunRound}
                disabled={isRunningRound}
                className="shrink-0 cursor-pointer rounded-lg bg-gradient-to-r from-violet-500 to-cyan-500 px-4 py-1.5 text-xs font-semibold text-white shadow-lg shadow-violet-500/20 transition-all duration-200 hover:shadow-xl hover:shadow-violet-500/30 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isRunningRound ? (
                  <span className="inline-flex items-center gap-1.5">
                    <svg className="h-3 w-3 animate-spin" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" className="opacity-25" />
                      <path d="M4 12a8 8 0 018-8" stroke="currentColor" strokeWidth="3" strokeLinecap="round" className="opacity-75" />
                    </svg>
                    Running…
                  </span>
                ) : (
                  "▶ Run Round"
                )}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Agent grid */}
      <div
        className="flex-1 min-h-0 grid gap-px bg-white/[0.06]"
        style={{
          gridTemplateColumns: `repeat(${cols}, 1fr)`,
          gridTemplateRows: `repeat(${rows}, 1fr)`,
        }}
      >
        {agents.map((agent, i) => {
          const agentMessages = messagesForAgent(agent.name)
          const status = deriveAgentStatus(
            agent.name,
            speakingAgent,
            isRunningRound,
            agentMessages.length > 0,
            doneAgents
          )
          const currentRow = Math.floor(i / cols)
          const colsInRow = currentRow === rows - 1 ? agents.length - currentRow * cols : cols
          const isLastInOddRow = colsInRow < cols && i === agents.length - 1
          const spanCols = isLastInOddRow ? cols - colsInRow + 1 : 1

          return (
            <div
              key={agent.name}
              className="min-h-0 min-w-0"
              style={spanCols > 1 ? { gridColumn: `span ${spanCols}` } : undefined}
            >
              <AgentPanel
                name={agent.name}
                persona={agent.persona}
                color={getAgentColor(agent.name, i)}
                messages={agentMessages}
                status={status}
                onSpeak={() => onSpeak(agent.name)}
                onSendMessage={(prompt) => onSendMessage(agent.name, prompt)}
              />
            </div>
          )
        })}
      </div>
    </div>
  )
}
