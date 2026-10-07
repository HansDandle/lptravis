# Editing the LP Travis website

A guide for party officers. You do not need to know how to code, and you cannot
permanently break anything — every change is saved with a history, and any change
can be undone.

- **[Part 1: Writing and editing posts](#part-1-writing-and-editing-posts)** — for everyone
- **[Part 2: Changing meeting details and officers](#part-2-changing-meeting-details-and-officers)** — for everyone
- **[Part 3: One-time setup](#part-3-one-time-setup)** — for whoever administers the site

---

## How the site works

The website is a set of files kept on GitHub. When a file changes, the site
rebuilds and republishes itself automatically, usually within about two minutes.

There is no database, no plugins to update, and no monthly hosting bill. The
tradeoff is that there is no WordPress-style admin panel built into the site
itself — instead you use the editor described below, which is a separate page
that saves your work back to GitHub.

**You need a free GitHub account**, and someone has to add you to the site's
repository as a collaborator. Ask whoever administers the site.

---

# Part 1: Writing and editing posts

## Opening the editor

Go to:

```
https://hansdandle.github.io/lptravis/admin/
```

Click **Sign in with GitHub** and authorize it the first time. You will land on
a dashboard with two sections in the left sidebar:

- **News & Announcements** — meeting announcements, ballot positions, updates
- **Pages** — standing pages like the bylaws

> If sign-in does nothing or shows an error, the editor has not been connected
> yet. See [Part 3](#part-3-one-time-setup).

## Writing a new post

1. Click **News & Announcements** in the sidebar.
2. Click **New Post** (top right).
3. Fill in the fields:

| Field | What to put |
| --- | --- |
| **Title** | The headline. Use normal capitalization, not ALL CAPS. |
| **Date** | The date the post should show. Defaults to today. |
| **Short summary** | One or two sentences. Shows on the news page and when the link is shared on Facebook. Worth writing — it is the first thing people read. |
| **Header image** | Optional. The picture at the top of the post and on the news card. |
| **Tags** | Optional. `MHHM` for monthly meetings, `Elections`, `Conventions`. |
| **Draft** | Leave off to publish. Turn **on** to save without showing it on the site. |
| **Body** | The post itself. |

4. Click **Publish** (or **Save** if Draft is on).

The site updates itself within a couple of minutes. Refresh the news page to see it.

## Writing the body

The body uses a simple formatting toolbar — bold, italic, links, headings,
bullet lists, and images, much like any text editor.

A few things worth knowing:

- **Leave a blank line between paragraphs.** A single line break will not start
  a new paragraph.
- **Links:** select the text, click the link button, paste the address.
- **Headings:** use *Heading 2* for section breaks within a post. Heading 1 is
  reserved for the post title itself.
- **Don't paste directly from Word or Google Docs** — it brings invisible
  formatting that can look wrong on the site. Paste as plain text
  (`Ctrl+Shift+V`), then format inside the editor.

## Adding images

Inside the body, click the image button, then **Upload** and choose a file. It
is saved to the site automatically.

For the **Header image** field, click it and upload the same way.

**Resize large photos before uploading.** Anything wider than about 1600 pixels
is bigger than the site needs and makes the page slow to load on phones. Most
phone photos are much larger than this.

## Editing or deleting a post

Click **News & Announcements**, click the post, make your changes, click
**Publish** again.

To take a post down without deleting it, turn **Draft** on and publish. It
disappears from the site but stays in the editor. To delete permanently, use
**Delete entry** at the bottom.

## Adding a page

Pages are for standing information that is not news — a volunteer handbook,
a candidate questionnaire, convention rules. Click **Pages** in the sidebar,
then **New Page**.

**What happens when you publish one:**

- It gets its own web address, based on the title. A page called
  *Volunteer Handbook* becomes `/volunteer-handbook`.
- It is listed automatically on the **[Archive](https://hansdandle.github.io/lptravis/archive)** page.
- It does **not** appear in the menu at the top of the site. That menu is
  deliberately short, and adding to it is a separate step (below).

So a new page is live and linkable immediately — you can paste its address into
an email or a Facebook post — but people browsing the site will not stumble on
it unless you link to it.

**Linking to a new page** is usually what you actually want. Edit a post or
another page, select some text, and link it to the new page's address.

**Adding it to the top menu** requires editing `src/site.config.ts`, in the
`nav` section:

```ts
export const nav = [
  { label: 'About', href: '/about' },
  { label: 'News', href: '/news' },
  ...
];
```

Copy a line, paste it in the position you want, and change the label and href.
Keep the menu short — more than about seven items and it stops working well on
phones.

**The Archived checkbox** keeps a page online but marks it as old. Archived
pages show a note at the top saying they are kept for the historical record,
and are listed separately on the Archive page. Use it for things like past
candidate slates rather than deleting them.

## What the different buttons mean

- **Publish** — saves and puts it on the live site
- **Save** — saves your work while Draft is on; nothing appears publicly
- **Delete entry** — removes it

---

# Part 2: Changing meeting details and officers

These live in a settings file rather than the editor, because they appear in
several places across the site at once.

Changing the venue in this one file updates the homepage, the About page, the
Events page, the Contact page, and the footer — all five.

## How to edit it

1. Go to <https://github.com/HansDandle/lptravis>
2. Open the `src` folder, then click **`site.config.ts`**
3. Click the **pencil icon** (top right) to edit
4. Make your change
5. Scroll down, click **Commit changes**

## The meeting

```ts
export const meeting = {
  cadence: 'Second Monday of every month',
  time: '6:45 – 9:00 PM',
  venue: 'Casa Chapala Mexican Cuisine & Tequila Bar',
  address: '9041 Research Blvd, Austin, TX 78758',
```

Change the words **between the quote marks**. Keep the quote marks and the
comma at the end of the line.

## The officers

```ts
export const officers = [
  { name: 'Austin Whaley', role: 'Chair' },
  { name: 'Ted Brown', role: 'Vice Chair' },
```

To change someone, edit the name or role between the quotes. To add someone,
copy an existing line and paste it below, then edit it.

## The committee photo

```ts
export const officersPhoto = {
  src: '/images/2026/officers2026-28.jpg',
  alt: 'The 2026 LP Travis County Executive Committee...',
  order: ['Girish Altekar', 'Lisa Schlinkert', 'Austin Whaley', 'Ted Brown', 'Bill Kelsey'],
};
```

`order` is the people **left to right as they appear in the photo**, which is
what the caption underneath the picture says. It is deliberately separate from
the officer list above, which is in order of office.

**When you replace the photo:** upload the new image, change `src` to its path,
and update `order` to match the new photo. If you change the photo without
changing `order`, the caption will name people in the wrong position.

## Links

The `links` section holds the donate link, the gear store, the newsletter, and
social media. Same rule — edit between the quote marks.

---

# Part 3: One-time setup

> This section is for whoever administers the site. **The editor will not work
> until these steps are done.** Officers can still edit files directly on GitHub
> in the meantime, which needs no setup.

## Step 1 — Create a GitHub OAuth app

1. Go to **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**
   (<https://github.com/settings/developers>)
2. Fill in:
   - **Application name:** `LP Travis CMS`
   - **Homepage URL:** `https://hansdandle.github.io/lptravis/`
   - **Authorization callback URL:** `https://sveltia-cms-auth.sveltia.workers.dev/callback`
3. Click **Register application**
4. Copy the **Client ID**, then click **Generate a new client secret** and copy that too

## Step 2 — Connect the auth service

The config at `public/admin/config.yml` currently points at Sveltia's shared
authentication relay. To use it you must register the credentials from Step 1
with that service, following the current instructions at:

<https://github.com/sveltia/sveltia-cms#readme>

Sveltia also supports running your own authentication worker on Cloudflare
(free), which avoids depending on a shared service. The same README covers it,
and the party already has a Cloudflare account.

If the callback URL changes because you self-host, update `base_url` in
`public/admin/config.yml` to match.

## Step 3 — Give officers access

Each officer needs:

1. A free GitHub account
2. To be added at **Settings → Collaborators → Add people** on the repository,
   with **Write** access

Currently the only person with access is `HansDandle`.

## Verifying it works

Open `/admin/`, sign in with GitHub, and create a test post with Draft turned
on. If it saves, everything is connected. Delete the test post afterward.

---

# If something goes wrong

**The site did not update.** Check the **Actions** tab on GitHub. A green check
means it published. A red X means the build failed — click it to see why. The
site stays on the last working version until it is fixed, so a bad change never
takes the site down.

**My post is not showing.** Check whether **Draft** is still on. Also check the
date — a post dated in the future still appears, but at the top or bottom of the
list depending on the date.

**I want to undo something.** On GitHub, open the file, click **History**, find
the version from before the change, and restore it. Nothing is ever truly lost.

**The editor will not sign in.** Either the setup in Part 3 is not finished, or
your GitHub account has not been added as a collaborator.

**I edited `site.config.ts` and the site broke.** Almost always a missing quote
mark, comma, or curly brace. Open the file's **History** on GitHub and restore
the previous version, then try again more carefully.

---

# Editing without the editor

Everything in Part 1 can also be done directly on GitHub, which needs no setup
at all. To add a post:

1. Go to the `src/content/news` folder on GitHub
2. Click **Add file → Create new file**
3. Name it with the date and a short slug ending in `.md`, for example
   `2026-03-09-march-meeting.md`
4. Paste this and edit it:

```markdown
---
title: "March 2026 ~ Guest Speaker Name"
date: 2026-03-09
description: "One or two sentences for the news page and link previews."
tags: ["MHHM"]
---

Write the post here.

Leave a blank line between paragraphs. Use **bold** with two asterisks,
links like [this](https://example.com), and images like this:

![](/images/2026/03/photo.jpg)
```

5. Click **Commit changes**

The part between the two `---` lines is required: `title` and `date` must be
there, and the quote marks matter. Everything after it is the post.

---

Technical documentation about how the site is built is in the
[README](../README.md).
