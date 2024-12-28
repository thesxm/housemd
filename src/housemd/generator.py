import markdown
from markdown_katex import makeExtension as markdown_katex_ext
from os import path

class Generator:
    def __init__(self, template_dir):
        "Initialize the Generator Object"

        self._md = markdown.Markdown(extensions = [
            "extra",
            "admonition",
            "codehilite",
            "meta",
            "nl2br",
            "sane_lists",
            "smarty",
            "toc",
            "wikilinks",
            markdown_katex_ext(),
        ])
        self._template_dir = template_dir

    def _md_to_html(self, md_txt):
        """
        Converts the given markdown text to html, returns a tuple (html_text, extension_outputs)
        """

        self._md.reset()
        html_txt = self._md.convert(md_txt)
        extension_outputs = {
                "metadata": self._md.Meta
        }

        return html_txt, extension_outputs

    def _get_template_txt(self, template_name):
        """
        Get the template text from a template file in template_dir
        """

        with open(path.join(self._template_dir, template_name), "r") as f:
            txt = f.read()

        return txt

    def _compile(self, template_txt, html_txt, extension_returns):
        """
        Generate the final static HTML file content, merging the template with generated HTML from Markdown and extension outputs
        """

        m = extension_returns["metadata"]
        res = template_txt.replace("{{ CONTENT }}", html_txt)

        for key, val in m.items():
            res = res.replace("{{ " + key.upper() + " }}", m[key][0])

        return res 

    def __call__(self, fname):
        """
        Run the generator on a file
        """

        with open(fname, "r") as f:
            md = f.read()

        html_txt, ext_outs = self._md_to_html(md)
        template_txt = self._get_template_txt(ext_outs["metadata"]["template"][0])

        return self._compile(template_txt, html_txt, ext_outs), ext_outs["metadata"]
