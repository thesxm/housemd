TEMPLATE: base.html
TITLE: HouseMD Documentation

# HouseMD - Static Site Generator

HouseMD is a simple and lightweight static site generator written in Python. Inspired by the TV show "House, M.D.," the name also reflects its core functionality: converting Markdown (`.md`) files into HTML. HouseMD takes a directory structure, processes all Markdown files to generate HTML, and copies all other files as-is to produce a complete static website.

## Table of Contents
[TOC]

## Features

- Converts Markdown files into HTML using the `markdown` library, all [standard extensions](https://python-markdown.github.io/extensions/) are enabled.
- Supports templates for consistent HTML formatting.
- Extracts and utilizes metadata from Markdown files.
- Retains the original directory structure of the input folder.
- Copies non-Markdown files (e.g., images, CSS, JavaScript) unchanged.
- Simple and efficient, designed for quick static site generation.
- Optionally dumps the metadata of all translated files as JSON to a specified path.

## Installation

Install using pip:

```bash
pip install git+https://github.com/thesxm/housemd
```

## Usage

HouseMD provides three main commands:

### 1. `housemd-init`
Generates the configuration file for `housemd` commands to use.

```bash
housemd-init
```

The config json should contain the following keys:
1. **source**: The directory containing your Markdown files and other assets.
2. **output**: The directory where the static site will be generated.
3. **templates**: The directory containing HTML templates.
4. *(Optional)* **mdb**: If provided, the metadata of all translated files will be dumped as a JSON file to this path.
5. *(Optional)* **port**: The port on which housemd-live http server should run. Defaults to whatever port is given by the Operating System.
6. *(Optional)* **trigger_threshold**: Amount of time to wait after the last change is detected by housemd-live before re-building the site. Defaults to 3 seconds.

### 2. `housemd-build`
Builds the static site by processing the source directory and generating the output directory.

```bash
housemd-build <config_file_path>
```

### 3. `housemd-live`
Builds the static site, starts a static server on the output path and actively monitors the source and template directories for changes. If any changes are detected, it rebuilds the static site 3 seconds after the last detected change, resetting the timer if new changes occur during this interval. This command takes the same arguments as the `housemd-build` command:

```bash
housemd-live <config_file_path>
```

Both `housemd-build` and `housemd-init` commands take the path of the config file as an argument.

### Example
Assuming a simple `housemd-config.json`:
```json
{
    "source": "./my-website",
    "output": "./output",
    "templates": "./templates",
    "mdb": "./output/metadatabase.json"
}
```

You can execute `housemd` commands as such:
```bash
housemd-build ./housemd-config.json
housemd-live ./housemd-config.json
```

### What Happens?

1. **Initialize Output Directory**: The output directory is emptied, and all subdirectories from the source directory are recreated in the output directory (empty for now).
2. **Process Markdown Files**:
   - Each `.md` file is translated into an HTML file using the `markdown` library.
   - Metadata written at the beginning of the `.md` file is extracted.
   - The translated HTML is embedded into the specified template (using the template name from the metadata).
   - Other template variables are populated using the metadata.
   - The resulting HTML file is written to the output directory, preserving the original directory structure.
   - If a `metadatabase_path` is provided, all extracted metadata is saved as a JSON file to the specified path.
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
├── images/
│   └── logo.png
└── metadata.json (if metadatabase_path is provided)
```

## Metadata Example

Markdown files in HouseMD support metadata at the top of the file, which helps determine the template to use and populate variables in the template. Below is an example of how to write metadata in a Markdown file:

### Input Markdown File (`index.md`):
````markdown
TEMPLATE: index.html
TITLE: Index

# Hello, World

``` python
print("Hello, World!")
```
````

### Explanation:
1. **TEMPLATE**: Specifies the HTML template to use (e.g., `index.html`), *required*.
2. **TITLE**: A variable that can be used in the template (e.g., for the `<title>` tag).
3. The rest of the Markdown content will be converted into HTML and inserted into the designated template.

### Output HTML (`index.html`):
Assuming a simple `index.html` template like this:
```html
<html>
<head><title>{{ TITLE }}</title></head>
<body>
    <div>{{ CONTENT }}</div>
</body>
</html>
```
The resulting HTML will look like this:
```html
<html>
<head><title>Index</title></head>
<body>
    <div>
        <h1>Hello, World</h1>
        <pre><code class="language-python">print("Hello, World!")</code></pre>
    </div>
</body>
</html>
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve HouseMD.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the amazing TV show "House, M.D."
- Built with the simplicity and power of Python and the `markdown` library.

