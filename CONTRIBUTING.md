# Contributing

Thanks for helping improve Querywise. Contributions should keep the app's single-page workflow clear and preserve the privacy boundary between schema metadata and database row data.

## Before you start

- Search existing issues and pull requests to avoid duplicate work.
- For a substantial change, open an issue first to discuss the approach.
- Never include API keys, database credentials, real customer data, or private schema dumps in issues, commits, tests, or pull requests.

## Development setup

Follow the [local setup instructions](./README.md#run-locally) in the README. Install backend dependencies from `backend/requirements.txt` and frontend dependencies from `frontend/package.json`.

## Making changes

- Keep changes focused and consistent with the existing Python and React patterns.
- Add or update tests for behavior changes.
- Update relevant documentation when setup, API behavior, or privacy behavior changes.
- Process pasted schema definitions locally and send only extracted table and column metadata.
- Do not add dependencies unless they are needed for the change.
- Keep generated SQL read-only and do not add execution against user databases without a separately reviewed design.

## Validation

Run the frontend tests and production build from `frontend`:

```powershell
npm test -- --watchAll=false
npm run build
```

For backend changes, also run Python compilation from the project root:

```powershell
python -m compileall -q backend
```

Run backend model tests with:

```powershell
python -m unittest discover -s backend\tests
```

Include the commands you ran and their results in your pull request.

## Pull requests

- Use the pull request template.
- Explain the problem and the behavior change.
- Link related issues.
- Include screenshots for user-interface changes when helpful.
- Call out any privacy, configuration, or database changes.
- Keep the pull request focused and ready for review.
