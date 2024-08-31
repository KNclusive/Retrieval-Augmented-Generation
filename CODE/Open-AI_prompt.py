from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini-2024-07-18",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a Farmer Bot, a specialist in crop management and farming. Your primary function is to provide accurate information on farming, including crops, soil management, pest control, weather effects, and farming equipment. You also assist with creating and managing to-do lists for farming tasks.\n\nFor farming-related queries:\n- Provide detailed, conversational responses.\n- Do not include a `todo_list` field in your response.\n\nFor to-do list queries:\n- Include a `todo_list` field in your response with `todo_chat_title` and `todo_task_list`.\n- Each task in `todo_task_list` must have: `task_title`, `task_description`, `due_date`, `completed`, `task_order`, and `intent`.\n- Respond in a natural, conversational manner.\n- Classify the intent as follows:\n  - `Create` for starting a new to-do list\n  - `Add` for adding a task to an existing list\n  - `Update` for updating a task on an existing list\n  - `No action` if not related to to-do lists\n\nFor non-farming and non-to-do list queries:\n- Politely state that you can only assist with farming-related topics.\n\nExamples:\n1. Query: \"Hello how are you?\"\n   Response: Greet the user in a farmer-like style.\n2. Query: \"How can I estimate potato yield?\"\n   Response: Provide detailed farming advice without including a `todo_list` field.\n3. Query: \"Can you help me create a to-do list for gardening?\"\n   Response: Include a `todo_list` with a title and tasks, setting the intent as `Create`.\n4. Query: \"I need to add a watering task to my to-do list.\"\n   Response: Update the `todo_list` with the new task, setting the intent as `Add`.\n\nAlways strive for accuracy in your responses and correct intent classifications. Maintain a helpful and knowledgeable demeanor while staying within your role as a farming specialist."
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "json_schema",
    "json_schema": {
      "name": "main_schema",
      "strict": true,
      "schema": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
          "response",
          "todo_list"
        ],
        "properties": {
          "response": {
            "type": "string",
            "description": "The LLM's conversational response to the user's query, formatted as a normal conversation."
          },
          "todo_list": {
            "type": "object",
            "required": [
              "todo_chat_title",
              "todo_task_list"
            ],
            "properties": {
              "todo_chat_title": {
                "type": "string",
                "description": "The title of the to-do chat or project."
              },
              "todo_task_list": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "task_title",
                    "task_description",
                    "due_date",
                    "completed",
                    "task_order",
                    "intent"
                  ],
                  "properties": {
                    "task_title": {
                      "type": "string",
                      "description": "The title or name of the task."
                    },
                    "task_description": {
                      "type": "string",
                      "description": "A detailed description of the task."
                    },
                    "due_date": {
                      "type": "string",
                      "description": "The due date of the task in ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)."
                    },
                    "completed": {
                      "type": "boolean",
                      "description": "Indicates whether the task has been completed."
                    },
                    "task_order": {
                      "type": "integer",
                      "description": "The order of the task in the list."
                    },
                    "intent": {
                      "type": "string",
                      "enum": [
                        "Create",
                        "Add",
                        "Read",
                        "Delete",
                        "No action"
                      ],
                      "description": "The intent related to the task action."
                    }
                  },
                  "additionalProperties": false
                },
                "description": "A list of tasks associated with the to-do list."
              }
            },
            "additionalProperties": false
          }
        },
        "additionalProperties": false
      }
    }
  }
)