# Better Undetected Chromedriver

This project is a Python-based web automation tool that uses Selenium WebDriver with undetected_chromedriver to automate browser tasks. It also includes features for managing proxies and profiles data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account (for Google Drive interactions)

### Installing

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file. You will need to include:

- `WORKDIR`: The working directory for the project.
- `CAPSOLVER_TOKEN`: Your Capsolver token. URL: https://www.capsolver.com/
- `GCP_SERVICE_ACCOUNT_FILE_PATH`: The path to your Google Cloud Platform service account file. URL: https://cloud.google.com/iam/docs/keys-create-delete
- `GCP_SERVICE_SUBJECT`: The subject for your Google Cloud Platform service. It is the email address associated with the service account. You can find this on the service account details page in the "IAM & Admin" > "Service Accounts" section. It will look something like my-service-account@my-project.iam.gserviceaccount.com.
- `GCP_DEFAULT_FOLDER`: The default folder ID on Google Drive where files will be uploaded and downloaded.

## Usage

The main class in this project is `UndetectedDriver` in `main.py`. This class sets up a Selenium WebDriver with undetected_chromedriver, and includes options for using proxies and a CAPTCHA solver.

Here is a basic example of how to use it:

```python
from main import UndetectedDriver

driver = UndetectedDriver(proxy="http://username:password@proxyhost:proxyport")
driver.get_driver().get("https://www.example.com")
```

## Acknowledgments

- Thanks to the creators of undetected_chromedriver for their great work on making Selenium WebDriver undetectable.
- Thanks to the creators of the Capsolver extension for making CAPTCHA solving easier.