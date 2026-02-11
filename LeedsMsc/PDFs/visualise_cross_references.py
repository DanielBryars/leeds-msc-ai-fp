"""
Cross-Reference Graph Visualiser for PDF Collection
=====================================================
Extracts text from each PDF, identifies cross-references between papers
in the collection, and produces an interactive HTML graph + static PNG.

Usage:
    python visualise_cross_references.py

Outputs:
    cross_references.html  - Interactive graph (open in browser)
    cross_references.png   - Static image
"""

import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PDF_DIR = Path(__file__).parent
INDEX_JSON = PDF_DIR / "paper_index.json"
MAX_PAGES_FOR_REFS = None  # None = all pages; set to e.g. 10 for speed
ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")

# Colours for clusters (by keyword in title/filename)
CATEGORY_COLOURS = {
    "VLA":          "#e74c3c",   # red
    "LLM":          "#3498db",   # blue
    "Reinforcement": "#2ecc71",  # green
    "Robot":        "#9b59b6",   # purple
    "Teleoperation": "#f39c12",  # orange
    "Survey":       "#1abc9c",   # teal
    "Fine":         "#e67e22",   # dark orange
    "Attention":    "#3498db",   # blue
}
DEFAULT_COLOUR = "#95a5a6"  # grey


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def extract_arxiv_id(filename: str) -> str | None:
    """Pull an arxiv-style ID (e.g. 2304.13705) from a filename."""
    m = ARXIV_ID_RE.search(filename)
    return m.group(1) if m else None


def short_label(filename: str) -> str:
    """Make a readable short label from a PDF filename."""
    name = Path(filename).stem
    # Strip version suffixes like v1, v2, etc.
    name = re.sub(r"v\d+$", "", name).strip()
    # Truncate long names
    if len(name) > 40:
        name = name[:37] + "..."
    return name


def categorise(label: str) -> str:
    """Return a colour based on keywords in the label."""
    upper = label.upper()
    for keyword, colour in CATEGORY_COLOURS.items():
        if keyword.upper() in upper:
            return colour
    return DEFAULT_COLOUR


def extract_text(pdf_path: Path) -> str:
    """Extract full text from a PDF using PyMuPDF."""
    try:
        doc = fitz.open(str(pdf_path))
        pages = doc if MAX_PAGES_FOR_REFS is None else doc[:MAX_PAGES_FOR_REFS]
        text = "\n".join(page.get_text() for page in pages)
        doc.close()
        return text
    except Exception as e:
        print(f"  [WARN] Could not read {pdf_path.name}: {e}")
        return ""


def extract_title(text: str, filename: str) -> str:
    """Try to get the paper title from the first ~2000 chars of text."""
    # Heuristic: title is usually in the first few lines, often the longest
    # line before the word "Abstract"
    header = text[:2000]
    lines = [l.strip() for l in header.split("\n") if l.strip()]
    # Find lines before "abstract"
    title_lines = []
    for line in lines[:15]:
        if re.match(r"^abstract", line, re.IGNORECASE):
            break
        title_lines.append(line)
    if title_lines:
        # Pick the longest line as a guess for the title
        best = max(title_lines, key=len)
        if len(best) > 10:
            return best[:80]
    return short_label(filename)


