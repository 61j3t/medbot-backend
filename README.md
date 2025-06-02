# Drug Interaction Classification API

A FastAPI-based service that provides drug classification and drug interaction information using machine learning and natural language processing powered by Groq's LLaMA models.

## Features

- **Drug Classification**: Classify drugs into their therapeutic categories
- **Drug Interaction Detection**: Find and analyze interactions between two drugs
- **Enhanced Explanations**: AI-powered detailed explanations of drug interactions
- **RESTful API**: Easy-to-use endpoints with JSON responses
- **Comprehensive Drug Database**: Contains over 800 drug names and classifications

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Groq API**: LLaMA 3.3 70B model for natural language processing
- **Pydantic**: Data validation and settings management
- **Python 3.7+**: Core programming language

## Prerequisites

- Python 3.7 or higher
- Groq API key (sign up at [Groq Console](https://console.groq.com/))

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd extraction-ml
   ```
2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn pydantic groq
   ```
4. **Set up your Groq API key**

   - Replace the API key in `drug_classifier.py` with your own Groq API key
   - Look for the line: `client = Groq(api_key="your-api-key-here")`
5. **Ensure data file is present**

   - Make sure `data_partitioned.json` is in the root directory
   - This file contains the drug interaction database

## Usage

### Starting the Server

```bash
uvicorn drug_classifier:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:

- **Interactive API docs**: `http://localhost:8000/docs`
- **Alternative docs**: `http://localhost:8000/redoc`

## API Endpoints

### 1. Drug Classification

**Endpoint**: `POST /classify`

**Description**: Classify a drug into its therapeutic category.

**Request Body**:

```json
{
  "drug_name": "aspirin"
}
```

**Response**:

```json
{
  "drug_name": "aspirin",
  "classification": "NSAIDs"
}
```

### 2. Drug Interaction Check

**Endpoint**: `POST /interaction`

**Description**: Check for interactions between two drugs and get detailed explanations.

**Request Body**:

```json
{
  "drug1": "warfarin",
  "drug2": "aspirin"
}
```

**Response**:

```json
{
  "drug1": {
    "name": "warfarin",
    "classification": "Coumarins"
  },
  "drug2": {
    "name": "aspirin",
    "classification": "NSAIDs"
  },
  "interaction": {
    "title": "Warfarin + Aspirin",
    "content": "Original interaction data...",
    "page": 123,
    "enhanced_explanation": "AI-enhanced explanation of the interaction..."
  }
}
```

## Example Usage with cURL

### Classify a drug:

```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"drug_name": "metformin"}'
```

### Check drug interaction:

```bash
curl -X POST "http://localhost:8000/interaction" \
     -H "Content-Type: application/json" \
     -d '{"drug1": "warfarin", "drug2": "aspirin"}'
```

## Example Usage with Python

```python
import requests

# Drug classification
response = requests.post(
    "http://localhost:8000/classify",
    json={"drug_name": "lisinopril"}
)
print(response.json())

# Drug interaction
response = requests.post(
    "http://localhost:8000/interaction",
    json={"drug1": "metformin", "drug2": "insulin"}
)
print(response.json())
```

## Supported Drug Categories

The system supports classification for over 800 drugs across various therapeutic categories including:

- ACE inhibitors
- Antibiotics (Penicillins, Cephalosporins, Quinolones, etc.)
- Antidepressants (SSRIs, SNRIs, etc.)
- Antidiabetics
- Anticoagulants
- NSAIDs
- Beta blockers
- Statins
- And many more...

## Data Sources

The drug interaction data is stored in `data_partitioned.json` and contains:

- Drug interaction pairs
- Detailed interaction descriptions
- Clinical significance information
- Reference page numbers

## Development

### Project Structure

```
extraction-ml/
├── drug_classifier.py      # Main FastAPI application
├── data_partitioned.json   # Drug interaction database
├── main.ipynb             # Data processing notebook
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Adding New Drugs

To add new drugs to the classification system:

1. Add the drug name to the `drug_list` in `drug_classifier.py`
2. Ensure proper categorization by the LLM model
3. Test the classification endpoint

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: LLM API failures or processing errors

## Limitations

- Requires active internet connection for Groq API calls
- LLM responses may vary slightly between requests
- Drug interaction database is limited to included entries
- API key usage limits apply based on Groq subscription

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions or issues:

- Check the API documentation at `/docs`
- Review the error messages in API responses
- Ensure your Groq API key is valid and has sufficient credits

## Disclaimer

This tool is for informational purposes only and should not be used as a substitute for professional medical advice. Always consult healthcare professionals for drug interaction concerns.
