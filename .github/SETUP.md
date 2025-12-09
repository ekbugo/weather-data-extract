# GitHub Actions Setup Guide

This repository includes a GitHub Actions workflow that automatically scrapes weather data daily and commits it to the weather-game repository.

## Prerequisites

The workflow requires a Personal Access Token (PAT) to push changes to the weather-game repository.

## Setup Steps

### 1. Create a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or visit: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name like "Weather Scraper Workflow"
4. Select the following scopes:
   - `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't be able to see it again!)

### 2. Add the Token as a Repository Secret

1. Go to your weather-data-extract repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `GH_PAT`
5. Value: Paste the token you copied in step 1
6. Click "Add secret"

### 3. Configure the Schedule (Optional)

The workflow is set to run daily at 2:00 AM UTC. To change this:

1. Edit `.github/workflows/scrape-weather.yml`
2. Modify the cron schedule:
   ```yaml
   schedule:
     - cron: '0 2 * * *'  # minute hour day month weekday
   ```

**Examples:**
- `'0 1 * * *'` - 1:00 AM UTC daily
- `'30 14 * * *'` - 2:30 PM UTC daily
- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * 1'` - Every Monday at midnight UTC

Use [crontab.guru](https://crontab.guru/) to help create cron schedules.

### 4. Test the Workflow

You can manually trigger the workflow without waiting for the schedule:

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. Select "Daily Weather Data Scraper" from the left sidebar
4. Click "Run workflow" → "Run workflow"

## Workflow Details

The workflow:
1. Checks out both the weather-data-extract and weather-game repositories
2. Sets up Python and installs dependencies
3. Runs `python weather_scraper.py`
4. The script automatically commits and pushes results to weather-game repository

## Troubleshooting

If the workflow fails:
- Check that the `GH_PAT` secret is set correctly
- Verify the token has `repo` scope
- Check the Actions logs for detailed error messages
- Ensure the weather-game repository exists and you have access to it
