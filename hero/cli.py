"""히어로 대화형 CLI.

사용:
    python -m hero.cli

종료: Ctrl+D 또는 빈 줄에서 Enter
"""

from __future__ import annotations

import asyncio
import os
import sys

from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock, ToolUseBlock

from .hero import hero_client


async def _stream_response(client) -> None:
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    print(
                        f"\n[히어로 → 도구 호출: {block.name}]",
                        flush=True,
                    )
        elif isinstance(msg, ResultMessage):
            print()  # 응답 끝 개행
            return


async def _interactive() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "❌ ANTHROPIC_API_KEY 환경변수가 필요합니다. "
            ".env 또는 셸에서 설정하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("=" * 60)
    print("히어로 (Hero) — 중소·벤처 기업 문서 에이전트")
    print("=" * 60)
    print("작성 가능: 벤처인증 / 메인비즈 / 이노비즈 / 연구노트 / 사업계획서")
    print("종료: 빈 줄 + Enter, 또는 Ctrl+D\n")

    async with hero_client() as client:
        # 첫 인사
        await client.query(
            "안녕하세요. 어떤 문서를 작성해 드릴까요? "
            "도와드릴 수 있는 5가지 작업을 안내해 주세요."
        )
        await _stream_response(client)

        while True:
            try:
                user_input = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n종료합니다.")
                break
            if not user_input:
                print("종료합니다.")
                break

            await client.query(user_input)
            await _stream_response(client)


def main() -> None:
    asyncio.run(_interactive())


if __name__ == "__main__":
    main()
