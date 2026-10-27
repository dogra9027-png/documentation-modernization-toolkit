# Migration and Authoring Standards

## Conversion rules
- Preserve the page title and meaningful heading hierarchy.
- Convert common paragraphs, ordered/unordered lists, emphasis, links, and images.
- Keep source filenames traceable through stable, readable slugs.
- Do not silently discard content that the converter does not support; review source and output.

## Metadata
Every knowledge article must include `title`, `slug`, `content_type`, `audience`, `tags`, and `review_date`.

## Chatbot knowledge quality
- Put one clear task or question in each article.
- State prerequisites before procedural steps.
- Use explicit action verbs and numbered steps for procedures.
- Include expected results and troubleshooting where relevant.
- Avoid relying on “above”, “below”, or visual layout alone for meaning.
- Keep each article understandable when retrieved independently.

## Review checklist
- [ ] Compare source and converted output.
- [ ] Verify all local links and image paths.
- [ ] Confirm metadata and tags.
- [ ] Check headings, lists, and code examples.
- [ ] Test instructions with a representative user task.
- [ ] Record reviewer and review date.
