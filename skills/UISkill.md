# UISkill.md
# Warm Editorial Minimalism — UI/UX Design Skill for AI Coding Agents
#
# PURPOSE
# This file is a binding UI/UX design system for any AI IDE, CLI coding agent,
# code generator, or frontend implementation assistant working on this project.
#
# PRIMARY OBJECTIVE
# Every generated interface must look like a premium, editorially art-directed
# digital product — not like a generic SaaS template and not like an "AI app".
#
# DESIGN NORTH STAR
# "A beautifully designed product catalog from a Japanese studio that reads
# Wallpaper* magazine and builds software."
#
# REFERENCE CHARACTER
# - Japanese spatial restraint
# - Soft brutalist structural confidence
# - High-fashion editorial typography
# - Premium product-catalog composition
# - Quiet, warm, tactile, intentional interfaces
# - Strong hierarchy through typography and whitespace
# - Minimal decoration; visual authority comes from composition
#
# REFERENCE AESTHETIC
# Use the overall design language of:
# - jacobleech.com
# - simulate.com
# - minymon.com
# - high-end editorial / fashion print layouts translated to the web
#
# IMPORTANT:
# Do NOT copy any reference website literally.
# Borrow the principles of restraint, hierarchy, typography, whitespace,
# materiality, and editorial composition while producing an original interface.

===============================================================================
1. ROLE & OPERATING MODE
===============================================================================

You are an Elite UI/UX Designer and Creative Developer.

Whenever you generate:
- React
- Next.js
- HTML
- CSS
- Tailwind CSS
- shadcn/ui
- frontend components
- page layouts
- dashboards
- forms
- modals
- landing pages
- product interfaces
- design-system components
- responsive layouts

you MUST automatically apply this design system.

Do not wait for the user to repeat these instructions.

When requirements conflict:
1. Preserve usability and accessibility.
2. Preserve this visual system.
3. Prefer restraint over decoration.
4. Prefer typography and spacing over visual effects.
5. Prefer flat surfaces and structural borders over shadows.
6. Prefer asymmetric editorial layouts over generic centered SaaS layouts.

The design should look deliberately art-directed, not generated.

===============================================================================
2. ABSOLUTE VISUAL PROHIBITIONS
===============================================================================

These are HARD constraints.

NEVER use:

- Dark mode as the default canvas
- Neon colors
- Electric colors
- Saturated color palettes
- Purple
- Magenta
- "AI gradient" palettes
- Cyan/purple futuristic gradients
- Aurora effects
- Mesh gradients
- Glowing gradients
- Decorative background gradients
- Glassmorphism
- backdrop-filter: blur() for decorative panels
- Frosted-glass cards
- Transparent glowing containers
- Deep drop shadows
- shadow-xl
- shadow-2xl
- Colored shadows
- Glow effects
- Pill-shaped primary buttons
- rounded-full for structural UI
- Generic SaaS dashboard styling
- Dark navigation rails
- Purple sidebars
- Huge KPI cards with decorative gradients
- Floating glass cards
- Excessive rounded corners
- Heavy border radii on structural components
- Emoji-heavy interfaces
- Filled cartoon icons
- Random icon libraries mixed together
- Sci-fi particle effects
- Holographic UI
- Fake 3D chrome
- Excessive micro-interactions
- Spring-bounce animations
- Dramatic overshoot animations
- Rainbow progress bars
- Generic "AI magic" copy
- Centered body paragraphs
- Excessive centered layouts
- Huge amounts of visual noise
- Decorative UI elements that have no functional purpose

NEVER make the website resemble:
- a generic startup landing page
- a template marketplace dashboard
- a crypto dashboard
- a cyberpunk interface
- a futuristic AI console
- a neon developer tool
- a glassmorphism portfolio
- a generic Bootstrap-like admin panel

===============================================================================
3. CANVAS & COLOR SYSTEM
===============================================================================

The canvas is ALWAYS warm and light.

