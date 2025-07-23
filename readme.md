# CMS PyTest Automation Suite

> End-to-end Selenium test automation for the CMS web application, fully migrated to **pytest** with a clean page-object model, reusable fixtures, test categorisation (markers) and one-command execution.

## 1. Project Overview

| Layer | Purpose |
|-------|---------|
| `app/pages/*` | **Page Object** classes that wrap every screen or reusable UI fragment. |
| `app/cms_actions.py` | High-level workflows (e.g. `perform_login`) that stitch page objects together. |
| `tests/` | All pytest suites, grouped by intent (`smoke/`, `login/`, `functional/`). |
| `tests/conftest.py` | Session & function-scoped fixtures (Chrome-driver, authenticated driver, config). |
| `pytest.ini` | Global pytest settings + marker registration. |
| `Makefile` | Convenience shortcuts (`make test`, `make smoke`, `make html-report` …). |
| `.venv/` | Local Python virtual environment (not committed). |
| `downloads/` / `screenshots/` | Runtime artefacts created by the tests. |

## 2. Test Cases Covered

| Suite | File | What it validates |
|-------|------|-------------------|
| **Smoke** | `tests/smoke/test_smoke_suite.py` | -  Site is up  -  Can log in  -  Dashboard loads |
| **Login** | `tests/login/test_login_suite.py` | -  Successful login  -  UI elements on login page  -  Multiple invalid-credential scenarios (parametrised) |
| **Dashboard** | `tests/functional/test_dashboard.py` | -  Dashboard header present  -  Core navigation elements visible |
| **Content Template** | `tests/functional/test_content_template.py` | -  Open "Content Templates" modal  -  Create template (registrant, filing type, style template) |
| **Section Creation** | `tests/functional/test_create_section.py` | -  Navigate to template page  -  Open first document  -  Create new section, positive workflow |
| **Batch Download** | `tests/functional/test_batch_download.py` | -  Select all docs  -  Trigger 4 download flavours  -  Verify at least one file lands in `downloads/` |

All tests use **implicit scrolling + explicit waits** to reduce flakiness and are tagged with markers (`smoke`, `login`, `functional`, `content_template`, `section`, `download`, `dashboard`, `slow`) so they can be orchestrated granularly.

## 3. Prerequisites

* Python 3.9 – 3.12  
* Google Chrome / Chromium  
* ChromeDriver (auto-installed via `webdriver‐manager`)  
* Git, make (optional but recommended)

## 4. Setup (from a blank machine)

```bash
# 1) Clone & enter the repo
git clone  cms_pytest
cd cms_pytest

# 2) Create isolated environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install all Python deps
pip install -r requirements.txt

# 4) One-off project folders
make setup          # creates downloads/ and screenshots/
```

### 4.1 Environment variables

The tests default to the public staging instance but can be pointed elsewhere:

```bash
export CMS_URL="http://:9000/login"
export CMS_USERNAME="admin@qualityedgar.com"
export CMS_PASSWORD="yourPassword"
```

You can also create a `.env` file (supported by `python-dotenv`).

## 5. Running the Tests

### 5.1 Quick commands (via Makefile)

```bash
make test            # all  ❯ 16 tests
make smoke           # just the 3 smoke tests
make login           # login suite
make functional      # dashboard + template + section + download
make html-report     # pytest-html single-file report
make parallel        # run everything on 4 CPU cores (needs pytest-xdist)
make clean           # wipe __pycache__, reports, screenshots
```

### 5.2 Raw pytest examples

```bash
pytest                       # run from project root; picks up pytest.ini
pytest -m smoke              # any marker expression
pytest tests/login/          # directory
pytest tests/...::test_name  # single test
pytest -n 8                  # parallel on 8 processes
pytest --maxfail=1 -q        # stop after first failure
```

## 6. Reports

| Format | How to generate | Output |
|--------|-----------------|--------|
| **HTML (built-in)** | `make html-report` | `report.html` |
| **JUnit XML** | `pytest --junitxml=report.xml` | CI/CD consumption |
| **Allure** | `pytest --alluredir=reports/allure && allure serve reports/allure` | Interactive dashboard |

## 7. Project Structure

```
cms_pytest/
├── app/
│   ├── __init__.py
│   ├── cms_actions.py              # High-level workflows
│   └── pages/
│       ├── __init__.py
│       ├── login_page.py           # Login page interactions
│       ├── dashboard_page.py       # Dashboard validation
│       ├── content_template_page.py # Content template creation
│       ├── create_section.py       # Section creation workflow
│       └── documents_page.py       # Batch download functionality
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures and configuration
│   ├── smoke/
│   │   ├── __init__.py
│   │   └── test_smoke_suite.py     # Quick validation tests
│   ├── login/
│   │   ├── __init__.py
│   │   └── test_login_suite.py     # Login functionality tests
│   └── functional/
│       ├── __init__.py
│       ├── test_dashboard.py       # Dashboard tests
│       ├── test_content_template.py # Template creation tests
│       ├── test_create_section.py  # Section creation tests
│       └── test_batch_download.py  # Download functionality tests
├── pytest.ini                     # Pytest configuration
├── requirements.txt                # Python dependencies
├── Makefile                        # Build and test commands
└── README.md                       # This file
```

