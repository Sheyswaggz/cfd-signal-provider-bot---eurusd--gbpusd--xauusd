# CFD Signal Provider Bot

A production-grade trading signal bot that monitors and generates trading signals for CFD pairs: EURUSD, GBPUSD, and XAUUSD. The bot implements a disciplined 1:5 risk-reward ratio strategy with comprehensive logging and monitoring capabilities.

## Overview

This automated trading signal provider analyzes real-time market data to identify high-probability trading opportunities across major forex pairs and gold. The system is containerized for consistent deployment across environments and includes robust error handling, health monitoring, and observability features.

### Key Features

- **Real-time Market Data Integration**: Connects to reliable market data providers for live price feeds
- **Multi-Asset Support**: Monitors EURUSD, GBPUSD, and XAUUSD CFD pairs
- **Risk Management**: Enforces 1:5 risk-reward ratio on all signals
- **Production-Ready**: Containerized with Docker, health checks, and structured logging
- **Development Tooling**: Pre-configured linting, formatting, and type checking
- **Hot-Reload Development**: Docker Compose setup for rapid iteration

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.11** or higher
- **Docker 20.10+**
- **docker-compose 2.0+**
- **Git** for version control

## Quick Start

### 1. Clone the Repository