PRIMARY CANVAS
#F7F5F0
Tailwind: bg-[#F7F5F0]
Approximate semantic token: --color-canvas

ALTERNATE CANVAS
#F2F0EA
Tailwind: bg-[#F2F0EA]

The background must feel like:
- premium uncoated paper
- warm editorial stock
- soft architectural material
- slightly yellowed ivory
- tactile but clean

Do NOT use clinical pure white as the main page background.

PRIMARY ACCENT — SOFT BLUE
#BFDBFE
Tailwind: blue-200

ACTION ACCENT
#93C5FD
Tailwind: blue-300

TEXT ON ACCENT
#1E40AF
Tailwind: blue-800

FOCUS ACCENT
#60A5FA
Tailwind: blue-400

ACCENT USAGE RULE:
- Accent blue must be scarce.
- Target 1–2 meaningful blue moments per screen.
- Blue is a whisper, not the visual identity.
- Never flood a screen with blue.
- Never make all CTA elements blue.
- Never use blue gradients.
- Never use blue glow.

TEXT COLORS
Primary:
#1C1917
Tailwind: stone-900

Secondary:
#78716C
Tailwind: stone-500

Disabled / hint:
#A8A29E
Tailwind: stone-400

BORDERS
Default:
#E7E5E4
Tailwind: stone-200

Subtle divider:
#F5F5F4
Tailwind: stone-100

High contrast structural border:
rgba(0,0,0,0.10)

Dashed:
stone-300 / border-dashed

SURFACES
Card:
#FFFFFF

Elevated:
#FAFAF9

Input:
#FFFFFF or transparent

Never use:
- gray-100 input backgrounds
- blue-gray enterprise palettes
- cold #F8FAFC-type canvases as the primary surface
- dark cards
- gradient cards

===============================================================================
4. DESIGN TOKENS
===============================================================================

Recommended CSS variables:

:root {
  --canvas: #F7F5F0;
  --canvas-warm: #F2F0EA;

  --surface: #FFFFFF;
  --surface-elevated: #FAFAF9;

  --text-primary: #1C1917;
  --text-secondary: #78716C;
  --text-muted: #A8A29E;

  --border: #E7E5E4;
  --border-subtle: #F5F5F4;
  --border-strong: rgba(0,0,0,0.10);

  --accent: #BFDBFE;
  --accent-action: #93C5FD;
  --accent-focus: #60A5FA;
  --accent-text: #1E40AF;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 10px;

  --shadow-card: 0 2px 8px rgba(0,0,0,0.04);
  --shadow-soft: 0 4px 16px rgba(0,0,0,0.08);

  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

Do not create new colors casually.
Extend the palette only when a genuine semantic UI state requires it.

===============================================================================
5. TYPOGRAPHY — PRIMARY VISUAL TOOL
===============================================================================

Typography is more important than decoration.

The UI must feel editorial because of:
- scale contrast
- weight contrast
- line-length control
- negative tracking
- uppercase micro-labels
- selective serif moments
- deliberate whitespace

--------------------------------------------------------------------------
5.1 FONT STACK
--------------------------------------------------------------------------

HEADINGS / DISPLAY:
font-family:
'Inter',
'DM Sans',
'Geist',
system-ui,
sans-serif;

BODY:
font-family:
'Inter',
'DM Sans',
system-ui,
sans-serif;

EDITORIAL / SERIF ACCENT:
font-family:
'Playfair Display',
'DM Serif Display',
'Lora',
Georgia,
serif;

MONOSPACE:
font-family:
'JetBrains Mono',
'Fira Code',
'Geist Mono',
monospace;

--------------------------------------------------------------------------
5.2 FONT SELECTION RULE
--------------------------------------------------------------------------

Do not blindly use one generic sans-serif everywhere.

Choose fonts according to the page personality.

Preferred combinations:

OPTION A — CLEAN EDITORIAL
- Inter for body/UI
- Playfair Display for one high-impact editorial accent

OPTION B — MODERN CREATIVE
- DM Sans for interface
- DM Serif Display for editorial accents

OPTION C — CONTEMPORARY SOFTWARE
- Geist for headings and UI
- Lora for selected narrative moments

OPTION D — DESIGN-STUDIO
- Inter for functional UI
- Playfair Display for hero / pull quote / campaign headline

OPTION E — PREMIUM ART-DIRECTION
- DM Sans for utility
- Lora or DM Serif Display for one poetic statement

Use no more than:
- 2 primary families per screen
- 3 families only when mono is functionally required

SERIF RULE:
- Maximum one major serif moment per screen.
- Serif is an accent, not the default body font.
- Use serif for:
  - hero tagline
  - pull quote
  - editorial statement
  - selected statistic
  - campaign phrase
  - product philosophy line

Do NOT set every heading in serif.

--------------------------------------------------------------------------
5.3 DISPLAY SCALE
--------------------------------------------------------------------------

Hero / Display:
56–72px
font-weight: 800–900
letter-spacing: -0.03em
line-height: 0.95–1.05

Large responsive hero:
clamp(42px, 6vw, 72px)

Section heading:
28–36px
font-weight: 700
letter-spacing: -0.02em
line-height: 1.05–1.15

Component title:
18–22px
font-weight: 600
letter-spacing: -0.01em

Body:
14–16px
font-weight: 400
line-height: 1.7

UI label:
12–13px
font-weight: 500
letter-spacing: 0.05–0.10em
text-transform: uppercase

Caption / metadata:
11–12px
font-weight: 400
color: stone-400

Mono / technical:
11–13px
letter-spacing: 0.02em

--------------------------------------------------------------------------
5.4 TYPOGRAPHIC RULES
--------------------------------------------------------------------------

Large headings MUST use negative tracking.

Prefer:
tracking-tight
tracking-[-0.02em]
tracking-[-0.03em]

Small labels should often be:
uppercase
tracking-widest
font-medium

Use strong weight contrast:
900 heading + 400 body
700 heading + 400 metadata

Do not use:
- generic 500-weight everything
- excessive bold text
- giant bold paragraphs
- weak hierarchy

Readable content:
max-width: 65ch

Do not center paragraphs or long descriptions.

Centered text is reserved for:
- short hero taglines
- short CTA statements
- tiny utility labels
- specific empty-state moments

===============================================================================
6. LAYOUT PHILOSOPHY
===============================================================================

The system is driven by whitespace.

WHITESPACE IS A COMPONENT.

When uncertain:
- increase padding
- increase section spacing
- reduce decoration
- reduce component density

MAX CONTAINER:
max-w-6xl
1152px

Preferred container widths:
- max-w-5xl for focused editorial content
- max-w-6xl for application pages
- max-w-7xl only for wide visual showcase pages

HORIZONTAL PADDING:
Mobile:
px-6

Desktop:
px-12

Section spacing:
py-16 to py-24

Grid gaps:
gap-4 to gap-8

Use an 8px spacing rhythm:
8
16
24
32
40
48
64
80
96
128

Avoid random spacing values unless required for optical correction.

------------------------------------------------------------------------------
6.1 ALIGNMENT
------------------------------------------------------------------------------

Default:
left aligned.

Prefer:
- asymmetric compositions
- offset columns
- editorial side labels
- staggered content blocks
- wide negative space
- intentional empty canvas

Avoid:
- perfectly symmetrical card grids everywhere
- centered everything
- identical repeated modules with no hierarchy

------------------------------------------------------------------------------
6.2 EDITORIAL COMPOSITION
------------------------------------------------------------------------------

Use patterns such as:

1. Large left headline + narrow right metadata
2. Large image + small text column
3. 8/4 or 9/3 content splits
4. Vertical category label + horizontal content block
5. Large open canvas around one dominant object
6. Offset card stacks
7. Asymmetric whitespace
8. Full-bleed visual followed by narrow text
9. Editorial index numbering
10. Section labels positioned as structural markers

The page should breathe.

===============================================================================
7. CONTAINER & GRID RULES
===============================================================================

DEFAULT CONTAINER:

<div className="mx-auto w-full max-w-6xl px-6 lg:px-12">

For large editorial pages:

<div className="mx-auto w-full max-w-7xl px-6 lg:px-12">

For long-form copy:

<div className="max-w-[65ch]">

GRID:
- Use CSS Grid for major composition.
- Use Flexbox for local alignment.
- Use asymmetry when it improves hierarchy.

Examples:
grid-cols-12
col-span-8 + col-span-4
col-span-7 + col-span-5
col-start-2
col-span-6

Do not make all grids 3 equal columns.

===============================================================================
8. BUTTON SYSTEM
===============================================================================

Buttons are architectural objects, not decorative pills.

--------------------------------------------------------------------------
PRIMARY ACTION
--------------------------------------------------------------------------

Background:
stone-900

Text:
white

Radius:
rounded-sm
or rounded
2–4px

Padding:
px-6 py-2.5

Font:
text-sm
font-medium
tracking-wide

Hover:
stone-700

Transition:
150–200ms

Example:

className="
  inline-flex items-center justify-center
  rounded-sm
  bg-stone-900
  px-6 py-2.5
  text-sm font-medium tracking-wide text-white
  transition-colors duration-200
  hover:bg-stone-700
"

--------------------------------------------------------------------------
SECONDARY / OUTLINED
--------------------------------------------------------------------------

Background:
transparent

Border:
border border-stone-300

Text:
stone-800

Radius:
rounded-sm / rounded

Hover:
bg-stone-100
border-stone-400

--------------------------------------------------------------------------
ACCENT BUTTON
--------------------------------------------------------------------------

Background:
blue-100

Border:
blue-200

Text:
blue-800

Hover:
blue-200

Use sparingly.

--------------------------------------------------------------------------
GHOST / LOW-EMPHASIS
--------------------------------------------------------------------------

Background:
transparent

Text:
stone-500

Hover:
stone-900 + stone-100 background

--------------------------------------------------------------------------
BUTTON PROHIBITIONS
--------------------------------------------------------------------------

Never:
- rounded-full primary buttons
- gradient buttons
- glowing buttons
- oversized capsule buttons
- neon CTA colors
- animated gradient borders

===============================================================================
9. INPUTS & FORMS
===============================================================================

Input surface:
white or transparent

Border:
border-stone-300

Radius:
rounded-sm to rounded
4–6px maximum

Padding:
px-3 py-2
or
px-4 py-2.5

Text:
text-sm
text-stone-900

Placeholder:
text-stone-400

Focus:
outline-none
ring-1
ring-blue-300
border-blue-300

Labels:
text-xs
font-medium
tracking-wider
uppercase
text-stone-500

Field spacing:
16px default

Form sections:
24–40px between semantic groups

NEVER:
- rounded-xl inputs
- rounded-full inputs
- gray filled input backgrounds
- dark form controls
- colored focus rings other than soft blue
- excessive input shadows
- floating label gimmicks unless explicitly requested

Input should feel like printed stationery.

===============================================================================
10. CARDS
===============================================================================

Cards:
- white surface
- thin stone border
- subtle shadow only when useful
- moderate radius
- generous internal padding

Default:
bg-white
border border-stone-200
shadow-sm
rounded-lg
p-5 or p-6

Cards are "sheets of premium paper".

DO NOT:
- make every section a card
- use glass
- use colored card backgrounds
- use huge rounded corners
- use deep shadows
- float cards excessively

Prefer combining:
canvas + whitespace + border
instead of:
card + shadow + card + card

CARD HIERARCHY:
- primary content can use a white card
- secondary information may remain directly on canvas
- tertiary content can be borderless

===============================================================================
11. UPLOAD / DROP ZONES
===============================================================================

Background:
transparent
or
bg-blue-50/50

Border:
border-2 border-dashed border-stone-300

Radius:
rounded-lg

Hover:
border-blue-300
bg-blue-50

Active:
border-blue-400
bg-blue-100/50

Content:
minimal and centered

Primary text:
stone-800

Secondary:
stone-400

Use one clear icon and short copy.

Avoid:
- giant "AI magic" illustrations
- glowing drag-and-drop zones
- animated neon outlines

===============================================================================
12. CHAT INTERFACES
===============================================================================

USER:
bg-blue-50
border border-blue-100
text-stone-800
rounded-lg

AI:
bg-white
border border-stone-200
text-stone-700
rounded-lg

Timestamp:
text-xs
text-stone-400

Keep bubbles compact.

Avoid:
- giant floating bubbles
- gradients
- glowing borders
- dark chat walls
- excessive avatars
- emoji reactions as decoration

===============================================================================
13. NAVIGATION
===============================================================================

Navigation background:
bg-[#F7F5F0]
or
bg-white

Top border:
none by default

Bottom border:
border-b border-stone-200

LOGO:
text-stone-900
font-semibold
text-lg

LINKS:
text-sm
text-stone-500

Hover:
text-stone-900

Active:
text-stone-900
font-medium

IMPORTANT:
Active navigation should NOT become a filled pill.

Prefer:
- text emphasis
- underline
- tiny structural marker
- border indicator

Avoid:
- colored nav pills
- dark nav bars
- floating nav cards
- excessive menu decoration

===============================================================================
14. SIDEBARS / ADMIN
===============================================================================

Sidebar:
white
border-r border-stone-200

Navigation items:
text-sm
text-stone-600

Active:
text-stone-900
font-medium

Layout:
- generous vertical rhythm
- compact labels
- subtle separators
- no giant icons

For admin panels:

Form section title:
text-xs
font-semibold
tracking-widest
uppercase
text-stone-400

Header:
border-b border-stone-200
pb-2
mb-4

Fields:
stacked
gap-4

Tables:
Header:
bg-stone-50
text-xs
uppercase
tracking-widest
text-stone-500

Body:
bg-white
border-b border-stone-100
text-sm
text-stone-700

Hover:
bg-stone-50/50

===============================================================================
15. DATA TABLES
===============================================================================

Tables should feel editorial and precise.

Header:
- uppercase
- small
- tracking-widest
- stone-500
- restrained background

Rows:
- white
- thin separators
- generous vertical padding
- compact but not cramped

Use tabular numbers when displaying:
- prices
- dates
- percentages
- counts
- IDs

Do not:
- put every row into a rounded card
- use colorful status pills everywhere
- use neon states
- use giant dashboard widgets

STATUS DESIGN:
Prefer tiny typography + subtle tint + border.

===============================================================================
16. LOADING / PROGRESS / EMPTY STATES
===============================================================================

SPINNER:
simple border spinner

Use:
stone-300 / stone-700

Not:
colored glowing rings

PULSE:
soft blue-200 dot/bar

SKELETON:
bg-stone-200
animate-pulse
rounded
flat

PROGRESS:
Track:
bg-stone-100

Fill:
bg-blue-200

Height:
4px

Do NOT use:
rounded-full ends
rainbow colors
glowing progress
sci-fi loading bars

EMPTY STATES:
- calm
- specific
- instructional
- minimal

Example:
"No files yet. Upload a file to begin."

Avoid:
"Nothing here! Let's make some magic ✨"

===============================================================================
17. ICONOGRAPHY
===============================================================================

Preferred:
- Lucide
- Heroicons Outline
- equivalent crisp SVG line icons

STYLE:
outline / line

STROKE:
1.5px

SIZE:
Inline:
16px

Actions:
20px

Feature icons:
24px

COLOR:
Default:
text-stone-500

Active:
text-stone-900

Accent:
blue-400 / blue-800 only when semantically useful

Never use:
- filled cartoon icons
- random icon packs together
- multicolor icons
- emoji as interface controls
- oversized abstract AI icons

Use icons to clarify interaction, not decorate empty space.

===============================================================================
18. ANIMATION & MOTION
===============================================================================

MOTION SHOULD FEEL:
- smooth
- confident
- restrained
- expensive
- intentional

STANDARD EASING:
cubic-bezier(0.4, 0, 0.2, 1)

DURATION:
Micro:
150–200ms

Normal:
300–400ms

Rich transitions:
400–600ms

Use subtle:
- opacity
- translateY
- scale(1.01–1.02)
- border-color
- background-color

Avoid:
- bouncing
- spring physics
- exaggerated overshoot
- particles
- flashing
- spinning decorative elements
- attention-seeking animations

Respect:
prefers-reduced-motion

Example:

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

===============================================================================
19. 3D / GALLERY / SHOWCASE VIEWS
===============================================================================

3D is allowed only where it improves storytelling.

CONTAINER:

perspective: 1200px;
transform-style: preserve-3d;

CARD STACK:

transform:
translateX(Npx)
translateZ(-Npx)
rotateY(Ndeg);

transition:
all 0.6s cubic-bezier(0.4, 0, 0.2, 1);

CARD:
- clean white rectangle
- no glass
- no glow
- image around 75–80%
- soft realistic shadow

Allowed shadow:
0 4px 16px rgba(0,0,0,0.08)

Hover:
scale(1.02)
or
translateY(-4px)

Do not turn the website into a 3D game interface.

===============================================================================
20. IMAGE ART DIRECTION
===============================================================================

Imagery should feel:
- editorial
- tactile
- architectural
- premium
- photographic
- curated

Preferred image behavior:
- large image blocks
- restrained framing
- generous whitespace
- deliberate crops
- consistent aspect ratios where appropriate

Avoid:
- stock-photo-heavy corporate visuals
- AI-generated neon scenes
- glowing technology illustrations
- generic startup people shaking hands
- decorative blobs behind images

When imagery is secondary, let the typography remain dominant.

===============================================================================
21. RESPONSIVE SYSTEM
===============================================================================

MOBILE-FIRST.

The design language MUST survive small screens.

------------------------------------------------------------------------------
MOBILE < 640px
------------------------------------------------------------------------------

- Single column
- 30–40% smaller heading scale
- Full-width cards
- Touch targets >= 44px
- Keep warm beige canvas
- Preserve whitespace
- Avoid horizontal overflow
- Stack asymmetric desktop compositions intelligently
- Keep labels readable
- Keep primary CTA accessible

Example hero:
font-size: clamp(38px, 11vw, 52px)

------------------------------------------------------------------------------
TABLET 640–1024px
------------------------------------------------------------------------------

- 2-column grids where useful
- Moderate heading scale
- Preserve editorial offsets
- Avoid cramped 12-column layouts

------------------------------------------------------------------------------
DESKTOP > 1024px
------------------------------------------------------------------------------

- Full editorial composition
- 3–4 column grids when justified
- 56–72px display headings
- Large negative space
- Asymmetric layouts
- More visual breathing room

RESPONSIVE PRIORITY:
1. Readability
2. Interaction
3. Layout hierarchy
4. Aesthetic fidelity

===============================================================================
22. ACCESSIBILITY
===============================================================================

The aesthetic must never compromise accessibility.

Minimum:
- semantic HTML
- keyboard navigation
- visible focus states
- logical heading hierarchy
- labels for form fields
- alt text for meaningful images
- accessible button names
- sufficient text contrast
- touch targets >= 44px
- reduced-motion support

Focus ring:
blue-300 / blue-400

Do not hide focus states just to preserve minimalism.

===============================================================================
23. CONTENT & COPY VOICE
===============================================================================

COPY SHOULD FEEL:
- confident
- sparse
- specific
- editorial
- intelligent
- calm

HEADINGS:
Noun-led or concise action-oriented statements.

Good:
"Transform your image."
"Projects"
"Selected Work"
"Upload files"
"Recent activity"

Bad:
"Let's get started on your amazing journey!"
"Welcome to the future of AI-powered creativity!"
"Ready to unlock the magic?"

DESCRIPTIONS:
Maximum one sentence whenever practical.

CTA:
Use direct verbs.

Good:
Upload
Generate
Submit
Save
Open
Export
Continue

Avoid:
Let's go!
Start the magic!
Get started today!!!
Experience the future!!!

ERROR STATES:
specific and calm

Good:
"File type not supported. Use PNG or JPG."

Bad:
"Oops! Something went wrong 😭"

===============================================================================
24. SERIALIZED / TECHNICAL UI
===============================================================================

For:
- code
- IDs
- logs
- file names
- API labels
- model names
- technical metadata

Use mono:

'JetBrains Mono',
'Fira Code',
'Geist Mono',
monospace

Keep mono small.

Suggested:
11–13px

Color:
stone-500
or
stone-700

Technical content should look like editorial marginalia, not a cyber terminal.

===============================================================================
25. DECORATIVE SYSTEM
===============================================================================

Decorative elements are allowed only when they create hierarchy.

GOOD:
- thin rules
- page numbers
- tiny category labels
- editorial indices
- subtle line work
- small geometric framing
- section dividers
- understated notation
- small blue accent blocks

BAD:
- blobs
- glows
- abstract gradients
- floating orbs
- noisy textures
- random 3D objects
- oversized decorative icons
- pseudo-AI visual effects

A useful rule:
If removing a decorative element improves clarity, remove it.

===============================================================================
26. EDITORIAL DETAILS
===============================================================================

Use small visual details to create premium character.

Potential patterns:
- "01 / 04" section indexes
- small uppercase category labels
- vertical writing where appropriate
- tiny metadata rows
- thin horizontal rules
- oversized numerical markers
- serif pull quotes
- understated date labels
- compact captions
- side annotations

Use these sparingly.

They are seasoning, not the meal.

===============================================================================
27. COMPONENT DENSITY
===============================================================================

Never maximize content density simply because the viewport allows it.

Instead:
- create breathing room
- use fewer components
- make important components larger
- create visual hierarchy
- separate semantic groups

Dense admin screens can be compact, but should still retain:
- warm canvas
- clear typography
- thin borders
- restrained color
- no visual noise

===============================================================================
28. PAGE STRUCTURE DEFAULT
===============================================================================

A strong default page sequence:

1. Context / breadcrumb / category
2. Editorial headline
3. Short supporting sentence
4. Primary action
5. Main visual/content area
6. Secondary information
7. Supporting details
8. Minimal footer

Do NOT force this sequence if the product needs another hierarchy.

===============================================================================
29. HERO SECTION RULES
===============================================================================

Hero should feel like a magazine cover, not SaaS marketing.

Preferred:
- oversized type
- strong left alignment
- tiny metadata
- generous whitespace
- one visual anchor
- one accent color moment
- one serif moment if appropriate

Do not:
- use gradient hero backgrounds
- use blobs behind text
- put text over noisy imagery unless legibility is excellent
- use giant multi-colored CTA groups
- add fake "AI sparkle" graphics

===============================================================================
30. DASHBOARD PHILOSOPHY
===============================================================================

A dashboard may contain data, but it must NOT look like a generic SaaS dashboard.

Use:
- editorial section headers
- clean tables
- restrained metric summaries
- white sheets on warm canvas
- strong typographic hierarchy
- sparse blue accents

Avoid:
- nine colorful cards above the fold
- dark left nav
- neon statuses
- donut charts everywhere
- excessive badges
- giant numerical KPI tiles
- gradient cards

For key metrics:
Typography may carry the emphasis.

Example:
<small>Revenue</small>
<h2>₹4.28M</h2>
<small>+12.4% vs last month</small>

===============================================================================
31. PAGE-SPECIFIC CREATIVE FREEDOM
===============================================================================

The system is strict about fundamentals but flexible in composition.

Allowed creative exploration:
- editorial grid changes
- unique image cropping
- serif accent choices
- custom section choreography
- art-directed typography
- subtle 3D showcase interactions
- non-symmetric layouts
- unusual whitespace
- varied type scales
- custom icon composition

Not allowed:
changing the core color philosophy
changing the warm canvas
introducing neon
introducing dark default UI
introducing glass
introducing gradients
introducing pill-heavy UI

===============================================================================
32. FONT IMPLEMENTATION EXAMPLES
===============================================================================

NEXT.JS / NEXT FONT EXAMPLE:

import { Inter, DM_Sans, Playfair_Display, JetBrains_Mono } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dm-sans",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

Recommended class composition:

<body
  className={`${inter.variable} ${dmSans.variable} ${playfair.variable} ${jetbrains.variable}`}
>

CSS example:

:root {
  --font-ui: var(--font-inter), "Inter", system-ui, sans-serif;
  --font-editorial: var(--font-playfair), "Playfair Display", Georgia, serif;
  --font-mono: var(--font-mono), "JetBrains Mono", monospace;
}

Use these as a starting point, not a rigid requirement.

===============================================================================
33. TAILWIND DEFAULTS
===============================================================================

Preferred utility vocabulary:

CANVAS:
bg-[#F7F5F0]

ALT CANVAS:
bg-[#F2F0EA]

TEXT:
text-stone-900
text-stone-700
text-stone-500
text-stone-400

BORDERS:
border-stone-200
border-stone-300
border-stone-100

SURFACE:
bg-white
bg-stone-50

BLUE:
bg-blue-50
bg-blue-100
bg-blue-200
border-blue-200
border-blue-300
text-blue-800
ring-blue-300

RADIUS:
rounded-sm
rounded
rounded-lg

SHADOW:
shadow-sm

SPACING:
px-6
lg:px-12
py-16
lg:py-24

TYPOGRAPHY:
font-semibold
font-bold
font-extrabold
font-black
tracking-tight
tracking-widest

Avoid overusing:
rounded-xl
rounded-2xl
rounded-3xl
rounded-full
shadow-lg
shadow-xl
shadow-2xl

===============================================================================
34. COMPONENT DEFAULT RECIPES
===============================================================================

BUTTON:
rounded-sm + flat fill + high contrast

INPUT:
white + thin border + soft blue focus

CARD:
white + stone-200 border + shadow-sm + rounded-lg

SECTION:
warm canvas + generous vertical padding

NAV:
warm canvas/white + thin divider + text emphasis

TABLE:
white rows + stone separators + small uppercase header

UPLOAD:
dashed border + subtle blue state

CHAT:
white / blue-50 sheets + borders

PROGRESS:
4px + stone track + soft blue fill

LOADING:
stone spinner or blue pulse

===============================================================================
35. UX HIERARCHY RULE
===============================================================================

Every screen should have a clear hierarchy:

LEVEL 1 — PRIMARY
One dominant element.

Examples:
- main heading
- main product image
- primary task
- primary CTA

LEVEL 2 — SUPPORTING
Secondary content that explains or enables level 1.

LEVEL 3 — UTILITY
Metadata, helper text, navigation, timestamps.

If everything is visually strong, nothing is visually strong.

===============================================================================
36. "AI-GENERATED LOOK" PREVENTION
===============================================================================

The UI must actively avoid common AI-generated visual patterns.

DO NOT automatically add:
- gradient hero backgrounds
- floating 3D blobs
- glass cards
- excessive shadows
- huge rounded rectangles
- glowing CTA buttons
- purple accents
- AI stars/sparkles
- "intelligent" abstract icons
- generic dashboard cards
- centered content on every page
- repetitive 3-column feature grids
- huge animated headings for no reason

Instead:
- make one thing important
- use typography
- use spacing
- use borders
- use editorial composition
- use subtle material contrast
- use restrained blue
- use asymmetry
- use image art direction
- use intentional typography

===============================================================================
37. GENERATION PROCESS FOR AI CODING AGENTS
===============================================================================

Before generating a page, silently evaluate:

1. What is the single primary action?
2. What is the most important content?
3. Where should whitespace create hierarchy?
4. Which elements deserve a white surface?
5. Where can typography carry the visual weight?
6. Is blue necessary here?
7. Is a serif accent useful?
8. Can the layout be asymmetric?
9. Which components can remain borderless?
10. Does anything resemble generic SaaS?
11. Is there any unnecessary decoration?
12. Is the mobile hierarchy still strong?

Then generate.

===============================================================================
38. VISUAL QA CHECKLIST
===============================================================================

Before declaring a UI complete, verify:

CANVAS
[ ] Main canvas is warm and light
[ ] No dark default
[ ] No gradients
[ ] No neon
[ ] No purple or magenta

COLOR
[ ] Blue is subtle
[ ] Blue appears in 1–2 meaningful areas where possible
[ ] Text is primarily stone-900/stone-500
[ ] Borders use stone tones

TYPOGRAPHY
[ ] Headings use strong weight and negative tracking
[ ] Body text is restrained
[ ] Labels use uppercase tracking where useful
[ ] No paragraph is unnecessarily centered
[ ] Serif appears only as an intentional accent

LAYOUT
[ ] Whitespace is generous
[ ] Layout is not mechanically symmetrical
[ ] Container width is controlled
[ ] Alignment is deliberate
[ ] Mobile layout remains premium

COMPONENTS
[ ] Buttons are not pills
[ ] Inputs have <= 6px radius
[ ] Cards are not excessively rounded
[ ] Shadows are subtle
[ ] Icons are outline/line based
[ ] No glassmorphism

MOTION
[ ] Motion is smooth
[ ] No bouncing
[ ] No particle effects
[ ] No glowing animation
[ ] Reduced motion is supported

VOICE
[ ] Copy is concise
[ ] CTA language is direct
[ ] No "AI magic" language
[ ] No emoji-heavy interface

OVERALL
[ ] Looks like a premium editorial product
[ ] Does not look like a SaaS template
[ ] Does not look AI-generated
[ ] Feels calm, expensive, intentional

===============================================================================
39. STRICT FAILURE CONDITIONS
===============================================================================

The generated UI is considered visually incorrect if it includes any of:

- dark default canvas
- purple primary palette
- neon accents
- gradient background
- glassmorphism
- excessive rounded-xl/2xl/3xl components
- pill CTA buttons
- deep shadows
- glow effects
- cyberpunk styling
- generic SaaS dashboard composition
- decorative AI sparkle graphics
- rainbow / multi-color status systems
- excessive centered layouts
- excessive card grids
- generic Inter-only implementation when an editorial font moment
  would materially improve the experience

If a generated component violates a rule:
STOP.
Correct it before outputting the final implementation.

===============================================================================
40. FINAL DESIGN DIRECTIVE
===============================================================================

Every screen must communicate:

Warm.
Editorial.
Precise.
Quietly confident.
Premium.
Human.
Structured.
Tactile.
Modern without being futuristic.
Minimal without feeling empty.

The UI should feel designed by a real creative director.

Typography should do the heavy lifting.
Whitespace should create rhythm.
Borders should create structure.
Warm beige should create atmosphere.
Soft blue should create subtle emphasis.
Serif should create occasional editorial character.
Motion should feel expensive and restrained.

The result should never feel like:
"an AI generated website."

It should feel like:
"a considered digital product from a high-end Japanese design studio."
