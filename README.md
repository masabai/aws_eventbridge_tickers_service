# Production-Ready Portfolio Tracker with Event Scheduling
Automated daily portfolio reporting on a scheduled EC2 instance, with systemd launching Python scripts at startup.


## The Problem

A client wanted a daily email summary of their $200k investment portfolio delivered automatically 
after the market closes, with a reliable, hands-off process requiring no manual effort.

---

**Phase I:** AWS EC2 & EventBridge Automation
Designed a Start → Run → Stop automation system on AWS. Instead of running continuously,
the server wakes up for ~10 minutes per day to complete the task and then shuts down.


**Phase II:** Kubernetes (K8s) Modernization
I upgraded the project into a containerized microservice to learn modern cloud-native orchestration and secure 
credential management.

Setup & Deployment
Detailed step-by-step instructions for Docker builds, K8s Secrets, and CronJob scheduling are located in the SETUP.md 
file at the root of this project.


## Data Processing Workflow


```mermaid
graph TD
    subgraph "Phase 1: AWS EC2"
    A[EventBridge] --> B[EC2 Instance]
    B --> C[systemd]
    end

    subgraph "Phase 2: Kubernetes"
    D[K8s CronJob] --> E[Docker Container]
    F[K8s Secrets] --> E
    end

    C --> G[SES Email]
    E --> G

    %% Final Professional Color Palette
    style A fill:#FF4F8B,stroke:#333,color:#fff
    style B fill:#FF9900,stroke:#333,color:#fff
    style C fill:#000000,stroke:#333,color:#0f0
    style D fill:#8a2be2,stroke:#333,color:#fff
    style E fill:#2496ed,stroke:#333,color:#fff
    style F fill:#8a2be2,stroke:#333,color:#fff
    style G fill:#1b5e20,stroke:#333,color:#fff

```



---

## How It Works

### Trigger
AWS EventBridge starts the EC2 instance at a scheduled time.

## EventBridge Start Instance

![Start Instance](https://github.com/masabai/aws_eventbridge_tickers_service/raw/main/screenshots/start_instance.png)


### Execution
When Linux boots, a **systemd service** automatically launches the Python scripts.

## Systemd Service Status


![mfunds service](https://github.com/masabai/aws_eventbridge_tickers_service/raw/main/screenshots/mfunds_service.png)

### Processing Logic

The scripts:

- Pulls live market prices using the yfinance API.
- Auto-generates HTML reports and distributes them via Amazon SES.
- Calculates portfolio value and progress toward the $200k goal.

### Reporting
Clean, easy-to-read email reports were sent using **Amazon SES**.

**NOTE:**

(Portfolio holdings, values, and email recipients are **DEMONSTRATION DATA** ONLY. This project showcases automation, 
reporting, and AWS service integration.)

![Portfolio Report](https://github.com/masabai/aws_eventbridge_tickers_service/raw/main/screenshots/portfolio_report.png)


### Shutdown
A second EventBridge rule stops the instance to minimize compute costs.


## EventBridge Schedule

![EventBridge Schedule](https://github.com/masabai/aws_eventbridge_tickers_service/raw/main/screenshots/event_bridge_schedule.png)

---

## Technical Solutions

**Linux Automation**  
Configured systemd to ensure scripts execute immediately at boot.

**Secure Permissions**  
Configured IAM roles to allow AWS services to communicate securely.

---

