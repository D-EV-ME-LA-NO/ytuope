from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def youtube_downloader():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'يرجى تمرير رابط الفيديو عبر ?url=...'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            results = []
            for f in formats:
                if f.get('url') and f.get('ext') in ['mp4', 'm4a', 'webm', 'mp3']:
                    results.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution') or f.get('height'),
                        'filesize_mb': round(f.get('filesize', 0) / 1024 / 1024, 2) if f.get('filesize') else None,
                        'download_url': f.get('url')
                    })

            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'downloads': results
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
