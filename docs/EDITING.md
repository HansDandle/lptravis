# Editing the LP Travis website

This guide is for party officers and volunteers who keep the site up to date.
You do not need to be a programmer. Nothing here can break the site permanently —
every change is tracked, and anything can be undone.

## How the site works, in one paragraph

The site is a set of text files kept in GitHub. When a file changes, GitHub
automatically rebuilds the site and publishes it, usually within two minutes.
There is no database, no login to maintain, no plugins to update, and no hosting
bill. The tradeoff is that editing happens either through the web editor
described below, or by editing text files directly.

---

## The things you will change most often

### Changing the meeting time, place, or officers

Open **`src/site.config.ts`** on GitHub and click the pencil icon to edit it.
Near the top you will find:

```ts
export const meeting = {
  cadence: 'Second Monday of every month',
  time: '6:45 – 9:00 PM',
  venue: 'Casa Chapala Mexican Cuisine & Tequila Bar',
  address: '9041 Research Blvd, Austin, TX 78758',
  ...
};
```

Change the text between the quote marks, keep the quote marks and the comma,
then scroll down and click **Commit changes**. The meeting details appear on the
homepage, the About page, the Events page, the Contact page, and the footer —
all of them update from this one edit.

The officer list is just below, in `officers`. To add someone:

```ts
{ name: 'Jane Doe', role: 'At Large', photo: null },
```

Use `photo: null` if you have no headshot. If you do, upload it (see below) and
write `photo: '/images/jane-doe.jpg'` instead.

---

## Writing a news post

There are two ways. Both produce exactly the same result.

### Option A — the web editor (easiest)

Once the editor is connected (see *Setting up the web editor* below), go to:

```
https://hansdandle.github.io/lptravis/admin/
```

Sign in with GitHub, click **News & Announcements**, then **New Post**. Fill in
the title, date, a one-sentence summary, and the body. Click **Publish**. The
site rebuilds itself within a couple of minutes.

### Option B — adding the file yourself

1. Go to the `src/content/news` folder on GitHub.
2. Click **Add file → Create new file**.
3. Name it using the date and a short slug, ending in `.md`:
   `2026-03-09-march-meeting.md`
4. Paste this in and edit it:

```markdown
---
title: "March 2026 ~ Guest Speaker Name"
date: 2026-03-09
description: "One or two sentences that show up on the news page and when the link is shared."
image: "/images/2026/03/speaker-photo.jpg"
tags: ["MHHM"]
---

Write the post here in plain text.

Leave a blank line between paragraphs. You can **bold** things with two
asterisks, link like [this](https://example.com), and add an image like this:

![](/images/2026/03/some-picture.jpg)
```

5. Click **Commit changes**.

**The part between the two `---` lines matters.** `title` and `date` are
required. `description`, `image`, and `tags` are optional but make the post look
much better on the news page. Keep the quote marks around the title and
description.

To hide a post without deleting it, add `draft: true` on its own line in that
top section.

---

## Adding images

1. Go to the `public/images` folder on GitHub.
2. Click **Add file → Upload files** and drag your image in.
3. Commit.

Reference it in a post by the path after `public`. An image uploaded to
`public/images/2026/03/photo.jpg` is written as:

```markdown
![](/images/2026/03/photo.jpg)
```

Resize large photos before uploading — anything wider than about 1600 pixels is
larger than the site needs and slows the page down.

---

## Editing an existing page

Pages like the bylaws live in `src/content/pages`. Open the file, click the
pencil icon, edit, and commit.

Some pages — the homepage, About, Events, Get Involved, Contact, and Gear — are
built from templates in `src/pages` rather than Markdown, because they pull in
live data like the meeting details and the latest posts. The wording on those
pages can still be edited directly in the matching `.astro` file; look for the
ordinary sentences between the HTML tags.

---

## Setting up the web editor

The editor at `/admin/` needs permission to write to the repository. This is a
one-time setup:

1. Go to **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**.
2. Name it `LP Travis CMS`. Set the homepage URL to the site's address.
3. Set the authorization callback URL to:
   `https://sveltia-cms-auth.sveltia.workers.dev/callback`
4. Create the app and copy the **Client ID** and **Client Secret**.
5. Follow the Sveltia CMS authentication setup to register those credentials:
   <https://github.com/sveltia/sveltia-cms#readme>

Anyone you want to let edit the site needs write access to the repository, under
**Settings → Collaborators**.

If you would rather not run the editor at all, Option B above works permanently
and needs no setup.

---

## If something goes wrong

**The site did not update.** Check the **Actions** tab in GitHub. A red X means
the build failed — click it to see why. The site stays on the last working
version until the problem is fixed, so a bad edit never takes the site down.

**A build failed after I added a post.** The usual causes are a missing `title`
or `date`, a date that is not in `YYYY-MM-DD` form, or a missing quote mark in
the top section. Compare your file against an existing post.

**I want to undo something.** Open the file's **History** on GitHub, find the
version from before your change, and restore it. Nothing is ever lost.

---

## Who to ask

Technical details about how the site is built are in the
[README](../README.md). The scripts that migrated the site off WordPress are in
`scripts/`, and the original WordPress export is kept in the repository root in
case anything needs to be recovered from it.
