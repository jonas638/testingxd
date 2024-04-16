import webbrowser

def play_youtube_video(video_url):
    webbrowser.open(video_url)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
    play_youtube_video(video_url)
