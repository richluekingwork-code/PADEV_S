# PADEV

PADEV is a Django content management website for Partners in Development.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the public site and `/admin/` for the CMS.

## Sevalla deployment

1. In Sevalla, create a PostgreSQL database.
2. Create an Application from the GitHub repository (branch `main`). Sevalla builds it with
   Nixpacks, which reads `runtime.txt` (Python 3.12) and runs the `web` process in `Procfile`.
3. Connect the database to the application under **Networking → Connected services** (or
   **Environment variables → Add from database**) so `DATABASE_URL` is set, using the internal connection.
4. Add these environment variables to the application:
   - `DJANGO_SECRET_KEY`: a long random string
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=.sevalla.app,your-custom-domain.org`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-custom-domain.org` (`https://*.sevalla.app` is always trusted)
   - `CLOUDINARY_URL`, or `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY` and `CLOUDINARY_API_SECRET`
5. On every deploy, `start.sh` migrates the database, collects static files, seeds the reference
   content when the database is empty, and starts Gunicorn on `$PORT`.
6. Create a Django admin user from the application's **Web terminal**:
   `python manage.py createsuperuser`.

Never commit `.env`, database files, Cloudinary credentials, or Django secret keys.