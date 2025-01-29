# Customer Care Chatbot

A sophisticated chatbot powered by DistilBERT for intelligent customer service automation at UpToSkills. This project was developed during my internship at UpToSkills, where I worked on implementing an AI-powered solution to enhance customer support efficiency. Built with Python, Flask, Node.js, and modern NLP technologies to provide accurate, context-aware responses to user queries.

## 🎯 Project Background

This chatbot was developed as part of an internship project at UpToSkills, with the goal of streamlining customer support operations. The project demonstrates the practical application of natural language processing in a real-world business context, utilizing DistilBERT's capabilities to understand and respond to customer inquiries effectively.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![Node](https://img.shields.io/badge/node-v18+-green.svg)

## 🚀 Features

- **Natural Language Processing**: Leverages DistilBERT for advanced query understanding
- **Multi-Backend Architecture**: Combines Python and Node.js for optimal performance
- **Real-time Response**: Instant message processing and response generation
- **Customizable Responses**: Easy-to-modify response database
- **Web Interface**: Clean, responsive chat interface
- **Scalable Design**: Built to handle multiple concurrent users

## Project Structure

```
project-root/
│
├── python-backend/
│   ├── chatbot_api.py            # Flask API for handling requests
│   ├── database.json             # Intents and responses database
│   ├── customer_care_bert_model/ # Directory for the trained BERT model
│   ├── customer_care_bert_tokenizer/ # Directory for the tokenizer
│            
├── node-backend/
│   ├── server.js                  # Node.js server
│   └── package.json               # Node.js dependencies and scripts
│
├── frontend/
│   ├── index.html                 # HTML file for the frontend
│   ├── styles.css                 # CSS file for styling
│   └── script.js                  # JavaScript for handling user input and displaying responses
│
├── run.py                         # Start file for the application
├── requirements.txt               # List of Python dependencies
```

## ⚙️ Installation

### Create a Virtual Environment

To get started, you'll need to create a virtual environment for the Python backend:

```bash
python -m venv venv
```

Activate the virtual environment:

* On macOS/Linux:
```bash
source venv/bin/activate
```

* On Windows:
```bash
venv\Scripts\activate
```

### Install Required Python Packages

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### Set Up Node.js Backend

Navigate to the Node.js backend directory:

```bash
cd chatbot-backend
```

Install the required Node.js packages:

```bash
npm install
```

### Model Setup

Ensure you have the DistilBERT model and tokenizer available in the `customer_care_bert_model/` and `customer_care_bert_tokenizer/` directories, respectively. If they are not available, refer to the model download steps, or reach out to the project administrator for access.

## 🚀 Running the Project

### Start Python Backend

To run the project, execute the following command in the root directory:

```bash
python run.py
```

### Start Node.js Server

In the `node-backend` directory, run the following command to start the Node.js server:

```bash
node server.js
```

**Important**: Ensure both the Flask API and the Node.js server are running before accessing the frontend.


## 🔍 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Verify Git LFS files are downloaded
   - Check Python environment activation
   - Ensure sufficient RAM is available

2. **Connection Issues**
   - Confirm both servers are running
   - Check port availability
   - Verify network settings

3. **Performance Issues**
   - Monitor system resources
   - Check log files
   - Verify model configuration

### Cloning with Git LFS

If you encounter issues with model files:

```bash
# Install Git LFS
git lfs install

# Clone repository
git clone https://github.com/frenziedD3X/Bert-Customer-care-Chatbot-.git

# Pull LFS files
git lfs pull
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Coding Standards

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write clear commit messages
- Include tests for new features

## 📈 Performance Tips

- Use production servers (Gunicorn/PM2)
- Enable response caching
- Implement rate limiting
- Monitor memory usage

## 📚 Documentation

Access additional documentation:
- Model training details
- API documentation
- Deployment guides
- Configuration options

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- UpToSkills team for the internship opportunity and project guidance
- HuggingFace team for DistilBERT
- Project contributors
- Mentors and supervisors at UpToSkills

## 📱 Support

For support:
- Open an issue on GitHub
- Check documentation
- Contact project maintainers

Need help? Feel free to reach out to the maintenance team or open an issue on GitHub.