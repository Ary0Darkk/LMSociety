import { useState } from "react"
import type { Agent } from "../types"
import { AVAILABLE_MODELS, DEFAULT_AGENTS } from "../types"

interface SetupFormProps {
  onStart: (topic: string, agents: Agent[], model: string) => void
  isLoading: boolean
}

export default function SetupForm({ onStart, isLoading }: SetupFormProps) {
  const [topic, setTopic] = useState("")
  const [model, setModel] = useState("Gemini")
  const [agents, setAgents] = useState<Agent[]>(() =>
    DEFAULT_AGENTS.map((a) => ({ ...a }))
  )

  function updateAgent(index: number, field: keyof Agent, value: string) {
    setAgents((prev) =>
      prev.map((a, i) => (i === index ? { ...a, [field]: value } : a))
    )
  }

  function removeAgent(index: number) {
    setAgents((prev) => prev.filter((_, i) => i !== index))
  }

  function addAgent() {
    setAgents((prev) => [...prev, { name: "", persona: "" }])
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!topic.trim() || agents.length < 2) return
    const valid = agents.filter((a) => a.name.trim() && a.persona.trim())
    if (valid.length < 2) return
    onStart(topic.trim(), valid, model)
  }

  const canSubmit =
    topic.trim().length > 0 &&
    agents.filter((a) => a.name.trim() && a.persona.trim()).length >= 2

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-12">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl space-y-8 rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-sm"
      >
        {/* Title */}
        <div className="text-center">
          <h1 className="bg-gradient-to-r from-violet-400 via-cyan-400 to-emerald-400 bg-clip-text text-4xl font-bold tracking-tight text-transparent">
            ⚡ LMSociety
          </h1>
          <p className="mt-2 text-sm text-white/50">
            Set up a debate between AI agents with distinct perspectives
          </p>
        </div>

        {/* Topic */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-white/70">Debate Topic</label>
          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Should AI control city traffic lights?"
            rows={3}
            className="w-full resize-none rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/25 outline-none transition-colors focus:border-violet-400/50 focus:bg-white/[0.07]"
          />
        </div>

        {/* Model selector */}
        <div className="space-y-3">
          <label className="block text-sm font-medium text-white/70">LLM Model</label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {AVAILABLE_MODELS.map((m) => (
              <button
                key={m.id}
                type="button"
                onClick={() => setModel(m.id)}
                className={`cursor-pointer rounded-lg border px-4 py-3 text-left transition-all duration-150 ${
                  model === m.id
                    ? "border-violet-400/60 bg-violet-400/10 text-white"
                    : "border-white/10 bg-white/5 text-white/60 hover:border-white/20 hover:bg-white/[0.07]"
                }`}
              >
                <div className="text-sm font-medium">{m.label}</div>
                <div className="mt-0.5 text-xs text-white/40">{m.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Agents */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="block text-sm font-medium text-white/70">Agents</label>
            <button
              type="button"
              onClick={addAgent}
              className="cursor-pointer rounded-md border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium text-white/60 transition-colors hover:bg-white/10 hover:text-white"
            >
              + Add Agent
            </button>
          </div>

          <div className="space-y-3">
            {agents.map((agent, i) => (
              <div
                key={i}
                className="flex gap-3 rounded-lg border border-white/10 bg-white/[0.03] p-3"
              >
                <div className="flex flex-1 flex-col gap-2 sm:flex-row">
                  <input
                    type="text"
                    value={agent.name}
                    onChange={(e) => updateAgent(i, "name", e.target.value)}
                    placeholder="Agent name"
                    className="w-full rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder-white/25 outline-none transition-colors focus:border-violet-400/50 sm:w-40"
                  />
                  <input
                    type="text"
                    value={agent.persona}
                    onChange={(e) => updateAgent(i, "persona", e.target.value)}
                    placeholder="Persona description"
                    className="flex-1 rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder-white/25 outline-none transition-colors focus:border-violet-400/50"
                  />
                </div>
                {agents.length > 2 && (
                  <button
                    type="button"
                    onClick={() => removeAgent(i)}
                    className="cursor-pointer self-center rounded-md px-2 py-1 text-white/30 transition-colors hover:bg-red-500/10 hover:text-red-400"
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={!canSubmit || isLoading}
          className="w-full cursor-pointer rounded-xl bg-gradient-to-r from-violet-500 to-cyan-500 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-violet-500/20 transition-all duration-200 hover:shadow-xl hover:shadow-violet-500/30 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {isLoading ? (
            <span className="inline-flex items-center gap-2">
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" className="opacity-25" />
                <path d="M4 12a8 8 0 018-8" stroke="currentColor" strokeWidth="3" strokeLinecap="round" className="opacity-75" />
              </svg>
              Starting Debate…
            </span>
          ) : (
            "Start Debate"
          )}
        </button>
      </form>
    </div>
  )
}
