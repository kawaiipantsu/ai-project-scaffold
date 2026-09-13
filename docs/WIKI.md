# Wiki maintenance

The maintained wiki is a separate Git repository:
`https://github.com/kawaiipantsu/ai-project-scaffold.wiki.git`.

```sh
git clone https://github.com/kawaiipantsu/ai-project-scaffold.wiki.git
cd ai-project-scaffold.wiki
# Edit pages and graphics; review changes for sensitive information.
git add Home.md
 git commit -m 'docs: explain the updated workflow'
git push
```

Keep focused commits and use the existing global identity. Add pages to `_Sidebar.md`.
Use relative wiki links, accessible descriptions for images, and diagrams that explain
real behavior. Keep screenshots free of account data and secrets. Source graphics
are stored in the wiki `assets/` folder. The main repository PR protections do not
apply to the separate wiki repository; its edits must be reviewed before pushing.
