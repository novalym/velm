# scaffold/semantic_injection/directives/kinesis_domain.py

"""
=================================================================================
== THE NERVOUS SYSTEM (V-Ω-KINESIS-DOMAIN)                                     ==
=================================================================================
LIF: 250,000,000,000

This artisan implements the `@kinesis` namespace. It enables Event-Driven
Architecture (EDA) by generating producers, consumers, and schemas.

Usage:
    events.py :: @kinesis/schema(name="OrderPlaced", fields="id:uuid, total:float")
    worker.py :: @kinesis/consumer(topic="orders", broker="redis")
    lib/bus.ts :: @kinesis/emitter(type="typed")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("kinesis")
class KinesisDomain(BaseDirectiveDomain):
    """
    The Weaver of Asynchronous Will.
    """

    @property
    def namespace(self) -> str:
        return "kinesis"

    def help(self) -> str:
        return "Generates Event-Driven Architecture scaffolding (Schemas, Pub/Sub)."

    def _directive_schema(self, context: Dict[str, Any], name: str, fields: str, lang: str = "python", *args,
                          **kwargs) -> str:
        """
        @kinesis/schema(name="UserCreated", fields="user_id:str, email:str")
        Generates a strongly-typed event envelope.
        """
        if lang == "python":
            # Pydantic Event Model
            field_defs = "\n    ".join(
                [f"{f.split(':')[0].strip()}: {f.split(':')[1].strip()}" for f in fields.split(',')])
            return dedent(f"""
                from pydantic import BaseModel
                from datetime import datetime
                from uuid import UUID, uuid4

                class {name}Event(BaseModel):
                    event_id: UUID = uuid4()
                    timestamp: datetime = datetime.utcnow()
                    type: str = "{name}"

                    # Payload
                    {field_defs}
            """).strip()
        elif lang == "typescript":
            # Zod Schema + Type
            field_defs = "\n  ".join(
                [f"{f.split(':')[0].strip()}: z.string()," for f in fields.split(',')])  # Simplified mapping
            return dedent(f"""
                import {{ z }} from 'zod';

                export const {name}Schema = z.object({{
                  eventId: z.string().uuid(),
                  timestamp: z.date(),
                  type: z.literal('{name}'),
                  payload: z.object({{
                    {field_defs}
                  }})
                }});

                export type {name}Event = z.infer<typeof {name}Schema>;
            """).strip()
        return "# Unknown language for schema."

    def _directive_consumer(self, context: Dict[str, Any], topic: str, broker: str = "redis", *args, **kwargs) -> str:
        """
        @kinesis/consumer(topic="orders", broker="redis")
        Generates a background worker loop.
        """
        if broker == "redis":
            return dedent(f"""
                import redis
                import json
                import os

                # Gnostic Requirement: pip install redis
                r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
                pubsub = r.pubsub()
                pubsub.subscribe('{topic}')

                print(f"[*] Kinesis Worker listening on channel: {topic}")

                for message in pubsub.listen():
                    if message['type'] == 'message':
                        data = json.loads(message['data'])
                        print(f"[x] Received event: {{data.get('type', 'Unknown')}}")
                        # Gnostic TODO: Handle event logic here
            """).strip()
        return "# Broker implementation not found."

    def _directive_emitter(self, context: Dict[str, Any], type: str = "simple", *args, **kwargs) -> str:
        """
        @kinesis/emitter
        Generates a singleton event bus.
        """
        return dedent("""
            import { EventEmitter } from 'events';

            class GnosticBus extends EventEmitter {
              private static instance: GnosticBus;

              private constructor() {
                super();
                this.setMaxListeners(20);
              }

              public static getInstance(): GnosticBus {
                if (!GnosticBus.instance) {
                  GnosticBus.instance = new GnosticBus();
                }
                return GnosticBus.instance;
              }

              public publish(event: string, payload: any) {
                console.log(`[Kinesis] Emitting: ${event}`, payload);
                this.emit(event, payload);
              }
            }

            export const bus = GnosticBus.getInstance();
        """).strip()