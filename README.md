# Image Generator

A web UI for generating images using Google's Gemini AI. Upload reference images, tweak parameters, and generate new images with natural language prompts.

## Features

- **Text-to-image generation** with Gemini 3.1 Flash
- **Image-to-image** - upload reference images to guide generation
- **Parameter controls** - aspect ratio, resolution, thinking level, temperature
- **History sidebar** - browse and reuse past generations
- **Lightbox** - view full-size images with "Use as Input" to chain generations
- **Auto WebP compression** - optimizes uploads for the API

## Quick Start

```bash
# Install dependencies
make install

# Set your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env.local

# Run both backend and frontend (opens browser automatically)
make dev
```

Then open http://localhost:5173

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Bun](https://bun.sh/) (JavaScript runtime)
- [Gemini API key](https://aistudio.google.com/apikey)

## Project Structure

```
image-gen/
├── api/                    # FastAPI backend
│   ├── main.py             # App entry, CORS, lifespan
│   ├── database.py         # SQLite setup
│   ├── models.py           # DB models
│   ├── schemas.py          # Pydantic schemas
│   ├── routes/             # API endpoints
│   └── services/           # Business logic
├── web/                    # React frontend
│   └── src/
│       ├── components/     # UI components
│       ├── store/          # Zustand state
│       └── api/            # API client
├── gemini.py               # Gemini API wrapper
├── compression.py          # WebP compression
└── main.py                 # CLI interface
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Start image generation |
| GET | `/api/generations/{id}` | Get generation status/results |
| GET | `/api/history` | List past generations |
| GET | `/api/images/{path}` | Serve stored images |
| DELETE | `/api/generations/{id}` | Delete generation |

## CLI Usage

You can also use the CLI directly:

```bash
uv run python main.py "a sunset over mountains" -o output.webp
uv run python main.py "make it more vibrant" -i input.png -o output.webp
```

## Make Commands

```bash
make dev        # Run backend + frontend, open browser
make backend    # Run backend only
make frontend   # Run frontend only
make install    # Install all dependencies
make clean      # Clear generated files
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, shadcn/ui, Zustand
- **AI**: Google Gemini 3.1 Flash

## License

MIT
