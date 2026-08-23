# Supported Projects

Automatic detection covers Go, Java, Python, Node.js, Vue, and React. Detection
is best-effort: an unrecognized layout can still be analyzed by supplying a
profile and source manifest manually.

The source collector favors first-party text source files and excludes common
dependency directories, build output, lockfiles, minified assets, and binaries.
