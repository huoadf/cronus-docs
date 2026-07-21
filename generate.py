import os
import re
import json

# Configuration of pages
PAGES = [
    {"id": "getting-started", "title": "Getting started", "group": "", "src": "getting-started.md", "url": "index.html", "breadcrumb": "Getting started"},
    {"id": "syntax", "title": "Syntax basics", "group": "Scripting Basics", "src": "syntax.md", "url": "syntax/index.html", "breadcrumb": "Syntax basics"},
    {"id": "user-functions", "title": "User Functions", "group": "Scripting Basics", "src": "user-functions.md", "url": "user-functions/index.html", "breadcrumb": "User Functions"},
    {"id": "input-output", "title": "Input & Output", "group": "API Reference", "src": "input-output.md", "url": "input-output/index.html", "breadcrumb": "Input & Output"},
    {"id": "combos-timing", "title": "Combos & Timing", "group": "API Reference", "src": "combos-timing.md", "url": "combos-timing/index.html", "breadcrumb": "Combos & Timing"},
    {"id": "controller", "title": "Controller Hardware", "group": "API Reference", "src": "controller.md", "url": "controller/index.html", "breadcrumb": "Controller Hardware"},
    {"id": "math", "title": "Math & Utilities", "group": "API Reference", "src": "math.md", "url": "math/index.html", "breadcrumb": "Math & Utilities"},
    {"id": "advanced-guides", "title": "Advanced Guides & Macros", "group": "Guides", "src": "advanced-guides.md", "url": "advanced-guides/index.html", "breadcrumb": "Advanced Guides & Macros"}
]

