import nbformat
from nbconvert import HTMLExporter
import sys

# -----------------------------
# CONFIG
# -----------------------------
# Notebook file (change as needed)
notebook_filename = "AQI_False_Color_Img_copy.ipynb"
# Output HTML file
html_filename = notebook_filename.replace(".ipynb", ".html")
# Title: if you want to override notebook first cell title, set here; else keep None
title = None
# -----------------------------

# Load notebook
nb = nbformat.read(notebook_filename, as_version=4)

# -----------------------------
# Remove warnings from outputs
# -----------------------------
for cell in nb.cells:
    if cell.cell_type == "code":
        new_outputs = []
        for output in cell.get("outputs", []):
            # Keep output only if it is not a warning
            if output.output_type == "stream":
                if "warning" not in output.get("text", "").lower():
                    new_outputs.append(output)
            elif output.output_type in ("execute_result", "display_data"):
                new_outputs.append(output)
        cell["outputs"] = new_outputs

# -----------------------------
# Setup HTML exporter
# -----------------------------
html_exporter = HTMLExporter()
html_exporter.template_name = "lab"

# Export notebook
(body, resources) = html_exporter.from_notebook_node(nb)

# -----------------------------
# Inject JavaScript for collapsible code
# -----------------------------
js = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('div.input').forEach((cell) => {
        const btn = document.createElement('button');
        btn.innerHTML = "Show/Hide Code";
        btn.style.margin = "5px 0";
        btn.onclick = () => {
            cell.style.display = (cell.style.display === "none") ? "block" : "none";
        };
        cell.parentNode.insertBefore(btn, cell);
        cell.style.display = "none"; // start collapsed
    });
});
</script>
"""

# Optional: override title with first markdown cell
if title:
    body = body.replace("<body>", f"<body><h1>{title}</h1>")

# Inject JS before </body>
body = body.replace("</body>", js + "</body>")

# Save HTML
with open(html_filename, "w") as f:
    f.write(body)

print(f"✅ Exported {html_filename} with foldable code and warnings hidden")
