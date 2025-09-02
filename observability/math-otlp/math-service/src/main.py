from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os, uvicorn
from controller.math import get_divisors_route
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import logging

logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)

resource = Resource.create(attributes={"service.name": "math-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

LoggingInstrumentor(log_level=logging.ERROR).instrument(set_logging_format=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)

app.include_router(get_divisors_route())

ip = os.getenv("HOST", "127.0.0.0")
port = int(os.getenv("PORT", "8080"))

if __name__ == "__main__":
    FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host=ip, port=port, log_level="info", access_log=True)
