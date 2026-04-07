import { useState } from "react"
import type { Agent, DebateConfig, DebateMessage } from "./types"
import { startDebate, agentSpeak, getMessages } from "./api"
import SetupForm from "./components/SetupForm"
import DebateView from "./components/DebateView"

type View = "setup" | "debate"

function App() {
  const [view, setView] = useState<View>("setup")
  const [debateId, setDebateId] = useState<number | null>(null)
  const [config, setConfig] = useState<DebateConfig | null>(null)
  const [messages, setMessages] = useState<DebateMessage[]>([])
  const [round, setRound] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [isRunningRound, setIsRunningRound] = useState(false)
  const [isAutoRunning, setIsAutoRunning] = useState(false)
  const [speakingAgent, setSpeakingAgent] = useState<string | null>(null)
  const [doneAgents, setDoneAgents] = useState<ReadonlySet<string>>(new Set())
  const [error, setError] = useState<string | null>(null)

  async function handleStart(topic: string, agents: Agent[], model: string) {
    setIsLoading(true)
    setError(null)
    try {
      const id = await startDebate({ topic, agents, model })
      setDebateId(id)
      setConfig({ topic, agents, model })
      setMessages([])
      setRound(0)
      setView("debate")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start debate")
    } finally {
      setIsLoading(false)
    }
  }

  async function handleRunRound() {
    if (!debateId || !config) return
    setIsRunningRound(true)
    setDoneAgents(new Set())
    setError(null)
    try {
      for (const agent of config.agents) {
        setSpeakingAgent(agent.name)
        await agentSpeak(debateId, agent.name)
        const updated = await getMessages(debateId)
        setMessages(updated)
        setSpeakingAgent(null)
        setDoneAgents((prev) => new Set([...prev, agent.name]))
      }
      setRound((r) => r + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to run round")
    } finally {
      setSpeakingAgent(null)
      setIsRunningRound(false)
      setDoneAgents(new Set())
    }
  }

  async function handleAutoRun() {
    if (!debateId || !config) return
    setIsAutoRunning(true)
    setIsRunningRound(true)
    setDoneAgents(new Set())
    setError(null)

    try {
      while (isAutoRunning) {
        for (const agent of config.agents) {
          if (!isAutoRunning) break
          setSpeakingAgent(agent.name)
          await agentSpeak(debateId, agent.name)
          const updated = await getMessages(debateId)
          setMessages(updated)
          setSpeakingAgent(null)
          setDoneAgents((prev) => new Set([...prev, agent.name]))
        }
        if (isAutoRunning) {
          setRound((r) => r + 1)
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Auto-run failed")
    } finally {
      setSpeakingAgent(null)
      setIsRunningRound(false)
      setIsAutoRunning(false)
      setDoneAgents(new Set())
    }
  }

  function handleStopAutoRun() {
    setIsAutoRunning(false)
  }

  async function handleSpeak(agentName: string) {
    if (!debateId) return
    setSpeakingAgent(agentName)
    setError(null)
    try {
      await agentSpeak(debateId, agentName)
      const updated = await getMessages(debateId)
      setMessages(updated)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Agent failed to speak")
    } finally {
      setSpeakingAgent(null)
    }
  }

  async function handleSendMessage(agentName: string, prompt: string) {
    if (!debateId) return
    setSpeakingAgent(agentName)
    setError(null)
    try {
      await agentSpeak(debateId, agentName, prompt)
      const updated = await getMessages(debateId)
      setMessages(updated)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message")
    } finally {
      setSpeakingAgent(null)
    }
  }

  function handleBack() {
    setView("setup")
    setDebateId(null)
    setConfig(null)
    setMessages([])
    setRound(0)
    setError(null)
  }

  return (
    <div className={`relative bg-[#0f0f14] text-white ${view === "debate" ? "h-screen overflow-hidden" : "min-h-screen"}`}>
      {/* Background gradient (setup only) */}
      {view === "setup" && (
        <div className="pointer-events-none fixed inset-0 bg-linear-to-br from-violet-500/3 via-transparent to-cyan-500/3" />
      )}

      {/* Error toast */}
      {error && (
        <div className="fixed top-4 right-4 z-50 animate-fade-in rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300 backdrop-blur-sm">
          <div className="flex items-center gap-2">
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="cursor-pointer text-red-300/60 hover:text-red-300"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Views */}
      {view === "setup" && (
        <SetupForm onStart={handleStart} isLoading={isLoading} />
      )}

      {view === "debate" && config && (
        <DebateView
          topic={config.topic}
          agents={config.agents}
          messages={messages}
          round={round}
          isRunningRound={isRunningRound}
          isAutoRunning={isAutoRunning}
          speakingAgent={speakingAgent}
          doneAgents={doneAgents}
          onRunRound={handleRunRound}
          onAutoRun={handleAutoRun}
          onStopAutoRun={handleStopAutoRun}
          onSpeak={handleSpeak}
          onSendMessage={handleSendMessage}
          onBack={handleBack}
        />
      )}
    </div>
  )
}

export default App
