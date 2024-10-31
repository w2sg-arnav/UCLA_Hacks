FROM ubuntu:22.04

# Set arguments and environment variables
ARG DEBIAN_FRONTEND=noninteractive
ARG PCCS_VERSION="1.21.100.3-jammy1"

# Install essential tools and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    curl \
    vim \
    git \
    python3.9 \
    python3-pip \
    tpm2-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install pandas numpy jupyterlab

# Configure JupyterLab
RUN jupyter lab --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py

# Download and setup Intel SGX dependencies
RUN wget https://download.01.org/intel-sgx/sgx-dcap/1.21/linux/distro/ubuntu22.04-server/sgx_debian_local_repo.tgz && \
    tar zxvf sgx_debian_local_repo.tgz && \
    rm -f sgx_debian_local_repo.tgz

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo "deb [trusted=yes arch=amd64] file:/sgx_debian_local_repo jammy main" | \
    tee /etc/apt/sources.list.d/sgx_debian_local_repo.list

RUN mkdir -p /etc/apt/keyrings
RUN set -o pipefail && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | \
    gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -o pipefail && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" | \
    tee /etc/apt/sources.list.d/nodesource.list

# Install SGX dependencies
RUN apt-get update && apt-get install -y \
    nodejs=18.18.2-1nodesource1 \
    cracklib-runtime \
    sgx-dcap-pccs=${PCCS_VERSION} \
    sgx-pck-id-retrieval-tool=${PCCS_VERSION} \
    && rm -rf /var/lib/apt/lists/*

# Setup Intel SGX PCCS
RUN cd /opt/intel/sgx-dcap-pccs/ && \
    npm config set engine-strict true && \
    npm install

RUN mkdir /opt/intel/sgx-dcap-pccs/ssl_key

# Copy necessary configuration files
COPY container/pccs/default.json /opt/intel/sgx-dcap-pccs/config/
COPY container/pccs/network_setting.conf /opt/intel/sgx-pck-id-retrieval-tool/
COPY container/pccs/ssl_key /opt/intel/sgx-dcap-pccs/ssl_key

# Add and configure a new user
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 ubuntu
USER ubuntu
WORKDIR /opt/intel/sgx-dcap-pccs/

# Expose necessary ports
EXPOSE 8081 8888

# Initialize TPM and create keys
RUN tpm2_createek --ek-context rsa_ek.ctx --key-algorithm rsa --public rsa_ek.pub && \
    tpm2_createak \
       --ek-context rsa_ek.ctx \
       --ak-context rsa_ak.ctx \
       --key-algorithm rsa \
       --hash-algorithm sha256 \
       --signing-algorithm rsassa \
       --public rsa_ak.pub \
       --private rsa_ak.priv \
       --ak-name rsa_ak.name && \
    tpm2_pcrread sha1:0,1,2+sha256:0,1,2

# Command to run both JupyterLab and PCCS
CMD ["bash", "-c", "jupyter lab --ip=0.0.0.0 --no-browser --allow-root & node pccs_server.js"]
