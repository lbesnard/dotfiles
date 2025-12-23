FROM python:3.12-alpine

RUN apk add --no-cache git
# Install the mpd-dynamic package directly from GitHub and other python deps
# Pin the repo URL so pip clones and installs the package
RUN pip install --no-cache-dir \
  "git+https://github.com/pauleve/mpd-dynamic.git@main#egg=mpd-dynamic" \
  spotipy python-mpd2 requests appdirs

# Work directory
WORKDIR /app

# Run the packaged CLI "mpd-dynamic"
CMD ["mpd-dynamic"]

