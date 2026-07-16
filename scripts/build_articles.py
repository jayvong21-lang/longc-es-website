#!/usr/bin/env python3
"""
龙溪企服 LongC-ES 文章静态生成系统
读取 /root/geo_articles/ 下的 .md 文件 → 转HTML → 输出到 /root/longc-es-website/articles/
自动更新 sitemap.xml
每页含：独立title、description、schema(Article+LocalBusiness+FAQPage)、canonical
"""

import os
import re
import json
import html as html_module
from datetime import datetime

SITE_URL = "https://www.longc-es.com"
ARTICLES_DIR = "/root/longc-es-website/articles"
SOURCE_DIR = "/root/geo_articles"
DATA_DIR = "/root/longc-es-website/data"
SITEMAP_PATH = "/root/longc-es-website/sitemap.xml"
CSS_VERSION = "20260626-articles"

# 确保目录存在
for d in [ARTICLES_DIR, DATA_DIR]:
    os.makedirs(d, exist_ok=True)


def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown file."""
    fm = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            for line in fm_text.split("\n"):
                line = line.strip()
                if ":" in line:
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip().strip("'").strip('"')
                    fm[key] = value
    return fm, body


def markdown_to_html(md_text):
    """Simple markdown to HTML converter for our article format."""
    html_lines = []
    in_table = False
    in_list = False
    table_lines = []

    for line in md_text.split("\n"):
        # Skip empty lines between sections
        stripped = line.strip()

        # Headers
        if stripped.startswith("###### "):
            html_lines.append(f"<h6>{escaped(stripped[7:])}</h6>")
        elif stripped.startswith("##### "):
            html_lines.append(f"<h5>{escaped(stripped[6:])}</h5>")
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4>{escaped(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{escaped(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{escaped(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{escaped(stripped[2:])}</h1>")

        # Blockquote
        elif stripped.startswith("> "):
            content = stripped[2:]
            # Handle bold in blockquote
            content = inline_format(content)
            html_lines.append(f'<blockquote><p>{content}</p></blockquote>')

        # Table
        elif "|" in stripped and stripped.startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(stripped)
        else:
            if in_table and not stripped.startswith("|"):
                # End of table, render it
                html_lines.append(render_table(table_lines))
                in_table = False
                table_lines = []

            # List items
            if stripped.startswith("- ") or stripped.startswith("* "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                content = inline_format(stripped[2:])
                html_lines.append(f"<li>{content}</li>")
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False

                # Regular paragraph
                if stripped and not stripped.startswith("|"):
                    content = inline_format(stripped)
                    html_lines.append(f"<p>{content}</p>")
                elif not stripped:
                    # Check if previous was paragraph - we might need spacing
                    pass

    # Close any open tags
    if in_table:
        html_lines.append(render_table(table_lines))
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def escaped(text):
    """HTML escape text."""
    return html_module.escape(text)


def inline_format(text):
    """Process inline formatting: bold, links."""
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:inherit;text-decoration:underline">\1</a>', text)
    return text


def render_table(rows):
    """Render markdown table to HTML."""
    if not rows:
        return ""
    # Remove header separator row (|---|)
    header = None
    body_rows = []
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if i == 0:
            header = cells
        elif re.match(r'^[\s\|:\-]+$', row):
            continue  # Skip separator
        else:
            body_rows.append(cells)

    html = '<div class="article-table-wrapper"><table class="article-table">\n'
    if header:
        html += "  <thead><tr>\n"
        for h in header:
            html += f"    <th>{escaped(h)}</th>\n"
        html += "  </tr></thead>\n"
    if body_rows:
        html += "  <tbody>\n"
        for row in body_rows:
            html += "    <tr>\n"
            for cell in row:
                html += f"      <td>{escaped(cell)}</td>\n"
            html += "    </tr>\n"
        html += "  </tbody>\n"
    html += "</table></div>\n"
    return html


def generate_html(article, body_html):
    """Generate complete HTML page for an article."""
    title = article.get("title", "区域专题")
    slug = article.get("slug", "")
    region = article.get("region", "")
    description = article.get("description", "")
    keywords = article.get("keywords", "")
    image = article.get("image", "/images/hero-bg.png")
    date = article.get("date", "2026-06-26")

    canonical = f"{SITE_URL}/articles/{slug}.html"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped(title)} | 龙溪企服 LongC-ES</title>
    <meta name="description" content="{escaped(description)}">
    <meta name="keywords" content="{escaped(keywords)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escaped(title)} | 龙溪企服 LongC-ES">
    <meta property="og:description" content="{escaped(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_URL}{image}">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="zh_CN">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{escaped(title)}",
        "description": "{escaped(description)}",
        "image": "{SITE_URL}{image}",
        "datePublished": "{date}",
        "dateModified": "{date}",
        "author": {{
            "@type": "Organization",
            "name": "厦门龙溪传芳企业服务有限公司"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "厦门龙溪传芳企业服务有限公司",
            "logo": {{
                "@type": "ImageObject",
                "url": "{SITE_URL}/images/hero-bg.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{canonical}"
        }},
        "about": {{
            "@type": "Thing",
            "name": "厦门{region}创业办公指南"
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "厦门龙溪传芳企业服务有限公司",
        "alternateName": "龙溪企服",
        "url": "{SITE_URL}/",
        "telephone": ["18016526868", "17750587110"],
        "email": "2029736860@qq.com",
        "description": "龙溪企服专业提供写字楼商业体招商运营、财务代理记账、工商注册等企业服务",
        "address": {{
            "@type": "PostalAddress",
            "streetAddress": "厦门市同安区西洲路1299号龙溪商务中心",
            "addressLocality": "厦门市",
            "addressRegion": "福建省",
            "addressCountry": "CN"
        }},
        "areaServed": {{
            "@type": "City",
            "name": "厦门"
        }},
        "priceRange": "¥¥"
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "厦门{region}租办公室多少钱一平米？",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "厦门{region}办公室租金因类型和位置而异。具体行情请参考页面内的租金表格，建议联系龙溪企服获取最新实时报价。"
                }}
            }},
            {{
                "@type": "Question",
                "name": "厦门{region}有哪些创业政策支持？",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "厦门{region}为入驻企业提供包括租金补贴、税收优惠、人才补贴等多项政策支持，具体补贴标准和申请条件请咨询龙溪企服。"
                }}
            }},
            {{
                "@type": "Question",
                "name": "在厦门{region}找办公室通过龙溪企服有什么优势？",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "龙溪企服深耕厦门，熟悉{region}各写字楼、产业园和厂房资源，可提供免费带看、商务谈判协助、合同审阅、政策对接、注册地址和代理记账等一站式服务。"
                }}
            }}
        ]
    }}
    </script>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">
                <a href="../index.html">
                    <span class="logo-cn">龙溪企服</span>
                    <span class="logo-en">LongC-ES</span>
                </a>
            </div>
            <ul class="nav-menu">
                <li><a href="../index.html">首页</a></li>
                <li><a href="../about.html">关于我们</a></li>
                <li><a href="../services.html">企业服务</a></li>
                <li><a href="../investment.html">招商合作</a></li>
                <li class="nav-dropdown">
                    <a href="#" class="dropdown-toggle">区域专题 <span class="dropdown-arrow">▾</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="../articles/tongan.html">同安区</a></li>
                        <li><a href="../articles/xiangan.html">翔安区</a></li>
                        <li><a href="../articles/huli.html">湖里区</a></li>
                        <li><a href="../articles/siming.html">思明区</a></li>
                        <li><a href="../articles/jimei.html">集美区</a></li>
                    </ul>
                </li>
                <li><a href="../news.html">资讯中心</a></li>
                <li><a href="../properties.html">合作项目</a></li>
                <li><a href="../contact.html">联系我们</a></li>
            </ul>
            <div class="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- 页面标题 -->
    <section class="page-header">
        <div class="container">
            <h1>{escaped(title)}</h1>
            <p class="breadcrumb"><a href="../index.html">首页</a> / <a href="../index.html">区域专题</a> / {region}</p>
        </div>
    </section>

    <!-- 文章内容 -->
    <section class="article-section">
        <div class="container">
            <article class="article-content">
                {body_html}
            </article>
        </div>
    </section>

    <!-- 联系我们 CTA -->
    <section class="cta-section">
        <div class="container">
            <div class="cta-content">
                <h2>在厦门{region}寻找办公室或厂房？</h2>
                <p>龙溪企服深耕厦门，熟悉{region}各写字楼、产业园和厂房资源，免费提供带看、谈判协助和政策对接服务</p>
                <div class="cta-contact">
                    <div class="cta-item">
                        <span class="cta-label">电话</span>
                        <span class="cta-value">黄 18016526868 / 李 17750587110</span>
                    </div>
                    <div class="cta-item">
                        <span class="cta-label">地址</span>
                        <span class="cta-value">厦门市同安区龙溪商务中心</span>
                    </div>
                </div>
                <a href="../contact.html" class="btn btn-primary btn-large">立即咨询</a>
            </div>
        </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="footer-logo">
                        <span class="logo-cn">龙溪企服</span>
                        <span class="logo-en">LongC-ES</span>
                    </div>
                    <p class="footer-desc">厦门龙溪传芳企业服务有限公司，专业提供写字楼商业体招商运营、财务代理记账、工商注册等企业服务。</p>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="../index.html">首页</a></li>
                        <li><a href="../about.html">关于我们</a></li>
                        <li><a href="../investment.html">招商运营</a></li>
                        <li><a href="../services.html">企业服务</a></li>
                        <li><a href="../news.html">资讯中心</a></li>
                        <li><a href="../enterprises.html">入驻企业</a></li>
                        <li><a href="../contact.html">联系我们</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>联系方式</h4>
                    <ul>
                        <li>
                            <span class="contact-icon">📍</span>
                            <span>厦门市同安区龙溪商务中心</span>
                        </li>
                        <li>
                            <span class="contact-icon">📞</span>
                            <span>黄 18016526868 / 李 17750587110</span>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 厦门龙溪传芳企业服务有限公司 版权所有 | 龙溪企服 LongC-ES</p>
                <p style="font-size:12px;color:#94a3b8;margin-top:4px"><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer" style="color:#94a3b8;text-decoration:none">闽ICP备2026020749号</a> &nbsp;|&nbsp; <a href="https://beian.mps.gov.cn/#/query/webSearch?code=35021202000945" rel="noreferrer" target="_blank" style="color:#94a3b8;text-decoration:none">闽公网安备35021202000945号</a></p>
            </div>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>
"""
    return html


