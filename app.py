import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse


BASE_DIR = Path(__file__).resolve().parent


def _section_config() -> Dict[str, Dict]:
    return {
        "section_c": {
            "label": "Section C - Sales & Population Exposure",
            "description": "Generates Section C with sales analytics and population exposure.",
            "script": "c.py",
            "cwd": BASE_DIR / "section_c",
            "output_dir": str(BASE_DIR / "section_c" / "output"),
            "voice": ["section c", "generate c", "sales section", "population section"],
        },
        "section_d": {
            "label": "Section D - Serious Incidents",
            "description": "Compiles Section D incident analytics and documentation.",
            "script": "d.py",
            "cwd": BASE_DIR / "section_d",
            "output_dir": str(BASE_DIR / "section_d" / "output"),
            "voice": ["section d", "generate d", "incident section"],
        },
        "section_f": {
            "label": "Section F - Performance And Safety",
            "description": "Produces Section F performance and safety data outputs.",
            "script": "f.py",
            "cwd": BASE_DIR / "section_f",
            "output_dir": str(BASE_DIR / "section_f" / "output"),
            "voice": ["section f", "generate f", "performance section", "safety section"],
        },
        "section_g": {
            "label": "Section G - Complaints And Trends",
            "description": "Generates Section G complaint trending analytics.",
            "script": "g.py",
            "cwd": BASE_DIR / "section_g",
            "output_dir": str(BASE_DIR / "section_g" / "output"),
            "voice": ["section g", "generate g", "complaints section"],
        },
        "section_j": {
            "label": "Section J - Literature Review",
            "description": "Runs Section J literature synthesis routines.",
            "script": "j.py",
            "cwd": BASE_DIR / "section_j",
            "output_dir": str(BASE_DIR / "section_j" / "output"),
            "voice": ["section j", "generate j", "literature section"],
        },
        "section_k": {
            "label": "Section K - Marketed vs Evaluated",
            "description": "Creates Section K comparative market analysis output.",
            "script": "k.py",
            "cwd": BASE_DIR / "section_k",
            "output_dir": str(BASE_DIR / "section_k" / "output"),
            "voice": ["section k", "generate k", "market section"],
        },
        "section_l": {
            "label": "Section L - Clinical Data",
            "description": "Builds Section L clinical data consolidation.",
            "script": "l.py",
            "cwd": BASE_DIR / "section_l",
            "output_dir": str(BASE_DIR / "section_l" / "output"),
            "voice": ["section l", "generate l", "clinical section"],
        },
        "section_m": {
            "label": "Section M - Risk Benefit",
            "description": "Generates Section M risk benefit documentation.",
            "script": "m.py",
            "cwd": BASE_DIR / "section_m",
            "output_dir": str(BASE_DIR / "section_m" / "output"),
            "voice": ["section m", "generate m", "risk section", "benefit section"],
        },
    }


SECTIONS = _section_config()


def _section_metadata() -> List[Dict]:
    payload = []
    for key, config in SECTIONS.items():
        payload.append(
            {
                "id": key,
                "label": config["label"],
                "description": config["description"],
                "outputDir": config["output_dir"],
                "voice": config["voice"],
            }
        )
    return payload


SECTION_METADATA = _section_metadata()
SECTION_METADATA_JSON = json.dumps(SECTION_METADATA)