# Load layout template
with open("template.html", "r", encoding="utf-8") as f:
    TEMPLATE = f.read()

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def parse_markdown(md_text, current_url):
    # Determine the depth/relative prefix
    depth = current_url.count('/')
    relative_prefix = "../" * depth
    
    # 1. Pre-process links starting with /cronus-docs/ to use relative prefix
    def rewrite_cronus_link(match):
        path = match.group(1)
        if not path or path == "/":
            return f'href="{relative_prefix}"'
        path = path.strip('/')
        return f'href="{relative_prefix}{path}/"'
        
    md_text = re.sub(r'href="/cronus-docs/([^"]*)"', rewrite_cronus_link, md_text)
    md_text = re.sub(r'href="/cronus-docs"', f'href="{relative_prefix}"', md_text)
    
    def rewrite_markdown_link(match):
        link_text = match.group(1)
        path = match.group(2) or ""
        if not path or path == "/":
            return f'[{link_text}]({relative_prefix})'
        path = path.strip('/')
        return f'[{link_text}]({relative_prefix}{path}/)'
        
    md_text = re.sub(r'\[([^\]]+)\]\(/cronus-docs/([^\)]*)\)', rewrite_markdown_link, md_text)
    md_text = re.sub(r'\[([^\]]+)\]\(/cronus-docs\)', f'[\\1]({relative_prefix})', md_text)
    
    # Also fix standard external link markup style
    md_text = re.sub(r'<([^>]+)>', r'<a href="\1">\1</a>', md_text)
    
    lines = md_text.split("\n")
    html_lines = []
    
    in_code = False
    code_block = []
    code_lang = ""
    
    in_list = False
    list_type = None # 'ul' or 'ol'
    
    in_callout = False
    callout_style = ""
    callout_body = []
    
    in_cards = False
    cards_content = []
    
    in_table = False
    table_headers = []
    table_rows = []
    
    # SVGs for callouts
    svgs = {
        "info": '<span class="callout-ico" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></svg></span>',
        "warning": '<span class="callout-ico" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4M12 17h.01"/></svg></span>',
        "danger": '<span class="callout-ico" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m15 9-6 6M9 9l6 6"/></svg></span>',
        "success": '<span class="callout-ico" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m9 12 2 2 4-4"/></svg></span>'
    }

    # Tracking for headers to generate TOC
    headings = []

    def inline_format(text):
        # Escaped code block backticks
        # Inline code `` `code` ``
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 1. Code block handling
        if stripped.startswith("```"):
            if in_code:
                in_code = False
                code_content = "\n".join(code_block)
                # Escaping HTML tags inside code
                code_content = code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                html_lines.append(f'<pre><code class="language-{code_lang}">{code_content}</code></pre>')
                code_block = []
                code_lang = ""
            else:
                in_code = True
                code_lang = stripped[3:].strip()
                if not code_lang:
                    code_lang = "txt"
            i += 1
            continue
            
        if in_code:
            code_block.append(line)
            i += 1
            continue
            
        # 2. Hint / Callout handling
        if stripped.startswith('{% hint style='):
            in_callout = True
            style_match = re.search(r'style="([^"]+)"', stripped)
            callout_style = style_match.group(1) if style_match else "info"
            callout_body = []
            i += 1
            continue
            
        if stripped.startswith('{% endhint %}'):
            in_callout = False
            parsed_callout_body = parse_markdown("\n".join(callout_body), current_url)[0]
            html_lines.append(f'<div class="callout callout-{callout_style}">{svgs.get(callout_style, svgs["info"])}<div class="callout-body">{parsed_callout_body}</div></div>')
            callout_body = []
            i += 1
            continue
            
        if in_callout:
            callout_body.append(line)
            i += 1
            continue
            
        # 3. Cards block handling
        if stripped.startswith('::: cards'):
            in_cards = True
            cards_content = []
            i += 1
            continue
            
        if stripped.startswith(':::'):
            if in_cards:
                in_cards = False
                # Parse list inside cards
                cards_html = []
                for card in cards_content:
                    card_stripped = card.strip()
                    if card_stripped.startswith("-") or card_stripped.startswith("*"):
                        card_stripped = card_stripped[1:].strip()
                    # Links format in cards: [**Title** description](url)
                    match = re.match(r'\[\*\*([^*]+)\*\*\s*([^\]]*)\]\(([^)]+)\)', card_stripped)
                    if match:
                        title, desc, url = match.groups()
                        # Resolve URL relativity
                        if url.startswith("/cronus-docs/"):
                            url = url.replace("/cronus-docs/", relative_prefix)
                            if not url.endswith("index.html") and not url.endswith("/"):
                                url += "/index.html"
                            elif url.endswith("/"):
                                url += "index.html"
                        elif url == "/cronus-docs":
                            url = relative_prefix + "index.html"
                            
                        desc_str = f" {desc}" if desc.strip() else ""
                        cards_html.append(f'<p><a href="{url}"><strong>{title}</strong>{desc_str}</a></p>')
                    else:
                        # plain link
                        link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', card_stripped)
                        if link_match:
                            title, url = link_match.groups()
                            if url.startswith("/cronus-docs/"):
                                url = url.replace("/cronus-docs/", relative_prefix) + "index.html"
                            cards_html.append(f'<p><a href="{url}">{title}</a></p>')
                
                html_lines.append(f'<div class="cards">{"".join(cards_html)}</div>')
                cards_content = []
            i += 1
            continue
            
        if in_cards:
            if stripped:
                cards_content.append(line)
            i += 1
            continue

        # 4. Table handling
        if stripped.startswith("|") and not in_table:
            # Check if next line is a separator like |---|---|
            if i + 1 < len(lines) and re.match(r'^[|\s:-]+$', lines[i+1].strip()):
                in_table = True
                # Parse headers
                table_headers = [c.strip() for c in stripped.split("|")[1:-1]]
                i += 2 # Skip header and separator
                table_rows = []
                continue
                
        if in_table:
            if stripped.startswith("|"):
                row_cells = [inline_format(c.strip()) for c in stripped.split("|")[1:-1]]
                table_rows.append(row_cells)
                i += 1
                continue
            else:
                in_table = False
                # Compile table
                thead = "<tr>" + "".join(f'<th>{h}</th>' for h in table_headers) + "</tr>"
                tbody = "".join("<tr>" + "".join(f'<td>{cell}</td>' for cell in row) + "</tr>" for row in table_rows)
                html_lines.append(f'<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>')
                table_headers = []
                table_rows = []
                # Fall through to process current line

        # 5. List handling
        is_list_item = stripped.startswith("* ") or stripped.startswith("- ") or re.match(r'^\d+\.\s', stripped)
        if is_list_item:
            if not in_list:
                in_list = True
                list_type = 'ol' if re.match(r'^\d+\.\s', stripped) else 'ul'
                html_lines.append(f'<{list_type}>')
            
            # Extract content
            if list_type == 'ol':
                item_content = re.sub(r'^\d+\.\s+', '', stripped)
            else:
                item_content = stripped[2:]
                
            html_lines.append(f'<li>{inline_format(item_content)}</li>')
            i += 1
            continue
        elif in_list:
            in_list = False
            html_lines.append(f'</{list_type}>')
            # Fall through

        # 6. Headers
        if stripped.startswith("#"):
            level = len(re.match(r'^#+', stripped).group(0))
            header_text = stripped.lstrip('#').strip()
            clean_text = header_text.replace("`", "").replace("*", "").replace(":", "")
            header_id = slugify(clean_text)
            
            formatted_text = inline_format(header_text)
            
            if level <= 3:
                headings.append({"level": level, "title": clean_text, "id": header_id})
                html_lines.append(f'<h{level} id="{header_id}" tabindex="-1">{formatted_text} <a class="header-anchor" href="#{header_id}" aria-hidden="true">#</a></h{level}>')
            else:
                html_lines.append(f'<h{level}>{formatted_text}</h{level}>')
            i += 1
            continue

        # 7. Horizontal rule
        if stripped == "---" or stripped == "***":
            html_lines.append('<hr>')
            i += 1
            continue

        # 8. Paragraphs and blank lines
        if stripped == "":
            i += 1
            continue
            
        html_lines.append(f'<p>{inline_format(stripped)}</p>')
        i += 1
        
    if in_list:
        html_lines.append(f'</{list_type}>')
        
    return "\n".join(html_lines), headings

