# Examples

One worked example, start to finish. Then acceptance-criteria pairs.

---

# Part 1. The brief as it arrived

> "We need a billing page so customers can see their invoices. Nothing fancy.
> Next sprint would be great."

Twenty-two words. Classified: **thin**. No user named, no boundary, no date, no
failure behaviour. Run the full interview.

Notice what a generic PRD generator would do with this brief. It would produce
four pages about invoice management, a search bar, filters, a CSV export, and a
payment flow. Every one of those is an invention. Three of them turn out to be
wrong.

---

# Part 2. The interview

## Round 1. The thing and the person

**Q1. Finish this sentence: "A [who] can [verb] [what], so that [outcome]." One sentence, no "and".**

> "A customer can see their invoices so they stop emailing support about them."

**Q2. Who is the user? Name a role. How many are there?**

> "Customers."

Too wide. One retry, with concrete options.

**Which customers? Everyone on the account, or the person who pays?**

> "The account owner. About 1,200 of them. Team members must not see billing at
> all."

That last clause is a requirement nobody would have guessed. It came out of a
question about who, not a question about permissions.

**Q3. What do they do today instead?**

> "They email support. Support opens Stripe, screenshots the invoice, sends it
> back. Around 30 emails a week, ten minutes each."

**Q4. What happens in the minute before they open this, and the minute after?**

> "Before: they got a card decline email, or their finance person asked for a
> receipt. After: they forward the PDF to their finance person."

The whole shape of the build changed on that answer. The job is not "see". The
job is "get a PDF I can forward". A viewer with no download link would have
passed every criterion the original brief implies and solved nothing.

## Round 2. The boundary

**Q5. Name three things a reasonable person would expect this to do, that it will not do.**

> "Use your judgement on that one."

This is the moment. Do not go quiet and generate. Make the calls, say what they
rule out, read them back in the same message.

**Assuming three non-goals. No changing the card on file. No cancelling the
plan. No seat changes. All three stay in the Stripe portal. Say now if any of
those is wrong.**

> "Changing the card is wrong. That is the number one support email. But it can
> be a link out to the Stripe portal, not a form we build."

One assumption, read back, corrected in fifteen seconds. Buried instead in a
generated document, that same assumption surfaces in week three as rework and an
argument about who said what.

**Q6. If the deadline moves in, what goes first?**

> "The search box. Twelve invoices in a list is enough if it comes to that."

**Q7. What must not change or break?**

> "The Stripe webhook handler. Do not touch it."

## Round 3. The evidence

**Q8. When it is finished, what do you look at to check?**

> "I log in as a test account and download an invoice PDF that actually opens."

**Q9. What is the smallest version you would still put in front of a real user?**

> "A list with dates, amounts, paid or unpaid, and a PDF link that works."

**Q10. On day one: how many users, how many rows?**

> "1,200 accounts. The oldest has about 40 invoices. Nobody is over 60."

Sixty rows maximum. No pagination. No virtual list. No index tuning. That answer
deleted three days of work that a guessed number would have added.

## Round 4. The edges

**Q11. What does the user see when the network drops or the list is empty?**

> "It should fail gracefully."

Vague. One retry, two concrete readings.

**When Stripe is unreachable, do you want the last synced list with a stale
notice, or an empty page with a retry button?**

> "The cached list with a notice. They mostly want old invoices anyway."

**Q12. What is off limits?**

> "Never show a full card number. We only hold the last four. And never an
> invoice from another account."

**Q13. Who else has to say yes?**

> "Me, and Priya has to read the copy."

**Q14. What is the deadline, and what is it attached to?**

> "24 September. That is when we turn off the old support macro."

## Round 5. The disagreement

**Q15. Name one decision inside this that you and I could reasonably decide differently.**

> "I do not know."

So name one. There is always one.

**The PDF. Either the row links straight to the Stripe hosted invoice URL, which
is an hour of work and sends the customer to a Stripe page, or we proxy the PDF
through our own domain, which keeps them on our site and costs a day. Which
one?**

> "Link to Stripe. I did not realise that was a choice."

That is the interview paying for itself. Two people were about to build two
different things, and neither of them knew it.

## Size check

