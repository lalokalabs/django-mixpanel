FROM gitpod/workspace-full

ENV PYTHON_VERSION=3.10.6
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

ENV NODE_VERSION=14.20.0

RUN bash -c ' source $HOME/.nvm/nvm.sh && nvm install ${NODE_VERSION} \
    && nvm use ${NODE_VERSION} && nvm alias default ${NODE_VERSION}'

RUN echo "nvm use default &>/dev/null" >> ~/.bashrc.d/51-nvm-fix

RUN pip install -U pip \
    && pip install pipx \
    && pipx install typecov==0.2.1 \
    && pipx install pre-commit==2.20.0 \
    && pipx install pre-commit-hooks==4.3.0 \
    && pipx install codespell==2.1.0

# [Optional] Uncomment this section to install additional OS packages.
RUN sudo apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && sudo apt-get -y install --no-install-recommends netcat util-linux \
        vim bash-completion yamllint postgresql-client

RUN poetry self update