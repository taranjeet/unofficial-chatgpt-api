FROM gitpod/workspace-full-vnc

# https://www.gitpod.io/blog/native-ui-with-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libx11-dev libxkbfile-dev libsecret-1-dev libgconf2–4 libnss3 && \
    sudo rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN npx playwright install --with-deps
