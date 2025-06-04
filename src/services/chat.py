from core.prompt import get_camera_recommendation


def output_message(cameras, reason, text):
    cameras_dash = [c.replace(" ", "-").lower() for c in cameras]
    print("Recommended Cameras:")
    for camera in cameras_dash:
        print(f"- {camera}")
        print(f"https://www.mpb.com/en-uk/product/{camera}")
    print("\nReasoning:")
    print(reason)
    print("\nFurther Reading:")

    for camera in cameras:
        print(f"- {camera}")
        print(
            f"  - DPReview: https://www.dpreview.com/search?query={camera.replace(' ', '%20')}"
        )
        print(
            f"  - PhotographyBlog: https://www.photographyblog.com/search/results?q={camera.replace(' ', '+')}"
        )
        print(
            f"\n  - Youtube: https://www.youtube.com/results?search_query={camera.replace(' ', '+')}+review"
        )
        print(
            f"  - Reddit: https://www.reddit.com/search/?q={camera.replace(' ', '+')}+review"
        )
        print(
            f"\n  - Brand Website: https://www.google.co.uk/search?q={camera.replace(' ', '%20')} (would be precalculated)\n\n"
        )

    print("\nHistory:")
    print(text)


__all__ = ["get_camera_recommendation", "output_message"]
