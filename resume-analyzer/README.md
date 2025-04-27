# Resume Analyzer

## Overview
The Resume Analyzer is a web application designed to help users analyze their resumes and receive recommendations for improvement. The application utilizes various technologies and libraries to provide a seamless user experience.

## Features
- User registration and profile management
- Resume upload and analysis
- Recommendations for skills and courses based on resume content
- Admin dashboard for managing user data and viewing analytics
- Integration with YouTube for video recommendations on resume writing and interview preparation

## Project Structure
```
resume-analyzer
├── src
│   ├── controllers          # Contains the logic for handling user and admin actions
│   ├── models               # Defines the data structures and database interactions
│   ├── views                # Manages the presentation layer of the application
│   ├── services             # Contains business logic and external service interactions
│   ├── utils                # Utility functions used throughout the application
│   ├── config               # Configuration settings for the application
│   └── app.py               # Entry point of the application
├── static                   # Contains static files like logos and images
├── tests                    # Unit tests for the application
├── requirements.txt         # Lists the dependencies required for the project
└── README.md                # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd resume-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/app.py
```
Visit `http://localhost:8501` in your web browser to access the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.