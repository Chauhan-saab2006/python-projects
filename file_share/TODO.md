# Frontend-Backend Separation Plan

## Completed Tasks

- [x] Analyze current codebase and understand structure
- [x] Read all relevant files (app.py, templates/\*.html, requirements.txt)

## Pending Tasks

- [ ] Create frontend/ folder and move templates/ contents
- [ ] Edit frontend/index.html: Remove Jinja templating, make static, update JS with backendUrl
- [ ] Edit frontend/login.html: Remove Jinja variables
- [ ] Edit frontend/error.html: Update home link if needed
- [ ] Update app.py: Add CORS, remove template rendering routes, convert to API-only
- [ ] Update requirements.txt: Add flask-cors
- [ ] Test local setup: Run backend API-only, serve frontend statically
- [ ] Prepare for deployment: Netlify config for frontend, backend ready for Render
