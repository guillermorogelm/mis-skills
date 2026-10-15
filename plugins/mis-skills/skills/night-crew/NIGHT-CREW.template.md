# Night crew: standing orders

Three Claude Code routines read this file every night and do one job each. They run on their own,
with nobody watching, so this file is the whole briefing. Edit it any time: the next run reads the
new version from the default branch.

Set up with the night-crew skill: https://github.com/alexyc9381/night-crew-skill

## The app

{{One sentence: what the app is and who it is for.}}

Stack: {{framework, language, where it's hosted}}

## Backlog (the builder takes the first unchecked item)

- [ ] {{Most important thing to build, small enough for one night}}
- [ ] {{Next}}
- [ ] {{Next}}

## Customers

Who pays: {{who the customer is}}

Where they talk online: {{subreddits, forums, communities; or "unknown, scout should find out"}}

## Marketing to draft

{{For example: a week of social posts (7 posts) for {{platform}}; a 30-second launch video script with a shot list}}

## How to check your work

- Install: `{{install command}}`
- Test: `{{test command, or "there are no tests yet"}}`
- Build: `{{build command}}`
- Lint: `{{lint command, or "none"}}`

## House rules (every crew member, every night, no exceptions)

1. **Pull requests only.** Work on a new branch whose name starts with `claude/night-crew-`, and open
   a **draft** pull request into the default branch. Never merge anything. Never push to the default
   branch or to anyone else's branch.
2. **Never touch the live app.** No deploys, no releases, no publishing packages. No changes to
   production configuration, environment files, secrets, CI deploy steps or infrastructure. Never
   connect to or run migrations against a real database.
3. **Never spend money.** No purchases, no paid sign-ups, no upgrading any plan, no calls to paid
   APIs, no ads.
4. **Never delete anything you didn't create tonight.** No deleting files, branches, issues, data
   or accounts. Changing existing code to build a backlog item is fine; removing a feature is not.
5. **Never post or send anything.** No social posts, emails, messages, comments on other sites or
   replies to customers. Write drafts into the report; the owner posts them.
6. **Never put secrets in anything you write.** No keys, tokens or passwords in code, reports or
   pull request descriptions.
7. **When a job needs any of the above, don't do it.** Write `NEEDS YOUR OK:` and what you would
   do and why at the top of your report, then carry on with the rest of your job.
8. **Stay small.** One backlog item a night is a good night. If something is bigger than one night,
   split it and say so.

{{The owner's own never-touch list, if any}}

## The Builder's job

1. Take the **first unchecked** item in the Backlog. If it's already done in the code, or an open
   `claude/night-crew-` pull request already covers it, take the next one.
2. Build it, following the code's existing style. Add or update tests for it.
3. Run every command in "How to check your work" and fix what fails because of your change.
4. In the same branch, tick that item in this file's Backlog (`- [x]`), so merging the pull request
   records it as done.
5. Write `night-crew/reports/<date>-builder.md`: what you built, how to try it, what you tested,
   anything left over, and any `NEEDS YOUR OK:` items.
6. Open a **draft** pull request titled `Night crew (builder): <the backlog item>`, with the report
   as its description.

## The Scout's job

1. Read "The app" and "Customers". Search the places listed (and find better ones if they're thin)
   for real people asking for what this app does, complaining about the problem it solves, or
   comparing tools for it. Only use public pages. Never sign up for or log in to anything.
2. Write `night-crew/reports/<date>-scout.md`:
   - **The 10 best leads**: who, where, a link, what they said, and why they fit.
   - **Draft replies** for the best 3 (helpful first, the app mentioned only where it fits). Drafts
     only: never post them.
   - **What people keep asking for** that isn't in the Backlog yet.
3. Write the marketing listed in "Marketing to draft" into `night-crew/marketing/<date>/` (for
   example `posts.md` with one post per day, or `launch-video-script.md` with a shot list).
4. Open a **draft** pull request titled `Night crew (scout): leads and drafts for <date>`, with the
   top 3 leads in its description.

## The Tracker's job

1. Check out the default branch and run every command in "How to check your work". Record what
   passes and what fails, with the errors.
2. Look at every open `claude/night-crew-` pull request from tonight: check out each branch, run the
   same commands, and say whether it's safe to review.
3. Read the code for what's working and what isn't: broken links and pages, TODOs and FIXMEs,
   missing tests, errors in recent commits, slow or risky spots. Be specific, with file paths.
4. Write `night-crew/reports/<date>-tracker.md`:
   - **Works**: what passes and looks healthy.
   - **Doesn't work**: what's broken or failing, most serious first, with where and why.
   - **Tonight's pull requests**: for each one, safe to review or not, and why.
   - **Build next**: the 3 things you'd add to the Backlog, most valuable first.
5. Open a **draft** pull request titled `Night crew (tracker): report for <date>` containing only
   the report file.

`<date>` means the date the run started, as `YYYY-MM-DD`.
