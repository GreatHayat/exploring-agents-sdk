# AI Agents Repository

This repository provides implementations of AI agents utilizing the OpenAI Agents SDK. The agents included are:

- **Basic Agent**: A foundational agent demonstrating the core functionalities of the OpenAI Agents SDK.
- **Weather Agent**: An agent that fetches current weather information using the OpenWeatherMap API.
- **Appointment Agent**: An agent that interacts with Google Calendar API to search for and create events.

## Prerequisites

Before running the agents, ensure you have the following:

- **Python 3.10+**: The codebase is compatible with Python version 3.10 and above.
- **OpenAI Agents SDK**: A lightweight framework for building agentic AI applications.
- **API Keys**:
  - **OpenAI API Key**: Required for utilizing the OpenAI Agents SDK.
  - **OpenWeatherMap API Key**: Needed for the Weather Agent to fetch weather data.
  - **Google Calendar API Credentials**: Necessary for the Appointment Agent to access and manage calendar events.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/ai-agents-repo.git
   cd ai-agents-repo
   ```


2. **Set Up a Virtual Environment** (Optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```


3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


## Configuration

1. **OpenAI API Key**:

   Set the `OPENAI_API_KEY` environment variable:

   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   ```


   Replace `'your_openai_api_key'` with your actual OpenAI API key.

2. **OpenWeatherMap API Key**:

   Set the `OPEN_WEATHER_API_KEY` environment variable:

   ```bash
   export OPEN_WEATHER_API_KEY='your_openweather_api_key'
   ```


   Replace `'your_openweather_api_key'` with your actual OpenWeatherMap API key.

3. **Google Calendar API Credentials**:

   Download your `credentials.json` from the Google Cloud Console and place it in the root directory of the project. Ensure the Google Calendar API is enabled for your project.

## Usage

### Basic Agent

To run the Basic Agent:


```bash
python basic_agent.py
```


This agent serves as a template to understand the integration of the OpenAI Agents SDK.

### Weather Agent

To run the Weather Agent:


```bash
python weather_agent.py
```


This agent fetches current weather data for a specified location using the OpenWeatherMap API. Ensure the `OPEN_WEATHER_API_KEY` is set as an environment variable.

### Appointment Agent

To run the Appointment Agent:


```bash
python appointment_agent.py
```


This agent interacts with the Google Calendar API to search for and create events. Ensure that your `credentials.json` is correctly configured and placed in the root directory.

## API References

- **OpenAI Agents SDK**: [Documentation](https://platform.openai.com/docs/guides/agents-sdk)
- **OpenWeatherMap API**: [Documentation](https://openweathermap.org/api)
- **Google Calendar API**: [Documentation](https://developers.google.com/calendar)
---

For any issues or contributions, please feel free to submit a pull request or open an issue in this repository. 
