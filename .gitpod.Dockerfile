FROM gitpod/workspace-full-vnc

RUN sudo apt-get -qq update

# Install Playwright dependencies
RUN npx playwright install --with-deps