INDEX_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PSUR Voice Orchestrator</title>
    <style>
        :root {{
            color-scheme: dark light;
            --bg: #07070a;
            --fg: #e8e9eb;
            --accent: #49a3ff;
            --muted: rgba(232, 233, 235, 0.45);
            --surface: rgba(17, 22, 33, 0.68);
            --success: #90ee90;
            --danger: #ff6b6b;
        }}
        * {{
            box-sizing: border-box;
            font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
        }}
        body {{
            margin: 0;
            min-height: 100vh;
            padding: 0;
            background: radial-gradient(circle at top, rgba(73,163,255,0.08), transparent 55%), var(--bg);
            color: var(--fg);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .shell {{
            width: min(1280px, 96vw);
            padding: 2.5rem 3rem;
            background: linear-gradient(135deg, rgba(9,12,20,0.92), rgba(9,12,20,0.75));
            backdrop-filter: blur(22px);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 28px;
            box-shadow: 0 22px 45px rgba(6,7,16,0.55);
            display: grid;
            gap: 2rem;
        }}
        header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        header .brand {{
            font-size: 1.6rem;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
            color: var(--muted);
        }}
        header .status-stack {{
            display: flex;
            align-items: center;
            gap: 1.2rem;
            color: var(--muted);
            font-size: 0.95rem;
        }}
        .signal {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--muted);
            position: relative;
            transition: transform 160ms ease, background 160ms ease;
        }}
        .signal.active {{
            background: var(--accent);
            transform: scale(1.2);
        }}
        .panel {{
            display: grid;
            gap: 1.5rem;
        }}
        .voice-card {{
            background: var(--surface);
            border-radius: 24px;
            padding: 2rem;
            display: grid;
            gap: 1.6rem;
            border: 1px solid rgba(255,255,255,0.06);
        }}
        .voice-control {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}
        .voice-btn {{
            all: unset;
            padding: 0.9rem 1.8rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(73,163,255,0.12);
            color: var(--fg);
            font-weight: 600;
            letter-spacing: 0.04rem;
            cursor: pointer;
            transition: transform 150ms ease, background 150ms ease, border 150ms ease;
        }}
        .voice-btn:hover {{
            transform: translateY(-1px);
            border-color: rgba(73,163,255,0.45);
        }}
        .voice-btn.live {{
            background: rgba(73,163,255,0.28);
            border-color: rgba(73,163,255,0.68);
            box-shadow: 0 0 0 8px rgba(73,163,255,0.08);
        }}
        .transcript {{
            background: rgba(8,11,20,0.68);
            border-radius: 20px;
            padding: 1.6rem;
            min-height: 140px;
            border: 1px solid rgba(255,255,255,0.05);
            display: grid;
            gap: 0.8rem;
        }}
        .transcript .label {{
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.22rem;
            color: var(--muted);
        }}
        #transcript-text {{
            font-size: 1.1rem;
            line-height: 1.6rem;
            color: var(--fg);
            white-space: pre-line;
        }}
        .grid {{
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }}
        .chip {{
            padding: 1rem 1.2rem;
            background: rgba(73,163,255,0.1);
            border: 1px solid rgba(73,163,255,0.22);
            border-radius: 18px;
            cursor: pointer;
            display: grid;
            gap: 0.5rem;
            transition: transform 150ms ease, background 150ms ease, border 150ms ease;
        }}
        .chip:hover {{
            transform: translateY(-2px);
            border-color: rgba(73,163,255,0.6);
        }}
        .chip .title {{
            font-weight: 600;
        }}
        .chip .copy {{
            font-size: 0.85rem;
            color: var(--muted);
        }}
        .log {{
            background: rgba(8,11,20,0.72);
            border-radius: 20px;
            padding: 1.6rem;
            border: 1px solid rgba(255,255,255,0.05);
            max-height: 280px;
            overflow-y: auto;
            font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
            font-size: 0.9rem;
            line-height: 1.45rem;
        }}
        .log::-webkit-scrollbar {{
            width: 6px;
        }}
        .log::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.14);
            border-radius: 4px;
        }}
        .log-line {{
            color: rgba(214, 218, 224, 0.88);
        }}
        .log-line.status {{
            color: var(--accent);
        }}
        .log-line.error {{
            color: var(--danger);
        }}
        .log-line.success {{
            color: var(--success);
        }}
        @media (max-width: 960px) {{
            .shell {{
                padding: 1.8rem;
                border-radius: 20px;
            }}
            header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="shell">
        <header>
            <div class="brand">PSUR // Real-Time Voice Console</div>
            <div class="status-stack">
                <span>Voice Link</span>
                <div class="signal" id="signal-indicator"></div>
            </div>
        </header>

        <section class="panel">
            <div class="voice-card">
                <div class="voice-control">
                    <button id="voice-btn" class="voice-btn">Start Voice Link</button>
                    <div id="voice-state" style="text-transform: uppercase; letter-spacing: 0.18rem; font-size: 0.72rem; color: var(--muted);">IDLE</div>
                </div>

                <div class="transcript">
                    <div class="label">Live Transcript</div>
                    <div id="transcript-text"></div>
                </div>

                <div class="grid" id="section-grid"></div>

                <div class="log" id="log-stream"></div>
            </div>
        </section>
    </div>
    <script>
        window.__sectionVoice = {SECTION_METADATA_JSON};
    </script>
    <script>
        (function () {{
            const sectionGrid = document.getElementById("section-grid");
            const logStream = document.getElementById("log-stream");
            const transcriptEl = document.getElementById("transcript-text");
            const voiceBtn = document.getElementById("voice-btn");
            const voiceState = document.getElementById("voice-state");
            const signal = document.getElementById("signal-indicator");
            const sections = window.__sectionVoice || [];
            const synth = window.speechSynthesis;
            let websocket = null;
            let recognition = null;
            let listening = false;
            let transcriptFinal = "";
            let transcriptInterim = "";

            function speak(message) {{
                if (!message) return;
                if (!("speechSynthesis" in window)) return;
                const utterance = new SpeechSynthesisUtterance(message);
                utterance.rate = 1.02;
                utterance.pitch = 1.0;
                synth.cancel();
                synth.speak(utterance);
            }}

            function appendLog(message, type = "log") {{
                const line = document.createElement("div");
                line.classList.add("log-line");
                if (type) line.classList.add(type);
                line.textContent = message;
                logStream.appendChild(line);
                logStream.scrollTop = logStream.scrollHeight;
            }}

            function updateTranscript() {{
                transcriptEl.textContent = [transcriptFinal.trim(), transcriptInterim ? "• " + transcriptInterim.trim() : ""]
                    .filter(Boolean)
                    .join("\\n");
            }}

            function setVoiceState(state) {{
                voiceState.textContent = state.toUpperCase();
                if (state === "listening") {{
                    voiceBtn.classList.add("live");
                    signal.classList.add("active");
                }} else {{
                    voiceBtn.classList.remove("live");
                    signal.classList.remove("active");
                }}
            }}

            function ensureWebSocket() {{
                if (websocket && websocket.readyState === WebSocket.OPEN) return;
                const proto = window.location.protocol === "https:" ? "wss" : "ws";
                websocket = new WebSocket(proto + "://" + window.location.host + "/ws/voice");

                websocket.addEventListener("open", () => {{
                    appendLog("Voice channel established.", "status");
                }});

                websocket.addEventListener("message", (event) => {{
                    try {{
                        const payload = JSON.parse(event.data);
                        if (payload.type === "hello") {{
                            appendLog("Session ready.", "status");
                        }} else if (payload.type === "status") {{
                            appendLog(payload.message, "status");
                            speak(payload.tts || payload.message);
                        }} else if (payload.type === "log") {{
                            appendLog(payload.message);
                        }} else if (payload.type === "error") {{
                            appendLog(payload.message, "error");
                            speak(payload.tts || payload.message);
                        }} else if (payload.type === "complete") {{
                            const statusMsg = payload.status === "success"
                                ? "Section " + payload.section + " complete. Output saved to " + payload.output_dir + "."
                                : payload.status === "cancelled"
                                    ? "Section " + payload.section + " cancelled."
                                    : "Section " + payload.section + " ended with errors.";
                            appendLog(statusMsg, payload.status === "success" ? "success" : "error");
                            speak(statusMsg);
                        }} else if (payload.type === "echo") {{
                            appendLog("Heard: " + payload.message, "status");
                        }}
                    }} catch (err) {{
                        appendLog("Stream error: " + err.message, "error");
                    }}
                }});

                websocket.addEventListener("close", () => {{
                    appendLog("Voice channel closed.", "status");
                }});

                websocket.addEventListener("error", () => {{
                    appendLog("Voice channel error.", "error");
                }});
            }}

            function sendWebSocket(data) {{
                ensureWebSocket();
                if (!websocket || websocket.readyState !== WebSocket.OPEN) {{
                    appendLog("Voice channel not ready.", "error");
                    return;
                }}
                websocket.send(JSON.stringify(data));
            }}

            function handleCommand(text) {{
                if (!text) return;
                const normalised = text.trim().toLowerCase();
                if (!normalised) return;

                if (["stop", "cancel", "abort"].some((token) => normalised.includes(token))) {{
                    sendWebSocket({{ type: "cancel" }});
                    speak("Cancelling current generation.");
                    return;
                }}

                for (const section of sections) {{
                    if (section.voice.some((voiceToken) => normalised.includes(voiceToken))) {{
                        sendWebSocket({{ type: "generate", section: section.id }});
                        speak("Executing " + section.label + ".");
                        return;
                    }}
                }}

                sendWebSocket({{ type: "utterance", text: normalised }});
            }}

            function initialiseRecognition() {{
                const VoiceRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!VoiceRecognition) {{
                    appendLog("Voice recognition not supported in this browser.", "error");
                    voiceBtn.disabled = true;
                    return;
                }}
                recognition = new VoiceRecognition();
                recognition.lang = "en-US";
                recognition.continuous = true;
                recognition.interimResults = true;

                recognition.onstart = () => {{
                    listening = true;
                    setVoiceState("listening");
                    appendLog("Listening...", "status");
                }};

                recognition.onerror = (event) => {{
                    appendLog("Voice error: " + event.error, "error");
                    stopListening();
                }};

                recognition.onend = () => {{
                    if (listening) {{
                        recognition.start();
                    }} else {{
                        setVoiceState("idle");
                    }}
                }};

                recognition.onresult = (event) => {{
                    let interim = "";
                    let final = "";
                    for (let i = event.resultIndex; i < event.results.length; i++) {{
                        const result = event.results[i];
                        const transcript = result[0].transcript;
                        if (result.isFinal) {{
                            final += transcript;
                        }} else {{
                            interim += transcript;
                        }}
                    }}
                    if (final) {{
                        transcriptFinal += " " + final;
                        handleCommand(final);
                    }}
                    transcriptInterim = interim;
                    updateTranscript();
                }};
            }}

            function startListening() {{
                ensureWebSocket();
                if (!recognition) initialiseRecognition();
                if (!recognition) return;
                if (listening) return;
                transcriptFinal = "";
                transcriptInterim = "";
                updateTranscript();
                recognition.start();
            }}

            function stopListening() {{
                listening = false;
                if (recognition) {{
                    recognition.stop();
                }}
                setVoiceState("idle");
            }}

            voiceBtn.addEventListener("click", () => {{
                if (listening) {{
                    stopListening();
                }} else {{
                    startListening();
                }}
            }});

            sections.forEach((section) => {{
                const chip = document.createElement("button");
                chip.type = "button";
                chip.classList.add("chip");
                chip.innerHTML = '<span class="title">' + section.label + '</span>' +
                    '<span class="copy">' + section.description + '</span>';
                chip.addEventListener("click", () => {{
                    sendWebSocket({{ type: "generate", section: section.id }});
                    speak("Executing " + section.label + ".");
                }});
                sectionGrid.appendChild(chip);
            }});

            ensureWebSocket();
        }})();
    </script>
</body>
</html>
"""


app = FastAPI(title="PSUR Voice Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)


@app.get("/api/sections", response_class=JSONResponse)
async def list_sections() -> JSONResponse:
    return JSONResponse(SECTION_METADATA)


async def handle_utterance(text: str, websocket: WebSocket) -> None:
    await websocket.send_json(
        {
            "type": "echo",
            "message": "Command not recognised. Try asking for a specific PSUR section.",
        }
    )


async def run_section(section_id: str, websocket: WebSocket, state: Dict) -> None:
    config = SECTIONS[section_id]
    await websocket.send_json(
        {
            "type": "status",
            "message": f"Launching {config['label']}...",
            "tts": f"Launching {config['label']}.",
        }
    )

    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-u",
        config["script"],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(config["cwd"]),
        env=os.environ.copy(),
    )
    state["process"] = process

    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            await websocket.send_json(
                {
                    "type": "log",
                    "message": line.decode("utf-8", errors="ignore").rstrip(),
                }
            )

        return_code = await process.wait()
        status = "success" if return_code == 0 else "error"
        await websocket.send_json(
            {
                "type": "complete",
                "status": status,
                "section": section_id,
                "output_dir": config["output_dir"],
                "return_code": return_code,
            }
        )
    except asyncio.CancelledError:
        try:
            await websocket.send_json(
                {
                    "type": "complete",
                    "status": "cancelled",
                    "section": section_id,
                    "output_dir": config["output_dir"],
                    "return_code": None,
                }
            )
        finally:
            raise
    finally:
        if process.returncode is None:
            process.kill()
        state["process"] = None


@app.websocket("/ws/voice")
async def voice_channel(websocket: WebSocket) -> None:
    await websocket.accept()
    session_state: Dict[str, asyncio.Task] = {"task": None, "process": None}
    await websocket.send_json({"type": "hello", "sections": SECTION_METADATA})

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid payload received.",
                        "tts": "Invalid message received.",
                    }
                )
                continue

            message_type = payload.get("type")

            if message_type == "generate":
                section_id = payload.get("section")
                if not section_id or section_id not in SECTIONS:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "Unknown section requested.",
                            "tts": "Unknown section requested.",
                        }
                    )
                    continue

                if session_state.get("task") and not session_state["task"].done():
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "A section is already running. Say cancel to stop it first.",
                            "tts": "A section is already running. Say cancel to stop it first.",
                        }
                    )
                    continue

                task = asyncio.create_task(run_section(section_id, websocket, session_state))
                session_state["task"] = task

            elif message_type == "cancel":
                task = session_state.get("task")
                process = session_state.get("process")

                if task and not task.done():
                    task.cancel()
                if process and process.returncode is None:
                    process.kill()

                await websocket.send_json(
                    {
                        "type": "status",
                        "message": "Cancellation requested.",
                        "tts": "Cancellation requested.",
                    }
                )

            elif message_type == "utterance":
                await handle_utterance(payload.get("text", ""), websocket)

            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Unsupported message type.",
                        "tts": "Unsupported message type.",
                    }
                )

    except WebSocketDisconnect:
        task = session_state.get("task")
        process = session_state.get("process")
        if task and not task.done():
            task.cancel()
        if process and process.returncode is None:
            process.kill()
    finally:
        task = session_state.get("task")
        process = session_state.get("process")
        if task and not task.done():
            task.cancel()
        if process and process.returncode is None:
            process.kill()
