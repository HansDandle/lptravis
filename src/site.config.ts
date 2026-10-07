/**
 * Site-wide settings. This is the one file to edit for the things that change
 * most often: where and when the monthly meeting is, who the officers are, and
 * the social/donation links. Nothing here requires touching page templates.
 */

export const site = {
  name: 'Libertarian Party of Travis County',
  shortName: 'LP Travis',
  tagline: 'Liberty in Texas, starting at home.',
  description:
    'The Libertarian Party of Travis County (LP Travis) is the Austin-area affiliate of the Libertarian Party of Texas. Monthly meetings, local candidates, and activism for a freer Travis County.',
  // Change this to 'https://lptravis.org' once the domain points at GitHub Pages.
  url: 'https://hansdandle.github.io/lptravis',
  locale: 'en_US',
};

/** The recurring monthly meeting. Update the venue here if it ever moves. */
export const meeting = {
  cadence: 'Second Monday of every month',
  time: '6:45 – 9:00 PM',
  venue: 'Casa Chapala Mexican Cuisine & Tequila Bar',
  address: '9041 Research Blvd, Austin, TX 78758',
  addressNote: '183 & Burnet Road',
  mapUrl:
    'https://www.google.com/maps/place/Casa+Chapala/@30.3737166,-97.7255182,17z',
  note: 'Free and open to the public. Most meetings feature a guest speaker.',
};

export const links = {
  donate: 'https://www.paypal.com/donate/?hosted_button_id=5CDNHUELJHMNG',
  gear: 'https://tclpgear.company.site/',
  calendar:
    'https://calendar.google.com/calendar/embed?src=lptravistx%40gmail.com&ctz=America%2FChicago',
  calendarPublic:
    'https://calendar.google.com/calendar/u/0/embed?src=lptravistx@gmail.com&ctz=America/Chicago',
  contactForm:
    'https://docs.google.com/forms/d/e/1FAIpQLSfnd2CIY6Sq4Xma1xTxJgPd7lDr1KXgGsZVzpABcCv9SqL80Q/viewform?embedded=true',
  contactFormDirect:
    'https://docs.google.com/forms/d/e/1FAIpQLSfnd2CIY6Sq4Xma1xTxJgPd7lDr1KXgGsZVzpABcCv9SqL80Q/viewform',
  email: 'lptravistx@gmail.com',
  newsletter: 'https://groups.google.com/g/austinliberator',
  meetup: 'https://www.meetup.com/austin-libertarians/',
  facebookPage: 'https://www.facebook.com/lptravistx',
  facebookGroup: 'https://www.facebook.com/groups/TravisCountyLibertarians',
  twitter: 'https://twitter.com/LPTravisTX',
  instagram: 'https://www.instagram.com/lptravistx/',
  lpTexas: 'https://lptexas.org/',
  lpNational: 'https://www.lp.org/',
  platform: 'https://www.lp.org/platform',
  registerToVote: 'https://www.votetexas.gov/register-to-vote/',
};

/** County Executive Committee, as listed on the About page. */
export const officers = [
  { name: 'Dan McCarthy', role: 'Chair', photo: '/images/2023/09/dan-best-headshot.png' },
  { name: 'Ted Brown', role: 'Vice Chair', photo: null },
  { name: 'Lisa Schlinkert', role: 'Secretary', photo: null },
  { name: 'Jonathan Patschke', role: 'Treasurer', photo: null },
  { name: 'Girish Altekar', role: 'At Large', photo: null },
];

export const nav = [
  { label: 'About', href: '/about' },
  { label: 'News', href: '/news' },
  { label: 'Events', href: '/events' },
  { label: 'Get Involved', href: '/get-involved' },
  { label: 'Gear', href: '/gear' },
  { label: 'Contact', href: '/contact' },
];
