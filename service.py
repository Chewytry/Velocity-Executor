from flask import Flask, send_file

app = Flask(__name__)

@app.route('/download_presentation/<path:filename>')
def download_presentation(filename):
    # Assuming `filename` is the path returned by `save_presentation_temporarily`
    # Ensure security measures are in place to validate filename to avoid security issues
    print(1)
    return send_file(filename, as_attachment=True)