def load_paper_index() -> dict:
    """Load paper_index.json if it exists, otherwise return empty dict."""
    if INDEX_JSON.exists():
        try:
            data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
            print(f"Loaded paper index with {len(data)} entries.")
            return data
        except Exception as e:
            print(f"  [WARN] Could not load paper index: {e}")
    else:
        print("  [INFO] No paper_index.json found. Run build_paper_index.py first for better labels.")
    return {}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDFs found in", PDF_DIR)
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDFs in {PDF_DIR}\n")

    # Load paper index for rich labels
    paper_index = load_paper_index()

    # -- Phase 1: Extract text and build identity maps ----------------------
    papers = {}  # filename -> {label, arxiv_id, title, text}
    arxiv_to_file = {}  # arxiv_id -> filename

    for pdf in pdf_files:
        print(f"  Reading {pdf.name}...")
        text = extract_text(pdf)
        arxiv_id = extract_arxiv_id(pdf.name)

        # Use paper index for label and title if available
        idx_entry = paper_index.get(pdf.name)
        if idx_entry:
            label = idx_entry.get("title_short") or short_label(pdf.name)
            title = idx_entry.get("title") or extract_title(text, pdf.name)
        else:
            label = short_label(pdf.name)
            title = extract_title(text, pdf.name)

        papers[pdf.name] = {
            "label": label,
            "arxiv_id": arxiv_id,
            "title": title,
            "text": text,
        }
        if arxiv_id:
            arxiv_to_file[arxiv_id] = pdf.name

    # Common words that appear everywhere - exclude from token matching
    STOPWORDS = {
        "learning", "model", "models", "robot", "robotic", "robotics",
        "language", "large", "vision", "based", "data", "deep", "neural",
        "network", "training", "policy", "action", "actions", "control",
        "manipulation", "generalization", "reinforcement", "autonomous",
        "intelligence", "physical", "review", "survey", "paper", "analysis",
        "using", "from", "with", "that", "this", "have", "their", "method",
        "approach", "scalable", "online", "fine", "tuning", "open",
        "hierarchical", "closed", "loop", "depth", "scene", "cluttered",
        "augmentation", "annotation", "enhancing", "advanced", "opinion",
        "small", "self", "behaviour", "behavior", "cloning", "proceedings",
        "book", "part", "failure", "collection", "scale",
    }

    # -- Phase 2: Find cross-references ------------------------------------
    print("\nSearching for cross-references...\n")
    edges = []  # (source, target)
    edge_set = set()

    for src_name, src_info in papers.items():
        src_text = src_info["text"]
        if not src_text:
            continue

        for tgt_name, tgt_info in papers.items():
            if src_name == tgt_name:
                continue

            found = False

            # Strategy 1: arxiv ID match (most reliable)
            tgt_arxiv = tgt_info["arxiv_id"]
            if tgt_arxiv and tgt_arxiv in src_text:
                found = True

            # Strategy 2: Title substring match (at least 40 chars of title)
            if not found:
                tgt_title = tgt_info["title"]
                if len(tgt_title) >= 40:
                    search_str = tgt_title[:60].lower()
                    if search_str in src_text.lower():
                        found = True

            if found:
                key = (src_name, tgt_name)
                if key not in edge_set:
                    edge_set.add(key)
                    edges.append(key)

    print(f"Found {len(edges)} cross-references between papers.\n")

    # -- Phase 3: Build graph -----------------------------------------------
    G = nx.DiGraph()

    for fname, info in papers.items():
        colour = categorise(info["label"] + " " + info["title"])
        G.add_node(fname, label=info["label"], title=info["title"],
                   color=colour, arxiv_id=info["arxiv_id"] or "")

    for src, tgt in edges:
        G.add_edge(src, tgt)

    # Remove isolated nodes (no references to/from other papers)
    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)
    if isolates:
        print(f"Removed {len(isolates)} isolated papers (no cross-refs found).")
    print(f"Graph has {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.\n")

    # -- Phase 4: Interactive HTML graph (pyvis) ----------------------------
    net = Network(
        height="900px", width="100%", directed=True,
        bgcolor="#1a1a2e", font_color="white",
        notebook=False,
    )
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=200,
        spring_strength=0.01,
        damping=0.09,
    )

    for node in G.nodes(data=True):
        fname, data = node
        in_deg = G.in_degree(fname)
        out_deg = G.out_degree(fname)
        size = 10 + in_deg * 5  # more-cited papers are bigger

        # Build hover tooltip with Harvard reference if available
        idx_entry = paper_index.get(fname)
        harvard = idx_entry.get("harvard_reference", "") if idx_entry else ""
        hover = (
            f"<b>{data['title']}</b><br>"
            f"File: {fname}<br>"
            f"Arxiv: {data['arxiv_id'] or 'N/A'}<br>"
            f"Cited by {in_deg} papers | Cites {out_deg} papers"
        )
        if harvard:
            hover += f"<br><br><i>{harvard}</i>"
        net.add_node(
            fname, label=data["label"], title=hover,
            color=data["color"], size=size,
            font={"size": 12, "color": "white"},
        )

    for src, tgt in G.edges():
        net.add_edge(src, tgt, color="#ffffff44", arrows="to")

    html_path = PDF_DIR / "cross_references.html"
    net.write_html(str(html_path))
    # Patch the HTML so it doesn't require a local lib/ folder
    print(f"Interactive graph saved to: {html_path}")

    # -- Phase 5: Static PNG (matplotlib) -----------------------------------
    fig, ax = plt.subplots(figsize=(20, 14))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    pos = nx.spring_layout(G, k=2.5, iterations=80, seed=42)

    # Size nodes by in-degree (citation count)
    in_degrees = dict(G.in_degree())
    node_sizes = [200 + in_degrees[n] * 150 for n in G.nodes()]
    node_colours = [G.nodes[n]["color"] for n in G.nodes()]

    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color="#ffffff22",
        arrows=True, arrowsize=12, arrowstyle="-|>",
        connectionstyle="arc3,rad=0.1", width=0.8,
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=node_sizes,
        node_color=node_colours, edgecolors="white",
        linewidths=0.5, alpha=0.9,
    )

    labels = {n: G.nodes[n]["label"][:25] for n in G.nodes()}
    nx.draw_networkx_labels(
        G, pos, labels, ax=ax, font_size=6,
        font_color="white", font_weight="bold",
    )

    # Legend
    legend_handles = []
    for keyword, colour in CATEGORY_COLOURS.items():
        legend_handles.append(mpatches.Patch(color=colour, label=keyword))
    legend_handles.append(mpatches.Patch(color=DEFAULT_COLOUR, label="Other"))
    ax.legend(
        handles=legend_handles, loc="upper left", fontsize=8,
        facecolor="#1a1a2e", edgecolor="white", labelcolor="white",
    )

    ax.set_title(
        "Paper Cross-Reference Graph",
        color="white", fontsize=18, fontweight="bold", pad=20,
    )
    ax.axis("off")
    plt.tight_layout()

    png_path = PDF_DIR / "cross_references.png"
    plt.savefig(str(png_path), dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Static graph saved to:     {png_path}")

    # -- Summary ------------------------------------------------------------
    print("\n--- Most-cited papers in your collection ---")
    top = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    for fname, deg in top:
        if deg > 0:
            title = papers[fname]['title']
            label = papers[fname]['label']
            display = title if len(title) <= 80 else label
            print(f"  [{deg} citations] {display}")

    print("\nDone! Open cross_references.html in a browser for the interactive version.")


if __name__ == "__main__":
    main()