Signals counted: summary has no "and" joining two verbs. One user. One data
source. Thirteen criteria. One deadline. Cut the smallest version and most
criteria go with it.

Zero signals. One project. Write it.

---

# Part 3. The spec that came out

```markdown
# Customer invoice page

**One sentence.** An account owner can see and download their invoices, so they
stop emailing support for a receipt.
**Owner.** Dan Whitaker
**Date.** 2026-09-02
**Status.** AGREED
**Path.** docs/spec-invoice-page.md

## 1. Who it is for

**Role.** Account owner. Not team members.
**How many.** 1,200 on day one.
**Where they are.** Laptop, usually chasing a receipt for their finance person.
**What they already have.** A login. No billing screen of any kind today.

## 2. Today, without this

The customer emails support. Support opens Stripe, screenshots the invoice, and
replies with the image. Around 30 emails a week, roughly ten minutes each. The
customer then asks for a real PDF, because a screenshot is not a receipt.

## 3. Must do

1. List this account's invoices, newest first.
2. Show the date, the amount, and whether it is paid.
3. Give a working PDF for each invoice.
4. Search invoices by number or amount.
5. Link out to the Stripe portal to change the card on file.
6. Hide the page from team members.

## 4. Non-goals

- No payments. Paying still happens through the Stripe email link.
- No card form. Section 3.5 is a link to the Stripe portal, not a form we own.
- No plan changes and no seat changes. Both stay in the Stripe portal.
- No CSV or bulk export. One PDF at a time.
- No invoice preview in the page. The PDF is the artefact people forward.

## 5. Assumed decisions

- `ASSUMED 2026-09-02` Invoices are read from the existing Stripe sync table,
  not the live API. Rules out invoices created in the last five minutes.
- `ASSUMED 2026-09-02` The PDF link points at the Stripe hosted invoice URL.
  Rules out serving the file from our own domain.

## 6. Open questions

1. Does the page appear in the main nav or only under Settings? Asked of: Priya.
   Waiting on it: nothing. Default is Settings.

## 7. Constraints

**Deadline.** 2026-09-24, because the old support macro is switched off that day.
**Must use.** The existing Stripe sync table.
**Must not touch.** The Stripe webhook handler.
**People.** One engineer, two weeks.
**Legal or policy.** Card numbers never rendered beyond the last four digits.

## 8. Failure and empty states

| Situation | What the user sees |
| --- | --- |
| No invoices yet | "No invoices yet. Your first one arrives after your first payment." |
| Loading | Five grey placeholder rows. No spinner. |
| Stripe sync stale over 24h | The cached list, plus "Last updated [time]. Some recent invoices may be missing." |
| Search matches nothing | "No invoice matches that." The list stays on screen. |
| Team member opens the URL | 404 page. Not a permission message. |

## 9. Acceptance criteria

| # | Criterion | Where to check | Pass |
| --- | --- | --- | --- |
| AC-1 | The page lists every invoice on the signed-in account, newest first. | /settings/billing, test account with 40 invoices | [ ] |
| AC-2 | Each row shows the invoice date, the amount with currency symbol, and the word Paid or Unpaid. | Same page | [ ] |
| AC-3 | Clicking the PDF link on any row opens a PDF that renders in Chrome and Preview. | Any row, downloaded file | [ ] |
| AC-4 | Typing an invoice number in the search box narrows the list to that one row. | Search box | [ ] |
| AC-5 | Typing an amount such as 49.00 narrows the list to invoices at that amount. | Search box | [ ] |
| AC-6 | A signed-in team member who opens /settings/billing gets a 404 page. | Team member test account | [ ] |
| AC-7 | The account owner cannot load another account's invoice by changing the id in the URL. Response is 404. | /settings/billing/inv_[other account id] | [ ] |
| AC-8 | With 60 invoices, the list finishes painting in under 1s on a Fast 3G throttle. | Network panel | [ ] |
| AC-9 | With no invoices, the page shows "No invoices yet. Your first one arrives after your first payment." | Fresh test account | [ ] |
| AC-10 | With the sync table older than 24h, the page shows the cached list plus "Last updated [time]. Some recent invoices may be missing." | Sync paused for 25h | [ ] |
| AC-11 | The page contains no payment form and no card input field. | View source, search for "input" | [ ] |
| AC-12 | The "Update card" button opens the Stripe portal in a new tab. | Click it | [ ] |
| AC-13 | No card digits beyond the last four appear anywhere in the page HTML or the network responses. | View source, Network panel | [ ] |

## 10. Data and scale

**Source.** The existing stripe_invoices sync table. Owned by the billing team.
**Freshness.** Within 15 minutes in normal operation.
**Day one.** 1,200 accounts, 60 invoices at most per account.
**In a year.** 3,000 accounts, 100 invoices at most.
**Personal data.** Billing address on the invoice PDF. Held by Stripe, not by us.

## 11. Cut list

1. Search by amount (AC-5).
2. Search entirely (AC-4 and AC-5).
3. The stale-sync notice (AC-10). Show the cached list with no notice.

## 12. Change log

| Date | Request | Verdict | Cost |
| --- | --- | --- | --- |
| 2026-09-11 | Filter invoices by year | NEXT | +2 criteria, +1.5 days |

## 13. Sign-off

Anything not in this document is not in this build.

- Dan Whitaker, 2026-09-02
- Priya Shah, 2026-09-03
```

