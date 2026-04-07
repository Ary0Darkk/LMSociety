PROJECT_NAME = "lmsociety"


def setup_phoenix():
    """Simple local Phoenix setup (NO OTEL collector)"""

    import phoenix as px
    from phoenix.otel import register

    # Launch Phoenix UI (localhost:6006)
    px.launch_app()

    # Register tracing to this local instance
    register(project_name=PROJECT_NAME)


def instrument_all():
    """Instrument everything you might use"""

    # DSPy
    try:
        from openinference.instrumentation.dspy import DSPyInstrumentor

        DSPyInstrumentor().instrument()
    except ImportError:
        pass

    # OpenAI (VERY IMPORTANT for your setup)
    try:
        from openinference.instrumentation.openai import OpenAIInstrumentor

        OpenAIInstrumentor().instrument()
    except ImportError:
        pass

    # LangChain (optional)
    try:
        from openinference.instrumentation.langchain import LangChainInstrumentor

        LangChainInstrumentor().instrument()
    except ImportError:
        pass
