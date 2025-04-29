# Smart Drawing Reviewer

An intelligent application for reviewing engineering drawings against industry standards (ASME Y14 and AED).

## Features

- PDF drawing upload and analysis
- Rule-based compliance checking
- Support for multiple drawing standards (ASME Y14, AED)
- Detailed compliance reports
- User-friendly web interface

## Project Structure

```
Smart-Drawing-Reviewer/
├── Backend/           # Python backend with rule engines
│   ├── engine/       # Core rule checking engine
│   ├── parser/       # PDF parsing utilities
│   └── reports/      # Report generation
├── Frontend/         # Web interface
└── data/            # Sample drawings and test data
```

## Installation

1. Clone the repository:
```bash
git clone git@github.com:mosesfuego/Smart-Drawing-Reviewer.git
cd Smart-Drawing-Reviewer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r Backend/requirements.txt
```

## Usage

1. Start the application:
```bash
cd Backend
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a PDF drawing and select the appropriate standard for analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Moses Makangila - mosesfuego@gmail.com

Project Link: [https://github.com/mosesfuego/Smart-Drawing-Reviewer](https://github.com/mosesfuego/Smart-Drawing-Reviewer)
