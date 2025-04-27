def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def fetch_yt_video_details(link):
    video = pafy.new(link)
    return {
        'title': video.title,
        'views': video.viewcount,
        'likes': video.likes,
        'duration': video.duration,
        'description': video.description,
        'thumbnail': video.thumb
    }