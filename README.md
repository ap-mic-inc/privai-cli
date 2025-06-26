# privai-cli

CLI tool for interacting with the PrivAI API.

## Installation

```bash
poetry install
```

## Configuration

Before using the CLI, you need to configure the API URL and your bearer token:

```bash
privai-cli config set --api-url <your-api-url> --token <your-bearer-token>
```

## Usage

### Models

*   `privai-cli models list`: Get a list of available models.

### Filesets

*   `privai-cli filesets list`: List filesets.
*   `privai-cli filesets create --file-ids <file-id-1> --metadata '{"key": "value"}'`: Create a new fileset.
*   `privai-cli filesets get <fileset-id>`: Get a specific fileset by its ID.
*   `privai-cli filesets update <fileset-id> --file-ids <file-id-1> --metadata '{"key": "value"}'`: Update a fileset's metadata or file list.
*   `privai-cli filesets delete <fileset-id>`: Delete a fileset by its ID.
*   `privai-cli filesets commit <fileset-id> --embedding-model <model-name>`: Commit a fileset to start the embedding process.
*   `privai-cli filesets duplicate <fileset-id>`: Create a duplicate of a fileset.

### Files

*   `privai-cli files list`: List files with filtering and pagination.
*   `privai-cli files upload <path-to-your-file> --purpose <purpose> --extra-metadata '{"key": "value"}'`: Upload a file.
*   `privai-cli files get <file-id>`: Get a specific file's metadata by its ID.
*   `privai-cli files delete <file-id>`: Delete a file by its ID.
*   `privai-cli files content <file-id> --file-type <type>`: Download the content of a specific file.

### Chat

*   `privai-cli chat completions --model <model> --messages '[{"role": "user", "content": "Hello"}]' [--prompt-id <prompt-id>] [--fileset-id <fileset-id>] [--temperature 0.7]`: Create a chat completion.

### Prompt

*   `privai-cli prompt create <value> [--metadata '{"key": "value"}']`: Create a new prompt.
*   `privai-cli prompt list`: List all prompts.
*   `privai-cli prompt get <prompt-id>`: Get a specific prompt by its ID.
*   `privai-cli prompt delete <prompt-id>`: Delete a prompt by its ID.
*   `privai-cli prompt optimize-auto <prompt-id> [--model <model-name>]`: Automatically optimize a prompt.
*   `privai-cli prompt optimize-instruct <prompt-id> --current-issue <issue> --desired-behavior <behavior>`: Optimize a prompt based on instructions.

### QA

*   `privai-cli qa generate --fileset-id <fileset-id> [--model-name <model>] [--extract-model-name <model>] [--temperature 0.7] [--target-amount 10]`: Generate QA pairs from a fileset.

### LangServe

*   `privai-cli langserve input-schema`: Get the input schema for the runnable.
*   `privai-cli langserve output-schema`: Get the output schema for the runnable.
*   `privai-cli langserve config-schema`: Get the config schema for the runnable.
*   `privai-cli langserve invoke '<input-json>' [--config-hash <hash>] [--config '<config-json>'] [--kwargs '<kwargs-json>']`: Invoke the runnable with a single request.
*   `privai-cli langserve stream '<input-json>' [--config-hash <hash>] [--config '<config-json>'] [--kwargs '<kwargs-json>']`: Stream the runnable execution results.