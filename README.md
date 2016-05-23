Taiga contrib bank holidays
===================

![Kaleidos Project](http://kaleidos.net/static/img/badge.png "Kaleidos Project")
[![Managed with Taiga.io](https://taiga.io/media/support/attachments/article-22/banner-gh.png)](https://taiga.io "Managed with Taiga.io")

The Taiga plugin for bank holidays.


Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-holidays` with:

```bash
  pip install ../taiga-contrib-holidays/back
```

Modify in `taiga-back` your `settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_holidays"]
```

Then run the migrations to generate the new need table and apply the patch:

```bash
  python manage.py makemigrations taiga_contrib_holidays
  python manage.py migrate taiga_contrib_holidays
  python ../taiga-contrib-holidays/back/patch/patch-taiga-holidays.py .
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-holidays` compiled code (you need subversion in your system):

```bash
  cd taiga-front-dist/dist
  mkdir -p plugins
  cd plugins
  cp -r ../../../taiga-contrib-holidays/front/dist holidays
```

Include in your `dist/conf.json` in the `contribPlugins` list the value `"/plugins/holidays/holidays.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/holidays/holidays.json"
    ]
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-back
  virtualenv env
  source env/bin/activate
  pip install -e ../taiga-contrib-holidays/back
```

Modify in `taiga-back` your `settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_holidays"]
```

Then run the migrations to generate the new need table:

```bash
  python manage.py makemigrations taiga_contrib_holidays
  python manage.py migrate taiga_contrib_holidays
  python ../taiga-contrib-holidays/back/patch/patch-taiga-holidays.py .
```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-holidays/front/dist holidays
```

Include in your `dist/conf.json` in the `contribPlugins` list the value `"/plugins/holidays/holidays.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/holidays/holidays.json"
    ]
...
```

In the plugin source dir `taiga-contrib-holidays/front` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.
