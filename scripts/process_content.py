
import json
import re
import os
import sys

def clean_text(text):
    return text.strip()

def process_forces(json_path, output_dir):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pages = data['pages']
    
    structure_md = "# Structure du Livret VIA-GESTION\n\n"
    content_md = "# Contenu Complet - Forces de Caractère VIA\n\n"
    
    current_category = ""
    
    # Map of pages to content (simplified logic based on visual inspection)
    # Categories seem to be introduced, but main content is on specific pages.
    # We'll look for "Ma force signature est :" to identify a Force page.
    
    forces = []
    
    for page in pages:
        text = page['text']
        
        # Detect Category (often at top left, but might be messy)
        # Better to rely on the consistent "Ma force signature est :" marker for forces
        
        if "Ma force signature est :" in text:
            # Extract Force Name
            # Usually follows "Ma force signature est :" on next line or same line
            # In the JSON, it looks like: "Ma force signature est :\nCRÉATIVITÉ..."
            
            match = re.search(r"Ma force signature est :[\s\n]+([^\n]+)", text, re.IGNORECASE)
            force_name = "Inconnue"
            if match:
                force_name = match.group(1).strip()
                # sometimes name is on multiple lines or followed by description.
                # Let's try to grab the line that looks like a title (Uppercased often)
                
            # Attempt to identifying Category from text headers if possible
            # Categories: SAGESSE ET SAVOIR, COURAGE, HUMANITÉ ET AMOUR, JUSTICE, MODÉRATION, TRANSCENDANCE
            categories = [r"SAGESSE\s+ET\s+SAVOIR", "COURAGE", r"HUMANITÉ\s+ET\s+AMOUR", "JUSTICE", "MODÉRATION", r"TRANSCEN\s?-\s?DANCE", "TRANSCENDANCE"]
            
            cat_found = "Non classé"
            for cat in categories:
                if re.search(cat, text, re.IGNORECASE):
                    cat_name = cat.replace("\\s+", " ").replace("TRANSCEN - DANCE", "TRANSCENDANCE").replace("TRANSCEN- DANCE", "TRANSCENDANCE")
                    if "TRANSCEN" in cat: cat_name = "TRANSCENDANCE"
                    if "SAGESSE" in cat: cat_name = "SAGESSE ET SAVOIR"
                    cat_found = cat_name
                    break
            
            forces.append({
                "category": cat_found,
                "name": force_name,
                "raw_text": text
            })

    # Group by category
    grouped = {}
    order = ["SAGESSE ET SAVOIR", "COURAGE", "HUMANITÉ ET AMOUR", "JUSTICE", "MODÉRATION", "TRANSCENDANCE", "Non classé"]
    
    for f in forces:
        cat = f['category']
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(f)
        
    # Build Structure MD
    for cat in order:
        if cat in grouped and grouped[cat]:
            structure_md += f"## {cat}\n"
            for force in grouped[cat]:
                structure_md += f"- {force['name']}\n"
            structure_md += "\n"
            
    # Build Content MD
    for cat in order:
        if cat in grouped and grouped[cat]:
            content_md += f"# {cat}\n\n"
            for force in grouped[cat]:
                content_md += f"## {force['name']}\n\n"
                
                # Parse sections from raw text
                # Sections to look for: UTILISATION OPTIMALE, SURUTILISATION, CONTEXTES DE SOUS-UTILISATION, OPTIMISATION, MÉTAPHORE, Description (after signature)
                
                txt = force['raw_text']
                
                # Helper to extract between markers
                def extract_section(start_marker, end_markers, text):
                    pattern = f"{start_marker}(.*?)(?:{'|'.join(end_markers)}|$)"
                    # This is tricky because order varies.
                    # Simplified: Split text by double newlines and look for headers?
                    pass

                # Let's dump cleaned text for now, or try simple regex split
                # The text extraction is "visual", so layout is preserved in 'text' field somewhat.
                # We'll just preserve the raw text but clean up extra newlines for readability
                
                # Try to isolate description
                desc_match = re.search(r"Ma force signature est :[\s\n]+[^\n]+[\n]+(.*?)(?:UTILISATION|OPTIMISATION|SURUTILISATION|CONTEXTES|MÉTAPHORE|$)", txt, re.DOTALL | re.IGNORECASE)
                if desc_match:
                    content_md += f"**Définition**:\n{desc_match.group(1).strip()}\n\n"
                
                # Other sections
                sections = ["UTILISATION OPTIMALE", "SURUTILISATION", "CONTEXTES DE SOUS-UTILISATION", "OPTIMISATION", "MÉTAPHORE", "Impacts"]
                
                for section in sections:
                    if section in txt:
                        # Find content until next section
                        section_pattern = re.escape(section)
                        others = [re.escape(s) for s in sections if s != section]
                        others.append("Ma force signature est") # sentinel
                        
                        pattern = f"{section_pattern}[\s\n:]+(.*?)(?:{'|'.join(others)}|$)"
                        # Note: This regex might be weak if sections are interleaved heavily or layout is complex.
                        # But typically these are blocks.
                        # Let's try a simpler approach: regex for the specific section content
                        
                        # Actually, raw text dump of the page might be better if parsing is brittle, 
                        # but user asked to "extract structures".
                        # Let's try to just dump the raw text organized by force if precise parsing is hard.
                        # User said "extract all text... recreate structure".
                        
                        pass
                
                content_md += "### Texte Complet Extrait\n"
                content_md += f"```text\n{txt}\n```\n\n"
                content_md += "---\n\n"

    # Write CSV
    import csv
    
    csv_path = os.path.join(output_dir, 'tableau_forces.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';') # Semicolon for Excel in Europe
        
        # Header
        writer.writerow(['Catégorie / Force', 'Utilisation Optimale', 'Surutilisation', 'Optimisation', 'Contexte de Sous-utilisation & Impacts'])
        
        for cat in order:
            if cat in grouped and grouped[cat]:
                # Category Row
                writer.writerow([f"LES FORCES DE CARACTÈRE DU LEADER : {cat.upper()}", '', '', '', ''])
                
                for force in grouped[cat]:
                    txt = force['raw_text']
                    
                    # Robust section extraction logic
                    # We assume sections appear in this order:
                    # [Definition] -> UTILISATION OPTIMALE -> SURUTILISATION -> OPTIMISATION -> CONTEXTES DE SOUS-UTILISATION -> [Impacts] -> MÉTAPHORE -> Ma force signature est
                    
                    # We will define a helper that finds content between a Start Header and the *Next Available Header*.
                    
                    def get_content_between(text, start_header, allowed_next_headers):
                        if start_header not in text:
                            return ""
                        
                        start_idx = text.find(start_header) + len(start_header)
                        
                        # Find the first occurrence of ANY allowed next header
                        # We use a large number if not found
                        end_idx = len(text)
                        
                        for h in allowed_next_headers:
                            if h == start_header: continue # Skip itself if in list
                            idx = text.find(h, start_idx)
                            if idx != -1 and idx < end_idx:
                                end_idx = idx
                        
                        # Extract and clean
                        content = text[start_idx:end_idx].strip()
                        # Removed typical leading chars like colon or newline
                        content = content.lstrip(": \n")
                        return content

                    # Specific usage for each section
                    
                    # 1. Utilisation Optimale -> Ends at Surutilisation, Optimisation, Contextes...
                    util_opt = get_content_between(
                        txt, 
                        "UTILISATION OPTIMALE", 
                        ["SURUTILISATION", "OPTIMISATION", "CONTEXTES DE SOUS-UTILISATION", "MÉTAPHORE", "Ma force signature est"]
                    )
                    
                    # 2. Surutilisation -> Ends at Optimisation, Contextes...
                    surutil = get_content_between(
                        txt, 
                        "SURUTILISATION", 
                        ["OPTIMISATION", "CONTEXTES DE SOUS-UTILISATION", "MÉTAPHORE", "Ma force signature est"]
                    )
                    
                    # 3. Optimisation -> Ends at Contextes...
                    optim = get_content_between(
                        txt, 
                        "OPTIMISATION", 
                        ["CONTEXTES DE SOUS-UTILISATION", "MÉTAPHORE", "Ma force signature est", "SURUTILISATION"] # Handle out of order just in case
                    )
                    
                    # 4. Contextes -> Ends at Impacts, Metaphore...
                    contexte = get_content_between(
                        txt, 
                        "CONTEXTES DE SOUS-UTILISATION", 
                        ["Impacts", "Impact", "MÉTAPHORE", "Ma force signature est"]
                    )
                    
                    # 5. Impacts -> Ends at Metaphore...
                    impacts = ""
                    if "Impacts" in txt:
                        impacts = get_content_between(
                            txt,
                            "Impacts",
                            ["MÉTAPHORE", "Ma force signature est", "OPTIMISATION"] # Safety checks
                        )
                    elif "Impact" in txt: # Singular case?
                         impacts = get_content_between(
                            txt,
                            "Impact",
                            ["MÉTAPHORE", "Ma force signature est"]
                        )


                    full_context = contexte
                    if impacts:
                        full_context += f"\n\nIMPACTS:\n{impacts}"

                    def clean(s):
                        return re.sub(r'\n+', '\n', s).strip()

                    # Force Row (Indented)
                    force_name_display = "    " + force['name'] # 4 spaces indent
                    
                    writer.writerow([
                        force_name_display,
                        clean(util_opt),
                        clean(surutil),
                        clean(optim),
                        clean(full_context)
                    ])

    print(f"Generated files in {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process.py <json_file> <output_dir>")
        sys.exit(1)
        
    process_forces(sys.argv[1], sys.argv[2])