def update_sitemap(new_urls):
    """Update sitemap.xml with new article URLs."""
    sitemap_path = SITEMAP_PATH

    # Read existing sitemap
    existing_urls = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract existing loc entries
        existing_urls = re.findall(r'<loc>(.*?)</loc>', content)

    # Add new URLs that don't already exist
    for url in new_urls:
        if url not in existing_urls:
            existing_urls.append(url)

    # Generate sitemap XML
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for url in existing_urls:
        priority = "0.6"
        changefreq = "monthly"
        if url == f"{SITE_URL}/":
            priority = "1.0"
            changefreq = "weekly"
        elif "/articles/" in url:
            priority = "0.6"
            changefreq = "monthly"

        xml_parts.append(f"""  <url>
    <loc>{url}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    xml_parts.append("</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_parts) + "\n")

    print(f"✅ Sitemap updated: {sitemap_path}")
    print(f"   Total URLs: {len(existing_urls)}")


def build():
    """Main build function."""
    print("=" * 60)
    print("龙溪企服 LongC-ES 文章静态生成系统")
    print("=" * 60)

    # Load articles index
    articles_path = os.path.join(DATA_DIR, "articles.json")
    if os.path.exists(articles_path):
        with open(articles_path, "r", encoding="utf-8") as f:
            articles = json.load(f)
    else:
        articles = []

    print(f"\n📚 Articles in index: {len(articles)}")

    # Process each article
    generated_files = []
    new_sitemap_urls = []

    for article in articles:
        source = article.get("source", "")
        slug = article.get("slug", "")

        if not os.path.exists(source):
            print(f"⚠️  Source not found: {source}")
            continue

        # Read markdown file
        with open(source, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Parse frontmatter and body
        fm, body = parse_frontmatter(md_content)

        # Convert markdown to HTML
        body_html = markdown_to_html(body)

        # Merge article data with frontmatter (article JSON takes precedence)
        article_data = {**fm, **article}

        # Generate full HTML
        full_html = generate_html(article_data, body_html)

        # Write output file
        output_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)

        generated_files.append(output_path)
        new_sitemap_urls.append(f"{SITE_URL}/articles/{slug}.html")

        print(f"✅ Generated: articles/{slug}.html ← {os.path.basename(source)}")

    print(f"\n📄 Total pages generated: {len(generated_files)}")

    # Update sitemap
    update_sitemap(new_sitemap_urls)

    print("\n🎉 Build complete!")
    return generated_files


if __name__ == "__main__":
    build()
