export const SITE = {
  name: 'Vireault',
  tagline: 'Private encrypted vault for Android',
  description:
    'Encrypt photos, videos and files on your Android phone. No account. Offline and local only. Argon2id + AES-256-GCM.',
  // Full public origin + base path, derived from astro.config (SITE_URL / BASE_PATH).
  domain: (import.meta.env.SITE as string).replace(/\/$/, '') + import.meta.env.BASE_URL.replace(/\/$/, ''),
  privacyUrl: '/privacy.html',
  packageId: 'com.vireault.app',
  supportEmail: 'chumiapp.support@gmail.com',
  playBase:
    'https://play.google.com/store/apps/details?id=com.vireault.app&utm_source=web&utm_medium=guide&utm_campaign=',
} as const;

export function playUrl(pageSlug: string): string {
  return `${SITE.playBase}${encodeURIComponent(pageSlug)}`;
}

export const PRICING = {
  free: { vaults: 1, items: 50 },
  weekly: '$1.99/week',
  annual: '$19.99/year',
  annualTrial: '3-day free trial',
  lifetime: '$29.99',
} as const;

export const NAV = [
  { href: '/features', label: 'Features' },
  { href: '/pricing', label: 'Pricing' },
  { href: '/guides', label: 'Guides' },
  { href: '/compare', label: 'Compare' },
  { href: '/faq', label: 'FAQ' },
  { href: '/about', label: 'About' },
] as const;

export const FEATURES = [
  {
    slug: 'encryption',
    title: 'AES-256 encryption on device',
    short: 'Argon2id key derivation, AES-256-GCM, random master key, encrypted index with hidden file names.',
    href: '/features/encryption',
  },
  {
    slug: 'offline',
    title: 'Offline and local only',
    short: 'No account, no cloud, no server that can open your vault. Everything stays on your phone.',
    href: '/features/offline',
  },
  {
    slug: 'unlock',
    title: 'PIN, pattern or passphrase',
    short: 'Unlock with a PIN, a 3×3 pattern, or a passphrase. Lockout after wrong attempts.',
    href: '/features/unlock',
  },
  {
    slug: 'multiple-vaults',
    title: 'Several vaults',
    short: 'Keep separate vaults, each with its own secret. Free plan includes one vault.',
    href: '/features/multiple-vaults',
  },
  {
    slug: 'import-media',
    title: 'Photos, video, audio and PDF',
    short: 'Import and view media inside the vault. Search, sort and filter. Optionally delete the original after import.',
    href: '/features/import-media',
  },
  {
    slug: 'backup-restore',
    title: 'Encrypted backup and restore',
    short: 'Export an encrypted backup file and restore it on a new phone. Auto-lock and screenshot blocking included.',
    href: '/features/backup-restore',
  },
] as const;

export const COMPARES = [
  {
    slug: 'keepsafe',
    title: 'Vireault vs Keepsafe',
    href: '/compare/keepsafe',
    short: 'Local encryption vs a vault that historically relied on accounts and cloud features.',
  },
  {
    slug: 'hide-it-pro',
    title: 'Vireault vs Hide it Pro',
    href: '/compare/hide-it-pro',
    short: 'Modern AES-256 vault compared with a long-running Android hider app.',
  },
  {
    slug: 'calculator-vault',
    title: 'Vireault vs calculator vault apps',
    href: '/compare/calculator-vault',
    short: 'Real cryptography versus disguise-only “calculator” vaults.',
  },
] as const;

export const GUIDES = [
  {
    slug: 'how-to-hide-photos-on-android',
    title: 'How to hide photos on Android',
    description: 'Practical ways to keep private photos off your gallery, and why encryption beats renaming folders.',
    href: '/guides/how-to-hide-photos-on-android',
  },
  {
    slug: 'secure-photo-vault-android',
    title: 'Secure photo vault for Android',
    description: 'What makes a photo vault actually secure on Android, from key derivation to offline storage.',
    href: '/guides/secure-photo-vault-android',
  },
  {
    slug: 'how-to-lock-folder-on-android',
    title: 'How to lock a folder on Android',
    description: 'Android does not ship a built-in locked folder for every phone. Here are honest options, including encrypted vaults.',
    href: '/guides/how-to-lock-folder-on-android',
  },
  {
    slug: 'encrypt-files-on-android',
    title: 'Encrypting files on Android',
    description: 'How AES-256-GCM file encryption works on a phone, and how to back up encrypted data safely.',
    href: '/guides/encrypt-files-on-android',
  },
  {
    slug: 'safest-private-gallery-android',
    title: 'Safest private gallery app for Android',
    description: 'A buyer’s checklist for private gallery apps: offline storage, real crypto, lockout, and no account required.',
    href: '/guides/safest-private-gallery-android',
  },
  {
    slug: 'photo-vault-lost-photos-android',
    title: 'Photo vault app lost my photos on Android',
    description: 'What to do when an Android photo vault goes empty after an update, reinstall or new phone — and how to avoid it.',
    href: '/guides/photo-vault-lost-photos-android',
  },
  {
    slug: 'keepsafe-alternative-android-no-account',
    title: 'Keepsafe alternative without an account (Android)',
    description: 'A factual Keepsafe alternative checklist for Android users who want a vault with no email account, citing Keepsafe’s own docs.',
    href: '/guides/keepsafe-alternative-android-no-account',
  },
] as const;
