from flask import Flask, request, jsonify, render_template, make_response
import os
import requests
import json
import subprocess
import codecs
from agents_configs import *
import re
import time
from app_EDA import process_app
import pdfkit
from datetime import datetime
from pdfkit.configuration import Configuration

app = Flask(__name__)

# Configure pdfkit with the path to wkhtmltopdf
path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
# outside docker ye chal raha tha inside docker ye bola chatgpt
# bewkuf bana dia chatgpt uapr wala se h chal gya docker me 1 hr waster krwa dia kuch bhi bolke
#path_to_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf.sh'
# config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf.sh')

options = {
    'no-images': '',  # Disables loading of images
    'disable-external-links': '',  # Disables external links
}

config = Configuration(wkhtmltopdf=path_to_wkhtmltopdf)


html_template = "..."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("//upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part in the request."
    file = request.files["file"]

    if file.filename == "":
        print("No file uploaded, exiting")
        return "No selected file."

    if file:
        os.makedirs(".", exist_ok=True)

        file.save(os.path.join(".", file.filename))
        file_path = os.path.join(".", file.filename)


        dummy_response = process_app(file_path)

        # with open("dummy_response_maf.json", "r") as file:
        #     dummy_response = json.load(file)

        # with open("tasks_deployment_updated.json", "w") as f:
        #     json.dump(task_json_with_op, f)
        time.sleep(30)
    return jsonify(dummy_response)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.json['tasks']
    # base_url = request.host_url.rstrip('/')
    base_url = 'https://aiternity.aigilityai.com/eda' 
    # Render the PDF template with the tasks data
    curr_date = datetime.now().strftime("%Y-%m-%d")
    rendered = render_template('pdf_template.html', tasks=data, date=curr_date, base_url=base_url)

    print("Rendered HTML: %s", rendered)
    
    # Convert HTML to PDF
    # pdf = pdfkit.from_string(rendered, False)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=data_analysis_report_{curr_date}.pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="data_analysis_report_{curr_date}.pdf"'

    # response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
