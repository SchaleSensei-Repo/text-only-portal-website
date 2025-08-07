# 📰 Text-Only Portal Website

![GCP](https://img.shields.io/badge/Google%20Cloud%20Platform-Serverless-blue)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-orange)
![Text-Only](https://img.shields.io/badge/Text--Only-HTML-lightgrey)
![Unlicense](https://img.shields.io/badge/license-Unlicense-brightgreen)
![RSS](https://img.shields.io/badge/News%20Sources-RSS%20Feeds-blueviolet)
![Lynx Compatible](https://img.shields.io/badge/Lynx-Compatible-success)

Welcome to the **Text-Only Portal Website** – a project that explores just how functional and useful a website can be without relying on JavaScript, CSS frameworks, or modern web enhancements. This portal is designed for speed, accessibility, and simplicity, delivering dynamic content in pure HTML, ideal for low-bandwidth users and vintage computers.

## 🌐 Live Demo

Visit the portal:  
**[https://text-only-portal-function-412268762612.asia-southeast2.run.app](https://text-only-portal-function-412268762612.asia-southeast2.run.app)**

## 🎯 Project Purpose

1. **Maximum Functionality, Minimum Enhancement**  
   - The main goal is to build a fully functional website using only server-generated static HTML, with no client-side JavaScript or heavy assets.
   - All dynamic content is generated on the server (Google Cloud Platform), then delivered as static HTML to users.

2. **Showcase Modern CI/CD Automation**  
   - Demonstrates a robust CI/CD pipeline using Jenkins and Google Cloud Functions.
   - Every update, test (not yet implemented), and deployment is automated for reliability and speed.

## 🌟 Features

- **Human-Curated News**: Aggregates headlines from 20+ trusted RSS feeds (CNN, BBC, NYT, TechCrunch, Indonesian & Japanese sources, and more). News selection depends on the sources, not AI.
- **Live Weather**: Displays current weather for Jakarta and Tokyo using wttr.in.
- **Curated Links**: Static sections for news, forums, weather, and search engines.
- **Ultra-Lightweight**: No JavaScript, no images, no CSS frameworks – just pure HTML.
- **Smart Caching**: Google Cloud Storage caches generated pages for fast delivery.
- **Accessible**: Designed for text-only browsers and low-bandwidth environments.

## 🚀 How It Works

- **Server-Side Generation**:  
  Google Cloud Platform (GCP) pulls data from RSS feeds and weather APIs, builds the HTML, and stores it in a cache bucket.
- **Static Delivery**:  
  End-users always receive static HTML, but with fresh, dynamic content.
- **Perfect for Vintage & Minimal Browsers**:  
  The site is readable on any device, including those with only basic text display capabilities.

## 🛠️ CI/CD Pipeline (Jenkins + GCP)

This project uses a modern CI/CD pipeline to automate every step:

1. **Source Control**:  
   - Code is managed in Git and integrated with Jenkins.

2. **Automated Testing**:  
   - Jenkins runs tests (expandable for your needs) on every commit (not yet implemented).

3. **Secure Deployment**:  
   - Jenkins authenticates with GCP using a service account.
   - Deploys the latest code as a Google Cloud Function.
   - Environment variables (like cache bucket name) are managed securely.

4. **Continuous Delivery**:  
   - Every change is automatically built, tested, and deployed.
   - Email notifications keep you updated on build status.

**See `jenkinsfile` for full pipeline details.**

## 🖥️ Text-Only Browsing with Lynx

**Lynx** is a legendary text-based web browser that runs in the terminal (Command Prompt, PowerShell, Bash, etc.).  
- **How Lynx Works**:  
  - Displays web pages as pure text, ignoring images, scripts, and styles.
  - Perfect for vintage computers, accessibility needs, and low-bandwidth connections.
  - Supports navigation via keyboard shortcuts.
- **How to Use Lynx**:  
  - Install Lynx (`sudo apt install lynx` on Linux, or use Windows builds).
  - Run in your shell:  
    ```
    lynx https://text-only-portal-function-412268762612.asia-southeast2.run.app
    ```
  - Browse using arrow keys, Enter, and keyboard commands.

**Why Lynx?**  
This project is built to be fully compatible with Lynx and similar browsers, ensuring everyone can access news and information, regardless of device or connection speed.

## 📦 Setup & Deployment

1. **Clone the repo**  
   `git clone <your-repo-url>`

2. **Install dependencies**  
   `pip install -r requirements.txt`

3. **Configure GCP & Jenkins**  
   - Set up your Google Cloud project and bucket.
   - Adjust environment variables in Jenkins as needed.

4. **Deploy**  
   - Use Jenkins or manually run the deployment commands in the `jenkinsfile`.

## 🤖 AI-Assisted Development

- **main.py** and **jenkinsfile** were generated with the help of AI tools, then customized for deployment and variable management.
- The result: a robust, scalable, and easy-to-maintain portal for text-only news and information.

## 📄 License

This project is released under the [Unlicense](https://unlicense.org/), dedicating the code to the public domain. You are free to use, modify, and distribute it for any purpose, without restriction. See `LICENSE` for full details.
