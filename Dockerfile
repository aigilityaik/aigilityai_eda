FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Install necessary packages for wkhtmltopdf and xvfb to work properly
RUN apt-get update && apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    xvfb \
    xauth \
    fontconfig \
    libfontconfig1 \
    libxrender1 \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a wrapper for wkhtmltopdf to run it with xvfb
RUN echo '#!/bin/sh' > /usr/local/bin/wkhtmltopdf.sh \
    && echo 'xvfb-run -a wkhtmltopdf "$@"' >> /usr/local/bin/wkhtmltopdf.sh \
    && chmod +x /usr/local/bin/wkhtmltopdf.sh \
    && ln -s /usr/local/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

EXPOSE 5000

CMD ["python", "app.py"]
