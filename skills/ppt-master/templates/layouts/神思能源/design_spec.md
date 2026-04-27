# 神思能源 - Design Specification

> A light corporate energy template for Jinan Energy Group / Synthesis solution proposals, data governance reports, and enterprise project briefings.

---

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | 神思能源 |
| **Category** | Brand |
| **Use Cases** | Energy group project proposals, gas and heating data governance, digital platform reporting, executive briefings |
| **Design Tone** | Clean, restrained, enterprise-grade, warm energy accents with ample white space |
| **Theme Mode** | Light theme with a pale map background, orange/gold energy accent, and green support accent |
| **Reference Source** | `req/神思能源PPT模板.pptx` |

---

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 x 720 px |
| **viewBox** | `0 0 1280 720` |
| **Page Margins** | Left/Right 80px, Top 90px, Bottom 52px |
| **Safe Area** | x: 80-1200, y: 96-668 |

---

## III. Color Scheme

### Primary Colors

| Role | Color Value | Notes |
| --- | --- | --- |
| **Energy Orange** | `#F26B21` | Main emphasis, chapter numbers, section markers |
| **Warm Gold** | `#B98945` | Secondary brand tone, dividers, TOC connector lines |
| **Leaf Green** | `#58B947` | Support accent for success/progress cues |
| **Deep Ink** | `#221815` | Primary title and body text |
| **Soft Brown** | `#8A6A42` | Secondary text and metadata |
| **Panel White** | `#FFFFFF` | Content surfaces over the pale background |
| **Pale Sand** | `#F7EFE5` | Subtle separators and chip backgrounds |

### Text Colors

| Role | Color Value | Usage |
| --- | --- | --- |
| **Primary Text** | `#221815` | Titles, body text |
| **Secondary Text** | `#6F6255` | Subtitles, notes |
| **Muted Text** | `#9B8E80` | Page numbers, source labels |
| **White Text** | `#FFFFFF` | Text on orange accent blocks |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Microsoft YaHei, SimHei, Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage | Size | Weight |
| --- | --- | --- | --- |
| H1 | Cover main title | 44-52px | Bold |
| H2 | Page title | 30-34px | Bold |
| H3 | Section title | 22-24px | Bold |
| Body | Body text | 16-20px | Regular |
| Meta | Footer, page number, source | 12-14px | Regular |
| Emphasis | Chapter number / large ending text | 56-72px | Bold |

---

## V. Page Structure

### Common Layout

| Area | Position/Size | Description |
| --- | --- | --- |
| **Background** | Full canvas | Uses `nengy_sdses_background.png`; includes pale world-map texture and top-right brand marks |
| **Title Region** | x=80, y=50, w=720 | Compact editable page title with orange accent rule |
| **Content Region** | x=72, y=110, w=1136, h=536 | Expanded flexible space for AI-generated native SVG content |
| **Footer** | y=664 | Small page number and source/copyright line |
| **Brand Area** | x=830-1235, y=28-90 | Reserved for the embedded logo in the background |

---

## VI. Page Types

### 1. Cover Page (`01_cover.svg`)

- Centered main title matching the original reference slide
- Subtitle/date/author arranged below the title
- Orange divider line for brand emphasis
- Keeps background branding visible without extra logo placeholders

### 2. Table of Contents (`02_toc.svg`)

- Large `目录` label on the left-center
- Six indexed TOC rows on the right, following the original deck rhythm
- Uses canonical indexed placeholders: `{{TOC_ITEM_1_TITLE}}` through `{{TOC_ITEM_6_TITLE}}`

### 3. Chapter Page (`02_chapter.svg`)

- Large chapter number with orange emphasis
- Chapter title centered in the visual field
- Minimal metadata line for optional chapter description

### 4. Content Page (`03_content.svg`)

- Left-aligned page title and small orange section marker
- Flexible content area placeholder with a light outline
- Footer page number and optional source field

### 5. Ending Page (`04_ending.svg`)

- Large thank-you message, based on the original ending slide
- Contact information and closing message below
- Uses the same brand background for continuity

---

## VII. Layout Modes (Recommended)

| Mode | Use Case | Layout Guidance |
| --- | --- | --- |
| **Four-Point Analysis** | Status, risks, objectives | 2x2 grid inside the content region; orange numeric labels |
| **Two-Column Standard** | Plan comparison, before/after | Left/right columns with restrained dividers |
| **Timeline / Workload** | Implementation plan | Horizontal timeline using orange milestones and gold connector |
| **Dashboard Summary** | Metrics or governance status | Large numeric indicators with green positive cues |

---

## VIII. Spacing Specification

| Property | Value | Description |
| --- | --- | --- |
| **Base Unit** | 8px | Use multiples of 8 for alignment |
| **Major Section Gap** | 32px | Gap between title and content modules |
| **Module Gap** | 24px | Gap between cards, columns, or grouped items |
| **Inner Padding** | 20-24px | Padding inside content blocks |
| **Card Radius** | 6px | Keep cards subtle and business-like |

---

## IX. SVG Technical Constraints

- All SVG files must use `viewBox="0 0 1280 720"`.
- Use inline SVG attributes only; no `<style>`, CSS classes, scripts, masks, or `foreignObject`.
- Use HEX colors plus `fill-opacity` or `stroke-opacity` for transparency.
- Keep text editable with `<text>` and `<tspan>`.
- Image assets are local to the template package: `nengy_sdses_background.png`.
- Preserve enough clear space in the top-right brand area so the background logo remains unobstructed.

---

## X. Placeholder Specification

| Placeholder | Purpose | Pages |
| --- | --- | --- |
| `{{TITLE}}` | Main title | Cover |
| `{{SUBTITLE}}` | Subtitle | Cover |
| `{{DATE}}` | Date | Cover |
| `{{AUTHOR}}` | Author / organization | Cover |
| `{{CHAPTER_NUM}}` | Chapter number | Chapter |
| `{{CHAPTER_TITLE}}` | Chapter title | Chapter |
| `{{CHAPTER_DESC}}` | Optional chapter description | Chapter |
| `{{PAGE_TITLE}}` | Page title | Content |
| `{{CONTENT_AREA}}` | Flexible generated content region | Content |
| `{{SOURCE}}` | Source note | Content |
| `{{PAGE_NUM}}` | Page number | Content |
| `{{THANK_YOU}}` | Ending message | Ending |
| `{{CLOSING_MESSAGE}}` | Closing subtitle | Ending |
| `{{CONTACT_INFO}}` | Contact information | Ending |
| `{{TOC_ITEM_1_TITLE}}` - `{{TOC_ITEM_6_TITLE}}` | TOC item titles | TOC |
| `{{TOC_ITEM_1_DESC}}` - `{{TOC_ITEM_6_DESC}}` | Optional TOC item descriptions | TOC |

---

## XI. Usage Guide (Recommended)

- Use this template when the source topic concerns energy services, address governance, GIS data, customer-service platforms, or government-enterprise reporting.
- Prefer clean white layouts with sparse orange/gold accents; avoid heavy dark blocks that obscure the pale map background.
- On content pages, keep the title line short and reserve the main region for native shapes, tables, process diagrams, or comparison matrices.