def build_toc(headings):
    if not headings:
        return ""
    toc_lines = ['<ul class="toc-list">']
    for h in headings:
        if h["level"] == 2:
            toc_lines.append(f'<li class="toc-l2"><a href="#{h["id"]}">{h["title"]}</a></li>')
        elif h["level"] == 3:
            toc_lines.append(f'<li class="toc-l3"><a href="#{h["id"]}">{h["title"]}</a></li>')
    toc_lines.append('</ul>')
    return "\n".join(toc_lines)

def build_pager(index):
    prev_page = PAGES[index - 1] if index > 0 else None
    next_page = PAGES[index + 1] if index < len(PAGES) - 1 else None
    
    current_page = PAGES[index]
    depth = current_page["url"].count('/')
    relative_prefix = "../" * depth
    
    def get_link_url(url):
        if url == "index.html":
            return ""
        return url.replace("index.html", "")

    pager_html = ['<nav class="pager">']
    
    if prev_page:
        prev_url = f"{relative_prefix}{get_link_url(prev_page['url'])}"
        pager_html.append(f'<a class="pager-link prev" href="{prev_url}">')
        pager_html.append('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transform: rotate(180deg)"><path d="M5 12h14M12 5l7 7-7 7"/></svg>')
        pager_html.append(f'<span><em>Previous</em>{prev_page["title"]}</span>')
        pager_html.append('</a>')
    else:
        pager_html.append('<span></span>')
        
    if next_page:
        next_url = f"{relative_prefix}{get_link_url(next_page['url'])}"
        pager_html.append(f'<a class="pager-link next" href="{next_url}">')
        pager_html.append(f'<span><em>Next</em>{next_page["title"]}</span>')
        pager_html.append('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>')
        pager_html.append('</a>')
        
    pager_html.append('</nav>')
    return "\n".join(pager_html)

# List to hold search index database
search_index_db = []

