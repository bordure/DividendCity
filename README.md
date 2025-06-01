<p align="center">
  <img src="staticfiles/logo-removebg.png" alt="DividendCity Logo" width="200"/>
</p>

<h1 align="center">DividendCity</h1>

<p align="center">
  <em>Track your dividend income from the Warsaw Stock Exchange (GPW)</em>
</p>

<p align="center">
  <a href="https://github.com/yourusername/dividendcity/releases/tag/v0.1">
    <img src="https://img.shields.io/badge/version-0.1-blue.svg" alt="Version">
  </a>
  <a href="https://github.com/SURFLOU/DividendCity/actions/workflows/fly-deploy.yml">
    <img src="https://github.com/SURFLOU/DividendCity/actions/workflows/fly-deploy.yml/badge.svg" alt="Tests">
  </a>
</p>

---

## 📈 Overview

**DividendCity** is a Django-based web application that helps investors monitor their dividend income from companies listed on the Warsaw Stock Exchange (GPW). The app calculates how much you've earned from dividends and notifies you when companies are scheduled to pay out.

Whether you're a seasoned investor or just starting to build your dividend portfolio, DividendCity provides a clean, simple, and automated way to stay on top of your passive income.

---

## 🚀 Features

- 📊 **Track Dividend Income**: Monitor earnings from all companies in your portfolio.
- 🧾 **Historical View**: See how much you've earned over time.
- 🌐 **Live Web App**: Deployed and accessible at [https://dividendcity.fly.dev](https://dividendcity.fly.dev)
- 🤖 **CI/CD with GitHub Actions**: Fully automated testing and deployment pipeline.

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Django Templates + Bootstrap 
- **Database**: PostgreSQL 
- **CI/CD**: GitHub Actions for testing and deployment
- **Hosting**: [Fly.io](https://fly.io)

---

## 🧪 CI/CD with GitHub Actions

This project uses GitHub Actions to automate:

- Running Django tests
- Automatic deployment to Fly.io on push to `main`

You’ll find the GitHub Actions workflows in `.github/workflows/`.


