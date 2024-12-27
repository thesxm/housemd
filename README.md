# HouseMD - Static Site Generator

HouseMD is a simple and lightweight static site generator written in Python. Inspired by the TV show "House, M.D.," the name also reflects its core functionality: converting Markdown (`.md`) files into HTML. HouseMD takes a directory structure, processes all Markdown files to generate HTML, and copies all other files as-is to produce a complete static website.

## Features

- Converts Markdown files into HTML using the `markdown` library.
- Supports templates for consistent HTML formatting.
- Extracts and utilizes metadata from Markdown files.
- Retains the original directory structure of the input folder.
- Copies non-Markdown files (e.g., images, CSS, JavaScript) unchanged.
- Simple and efficient, designed for quick static site generation.

## Installation

Install using pip:

```bash
pip install git+https://github.com/thesxm/housemd
```

## Usage

Run the `housemd` package from the command line with three arguments:
1. **Source Directory**: The directory containing your Markdown files and other assets.
2. **Output Directory**: The directory where the static site will be generated.
3. **Template Directory**: The directory containing HTML templates.

```bash
python -m housemd <source_directory> <output_directory> <template_directory>
```

### Example

```bash
python -m housemd ./my-website ./output ./templates
```

### What Happens?

1. **Initialize Output Directory**: The output directory is emptied, and all subdirectories from the source directory are recreated in the output directory (empty for now).
2. **Process Markdown Files**:
   - Each `.md` file is translated into an HTML file using the `markdown` library.
   - Metadata written at the beginning of the `.md` file is extracted.
   - The translated HTML is embedded into the specified template (using the template name from the metadata).
   - Other template variables are populated using the metadata.
   - The resulting HTML file is written to the output directory, preserving the original directory structure.
3. **Copy Non-Markdown Files**: All non-Markdown files (e.g., images, CSS, JavaScript) are copied unchanged to the output directory, maintaining their original paths.

## Example Directory Structure

### Input (Source)
```
my-website/
├── index.md
├── about.md
├── assets/
│   ├── styles.css
│   └── script.js
└── images/
    └── logo.png
```

### Templates
```
templates/
├── default.html
├── blog.html
```

### Output (Destination)
```
output/
├── index.html
├── about.html
├── assets/
│   ├── styles.css
│   └── script.js
└── images/
    └── logo.png
```

## How It Works

1. **Markdown to HTML Conversion**: All `.md` files are read, processed using the `markdown` library, and saved as `.html` files. Metadata from the `.md` files is extracted and used to determine the appropriate template and populate template variables.
2. **Template Integration**: The translated HTML content is inserted into the specified template. Metadata variables are replaced within the template.
3. **File Copying**: Non-Markdown files are copied directly to the output directory without any modifications.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve HouseMD.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the amazing TV show "House, M.D."
- Built with the simplicity and power of Python and the `markdown` library.