## 8. Page Objects Overview

### 8.1 LoginPage (`app/pages/login_page.py`)
- Handles user authentication
- Validates login success/failure
- Returns DashboardPage object on successful login

### 8.2 DashboardPage (`app/pages/dashboard_page.py`)  
- Validates dashboard loading
- Checks for core navigation elements
- Provides `is_loaded()` method for verification

### 8.3 ContentTemplate (`app/pages/content_template_page.py`)
- Opens content template creation modal
- Handles dropdown selections (Registrant, Filing Type, Style Template)
- Submits template creation form

### 8.4 CreateSectionPage (`app/pages/create_section.py`)
- Navigates to content template page
- Opens first document for editing
- Creates new sections with specified names

### 8.5 DocumentsPage (`app/pages/documents_page.py`)
- Manages batch download workflow
- Selects all documents
- Handles multiple download formats (PDF, HTML, etc.)

## 9. Troubleshooting Checklist

1. **Markers unknown?**  
   Run pytest from the project root so `pytest.ini` is discovered.

2. **Chrome version mismatch?**  
   Delete `~/.wdm` and re-run; `webdriver-manager` will fetch the correct driver.

3. **Downloads not detected?**  
   - Ensure `downloads/` is writable.  
   - Check Chrome's "Ask where to save each file" is disabled.

4. **CI headless mode** (if needed):  
   Add `chrome_options.add_argument("--headless=new")` in `tests/conftest.py`.

5. **Timeout exceptions?**
   - Check if UI elements have changed
   - Verify network connectivity
   - Increase wait times in page objects if needed

6. **Import errors?**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

## 10. Development Guidelines

### 10.1 Adding New Tests
1. Create test files following the pattern `test_*.py`
2. Use appropriate markers (`@pytest.mark.smoke`, `@pytest.mark.functional`, etc.)
3. Follow the existing page object pattern
4. Add proper error handling and screenshots on failure

### 10.2 Page Object Best Practices
- Use explicit waits instead of sleep()
- Implement scrolling before clicking elements
- Add proper exception handling
- Use meaningful locator strategies (prefer ID > CSS > XPath)

### 10.3 Test Organization
- **Smoke tests**: Quick validation, should complete in under 2 minutes
- **Functional tests**: Full feature testing, can take longer
- **Login tests**: Authentication and authorization scenarios

## 11. Configuration Options

### 11.1 Environment Variables
```bash
CMS_URL                 # Target application URL
CMS_USERNAME           # Login username
CMS_PASSWORD           # Login password
```

### 11.2 Pytest Markers
- `smoke`: Quick validation tests
- `login`: Authentication tests  
- `functional`: Full feature tests
- `content_template`: Template creation tests
- `section`: Section management tests
- `download`: File download tests
- `dashboard`: Dashboard functionality tests
- `slow`: Long-running tests

## 12. Continuous Integration

### 12.1 CI/CD Integration
```bash
# Example CI script
source .venv/bin/activate
pytest --junitxml=results.xml --html=report.html
```

### 12.2 Parallel Execution
```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto          # Use all available CPU cores
pytest -n 4             # Use 4 processes
```

## 13. Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow existing code patterns and conventions
4. Add tests for new functionality
5. Ensure all tests pass: `make test`
6. Submit a pull request

### 13.1 Code Standards
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and methods
- Keep functions focused and single-purpose

## 14. License

This repository is distributed under the **MIT License**—see `LICENSE` for details.

## 15. Support

For issues and questions:
1. Check the troubleshooting section above
2. Review existing test patterns for guidance
3. Create detailed bug reports with screenshots and logs
4. Include steps to reproduce any issues

Happy testing! 🚀

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/94dfbfec-6c20-4fa0-ac3e-9effdfee72bd/test_create_section.py
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/ee8a88e0-b586-4ae2-801f-53cec97a286d/test_login.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/d6692257-5ba5-4cd3-ad46-2be2b8523329/run_all_tests.py
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/cfb017ce-6f83-4cc2-931c-effe80e5c557/test_content_template.py
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/3a81abc6-ca74-4254-b5db-da002738a361/test_batch_download.py
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/ebfd9ffd-38d7-4f70-9702-82854bdcecf6/test_dashboard.py
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/66bfd483-ac83-46fb-a131-53593ad16c0e/cms_actions.py
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/9c8d7aa0-2e8f-49d1-8d34-dfeee715942a/create_section.py
[9] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/1e64b7ea-1272-4fa0-9530-e5333f2f3a61/content_template_page.py
[10] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/efc24d91-8e67-46b7-9e00-e50f915808d9/documents_page.py
[11] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/8e8f646e-40b4-4e57-be59-2deb6c7a9e88/login_page.py
[12] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82855156/282f6423-961c-41a5-ac7d-82010df08e6c/dashboard_page.py