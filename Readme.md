# UCLA-Hackathon

Presentation : [Trustworthy AI Lab x GES UCLA Hackathon - Team BitBuilders](./Trustworthy%20AI%20Lab%20x%20GES%20UCLA%20Hackathon.pdf)

- [Implementation of DCR](./data_clean_room/dcr_implementation.md)
---
### Overview 

Highlighting the main theme of this event  of utilizing Generative AI to empower “Data Collaboration Intelligence”. We developed a data sharing platform that allows private data sharing, predictive analytics and model building among different data parties, in essence, the “Data Clean Room” to enhance Click-through Rate (CTR) predictions using privacy-preserving synthetic data.

In both of the Parts, i.e., Implementation and Evaluation, we used various technologies including Azure Confidential Cloud VM, imbibing TDVM was well as TEE (Trusted Execution Environments),specifically Intel® TDX and SGX, GAN neural network, Gen AI, and Machine Learning Models. Similarly, several concepts like Hashing, Trusted Computing, Synthetic Data Fidelity and Synthetic Data Utility, Verification of Quote and Return Key.

---

## Data Clean Room Overview

Our secure Data Clean Room (DCR) uses Microsoft Azure Confidential VMs (Cloud VM) for enhanced data protection. These C VMs utilize Trusted Execution Environment (TEE) technology, specifically Intel® TDX and SGX , to create a secure enclave for processing data and cryptographically isolate and protect your data confidentiality and integrity.
These C VM’s have virtual Trusted Platform Modules (vTPM) built-in, and also combining the use tpm2-tools we can setup enables Remote Attestation ( which creates the keys),required for verifying that the environment is trustable.
For additional security, our programs are containerized using Docker. Containerization isolates applications from the underlying system and other applications, minimizing potential vulnerabilities.
While this approach focuses on data-in-use security, we acknowledge the importance of protecting data at rest and in transit. To achieve this, we plan to implement Azure storage encryption for data at rest and secure transfer protocols like FTPS for data transfers

![ubuntu_confidential_vm_jammy](./data_clean_room/dcr_src/ubuntu_confidential_vm_jammy.png)
![remote_attestation](./data_clean_room/dcr_src/remote_attestation.png)
|![docker_live](./data_clean_room/dcr_src/docker_live.png) |  ![docker_running_status](./data_clean_room/dcr_src/docker_running_status.png)|
|:-------------------------------------------:|:-------------------------------------------:|

---

## Data Evaluation

We aim to derive insights about potential customers by analyzing various aspects of user behavior and demographics. The following insights can help ad agencies better understand their potential customers and refine their advertising strategies to increase engagement and conversion rates.
We aimed to train a predictive model with the following parameters - Identifying Potential Customers, Incorporating Diverse Attributes, Probability Prediction. which utilizes a comprehensive set of attributes, including audience demographics, news content attributes, advertisement attributes, and device attributes, to enhance the prediction accuracy and predicts the probability that a given audience member will become a potential customer based on the aforementioned attributes, enabling more targeted and effective advertising strategies.

|![age_grp_distribution](./data_eval_src/image%20copy.png) | ![daily_engagement_ctr](./data_eval_src/image%20copy%202.png)|
|:-------------------------------------------:|:-------------------------------------------:|
| ![hourly_engagement_ctr](./data_eval_src/image%20copy.png)| ![location_users_ctr](./data_eval_src/image%20copy%203.png)|
| ![top_devices_distr](./data_eval_src/image%20copy%204.png) | ![potential_customer_ctr](./data_eval_src/potential_customer_ctr.jpg)|
|![absolute_log_mean](./task-3/src/absolute_log_mean.jpg) | ![cum_sums_per](./task-3/src/cum_sums_per.jpg)|
| ![cum_sums_per_fea](./task-3/src/cum_sums_per_fea.jpg)| ![cumson](./task-3/src/cumson.jpg)|

---

 Team Name: BitBuilders

Team Leader: Arnav Sonavane

Members:
- Manas Sewatkar
- Aarian Thakur
- Harshal More
- Devdatta Talele