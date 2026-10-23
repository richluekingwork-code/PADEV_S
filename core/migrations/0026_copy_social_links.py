from django.db import migrations

# Keys used in the old social_links JSON (including common spellings) -> new field.
KEY_TO_FIELD = {
    'facebook': 'facebook_url',
    'x': 'x_url',
    'twitter': 'x_url',
    'instagram': 'instagram_url',
    'linkedin': 'linkedin_url',
    'youtube': 'youtube_url',
    'tiktok': 'tiktok_url',
    'whatsapp': 'whatsapp_url',
}


def copy_social_links(apps, schema_editor):
    SiteSetting = apps.get_model('core', 'SiteSetting')
    for setting in SiteSetting.objects.all():
        links = setting.social_links or {}
        changed = False
        for key, url in links.items():
            field = KEY_TO_FIELD.get(str(key).strip().lower())
            if field and url and not getattr(setting, field):
                setattr(setting, field, str(url).strip())
                changed = True
        if changed:
            setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_sitesetting_social_urls'),
    ]

    operations = [
        migrations.RunPython(copy_social_links, migrations.RunPython.noop),
    ]
