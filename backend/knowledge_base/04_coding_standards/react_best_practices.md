# React & Frontend Best Practices — Nexus AI Innovations

## Component Design
* Use **functional components** exclusively (no class components).
* Keep components under **150 lines**. Extract sub-components early.
* Use `React.memo()` for expensive renders.

## Hooks Guidelines
* Custom hooks must be prefixed with `use` (e.g., `useChat`).
* Never call hooks conditionally or inside loops.
* Use `useCallback` for event handlers passed as props.
* Use `useMemo` for expensive computed values.

## State Management
* Local state → `useState`
* Cross-component state → React Context API
* Server state → Custom hooks with Axios (no Redux needed for
  this project scale).

## Styling
* Use **Tailwind CSS** utility classes directly in JSX.
* Custom styles go in `index.css` using `@layer components`.
* Avoid inline `style={{}}` except for dynamic values.

## File Naming
| Type          | Convention            | Example              |
|---------------|-----------------------|----------------------|
| Components    | PascalCase.jsx        | `MessageBubble.jsx`  |
| Hooks         | camelCase.js          | `useChat.js`         |
| API modules   | camelCase.js          | `auth.js`            |
| Pages         | PascalCase.jsx        | `LoginPage.jsx`      |

## Performance
* Lazy-load routes with `React.lazy()` + `Suspense`.
* Use the `key` prop correctly in `.map()` — never use array index
  as key for dynamic lists.
* Debounce search inputs with 300ms delay.

---
*Frontend Standards: Manas Gupta*
