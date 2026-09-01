# Supported Projects

Automatic project adapters recognize Go, Java/Spring conventions, Python
(Django, Flask, FastAPI conventions), Node.js (Express, NestJS, Next.js, Nuxt,
Vue and React conventions), PHP/Laravel, .NET, Flutter, and common mini-program
layouts. Detection is best-effort: an unrecognized layout can still be analyzed
by supplying a profile and source manifest manually. Adapters share one evidence
contract, so adding a framework does not change the workflow or quality gates.

The source collector favors first-party text source files and excludes common
dependency directories, build output, lockfiles, minified assets, and binaries.
