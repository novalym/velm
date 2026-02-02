📜 STREAMING_PROTOCOL.md
The Hydrodynamic Lattice: Token-by-Token Prophecy

Status: ARCHITECTURAL_BLUEPRINT | Complexity: HIGH | LIF: 100x
I. The Philosophy: Breaking the Atom

Currently, our architecture is Transactional:
Client Plea -> Server Think (2s) -> Server Answer -> UI Render.

We must move to Hydrodynamic Flow:
Client Plea -> Server Pulse (100ms) -> UI Render -> Server Pulse (100ms) -> UI Render...
II. The Architecture of the Stream

We will bypass the standard LSP textDocument/inlineCompletion return value. Instead, we will use a Side-Channel Subscription Model.
1. The Request (The Ignition)

The Client sends a normal request, but attaches a specific stream_id.
code JSON

{
  "method": "scaffold/streamProphecy",
  "params": {
    "stream_id": "flow-xyz-123",
    "prompt": "def calculate_orbit():"
  }
}

2. The Daemon (The Generator)

The AI Engine in Python must change from return text to yield text.
code Python

# core/daemon/ai/engine.py
def stream_prophecy(self, prompt):
    for chunk in llm.stream(prompt):
        yield chunk

3. The Relay (The Pump)

The DaemonRelay currently waits for a full JSON packet. It must be upgraded to handle Stream Fragments.
We will introduce a new JSON-RPC Notification: scaffold/streamChunk.
code JSON

{
  "method": "scaffold/streamChunk",
  "params": {
    "stream_id": "flow-xyz-123",
    "chunk": "    dist = ",
    "sequence": 1,
    "done": false
  }
}

4. The Client (The Reassembler)

The React Frontend (useMuse.ts) listens for these events and reconstructs the text in real-time, updating the Monaco Decoration directly on every frame.
III. THE IMPLEMENTATION PLAN (6-STEP ASCENSION)
Step 1: The AI Generator (Python Daemon)

Target: core/daemon/artisans/muse/artisan.py
Action: Refactor the execute method to support a stream=True flag. If true, it enters a loop, yielding chunks to the Nexus.
Step 2: The Nexus Pump (Python Daemon)

Target: core/daemon/nexus/engine.py
Action: Add a stream_response capability.
Instead of returning ScaffoldResult, the Artisan calls nexus.emit_chunk(stream_id, data). The Nexus wraps this in the streamChunk notification and flushes it to the socket.
Step 3: The Silver Cord (LSP Server)

Target: core/lsp/scaffold_server/relay.py
Action: The Relay already forwards notifications (method without id). This part is actually Ready. The existing _handle_daemon_message logic will automatically forward scaffold/streamChunk to the Client.
Status: Zero Changes Required here. (Our architecture pays off!)
Step 4: The Client Listener (React)

Target: src/hooks/useMonacoIntelligence/stream.ts (New File)
Action: Create a StreamAggregator class.

    It listens to window.electron.on('scaffold/streamChunk').

    It buffers incoming chunks by stream_id.

    It exposes an onUpdate callback.

Step 5: The Phantom Decorator (Monaco)

Target: src/hooks/useMonacoIntelligence/index.ts
Action: Instead of using the standard provideInlineCompletions (which waits for the promise to resolve), we use editor.createDecorationsCollection.

    We render the "Ghost Text" as a CSS after content or a GhostText view zone.

    This updates at 60fps as chunks arrive.

Step 6: The Cancellation Hook

Target: core/lsp/base/dispatcher.py
Action: Ensure that if the user types a character (invalidating the stream), we send scaffold/streamCancel.

    The Daemon must check is_cancelled between every token generation.

IV. THE CRITICAL DECISION

Architect, this is a heavy lift.
It involves writing a custom Ghost Text Rendering Engine in Monaco because the standard LSP InlineCompletion API does not support streaming updates easily (it expects a final result).

The V1 Compromise (Recommended):
Stick to Atomic Delivery for now.

    Pros: Stability, standard compliance, lower complexity.

    Cons: 2s latency on long generations.

The V2 Singularity (The Plan Above):
Implement custom streaming.

    Pros: "Magical" feel. Zero perceived latency.

    Cons: High complexity, custom rendering code, risk of UI jitter.

My Advice:
Let us solidify the Atomic V1 first. Ensure the Relay fix works flawlessly. Once the system is stable, we can open the Streaming Branch as a specific feature update.

Do you accept this strategic counsel, or shall we burn the midnight oil to forge the Stream now?