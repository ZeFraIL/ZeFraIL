#!/usr/bin/env python3
"""
Generate a comprehensive catalog of all repositories for ZeFraIL.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
import requests

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API = 'https://api.github.com'
OWNER = 'ZeFraIL'

# Category mappings
CATEGORY_MAPPING = {
    'sqlite': 'Database & Data Management',
    'database': 'Database & Data Management',
    'db': 'Database & Data Management',
    'contentprovider': 'Database & Data Management',
    'excel': 'Database & Data Management',
    'math': 'Educational (Science & Math)',
    'physics': 'Educational (Science & Math)',
    'chemistry': 'Educational (Science & Math)',
    'learning': 'Educational (Science & Math)',
    'learn': 'Educational (Science & Math)',
    'triangle': 'Educational (Science & Math)',
    'geometry': 'Educational (Science & Math)',
    'gauss': 'Educational (Science & Math)',
    'vector': 'Educational (Science & Math)',
    'geography': 'Geography & Maps',
    'geo': 'Geography & Maps',
    'map': 'Geography & Maps',
    'gps': 'Geography & Maps',
    'country': 'Geography & Maps',
    'moon': 'Astronomy & Space',
    'planet': 'Astronomy & Space',
    'solar': 'Astronomy & Space',
    'star': 'Astronomy & Space',
    'sunrise': 'Astronomy & Space',
    'natal': 'Astronomy & Space',
    'game': 'Games & Entertainment',
    'puzzle': 'Games & Entertainment',
    'catch': 'Games & Entertainment',
    'tile': 'Games & Entertainment',
    'tap': 'Games & Entertainment',
    'image': 'Media & Graphics',
    'pic': 'Media & Graphics',
    'camera': 'Media & Graphics',
    'gallery': 'Media & Graphics',
    'font': 'Media & Graphics',
    'graphic': 'Media & Graphics',
    'sensor': 'Sensors & Hardware',
    'accelerometer': 'Sensors & Hardware',
    'tilt': 'Sensors & Hardware',
    'phone': 'Sensors & Hardware',
    'proximity': 'Sensors & Hardware',
    'music': 'Audio & Music',
    'audio': 'Audio & Music',
    'metronome': 'Audio & Music',
    'radio': 'Audio & Music',
    'tts': 'Audio & Music',
    'chat': 'Communication & Web',
    'firebase': 'Communication & Web',
    'api': 'Communication & Web',
    'web': 'Communication & Web',
    'weather': 'Communication & Web',
    'json': 'Communication & Web',
    'xml': 'Communication & Web',
    'currency': 'Communication & Web',
    'fragment': 'Navigation & UI',
    'navigation': 'Navigation & UI',
    'drawer': 'Navigation & UI',
    'menu': 'Navigation & UI',
    'dialog': 'Navigation & UI',
    'listview': 'Navigation & UI',
    'recyclerview': 'Navigation & UI',
    'button': 'Navigation & UI',
    'custom': 'Navigation & UI',
    'design': 'Navigation & UI',
    'broadcast': 'Advanced Topics',
    'service': 'Advanced Topics',
    'receiver': 'Advanced Topics',
    'notification': 'Advanced Topics',
    'alarm': 'Advanced Topics',
    'crypto': 'Advanced Topics',
    'cipher': 'Advanced Topics',
    'morse': 'Advanced Topics',
}

def get_headers() -> Dict[str, str]:
    """Get headers for GitHub API requests."""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def get_all_repos() -> List[Dict[str, Any]]:
    """Fetch all repositories for the user."""
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f'{GITHUB_API}/users/{OWNER}/repos?per_page={per_page}&page={page}&sort=updated&direction=desc'
        response = requests.get(url, headers=get_headers())
        
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            break
        
        data = response.json()
        if not data:
            break
        
        repos.extend(data)
        page += 1
    
    return repos

def categorize_repo(repo: Dict[str, Any]) -> str:
    """Categorize repository based on name and description."""
    name = repo['name'].lower()
    desc = (repo['description'] or '').lower()
    full_text = f"{name} {desc}"
    
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in full_text:
            return category
    
    return 'Other Projects'

def format_language(language: str) -> str:
    """Format language string."""
    return language if language else 'Other'

def group_repos_by_category(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group repositories by category."""
    categories = {}
    
    for repo in repos:
        category = categorize_repo(repo)
        if category not in categories:
            categories[category] = []
        categories[category].append(repo)
    
    return dict(sorted(categories.items()))

def generate_table(repos: List[Dict[str, Any]]) -> str:
    """Generate markdown table for repositories."""
    lines = [
        "| Название | Описание | Язык |",
        "|----------|---------|------|"
    ]
    
    for repo in sorted(repos, key=lambda r: r['name']):
        name = repo['name']
        url = repo['html_url']
        desc = repo['description'] or '-'
        lang = format_language(repo['language'])
        
        # Clean description
        desc = desc.replace('|', '\\|').replace('\n', ' ')[:100]
        
        lines.append(f"| [{name}]({url}) | {desc} | {lang} |")
    
    return '\n'.join(lines)

def generate_catalog(repos: List[Dict[str, Any]]) -> str:
    """Generate complete catalog markdown."""
    categories = group_repos_by_category(repos)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    catalog = f"""# 📚 Каталог репозиториев ZeFraIL

Последнее обновление: {timestamp}

Всего репозиториев: **{len(repos)}** 🎯

---

"""
    
    for category, category_repos in categories.items():
        catalog += f"## {category}\n\n"
        catalog += generate_table(category_repos)
        catalog += "\n\n---\n\n"
    
    # Add statistics
    languages = {}
    for repo in repos:
        lang = format_language(repo['language'])
        languages[lang] = languages.get(lang, 0) + 1
    
    catalog += "## 📊 Статистика\n\n"
    catalog += f"- **Всего репозиториев**: {len(repos)}\n"
    catalog += f"- **Дата обновления**: {timestamp}\n"
    catalog += "- **Распределение по языкам**:\n"
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        catalog += f"  - {lang}: {count}\n"
    
    catalog += f"\n- **Дата создания каталога**: {datetime.now().isoformat()}\n"
    catalog += "\n💡 **Примечание**: Этот каталог обновляется автоматически каждый день.\n"
    
    return catalog

def main():
    """Main function."""
    print("🚀 Fetching repositories...")
    repos = get_all_repos()
    
    if not repos:
        print("❌ No repositories found!")
        return
    
    print(f"✅ Found {len(repos)} repositories")
    
    print("📝 Generating catalog...")
    catalog = generate_catalog(repos)
    
    output_file = 'REPOSITORIES_CATALOG.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(catalog)
    
    print(f"✅ Catalog saved to {output_file}")

if __name__ == '__main__':
    main()