# Generate all pages
for idx, page in enumerate(PAGES):
    src_file = os.path.join("src", page["src"])
    if not os.path.exists(src_file):
        print(f"Warning: Source file {src_file} does not exist. Skipping.")
        continue
        
    with open(src_file, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    dest_file = page["url"]
    dest_dir = os.path.dirname(dest_file)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        
    # Relative path calculations
    depth = dest_file.count('/')
    relative_path = "../" * depth
    
    # Parse Markdown
    html_content, headings = parse_markdown(md_content, dest_file)
    toc_html = build_toc(headings)
    pager_html = build_pager(idx)
    
    # Assemble templates
    output_html = TEMPLATE
    output_html = output_html.replace("{{ title }}", page["title"])
    output_html = output_html.replace("{{ page_id }}", page["id"])
    output_html = output_html.replace("{{ relative_path }}", relative_path)
    output_html = output_html.replace("{{ breadcrumb }}", page["breadcrumb"])
    output_html = output_html.replace("{{ content }}", html_content)
    output_html = output_html.replace("{{ toc }}", toc_html)
    output_html = output_html.replace("{{ pager }}", pager_html)
    
    # Active navigation highlights
    for active_page in PAGES:
        placeholder = f"{{{{ active_{active_page['id'].replace('-', '_')} }}}}"
        if active_page["id"] == page["id"]:
            output_html = output_html.replace(placeholder, "active")
        else:
            output_html = output_html.replace(placeholder, "")
            
    with open(dest_file, "w", encoding="utf-8") as f_out:
        f_out.write(output_html)
        
    print(f"Generated {dest_file}")
    
    # Search index entry
    headings_titles = [h["title"] for h in headings]
    search_body = re.sub(r'<[^>]+>', ' ', html_content)
    search_body = re.sub(r'\s+', ' ', search_body).strip()
    
    def get_link_url(url):
        if url == "index.html":
            return ""
        return url.replace("index.html", "")

    search_index_db.append({
        "title": page["title"],
        "url": get_link_url(page["url"]),
        "group": page["group"],
        "headings": headings_titles,
        "body": search_body
    })

# Write search index database
with open("search-index.json", "w", encoding="utf-8") as f_idx:
    json.dump(search_index_db, f_idx, indent=2)

print("Generated search-index.json")

# Generate llms-full.txt
llms_full_content = ["# Cronus GPC documentation\n\n> Zen GPC Scripting documentation\n\n"]
for page in PAGES:
    src_file = os.path.join("src", page["src"])
    if os.path.exists(src_file):
        with open(src_file, "r", encoding="utf-8") as f_in:
            page_md = f_in.read()
        # Clean up GitBook specific tags for LLM readability
        page_md = re.sub(r'\{% hint style="([^"]+)" %\}', r'> **[\1]**', page_md)
        page_md = page_md.replace('{% endhint %}', '')
        page_md = page_md.replace('::: cards', '').replace(':::', '')
        
        url_subpath = page['url'].replace('index.html', '')
        llms_full_content.append(f"---\n\n# {page['title']}\n\nSource: https://huoadf.github.io/cronus-docs/{url_subpath}\n\n{page_md}\n")

with open("llms-full.txt", "w", encoding="utf-8") as f_llms_full:
    f_llms_full.write("\n".join(llms_full_content))
print("Generated llms-full.txt")

# Generate llms.txt (brief summary)
llms_summary = """# Cronus GPC Docs
> GPC Scripting documentation for Cronus Zen

## Directory
- [Getting started](https://huoadf.github.io/cronus-docs/) - Setup, compilation, and device loading.
- [Syntax basics](https://huoadf.github.io/cronus-docs/syntax/) - Code structure, variables, loop concepts, compiler constraints.
- [User Functions](https://huoadf.github.io/cronus-docs/user-functions/) - Declaring functions with user parameters, scoping, recursion bans.
- [Input & Output](https://huoadf.github.io/cronus-docs/input-output/) - Reading inputs, setting values, press and release events, blocking.
- [Combos & Timing](https://huoadf.github.io/cronus-docs/combos-timing/) - Writing combos, wait timers, state time measurements.
- [Controller Hardware](https://huoadf.github.io/cronus-docs/controller/) - Rumble motors, color LEDs, controller button aliases.
- [Math & Utilities](https://huoadf.github.io/cronus-docs/math/) - Clamp, absolute values, random generators, fixed-point math patterns.
- [Advanced Guides & Macros](https://huoadf.github.io/cronus-docs/advanced-guides/) - Progressive anti-recoil, adjustable rapid fire, slide cancellations, and CPU optimization.

For the full detailed documentation text, visit [llms-full.txt](https://huoadf.github.io/cronus-docs/llms-full.txt).
"""

with open("llms.txt", "w", encoding="utf-8") as f_llms:
    f_llms.write(llms_summary)
print("Generated llms.txt")

print("All documentation generated successfully!")
