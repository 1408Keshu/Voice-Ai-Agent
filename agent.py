from dotenv import load_dotenv
load_dotenv()
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
   
    noise_cancellation,
  
)

from prompt import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web ,send_email
# from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import google


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
                llm=google.beta.realtime.RealtimeModel(
                model="gemini-2.0-flash-exp",
                voice="Aoede",
                temperature=1.7,
            ) ,
            tools=[
                get_weather,
                  search_web,
                send_email
                  ],
            )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
    #     stt=deepgram.STT(model="nova-3", language="multi"),
    #    # Gemini LLM use
    #     tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
    #     vad=silero.VAD.load(),
    #     turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
