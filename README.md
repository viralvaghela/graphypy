# GraphQL Endpoint Detector

This tool is designed to help bug bounty hunters and penetration testers detect GraphQL endpoints within a specified URL. It goes through multiple steps to ensure the identification of GraphQL endpoints and schema. Below are the steps followed by the tool:

1. Brute force all endpoints to find the GraphQL endpoint.
2. Tries the introspection query to find the schema.
3. If introspection is disabled, it attempts a GET query to find the schema.
4. If the GET query doesn't work, it tries URL Encoding.

![image](https://github.com/viralvaghela/graphypy/assets/34627404/0a81a129-c19c-4f4e-b669-006b0e972ebc)


### ToDo
- [ ] Allows users to check common mutations once a valid GraphQL endpoint is detected. and displays the results of the mutation checks at the end.

## Usage

Make sure you have Python 3.x installed. Use the following command to run the script:

```
pip install requirements.txt
python graphypy.py URL
```
Note: You might need to install the necessary Python packages specified in the requirements file before running the script.

## Bugs
If you find any issues in the tool, Feel free to create an issue [here](https://github.com/viralvaghela/graphypy/issues/new) 

Feel free to contribute and enhance the tool for better functionality and broader use cases.
