FROM python:3

ARG workdir=/app
ARG appuser=usero

WORKDIR ${workdir}

RUN apt update && \
    apt --yes dist-upgrade && \
    apt --yes install libdbus-glib-1-2 libgtk-3-0 && \
    apt clean

RUN wget http://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.24.0-linux64.tar.gz && \
    rm geckodriver-v0.24.0-linux64.tar.gz && \
    chmod +x geckodriver

RUN wget -O FirefoxSetup.tar.bz2 "http://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" && \
    mkdir /opt/firefox && \
    tar xjf FirefoxSetup.tar.bz2 -C /opt/ && \
    rm FirefoxSetup.tar.bz2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PATH=$PATH:/opt/firefox/:${workdir}
#ENV FLASK_APP=app.py

RUN useradd -m -d /home/${appuser} ${appuser}

COPY . .

RUN chown -R ${appuser}:${appuser} ${workdir}

USER ${appuser}

ENV FLASK_ENV=development

RUN pytest test/

ENV FLASK_ENV=production

#CMD [ "python", "-m", "flask",  "run", "--host=0.0.0.0", "--port=9999" ]
#CMD [ "python", "-m", "flask",  "run", "--host=0.0.0.0" ]
ENTRYPOINT [ "./entry-point.sh" ]

# FLASK_APP=sript.py python -m flask run --host=0.0.0.0 --port=9999
