# Copilot Instructions for Event Management

## Project Overview
A Django-based event management web application (EventyFly) using PostgreSQL with a Tailwind CSS frontend. Core functionality: CRUD operations for events, categories, and participants with search/filtering capabilities.

## Architecture & Key Components

### Django Structure
- **App**: `events` (monolithic single-app architecture)
- **Models** ([events/models.py](events/models.py)):
  - `Category`: Manages event categories
  - `Event`: Core event entity with ForeignKey to Category
  - `Participant`: Users joining events via ManyToMany relationship
  
### View Pattern (Query Optimization First)
All views use `prefetch_related('participants')` and `select_related('category')` to prevent N+1 queries:
```python
mainquery = Event.objects.prefetch_related('participants').select_related('category')
```
When querying: always prefetch participants, select_related category. This is non-negotiable for performance.

### URL Query String Pattern
The app uses query parameters to control behavior:
- Dashboard view: `?event=all_events|upcoming_events|past_events|all_category|all_Participant`
- Delete operations: `?deleteid=X|participant_id=X|catagoryid=X`
- Create form selection: `?create=category|event|participant`
- Update form: `?editid=X|catagoryid=X|participant_id=X`

**Critical**: Always use GET parameters for filtering/navigation, POST for mutations.

## Development Workflow

### Environment Setup
```bash
# Activate virtual environment
source event_env/bin/activate.fish  # or .bash_activate on non-fish shells

# Development server (Django default: localhost:8000)
python manage.py runserver

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Frontend: Tailwind CSS
- **Build CSS**: `npm run build:tailwind` (minified production build)
- **Watch mode**: `npm run watch:tailwind` (auto-compile during development)
- **Input**: [static/css/tailwind.css](static/css/tailwind.css) → **Output**: [static/css/output.css](static/css/output.css)
- Output CSS is imported in templates; regenerate if Tailwind classes aren't applying

### Database
- **Engine**: PostgreSQL (psycopg2/psycopg3 installed)
- **Fallback**: SQLite3 (commented in settings.py)
- **Credentials**: postgres/postgres (hardcoded in settings.py, dev-only)
- **Production**: Uses `dj-database-url` to parse DATABASE_URL environment variable

## Code Patterns & Conventions

### Form Styling Pattern
Forms use `StyleFormMixin` ([events/forms.py](events/forms.py)) to apply consistent Tailwind classes:
```python
class CreateEvent(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = "name", "imagelink", "location", "date", "time", "description", "category"
```
**Rule**: All new forms must inherit `StyleFormMixin` for consistency.

### View Response Pattern
- Dashboard aggregates via `Q` queries and `Count` filters to calculate statistics
- Success messages: render same template with `{'message': "Text"}`
- Errors: re-render form with validation errors (Django built-in)
- Redirects: use `redirect()` for participant deletion only; otherwise render templates

### URL Namespace
Single app (`events`) means no namespace. Routes:
- `/` or `/event/` → home (search/filter landing)
- `/event/<id>/` → event details
- `/dashboard/` → admin dashboard (CRUD interface)
- `/create/?create=X` → form submission view
- `/update/?editid=X` → update form view

## Critical Dependencies & Integration Points

### Debugging
- Django Debug Toolbar installed (`debug_toolbar`, port 127.0.0.1 only)
- CSRF trusted origins include Render.com (production deployment)

### Frontend Components
- **Header** ([events/templates/components/header.html](events/templates/components/header.html)): 
  - Orange accent color (#FFA500)
  - Responsive nav with active route highlighting using `request.resolver_match.url_name`
  - Logo: "EVENTYFLY" with subtitle
- Reusable components in [events/templates/components/](events/templates/components/): catagorylist, eventlist, search, participantlist, hero

### Template Inheritance
Base template: [events/templates/](events/templates/) (app_dirs=True in settings)

## Common Tasks

**Adding a new entity type**: Create Model → Create Form with StyleFormMixin → Add view in views.py (with proper query optimization) → Add URL route → Create templates

**Fixing N+1 query issues**: Use `select_related()` for ForeignKeys, `prefetch_related()` for reverse relations—see mainquery pattern

**Modifying dashboard statistics**: Edit `aggregate()` call in dashboard view with appropriate `Q` filters

**Styling new elements**: Add Tailwind classes directly (no separate CSS needed), rebuild with `npm run watch:tailwind`

## Known Constraints & Tech Debt
- Single app design (no separation of concerns)
- Query strings for state management instead of URL structure
- Category typo in codebase: "catagory"/"catagoryid" (preserve for backward compatibility)
- DEBUG=True and SECRET_KEY exposed in settings.py (dev-only, move to .env)
