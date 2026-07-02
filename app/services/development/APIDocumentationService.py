class APIDocumentationService:
    def get_api_doc_prompt(self, framework: str) -> str:
        prompt = f"""
You are a senior technical writer responsible for creating clear, accurate, and developer-friendly API documentation.

Generate comprehensive API documentation for a {framework} application.

The documentation should include the following sections:

- API Overview
- Endpoint URL
- HTTP Method
- Purpose of the Endpoint
- Request Headers
- Path Parameters
- Query Parameters
- Request Body
- Response Body
- HTTP Status Codes
- Error Responses
- Authentication Requirements
- Example Request
- Example Response
- Notes and Best Practices

Ensure the documentation is well-structured, concise, and follows industry-standard REST API documentation practices.

The API implementation details will be provided in the next user message.
"""
        return prompt