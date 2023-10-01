from TikTokApi import TikTokApi
import asyncio
import os

ms_token = os.environ.get(
    "ms_token", 'r_zFL2ZdzQi_pNX7pg7UlOVeaXGJ6HCh1UIKEoluakZk-Y6i4PSA-vqpd5r_1aSZcFm91zR09iedU4BotChzQYnz6XNsRz6xcVyq_gec1Hyl4QW3aVlLkqB_uUvnVi-XkWfiTO71vguoT-fW'
)  # set your own ms_token, think it might need to have visited a profile


video_id = 7248300636498890011


async def get_comments():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(id=video_id)
        count = 0
        async for comment in video.comments(count=30):
            print(comment)
            print(comment.as_dict)


if __name__ == "__main__":
    asyncio.run(get_comments())