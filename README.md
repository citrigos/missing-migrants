# Visualizing Deaths of Migrants at Borders

🌍 **[View Live Application](https://missing-migrants.streamlit.app/)**

## About

This project documents and honors the lives lost during migration worldwide. Beginning as a group project at the University of Helsinki in 2022 between [Citlali Trigos-Raczkowski](https://www.linkedin.com/in/citlali-trigos-raczkowski/) and [Sebastian Rodriguez-Beltran](https://www.linkedin.com/in/sebastian-rodriguez-beltran-1e/?originalSubdomain=fi), it has evolved into an interactive data visualization that brings awareness to the scale and ongoing nature of this humanitarian crisis.

The project relies on data from the [Missing Migrants Project](https://missingmigrants.iom.int/), a comprehensive database tracking migrant deaths and disappearances worldwide since 2014. The dataset currently spans through 2026 and includes over 21,000 documented incidents across the globe. Each point represents one or more individuals who died while migrating, with available details about location, cause of death, time period, and circumstances.

The interactive visualization allows you to explore how these tragedies vary by geographic region, migration route, cause of death, and time period. These figures represent minimum estimates; many deaths go unreported or undocumented. Behind each data point is a person with a story, a family grieving their loss, and a community forever changed.

## Technology Stack

This application is built and deployed using [Streamlit](https://streamlit.io/). The project is written in Python, with exploratory data analysis documented in Jupyter notebooks (available in the [exploration](./exploration/) folder).

### Key Libraries

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[Plotly](https://plotly.com/)** - Interactive visualizations and maps
- **[Altair](https://altair-viz.github.io/)** - Declarative statistical visualization
- **[millify](https://pypi.org/project/millify/)** - Number formatting (`1220098` → `1,220,098`)

### Data Sources

- CSV data from the [Missing Migrants Project](https://missingmigrants.iom.int/)
- Additional recent data gathered via the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) (accessible through the Twitter page of the application)

## Running Locally

### Prerequisites

- Python 3.10 or higher
- pip or conda for package management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/citrigos/missing-migrants.git
cd missing-migrants
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using conda:
```bash
conda create -n migrant-viz python=3.10
conda activate migrant-viz
pip install -r requirements.txt
```

### Running the Application

From the project root directory, run:

```bash
streamlit run src/Home.py
```

The application will start and you'll see output similar to:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.101.106:8501
```

Open the Local URL in your browser to view the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project uses data from the [Missing Migrants Project](https://missingmigrants.iom.int/) by the International Organization for Migration (IOM).

## Acknowledgments

- International Organization for Migration's Missing Migrants Project for providing comprehensive data
- University of Helsinki for supporting the initial development of this project
