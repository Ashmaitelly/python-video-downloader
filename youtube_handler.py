from yt_dlp import YoutubeDL

url = "YOUR_VIDEO_URL"

def get_video_formats(url):
  """Extracts metadata from the URL and returns a list of available formats."""
  ydl_opts = {}
  with YoutubeDL(ydl_opts) as ydl:
    # download=False only fetches metadata without downloading the video
    info_dict = ydl.extract_info(url, download=False)
    formats = info_dict.get("formats", [])
    return formats

def download_media(url, format_id=None, output_type="mp4"):
  """Downloads media based on the specified output type using match-case.

  :param url: The video URL string.
  :param format_id: The specific format ID to download (ignored for audio).
  :param output_type: 'mp4' (video), 'audio', or 'best' (auto max quality).
  """

  # This works exactly like a switch statement
  match output_type.lower():
    case "audio":
      ydl_opts = {
          "format": "bestaudio/best",
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": "192",
          }],
      }

    case "mp4":
      fmt_string = (
          f"{format_id}+bestaudio/best"
          if format_id
          else "bestvideo+bestaudio/best"
      )
      ydl_opts = {
          "format": fmt_string,
          "merge_output_format": "mp4",
      }

    case "best":
      # Bonus case: Just grab the absolute best single file format without merging
      ydl_opts = {
          "format": "best",
      }

    case _:
      # The "_" acts as the 'default' case if no match is found
      raise ValueError(
          f"Invalid output_type: '{output_type}'. Choose 'mp4', 'audio', or"
          " 'best'."
      )

  # Execute the download using the selected switch configurations
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
