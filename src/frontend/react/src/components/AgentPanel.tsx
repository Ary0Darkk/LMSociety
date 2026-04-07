import { useEffect, useRef, useState } from "react"
import type { AgentStatus, DebateMessage } from "../types"
import { STATUS_CONFIG } from "../types"

const COLOR_HEX: Record<string, string> = {
  violet: "#a78bfa",
  cyan: "#22d3ee",
  amber: "#fbbf24",
  emerald: "#34d399",
  rose: "#fb7185",
  orange: "#fb923c",
  sky: "#38bdf8",
  lime: "#a3e635",
  fuchsia: "#e879f9",
  teal: "#2dd4bf",
}

type ViewMode = "verbal" | "internal" | "withheld" | "subtext"

interface AgentPanelProps {
  name: string
  persona: string
  color: string
  messages: DebateMessage[]
  status: AgentStatus
  onSpeak: () => void
  onSendMessage: (prompt: string) => void
}

export default function AgentPanel({
  name,
  persona,
  color,
  messages,
  status,
  onSpeak,
  onSendMessage,
}: AgentPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [input, setInput] = useState("")
  const [viewMode, setViewMode] = useState<ViewMode>("verbal")
  const accent = COLOR_HEX[color] ?? "#a78bfa"
  const cfg = STATUS_CONFIG[status]
  const isBusy = status === "thinking"

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isBusy) return
    setInput("")
    onSendMessage(trimmed)
  }

  function getContent(msg: DebateMessage): string {
    switch (viewMode) {
      case "internal":
        return msg.internal_monologue || ""
      case "withheld":
        return msg.withheld_info || ""
      case "subtext":
        return msg.subtext || ""
      default:
        return msg.content
    }
  }

  return (
    <div
      className="flex h-full min-h-0 flex-col overflow-hidden bg-[#0f0f14] border-l-[3px]"
      style={{ borderLeftColor: accent }}
    >
      {/* Header */}
      <div className="flex shrink-0 items-center justify-between px-4 pt-3 pb-1">
        <div className="flex items-center gap-3 min-w-0">
          <h3 className="text-sm font-bold uppercase tracking-wide truncate" style={{ color: accent }}>
            {name}
          </h3>
          <button
            onClick={onSpeak}
            disabled={isBusy}
            className="shrink-0 cursor-pointer rounded px-1.5 py-0.5 text-xs text-white/20 transition-colors hover:bg-white/10 hover:text-white/60 disabled:cursor-not-allowed disabled:opacity-30"
            title={`Make ${name} speak`}
          >
            ▶
          </button>
        </div>

        {/* Status badge */}
        <div
          className={`flex shrink-0 items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${cfg.badgeClass} ${cfg.animation}`}
        >
          <span className={`h-1.5 w-1.5 rounded-full ${cfg.dotClass}`} />
          {cfg.label}
        </div>
      </div>

      {/* Persona */}
      <p className="shrink-0 truncate px-4 pb-2 text-xs text-white/25">{persona}</p>

      {/* View Mode Tabs */}
      <div className="shrink-0 flex gap-1 px-4 pb-2">
        {(["verbal", "internal", "withheld", "subtext"] as ViewMode[]).map((mode) => (
          <button
            key={mode}
            onClick={() => setViewMode(mode)}
            className={`shrink-0 rounded px-2 py-0.5 text-[10px] font-medium transition-colors ${
              viewMode === mode
                ? "bg-white/15 text-white/90"
                : "text-white/30 hover:text-white/60"
            }`}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>

      {/* Separator */}
      <div className="shrink-0 border-t border-white/[0.06]" />

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 min-h-0 overflow-y-auto px-4 py-3 space-y-3"
      >
        {messages.length === 0 && status !== "thinking" && (
          <p className="flex h-full items-center justify-center text-sm italic text-white/15">
            Waiting to speak…
          </p>
        )}

        {messages.map((msg) =>
          msg.agent_name.startsWith("user:") ? (
            <div
              key={msg.id}
              className="animate-fade-in flex flex-col items-end"
            >
              <div className="max-w-[85%] rounded-lg bg-violet-500/15 border border-violet-400/20 px-3 py-2 text-sm leading-relaxed text-violet-200/80">
                {msg.content}
              </div>
              <span className="mt-1 text-[10px] text-white/20">{msg.timestamp}</span>
            </div>
          ) : (
            <div
              key={msg.id}
              className="animate-fade-in text-sm leading-relaxed text-white/75 border-b border-white/[0.04] pb-3 last:border-b-0"
            >
              <span className="block text-[10px] text-white/20 mb-1">{msg.timestamp}</span>
              {getContent(msg)}
            </div>
          )
        )}

        {status === "thinking" && (
          <div className="flex items-center gap-2 pt-1 text-sm text-amber-400/60">
            <span className="inline-flex gap-1">
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-amber-400/60" style={{ animationDelay: "0ms" }} />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-amber-400/60" style={{ animationDelay: "150ms" }} />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-amber-400/60" style={{ animationDelay: "300ms" }} />
            </span>
            Thinking…
          </div>
        )}
      </div>

      {/* Chat input */}
      <div className="shrink-0 border-t border-white/[0.06] px-3 py-2">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isBusy}
            placeholder={isBusy ? "Waiting…" : `Ask ${name}…`}
            className="flex-1 min-w-0 rounded-md border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-white placeholder-white/20 outline-none transition-colors focus:border-violet-400/40 focus:bg-white/[0.07] disabled:opacity-30"
          />
          <button
            type="submit"
            disabled={isBusy || !input.trim()}
            className="shrink-0 cursor-pointer rounded-md px-3 py-1.5 text-sm font-medium transition-all duration-150 disabled:cursor-not-allowed disabled:opacity-20"
            style={{
              backgroundColor: `${accent}15`,
              color: accent,
              borderWidth: "1px",
              borderColor: `${accent}30`,
            }}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}