Thirteen criteria. Four of them (AC-6, AC-7, AC-11, AC-13) exist because of a
non-goal or an off-limits answer, not because of a feature request. Those are
the ones that catch the quiet mistakes.

---

# Part 4. Week two, when the scope arrived

Day nine. Dan sends a message.

> "Small one. Can we add a filter by year? Finance people always want last year."

Classify it out loud. Not in the spec, not a defect against a criterion.
Therefore new. It goes to the log before anything else happens.

The reply:

> Logged. Filter by year is new scope. It adds two criteria, one for the filter
> and one for the empty result inside a filtered year, and about a day and a
> half including the test data. Three options.
>
> IN: it goes in and 24 September becomes 26 September.
> NEXT: logged, shipped after the deadline.
> TRADE: it goes in and search by amount (AC-5, already first on the cut list)
> comes out. Same date.
>
> Which one?

> "NEXT. The date matters more."

One row in the change log. No silent absorption, no quiet slip, and no argument
at the end about why it took longer, because there is no "longer".

The word "small" appeared in the request and nowhere in the answer. Cost gets
stated in criteria and days.

---

# Part 5. Vague versus falsifiable

Four more pairs. The test on every one: two people read the line, look at the
same finished build, and cannot disagree about the verdict.

**1. Sign-up**

Vague: "Sign-up should be smooth and not lose people."

Falsifiable: "A new user reaches the dashboard from the sign-up form in three
fields and one click. Submitting with an email already in the database shows
'That email is already registered. Sign in instead.' next to the email field and
keeps the password field filled."

What changed: a count of fields, a count of clicks, one exact string, and the
behaviour of the field that would otherwise be silently cleared.

**2. Import**

Vague: "The importer handles messy CSVs."

Falsifiable: "Importing a 10,000-row CSV with three malformed rows loads 9,997
rows and writes the three rejected rows, with their line numbers, to a file the
user can download from the results screen. No import is partially applied: on a
failure the table row count is unchanged."

What changed: "handles" was doing all the work and meant nothing. Now the
rejected rows have somewhere to go, and the transaction behaviour is stated.

**3. Permissions**

Vague: "Only the right people can see the admin area."

Falsifiable: "A user without the admin role who requests /admin gets a 404, not
a 403. The string 'admin' does not appear in the nav HTML for that user. This
holds for direct URL entry as well as in-app navigation."

What changed: "the right people" named a role, and the 404-versus-403 choice
became explicit instead of being made by whoever wrote the middleware.

**4. Notifications**

Vague: "Users get notified of important changes in a timely way."

Falsifiable: "When a document a user follows is edited, that user receives one
email within five minutes. Ten edits inside one hour produce one email, not ten.
The email subject is 'Changes to [document title]' and the body links to the
document."

What changed: "timely" became five minutes, "important" became a defined event,
and the batching rule was written down instead of being discovered in production
by a user who got ten emails.

---

# What the pairs have in common

The falsifiable version is longer every time. That is the trade. Every extra
clause is a decision that would otherwise get made silently, by whoever happened
to write that line of code, on the day they wrote it.

The vague version is not shorter. It is unfinished.
