FROM ubuntu:24.04

ARG NODE_MAJOR=22
ARG JDK_VERSION=21
ARG ANDROID_API_LEVEL=35
ARG ANDROID_BUILD_TOOLS=35.0.0
ARG ANDROID_NDK_VERSION=27.2.12479018
ARG CMAKE_VERSION=3.22.1

ENV DEBIAN_FRONTEND=noninteractive

# ── System packages ──────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl wget unzip git xclip fontconfig \
    build-essential software-properties-common \
    sudo locales \
    usbutils \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# ── Python 3.14 ──────────────────────────────────────────────────────
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.14 \
    python3.14-dev \
    python3.14-venv \
    && rm -rf /var/lib/apt/lists/*

# Bootstrap pip for 3.14 (deadsnakes does not ship pip packages)
RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3.14



# Make python3.14 the default python
RUN ln -sf /usr/bin/python3.14 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.14 /usr/bin/python


# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# ── OpenJDK ──────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-${JDK_VERSION}-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-${JDK_VERSION}-openjdk-amd64

# ── Node.js ──────────────────────────────────────────────────────────
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && corepack enable

# ── Android SDK ──────────────────────────────────────────────────────
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=${ANDROID_HOME}
ENV PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

RUN mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \
       -O /tmp/cmdline-tools.zip \
    && unzip -q /tmp/cmdline-tools.zip -d /tmp/cmdline-tools \
    && mv /tmp/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest \
    && rm /tmp/cmdline-tools.zip

RUN yes | sdkmanager --licenses > /dev/null 2>&1 \
    && sdkmanager --no_https \
       "platform-tools" \
       "platforms;android-${ANDROID_API_LEVEL}" \
       "build-tools;${ANDROID_BUILD_TOOLS}" \
       "ndk;${ANDROID_NDK_VERSION}" \
       "cmake;${CMAKE_VERSION}"


# ── Global npm tools ─────────────────────────────────────────────────
RUN npm install -g eas-cli @google/gemini-cli &&  npm install -g repomix && npm install -g @zed-industries/claude-code-acp
# ── Non-root user ────────────────────────────────────────────────────
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN EXISTING_USER=$(getent passwd ${USER_UID} | cut -d: -f1) \
    && if [ -n "$EXISTING_USER" ] && [ "$EXISTING_USER" != "${USERNAME}" ]; then \
         usermod -l ${USERNAME} -d /home/${USERNAME} -m "$EXISTING_USER"; \
         EXISTING_GROUP=$(getent group ${USER_GID} | cut -d: -f1); \
         [ -n "$EXISTING_GROUP" ] && groupmod -n ${USERNAME} "$EXISTING_GROUP"; \
       elif [ -z "$EXISTING_USER" ]; then \
         getent group ${USER_GID} >/dev/null || groupadd --gid ${USER_GID} ${USERNAME}; \
         useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}; \
       fi \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Let the non-root user write to the Android SDK (gradle downloads extras)
RUN chown -R ${USER_UID}:${USER_GID} ${ANDROID_HOME}

ENV PATH="/usr/local/bin:$HOME/.local/bin:$PATH"

USER ${USERNAME}
WORKDIR /workspace

CMD ["/bin/bash"]
