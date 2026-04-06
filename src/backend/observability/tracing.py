import os
from dotenv import load_dotenv

load_dotenv()

PHOENIX_TRACING_URL = os.getenv("PHOENIX_TRACING_URL")
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")
ARIZE_SPACE_ID = os.getenv("ARIZE_SPACE_ID")


def setup_phoenix():
    """Phoenix setup of cloud or self-hosted"""
    if ARIZE_API_KEY and ARIZE_SPACE_ID:
        try:
            import arize.otel as arize_otel

            arize_otel.register(
                project_name="lmsociety",
                api_key=ARIZE_API_KEY,
                space_id=ARIZE_SPACE_ID,
            )
        except ImportError:
            pass
    elif PHOENIX_TRACING_URL:
        try:
            from phoenix.otel import register

            register(project_name="lmsociety", endpoint=PHOENIX_TRACING_URL)
        except ImportError:
            pass
    else:
        try:
            import phoenix as px

            px.launch_app()
        except ImportError:
            pass


def instrument_dspy():
    """DSPy traces logging"""
    try:
        from openinference.instrumentation.dspy import DSPyInstrumentor

        DSPyInstrumentor().instrument()
    except ImportError:
        pass


# def instrument_langchain():
#     try:
#         from openinference.instrumentation.langchain import LangChainInstrumentor

#         LangChainInstrumentor().instrument()
#     except ImportError:
#         pass
