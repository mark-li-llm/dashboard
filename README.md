# Wildlife Health Watch Dashboard

A Streamlit dashboard for visualizing wildlife health surveillance data from Kenya's Wildlife Health Watch program.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Features

- **Interactive Map**: Geographic distribution of wildlife health events across Kenya
- **Key Metrics**: Total cases, active alerts, critical cases, animals affected
- **Time Series Analysis**: Weekly case trends and severity patterns
- **Species Analysis**: Distribution of cases by wildlife species
- **Syndrome Distribution**: Breakdown of syndromic categories
- **Filtering**: Filter by date range, region, species, severity, and status

## Project Structure

```
dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/
│   └── generate_data.py     # Synthetic data generator
└── README.md
```

## Data

This demo uses synthetic data representing wildlife health surveillance records including:
- 8 monitoring regions across Kenya
- 10 wildlife species
- 8 syndromic categories
- Severity levels: Low, Moderate, High, Critical

---

*Smithsonian Global Health Program | Kenya Wildlife Service*
